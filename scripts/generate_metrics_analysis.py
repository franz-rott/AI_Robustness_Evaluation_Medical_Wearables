# .\scripts\generate_metrics_analysis.py

import os
import pandas as pd
import numpy as np

# Paths for input and output CSV files
input_csv = "data/results/nutrition_evaluation.csv"
output_csv = "data/results/metrics_analysis.csv"

# Load the nutrition evaluation data
df = pd.read_csv(input_csv)

# For convenience, rename the columns containing ground truth
# (Here assuming 'calories_x' is the ground truth for calories, etc.)
ground_truth_cols = ["calories_x", "mass", "fat", "carb", "protein"]

# Prepare a list to accumulate results
results = []

# Define the superconditions and conditions
superconditions = ["overhead", "side_angle"]
conditions = [
    "rgb", 
    "rgb_brightness_minus", 
    "rgb_brightness_plus",
    "rgb_contrast_minus", 
    "rgb_contrast_plus",
    "rgb_saturation_minus", 
    "rgb_saturation_plus"
]

# Compute metrics for each condition
for supercondition in superconditions:
    for condition in conditions:
        metrics = {
            "condition": f"{supercondition}_{condition}",
        }

        for nutrient in ground_truth_cols:
            ground_truth_col = nutrient
            prediction_col = f"{supercondition}_{condition}_{nutrient}"

            if prediction_col in df.columns and ground_truth_col in df.columns:
                # Drop rows with missing data
                valid_data = df[[ground_truth_col, prediction_col]].dropna()
                ground_truth = valid_data[ground_truth_col]
                predictions = valid_data[prediction_col]

                if len(ground_truth) > 0:
                    mae = np.mean(np.abs(ground_truth - predictions))
                    mape = np.mean(np.abs((ground_truth - predictions) / ground_truth)) * 100
                    prop_below_20 = np.mean(np.abs((ground_truth - predictions) / ground_truth) < 0.2)
                    avg_error = np.mean(predictions - ground_truth)
                    avg_rel_error = np.mean((predictions - ground_truth) / ground_truth) * 100
                else:
                    mae = mape = prop_below_20 = avg_error = avg_rel_error = np.nan

                metrics[f"mae_{nutrient}"] = mae
                metrics[f"mape_{nutrient}"] = mape
                metrics[f"prop_below_20_{nutrient}"] = prop_below_20
                metrics[f"avg_error_{nutrient}"] = avg_error
                metrics[f"avg_rel_error_{nutrient}"] = avg_rel_error

        results.append(metrics)

# Create a DataFrame from the computed metrics
results_df = pd.DataFrame(results)

# Ensure the output directory exists
os.makedirs(os.path.dirname(output_csv), exist_ok=True)
results_df.to_csv(output_csv, index=False)

print(f"Metrics analysis saved to {output_csv}")
