from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import train_test_split
import pandas as pd
from cassandra.data.trasformations.trasformations import create_model
from cassandra.model.utils import choose_metric
import numpy as np


def logLog(df, X_trasformations_columns, X_columns, target, name_model, model_regression='linear', medias=[],
           organic=[], metric=None, return_metric=False, size=0.2, positive=False, random_state=42, force_coeffs=False, coeffs=[], intercept=0):
    if metric is None:
        metric = ['rsq_train', 'rsq_test', 'nrmse_train', 'nrmse_test', 'mape_train', 'mape_test']
    X_trasformations = df[X_trasformations_columns]
    X = df[X_columns]
    y = df[target]

    X_log = np.log(abs(X_trasformations) + 1)
    X_all = pd.merge(X_log, X, left_index=True, right_index=True)
    y_log = np.log(y + 1)

    X_train, X_test, y_train, y_test = train_test_split(X_all, y_log, test_size=size, random_state=random_state)

    if model_regression == 'linear':
        if medias or organic:
            model = create_model(medias, organic, LinearRegression(positive=positive))
        else:
            model = LinearRegression(positive=positive)
    elif model_regression == 'ridge':
        if medias or organic:
            ridge_number = len(medias + organic)
            model = create_model(medias, organic, Ridge(alpha=ridge_number, positive=positive))
        else:
            ridge_number = len(X.columns)
            model = Ridge(alpha=ridge_number, positive=positive)

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
        # TODO
        result['prediction'] = np.exp(model.predict(np.log(abs(result) + 1))) - 1
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)
    else:
        result['prediction'] = np.exp(model.predict(X_all)) - 1
        y_train_pred = model.predict(X_train)
        y_test_pred = model.predict(X_test)

    metrics_values = choose_metric(name_model, metric, return_metric, y_train, y_test, y_train_pred, y_test_pred)

    if metrics_values:
        return result, model, metrics_values
    else:
        return result, model
