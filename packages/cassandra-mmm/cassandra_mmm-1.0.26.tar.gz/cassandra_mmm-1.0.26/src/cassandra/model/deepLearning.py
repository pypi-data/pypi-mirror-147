from dataProcessing.cleanFormatMerge import guess_categorical_variables, guess_numerical_variables
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, QuantileTransformer, Normalizer
from cassandra.model.modelEvaluation.plot import show_nrmse, show_mape, show_rsquared
import numpy as np


def deepLearning(df, X_columns, target, name_model, metric=['rsq', 'nrmse', 'mape'], return_metric=False, cv=5,
                 verbose=2, size=0.2, random_state=42, force_coeffs=False, coeffs=[], intercept=0):
    metrics_values = {}
    X = df[X_columns]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=size, random_state=random_state)
    all_features = list(X_train.columns)
    categorical = guess_categorical_variables(X_train)
    numerical = guess_numerical_variables(X_train.drop(categorical, axis=1))

    transformers = [
        ('one hot', OneHotEncoder(handle_unknown='ignore'), categorical),
        ('scaler', QuantileTransformer(), numerical),
        ('normalizer', Normalizer(), all_features)
    ]
    ct = ColumnTransformer(transformers)

    if len(df.index) < 1000:
        solver_value = 'lbfgs'
    else:
        solver_value = 'adam'

    steps = [
        ('column_transformer', ct),
        ('model', MLPRegressor(solver=solver_value))
        # solver 'lbfgs' is used for dataset with less than 1000 rows, if more than 1000 use solver 'adam'
    ]
    pipeline = Pipeline(steps)
    param_space = {
        'column_transformer__scaler__n_quantiles': [80, 100, 120],
        'column_transformer__normalizer': [Normalizer(), 'passthrough'],
        'model__hidden_layer_sizes': [(35, 35), (50, 50), (75, 75)],
        'model__alpha': [0.005, 0.001]
    }

    # input the param space into "param_grid", define what pipeline it needs to run, in our case is named "pipeline", and the you can decide how many cross validation can do "cv=" and the verbosity.
    model = GridSearchCV(pipeline, param_grid=param_space, cv=cv, verbose=verbose)
    model.fit(X_train, y_train)

    if force_coeffs and coeffs:
        model.coef_ = np.array(coeffs)
        model.intercept_ = intercept

    # model.best_estimator_

    # Ask the model to predict on X_test without having Y_test
    # This will give you exact predicted values

    # We can use our NRMSE and MAPE functions as well

    # Create new DF not to edit the original one
    result = df

    # Create a new column with predicted values
    result['prediction'] = model.predict(result)
    y_train_pred = model.predict(X_train)
    y_test_pred = model.predict(X_test)

    # Score returns the accuracy of the above prediction or R^2
    if 'rsq' in metric:
        try:
            rsq = show_rsquared(result[target], result['prediction'])
        except:
            rsq = -100
        if return_metric:
            metrics_values[name_model + '_rsq'] = rsq
        print(name_model, 'RSQ: ', rsq)

    # Get the NRMSE & MAPE values
    if 'nrmse' in metric:
        try:
            nrmse_val = show_nrmse(np.array(y_train), np.array(y_train_pred))
        except:
            nrmse_val = 100
        if return_metric:
            metrics_values[name_model + '_nrmse'] = nrmse_val
        print(name_model, 'NRMSE: ', nrmse_val)

    if 'mape' in metric:
        try:
            mape_val = show_mape(np.array(y_test), np.array(y_test_pred))
        except:
            mape_val = 100
        if return_metric:
            metrics_values[name_model + '_mape'] = mape_val
        print(name_model, 'MAPE: ', mape_val)

    if metrics_values:
        return result, model, metrics_values
    else:
        return result, model
