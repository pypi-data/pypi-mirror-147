from sklearn.neural_network import MLPRegressor
from sklearn.model_selection import train_test_split
from cassandra.data.trasformations.trasformations import create_model
from cassandra.model.modelEvaluation.plot import show_nrmse, show_mape, show_rsquared
import numpy as np



def mlpRegressor(df, X_columns, target, name_model, random_state=1, max_iter=500, medias=[], organic=[],
                 metric=['rsq', 'nrmse', 'mape'], return_metric=False, size=0.2, positive=False, force_coeffs=False, coeffs=[], intercept=0):
    metrics_values = {}
    X = df[X_columns]
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=size, random_state=random_state)

    if medias or organic:
        model = create_model(medias, organic, MLPRegressor(random_state=random_state, max_iter=max_iter))
    else:
        model = MLPRegressor(random_state=random_state, max_iter=max_iter)

    model.fit(X_train, y_train)

    if force_coeffs and coeffs:
        model.coef_ = np.array(coeffs)
        model.intercept_ = intercept

    # Ask the model to predict on X_test without having Y_test
    # This will give you exact predicted values

    # We can use our NRMSE and MAPE functions as well

    # Create new DF not to edit the original one
    result = df

    # Create a new column with predicted values
    if medias or organic:
        result['prediction'] = model.predict(result)
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
    else:
        result['prediction'] = model.predict(X)
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
