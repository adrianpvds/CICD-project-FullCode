# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License.
"""
Registers the best-trained ML model from the sweep job.
"""

import argparse
from pathlib import Path
import mlflow
import os 
import json
import sys

def parse_args():
    '''Parse input arguments'''

    print("Command-line arguments:", sys.argv)
    print("starting parse")

    parser = argparse.ArgumentParser()
    parser.add_argument('--model_name', type=str, help='Name under which model will be registered')  # Hint: Specify the type for model_name (str)
    parser.add_argument('--model_path', type=str, help='Model directory')  # Hint: Specify the type for model_path (str)
    parser.add_argument("--model_info_output_path", type=str, help="Path to write model info JSON")  # Hint: Specify the type for model_info_output_path (str)
    args, _ = parser.parse_known_args()
    print(f'Arguments: {args}')

    return args

def main(args):
    '''Loads the best-trained model from the sweep job and registers it'''

    print("Registering ", args.model_name)

    # -----------  WRITE YOR CODE HERE -----------
    
    print(args.model_path)
    print(args.model_info_output_path)
    
    # Step 1: Load the model from the specified path using `mlflow.sklearn.load_model` for further processing.  
    
    model = mlflow.sklearn.load_model(args.model_path)
    
    # Step 2: Log the loaded model in MLflow with the specified model name for versioning and tracking.  
    
    mlflow.sklearn.log_model(model, args.model_name)

    # Step 3: Register the logged model using its URI and model name, and retrieve its registered version.  
    
    run_id = mlflow.active_run().info.run_id
    model_uri = f'runs:/{run_id}/{args.model_name}'
    mlflow_model = mlflow.register_model(model_uri, args.model_name)
    model_version = mlflow_model.version
    
    # Step 4: Write model registration details, including model name and version, into a JSON file in the specified output path.  
    
    model_info = {
        "model_name": args.model_name,
        "model_version": model_version,
        "model_path": args.model_path
    }
    output_info_path = os.path.join(args.model_info_output_path, "model_info.json")
    with open(output_info_path, 'w') as f:
        json.dump(model_info, f, indent=4)
    print(f"Model registered under version: {model_version}")


if __name__ == "__main__":
    
    print("starting run")
    mlflow.start_run()
    print("run started")
    # Parse Arguments
    args = parse_args()
    
    lines = [
        f"Model name: {args.model_name}",
        f"Model path: {args.model_path}",
        f"Model info output path: {args.model_info_output_path}"
    ]

    for line in lines:
        print(line)

    main(args)

    mlflow.end_run()