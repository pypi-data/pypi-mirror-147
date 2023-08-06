from cassandra.model.utils import choose_metric
from cassandra.data.trasformations.trasformations import create_model
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
import numpy as np


def logLinear(df, X_columns, target, name_model, medias=[], organic=[], metric=None,
              return_metric=False, size=0.2, positive=False, random_state=42, force_coeffs=False, coeffs=[], intercept=0):
    if metric is None:
        metric = ['rsq_train', 'rsq_test', 'nrmse_train', 'nrmse_test', 'mape_train', 'mape_test']
    X = df[X_columns]
    y = df[target]
    logged_y = np.log(y + 1)
    X_train, X_test, y_train, y_test = train_test_split(X, logged_y, test_size=size, random_state=random_state)

    if medias or organic:
        model = create_model(medias, organic, LinearRegression(positive=positive))
    else:
        model = LinearRegression(positive=positive)

    model.fit(X_train, y_train)

    if force_coeffs and coeffs:
        model.coef_ = np.array(coeffs)
        model.intercept_ = intercept

    # y_pred = np.exp(model.predict(X))  # Apply exponential function (inverse of natural log) to the predictions

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

    metrics_values = choose_metric(name_model, metric, return_metric, y_train, y_test, y_train_pred, y_test_pred)

    if metrics_values:
        return result, model, metrics_values
    else:
        return result, model
