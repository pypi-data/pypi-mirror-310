"""
RobustPreprocessor_v1

- Modify contant logic to choose only std == 0.

This class is designed to handle typical preprocessing requirements with options that theoretically align well with best practices for handling outliers, infinity values, missing values, and low-variance feature removal. The added flexibility in choosing methods ensures that it can adapt to different data distributions and user needs without requiring further statistical or hypothesis tests for most practical purposes.

The theoretical guarantees are effectively addressed by:
- **Outlier handling** through configurable methods (IQR and Z-score),
- **Infinity handling** with options to replace, drop, or set values, 
- **Missing value imputation** with common strategies (mean, median, mode), and
- **Feature removal** for constant or near-constant columns, optimizing feature relevance.

This setup should be robust for typical datasets and preprocessing workflows. There’s no need for additional statistical or hypothesis testing steps unless specific analysis requirements emerge. 

All set—nothing more is needed for now!

----

Key Changes:
Outlier Handling (outlier_method): Now you can choose "IQR" (default) or "Z-score."
Infinity Handling (infinity_handling): Options include "replace" (default), "drop_rows," or "set_value."
Missing Value Imputation (missing_value_strategy): Options are "mean" (default), "median," or "most_frequent."
Feature Removal (feature_removal_criteria): Options are "constant" (default), "near_constant," or "none."

Logging:
User Selections: The user_selections key in json_output records the user's chosen parameters for outlier_method, infinity_handling, missing_value_strategy, and feature_removal_criteria.
Steps Executed: The steps_executed dictionary in json_output logs each preprocessing step with details about actions taken, such as the number of columns dropped and the imputation strategy used.
Execution Time and Output Summary: At the end of the preprocess method, json_output contains a comprehensive summary that includes all user selections, actions taken in each step, the number of dropped columns, and the total execution time.

"""

import time
import json
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
import matplotlib.pyplot as plt
from scipy.stats import zscore

