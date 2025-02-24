# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""
Trains ML model using training dataset and evaluates using test dataset. Saves trained model.
"""

import argparse
from pathlib import Path
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import mlflow
import mlflow.sklearn

def parse_args():
    '''Parse input arguments'''

    parser = argparse.ArgumentParser("train")
    
    # -------- WRITE YOUR CODE HERE --------
    
    # Step 1: Define arguments for train data, test data, model output, and RandomForest hyperparameters. Specify their types and defaults.  
    
    parser = argparse.ArgumentParser("train")
    parser.add_argument("--train_data", type=str, help="Path to training dataset")
    parser.add_argument("--test_data", type=str, help="Path to testing dataset")
    parser.add_argument("--model_output", type=str, help="Path of output")
    parser.add_argument('--n_estimators', type=int, default=100, help='Number of trees in forest')
    parser.add_argument('--max_depth', type=int, default=None, help='Max tree depth')
    
    args = parser.parse_args()

    return args

def main(args):
    '''Read train and test datasets, train model, evaluate model, save trained model'''

    # -------- WRITE YOUR CODE HERE --------

    # Step 2: Read the train and test datasets from the provided paths using pandas. Replace '_______' with appropriate file paths and methods.  
    
    train_df = pd.read_csv(Path(args.train_data)/ "train_data.csv")
    test_df = pd.read_csv(Path(args.test_data)/ "test_data.csv")
    
    # Step 3: Split the data into features (X) and target (y) for both train and test datasets. Specify the target column name.
    
    target_column = 'price'  # Adjust 'target' to your actual target column name
    y_train = train_df[target_column]
    X_train = train_df.drop(columns=[target_column])
    y_test = test_df[target_column]
    X_test = test_df.drop(columns=[target_column])
     
    # Step 4: Initialize the RandomForest Regressor with specified hyperparameters, and train the model using the training data.
    
    model = RandomForestRegressor(n_estimators=args.n_estimators, max_depth=args.max_depth, random_state=42)
    model.fit(X_train, y_train)
     
    # Step 5: Log model hyperparameters like 'n_estimators' and 'max_depth' for tracking purposes in MLflow. 
    
    mlflow.log_param("model_type", "RandomForestRegressor")
    mlflow.log_param("n_estimators", args.n_estimators)
    mlflow.log_param("max_depth", args.max_depth)
     
    # Step 6: Predict target values on the test dataset using the trained model, and calculate the mean squared error. 
    
    yhat_test = model.predict(X_test)
    mse = mean_squared_error(y_test, yhat_test)
    print('Mean squared error: {:.2f}'.format(mse))
    
    # Step 7: Log the MSE metric in MLflow for model evaluation, and save the trained model to the specified output path.  

    mlflow.log_metric("mse", float(mse))
    mlflow.sklearn.log_model(model, args.model_output)

if __name__ == "__main__":
    
    mlflow.start_run()

    # Parse Arguments
    args = parse_args()

    lines = [
        f"Train dataset input path: {args.train_data}",
        f"Test dataset input path: {args.test_data}",
        f"Model output path: {args.model_output}",
        f"Number of Estimators: {args.n_estimators}",
        f"Max Depth: {args.max_depth}"
    ]

    for line in lines:
        print(line)

    main(args)

    mlflow.end_run()

