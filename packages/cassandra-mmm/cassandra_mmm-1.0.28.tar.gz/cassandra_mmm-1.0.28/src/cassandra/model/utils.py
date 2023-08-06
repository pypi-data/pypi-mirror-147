from cassandra.model.linear import linear
from cassandra.model.logLinear import logLinear
from cassandra.model.modelEvaluation.plot import show_rsquared, show_mape, show_nrmse
from cassandra.model.ridge import ridge
from cassandra.model.logLog import logLog
import numpy as np


def choose_model(df, X_columns, y_column, model_regression='linear', X_trasformations_columns=[],
                 model_regression_log_log='linear', ridge_number=0, metric=None,
                 return_metric=False, size=0.2, positive=False, random_state=42, force_coeffs=False, coeffs=[],
                 intercept=0):
    if metric is None:
        metric = ['rsq_train', 'rsq_test', 'nrmse_train', 'nrmse_test', 'mape_train', 'mape_test']
    metrics_values = {}

    if 'linear' in model_regression:
        if return_metric:
            result, model, metrics_values = linear(df, X_columns, y_column, model_regression, metric=metric,
                                                   return_metric=return_metric, size=size, positive=positive,
                                                   random_state=random_state, force_coeffs=force_coeffs, coeffs=coeffs,
                                                   intercept=intercept)
        else:
            result, model = linear(df, X_columns, y_column, model_regression, metric=metric,
                                   return_metric=return_metric,
                                   size=size, positive=positive, random_state=random_state, force_coeffs=force_coeffs,
                                   coeffs=coeffs, intercept=intercept)

    elif 'logLinear' in model_regression:
        if return_metric:
            result, model, metrics_values = logLinear(df, X_columns, y_column, model_regression, metric=metric,
                                                      return_metric=return_metric, size=size, positive=positive,
                                                      random_state=random_state, force_coeffs=force_coeffs,
                                                      coeffs=coeffs, intercept=intercept)
        else:
            result, model = logLinear(df, X_columns, y_column, model_regression, metric=metric,
                                      return_metric=return_metric,
                                      size=size, positive=positive, random_state=random_state,
                                      force_coeffs=force_coeffs, coeffs=coeffs, intercept=intercept)

    elif 'logLog' in model_regression:
        if return_metric:
            result, model, metrics_values = logLog(df, X_trasformations_columns, X_columns, y_column, model_regression,
                                                   model_regression=model_regression_log_log, metric=metric,
                                                   return_metric=return_metric, size=size, positive=positive,
                                                   random_state=random_state, force_coeffs=force_coeffs, coeffs=coeffs,
                                                   intercept=intercept)
        else:
            result, model = logLog(df, X_trasformations_columns, X_columns, y_column, model_regression,
                                   model_regression=model_regression_log_log, metric=metric,
                                   return_metric=return_metric, size=size, positive=positive, random_state=random_state,
                                   force_coeffs=force_coeffs, coeffs=coeffs, intercept=intercept)

    elif 'ridge' in model_regression:
        if return_metric:
            result, model, metrics_values = ridge(df, X_columns, y_column, model_regression, ridge_number=ridge_number,
                                                  metric=metric,
                                                  return_metric=return_metric, size=size, positive=positive,
                                                  random_state=random_state, force_coeffs=force_coeffs, coeffs=coeffs,
                                                  intercept=intercept)
        else:
            result, model = ridge(df, X_columns, y_column, model_regression, ridge_number=ridge_number, metric=metric,
                                  return_metric=return_metric, size=size, positive=positive, random_state=random_state,
                                  force_coeffs=force_coeffs, coeffs=coeffs, intercept=intercept)

    if metrics_values:
        return result, model, metrics_values
    else:
        return result, model


def choose_metric(name_model, metric, return_metric, y_train, y_test, y_train_pred, y_test_pred):
    metrics_values = {}

    # Score returns the accuracy of the above prediction or R^2
    if 'rsq_train' in metric:
        try:
            rsq_train = show_rsquared(np.array(y_train), np.array(y_train_pred))
        except:
            rsq_train = -100
        if return_metric:
            metrics_values[name_model + '_rsq_train'] = rsq_train
        print(name_model, 'RSQ train: ', rsq_train)

    if 'rsq_test' in metric:
        try:
            rsq_test = show_rsquared(np.array(y_test), np.array(y_test_pred))
        except:
            rsq_test = -100
        if return_metric:
            metrics_values[name_model + '_rsq_test'] = rsq_test
        print(name_model, 'RSQ test: ', rsq_test)

    # Get the NRMSE values
    if 'nrmse_train' in metric:
        try:
            nrmse_train_val = show_nrmse(np.array(y_train), np.array(y_train_pred))
        except:
            nrmse_train_val = 100
        if return_metric:
            metrics_values[name_model + '_nrmse_train'] = nrmse_train_val
        print(name_model, 'NRMSE train: ', nrmse_train_val)

    if 'nrmse_test' in metric:
        try:
            nrmse_test_val = show_nrmse(np.array(y_test), np.array(y_test_pred))
        except:
            nrmse_test_val = 100
        if return_metric:
            metrics_values[name_model + '_nrmse_test'] = nrmse_test_val
        print(name_model, 'NRMSE test: ', nrmse_test_val)

    # Get the MAPE values
    if 'mape_train' in metric:
        try:
            mape_train_val = show_mape(np.array(y_train), np.array(y_train_pred))
        except:
            mape_train_val = 100
        if return_metric:
            metrics_values[name_model + '_mape_train'] = mape_train_val
        print(name_model, 'MAPE train: ', mape_train_val)

    if 'mape_test' in metric:
        try:
            mape_test_val = show_mape(np.array(y_test), np.array(y_test_pred))
        except:
            mape_test_val = 100
        if return_metric:
            metrics_values[name_model + '_mape_test'] = mape_test_val
        print(name_model, 'MAPE test: ', mape_test_val)

    return metrics_values