class RobustPreprocessor:
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.imputer = None  # Placeholder for the imputer
        self.json_output = {}

    def preprocess(self, X, outlier_method="IQR", infinity_handling="set_value", missing_value_strategy="mean", feature_removal_criteria="constant"):
        start_time = time.time()  # Record start time

        # Initialize json_output with all required fields and user selections
        self.json_output = {
            "process_type": "RobustPreprocessor",
            "user_selections": {
                "outlier_method": outlier_method,
                "infinity_handling": infinity_handling,
                "missing_value_strategy": missing_value_strategy,
                "feature_removal_criteria": feature_removal_criteria
            },
            "steps_executed": {},
            "dropped_columns": 0,
            "execution_time_seconds": None
        }
        
        if self.verbose:
            print("Starting data preprocessing steps...\n")

        # Step 1: Select numeric columns only
        X = X.select_dtypes(include=[np.number])
        self.json_output["steps_executed"]["select_numeric_columns"] = f"Selected {len(X.columns)} numeric columns"
        if self.verbose:
            print(f"Step 1: Selected {len(X.columns)} numeric columns only.")

        # Step 2: Handle outliers based on the selected method
        if outlier_method == "IQR":
            # IQR method
            for col in X.columns:
                Q1, Q3 = X[col].quantile(0.25), X[col].quantile(0.75)
                IQR = Q3 - Q1
                X[col] = X[col].clip(lower=Q1 - 1.5 * IQR, upper=Q3 + 1.5 * IQR)
            self.json_output["steps_executed"]["outlier_handling"] = "Handled outliers using IQR method."
            if self.verbose:
                print("Step 2: Handled outliers using IQR method.")
        elif outlier_method == "Z-score":
            # Z-score method
            X = X[(np.abs(zscore(X)) < 3).all(axis=1)]
            self.json_output["steps_executed"]["outlier_handling"] = "Handled outliers using Z-score method."
            if self.verbose:
                print("Step 2: Handled outliers using Z-score method.")
        else:
            raise ValueError("Invalid outlier_method. Choose either 'IQR' or 'Z-score'.")

        # Step 3: Handle infinity values based on the selected handling option
        if infinity_handling == "replace":
            for col in X.columns:
                if np.isinf(X[col]).any():
                    finite_vals = X[col][np.isfinite(X[col])]
                    if not finite_vals.empty:
                        X[col] = X[col].replace([np.inf, -np.inf], 
                                                [finite_vals.max(), finite_vals.min()])
            self.json_output["steps_executed"]["infinity_handling"] = "Replaced infinity values with finite extremes."
            if self.verbose:
                print("Step 3: Replaced infinity values with finite extremes.")
        elif infinity_handling == "drop_rows":
            X = X.replace([np.inf, -np.inf], np.nan).dropna()
            self.json_output["steps_executed"]["infinity_handling"] = "Dropped rows containing infinity values."
            if self.verbose:
                print("Step 3: Dropped rows with infinity values.")
        elif infinity_handling == "set_value":
            X = X.replace([np.inf, -np.inf], 0)
            self.json_output["steps_executed"]["infinity_handling"] = "Replaced infinity values with a set value (0)."
            if self.verbose:
                print("Step 3: Replaced infinity values with a set value (0).")
        else:
            raise ValueError("Invalid infinity_handling. Choose 'replace', 'drop_rows', or 'set_value'.")

        # Step 4: Impute missing values based on the selected strategy
        if missing_value_strategy == "mean":
            self.imputer = SimpleImputer(strategy='mean')
        elif missing_value_strategy == "median":
            self.imputer = SimpleImputer(strategy='median')
        elif missing_value_strategy == "most_frequent":
            self.imputer = SimpleImputer(strategy='most_frequent')
        else:
            raise ValueError("Invalid missing_value_strategy. Choose 'mean', 'median', or 'most_frequent'.")

        X = pd.DataFrame(self.imputer.fit_transform(X), columns=X.columns)
        self.json_output["steps_executed"]["missing_value_imputation"] = f"Imputed missing values with {missing_value_strategy} strategy."
        if self.verbose:
            print(f"Step 4: Imputed missing values with {missing_value_strategy} strategy.")

        # Step 5: Drop features based on feature removal criteria
        to_drop = []
        if feature_removal_criteria == "constant":
            to_drop = [col for col in X.columns if X[col].std() == 0]
            self.json_output["steps_executed"]["feature_removal"] = f"Dropped {len(to_drop)} constant columns."
        elif feature_removal_criteria == "near_constant":
            to_drop = [col for col in X.columns if X[col].std() < 1e-3]
            self.json_output["steps_executed"]["feature_removal"] = f"Dropped {len(to_drop)} near-constant columns."
        elif feature_removal_criteria == "none":
            to_drop = []  # No columns to drop
            self.json_output["steps_executed"]["feature_removal"] = "No columns dropped."
        else:
            raise ValueError("Invalid feature_removal_criteria. Choose 'constant', 'near_constant', or 'none'.")

        X = X.drop(columns=to_drop)
        self.json_output["dropped_columns"] = len(to_drop)
        
        if self.verbose:
            print(f"Step 5: Dropped columns based on {feature_removal_criteria} criteria. Columns dropped: {len(to_drop)}")

        # Calculate execution time
        end_time = time.time()
        execution_time = end_time - start_time
        self.json_output["execution_time_seconds"] = execution_time
        
        if self.verbose:
            print(f"\nData preprocessing completed in {execution_time:.4f} seconds.")
        else:
            print(json.dumps(self.json_output, indent=4))

        return X

    def plot_feature_distributions(self, X):
        """Plots the distribution of each feature in the dataset."""
        num_features = X.shape[1]
        cols = 3  # Number of columns for subplots
        rows = (num_features // cols) + (num_features % cols > 0)  # Calculate rows needed

        fig, axes = plt.subplots(rows, cols, figsize=(15, 5 * rows))
        axes = axes.flatten()  # Flatten the array of axes for easy iteration

        for i, col in enumerate(X.columns):
            ax = axes[i]
            ax.hist(X[col], bins=30, color='skyblue', edgecolor='black')
            ax.set_title(f'{col}')
            ax.set_xlabel('Value')
            ax.set_ylabel('Frequency')

        # Hide any unused subplots
        for j in range(i + 1, len(axes)):
            fig.delaxes(axes[j])

        plt.tight_layout()
        plt.show()
