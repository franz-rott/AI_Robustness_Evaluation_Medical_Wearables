import os
import pandas as pd
import numpy as np

# Define paths
input_csv = "data/results/nutrition_evaluation.csv"
output_csv = "data/results/metrics_analysis.csv"

# Load the nutrition evaluation data
df = pd.read_csv(input_csv)

# Ground truth columns
ground_truth_cols = ["calories", "mass", "fat", "carb", "protein"]

# Initialize a list for results
results = []

# Iterate through superconditions and conditions
superconditions = ["overhead", "side_angle"]
conditions = ["rgb", "rgb_brightness_minus", "rgb_brightness_plus",
              "rgb_contrast_minus", "rgb_contrast_plus",
              "rgb_saturation_minus", "rgb_saturation_plus"]

for supercondition in superconditions:
    for condition in conditions:
        metrics = {
            "condition": f"{supercondition}_{condition}",
        }

        for nutrient in ground_truth_cols:
            ground_truth_col = nutrient
            prediction_col = f"{supercondition}_{condition}_{nutrient}"
            
            if prediction_col in df.columns and ground_truth_col in df.columns:
                # Drop rows with NaN values
                valid_data = df[[ground_truth_col, prediction_col]].dropna()
                ground_truth = valid_data[ground_truth_col]
                predictions = valid_data[prediction_col]

                if len(ground_truth) > 0:
                    # Calculate metrics
                    mae = np.mean(np.abs(predictions - ground_truth))
                    mape = np.mean(np.abs((predictions - ground_truth) / ground_truth)) * 100
                    prop_below_20 = np.mean(np.abs((predictions - ground_truth) / ground_truth) < 0.2)
                    avg_error = np.mean(predictions - ground_truth)
                    avg_rel_error = np.mean((predictions - ground_truth) / ground_truth) * 100
                else:
                    mae, mape, prop_below_20, avg_error, avg_rel_error = np.nan, np.nan, np.nan, np.nan, np.nan

                # Store metrics
                metrics[f"mae_{nutrient}"] = mae
                metrics[f"mape_{nutrient}"] = mape
                metrics[f"prop_below_20_{nutrient}"] = prop_below_20
                metrics[f"avg_error_{nutrient}"] = avg_error
                metrics[f"avg_rel_error_{nutrient}"] = avg_rel_error

        # Append results for the current condition
        results.append(metrics)

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Save the metrics analysis to CSV
os.makedirs(os.path.dirname(output_csv), exist_ok=True)
results_df.to_csv(output_csv, index=False)

print(f"Metrics analysis saved to {output_csv}")