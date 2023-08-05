from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.base import BaseEstimator, TransformerMixin, RegressorMixin, clone
import xgboost as xgb
import optuna

class OptunaXGBRegressor(BaseEstimator, TransformerMixin):
  def __init__(self, n_trials):
    self.colsample_bytree = 0.6
    self.learning_rate = 0.01
    self.max_depth = 3
    self.min_child_weight = 1
    self.n_estimators = 1000
    self.subsample = 0.95
    self.nthread = 30
    self.n_trials = n_trials
    self.x = None
    self.y = None
    self.model = None
  def fit(self, X, y):
    X_train, X_val, y_train, y_val = train_test_split(X, y, train_size = 0.7, test_size = 0.3)
    def objective(trial):
      colsample_bytree = trial.suggest_uniform(f"colsample_bytree", 0.01, 0.5)
      learning_rate = trial.suggest_uniform(f"learning_rate", 0.01, 1)
      max_depth  = trial.suggest_int("max_depth", 1, 20)
      min_child_weight = trial.suggest_int("min_child_weight", 1, 20)
      n_estimators = trial.suggest_int("n_estimators", 1, 2000)
      subsample = trial.suggest_uniform(f"subsample", 0.01, 1)
      nthread = trial.suggest_int("nthread", 1, 30)
      model = xgb.XGBRegressor(nthread = nthread, colsample_bytree = colsample_bytree, gamma = 0, learning_rate = learning_rate, max_depth = max_depth, min_child_weight = min_child_weight, n_estimators = n_estimators, subsample = subsample, seed = 42)
      model.fit(X_train, y_train)
      y_pred = model.predict(X_val)
      error = mean_squared_error(y_val, y_pred)
      return error
    study = optuna.create_study(direction='maximize')
    study.optimize(objective, n_trials = self.n_trials)
    self.colsample_bytree = study.best_params['colsample_bytree']
    self.learning_rate = study.best_params['learning_rate']
    self.max_depth = study.best_params['max_depth']
    self.min_child_weight = study.best_params['min_child_weight']
    self.n_estimators = study.best_params['n_estimators']
    self.subsample = study.best_params['subsample']
    self.nthread = study.best_params['nthread']
    self.model = xgb.XGBRegressor(nthread = self.nthread, colsample_bytree = self.colsample_bytree, gamma = 0, learning_rate = self.learning_rate,
                                      max_depth = self.max_depth,
                                      min_child_weight = self.min_child_weight,
                                      n_estimators = self.n_estimators,                                                                    
                                      subsample = self.subsample, seed = 42)
    evalset = [(X_train, y_train), (X_val, y_val)]
    self.model.fit(X_train, y_train, eval_set = evalset)
    return self.model
  def predict(self, X):
    pred_y = self.model.predict(X)
    return pred_y 