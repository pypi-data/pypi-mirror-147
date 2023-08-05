import numpy as np
import pandas as pd
from sklearn.metrics import mean_squared_error, mean_absolute_percentage_error
import math

def mse(y_true, y_pred):
    mse = mean_squared_error(y_true, y_pred)
    return round(mse, 2)

def rmse(y_true, y_pred):
    rmse = mean_squared_error(y_true, y_pred) ** 0.5
    return round(rmse, 2)

def mae(y_true, y_pred):
    mae = np.mean(np.abs(y_true - y_pred))
    return round(mae, 2)

def mape(y_true, y_pred):
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    return round(mape, 2)

def mape_acc(y_true, y_pred):
    mape = np.mean(np.abs((y_true - y_pred) / y_true)) * 100
    mape = 100 - mape
    mape = mape if (mape > 0 and mape < 100) else 0
    return round(mape, 2)

def smape(y_true, y_pred):
    smape = 1/len(y_pred) * np.sum(2 * np.abs(y_true-y_pred) / (np.abs(y_pred) + np.abs(y_true))*100)
    return round(smape, 2)