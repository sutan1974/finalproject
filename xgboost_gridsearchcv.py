# -*- coding: utf-8 -*-
"""XGBoost GridSearchCV.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1KhbLr7idQg4NLjtGfRJKLkWiNNJPy_JX
"""

from google.colab import drive
drive.mount('/content/drive')

import numpy as np
import pandas as pd
import statsmodels
import patsy
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns

#Import model
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics

import warnings
warnings.filterwarnings("ignore")

calendar_df = pd.read_csv('drive/MyDrive/Rakamin/Dataset Final Project/calendar.csv')
listings_df = pd.read_csv('drive/MyDrive/Rakamin/Dataset Final Project/listings.csv')
reviews_df = pd.read_csv('drive/MyDrive/Rakamin/Dataset Final Project/reviews.csv')

from xgboost import XGBRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.model_selection import train_test_split, KFold, cross_val_score
import numpy as np
import matplotlib.pyplot as plt

# Generate dataset
from sklearn.datasets import make_regression
X, y = make_regression(n_samples=1000, n_features=10, noise=0.1, random_state=42)

# Split into train and test sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create XGBoost Regressor model with default parameters
xgb_model = XGBRegressor(objective='reg:squarederror', random_state=42)

# Train the model
xgb_model.fit(X_train, y_train)

# Predict with the trained model
y_xgb_pred = xgb_model.predict(X_test)

# Calculate MAE and RMSE for the model
xgb_mae = mean_absolute_error(y_test, y_xgb_pred)
xgb_rmse = np.sqrt(mean_squared_error(y_test, y_xgb_pred))

print(f"Mean Absolute Error (MAE) for XGBoost: {xgb_mae}")
print(f"Root Mean Squared Error (RMSE) for XGBoost: {xgb_rmse}")

# Define function to calculate MAPE
def mean_absolute_percentage_error(y_true, y_pred):
    return np.mean(np.abs((y_true - y_pred) / y_true)) * 100

# Compute MAPE for the model
xgb_mape = mean_absolute_percentage_error(y_test, y_xgb_pred)
print(f"Mean Absolute Percentage Error (MAPE) for XGBoost: {xgb_mape}")

# K-Fold Cross Validation
kf = KFold(n_splits=3, shuffle=True, random_state=42)

# Using cross_val_score to calculate MAE, RMSE with cross-validation
cv_mae_xgb = cross_val_score(xgb_model, X_train, y_train, cv=kf, scoring='neg_mean_absolute_error')
cv_rmse_xgb = cross_val_score(xgb_model, X_train, y_train, cv=kf, scoring='neg_root_mean_squared_error')

# Evaluasi MAPE dengan k-fold cross-validation
cv_mape_xgb = cross_val_score(xgb_model, X_train, y_train, cv=kf,
                              scoring=lambda estimator, X, y: -mean_absolute_percentage_error(y, estimator.predict(X)))

# Display cross-validation results
print(f"K-Fold Cross-Validation MAE for XGBoost: {-cv_mae_xgb.mean()}")
print(f"K-Fold Cross-Validation RMSE for XGBoost: {-cv_rmse_xgb.mean()}")
print(f"K-Fold Cross-Validation MAPE for XGBoost: {-cv_mape_xgb.mean()}")

from sklearn.model_selection import GridSearchCV

# Define the parameter grid for GridSearchCV for XGBoost
param_grid_xgb = {
    'n_estimators': [50, 100, 150, 200],  # Number of boosting rounds
    'learning_rate': [0.01, 0.05, 0.1, 0.2],  # Learning rate
    'max_depth': [3, 4, 5, 6],  # Depth of the trees
    'subsample': [0.7, 0.8, 0.9, 1.0],  # Fraction of samples used per boosting round
    'colsample_bytree': [0.7, 0.8, 0.9, 1.0]  # Fraction of features used per tree
}

# Create GridSearchCV with XGBoost Regressor
grid_search_xgb = GridSearchCV(estimator=xgb_model, param_grid=param_grid_xgb,
                               cv=3, n_jobs=-1, verbose=2)

# Train the model with GridSearchCV
grid_search_xgb.fit(X_train, y_train)

# Display the best hyperparameters from GridSearchCV
best_params_grid_xgb = grid_search_xgb.best_params_
print("Best hyperparameters using GridSearchCV (XGBoost): ", best_params_grid_xgb)

# Predict with the best model
y_xgb_pred_grid = grid_search_xgb.predict(X_test)

# Calculate MAE and RMSE for the best model
xgb_mae_grid = mean_absolute_error(y_test, y_xgb_pred_grid)
xgb_rmse_grid = np.sqrt(mean_squared_error(y_test, y_xgb_pred_grid))

print(f"Mean Absolute Error (MAE) for XGBoost after GridSearchCV: {xgb_mae_grid}")
print(f"Root Mean Squared Error (RMSE) for XGBoost after GridSearchCV: {xgb_rmse_grid}")

# Compute MAPE for the best model
xgb_mape_grid = mean_absolute_percentage_error(y_test, y_xgb_pred_grid)
print(f"Mean Absolute Percentage Error (MAPE) for XGBoost after GridSearchCV: {xgb_mape_grid}")

# K-Fold Cross Validation
cv_mae_grid_xgb = cross_val_score(grid_search_xgb.best_estimator_, X_train, y_train, cv=kf, scoring='neg_mean_absolute_error')
cv_rmse_grid_xgb = cross_val_score(grid_search_xgb.best_estimator_, X_train, y_train, cv=kf, scoring='neg_root_mean_squared_error')

# Evaluasi MAPE dengan k-fold cross-validation
cv_mape_grid_xgb = cross_val_score(grid_search_xgb.best_estimator_, X_train, y_train, cv=kf,
                                   scoring=lambda estimator, X, y: -mean_absolute_percentage_error(y, estimator.predict(X)))

# Display cross-validation results
print(f"K-Fold Cross-Validation MAE for XGBoost (GridSearchCV): {-cv_mae_grid_xgb.mean()}")
print(f"K-Fold Cross-Validation RMSE for XGBoost (GridSearchCV): {-cv_rmse_grid_xgb.mean()}")
print(f"K-Fold Cross-Validation MAPE for XGBoost (GridSearchCV): {-cv_mape_grid_xgb.mean()}")