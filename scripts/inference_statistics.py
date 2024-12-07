import pandas as pd
import numpy as np
from scipy.stats import ttest_1samp

# Load the dataset
input_csv = "data/results/nutrition_evaluation.csv"
output_csv = "data/results/statistical_tests_calories.csv"
df = pd.read_csv(input_csv)

# Rename columns for clarity
df.rename(columns={"calories_x": "ground_truth_calories"}, inplace=True)

# Ground truth column for calories
ground_truth_col = "ground_truth_calories"

# Conditions to compare
superconditions = ["overhead", "side_angle"]
conditions = ["rgb", "rgb_brightness_minus", "rgb_brightness_plus",
              "rgb_contrast_minus", "rgb_contrast_plus",
              "rgb_saturation_minus", "rgb_saturation_plus"]

# Results container
results = []

# Perform the one-sample t-tests for all comparisons
for supercondition in superconditions:
    for condition in conditions:
        condition_name = f"{supercondition}_{condition}"
        predicted_col = f"{condition_name}_calories"
        test_result = {"condition": condition_name}

        # Ground Truth Comparison
        if predicted_col in df.columns and ground_truth_col in df.columns:
            valid_data = df[[ground_truth_col, predicted_col]].dropna()
            ground_truth = valid_data[ground_truth_col]
            predictions = valid_data[predicted_col]
            abs_differences = np.abs(predictions - ground_truth)

            if len(abs_differences) > 1:  # Ensure sufficient data points
                t_stat, p_value = ttest_1samp(abs_differences, 0)
                mean_abs_diff = np.mean(abs_differences)
                test_result["p_value_ground_truth"] = p_value
                test_result["mean_absolute_difference_ground_truth"] = mean_abs_diff
            else:
                test_result["p_value_ground_truth"] = None
                test_result["mean_absolute_difference_ground_truth"] = None

        # Counterpart Comparison
        counterpart_condition = (
            f"overhead_{condition}" if supercondition == "side_angle" else f"side_angle_{condition}"
        )
        counterpart_col = f"{counterpart_condition}_calories"
        if counterpart_col in df.columns and predicted_col in df.columns:
            valid_data = df[[predicted_col, counterpart_col]].dropna()
            predictions = valid_data[predicted_col]
            counterpart_predictions = valid_data[counterpart_col]
            abs_differences = np.abs(predictions - counterpart_predictions)

            if len(abs_differences) > 1:  # Ensure sufficient data points
                t_stat, p_value = ttest_1samp(abs_differences, 0)
                mean_abs_diff = np.mean(abs_differences)
                test_result["p_value_counterpart"] = p_value
                test_result["mean_absolute_difference_counterpart"] = mean_abs_diff
            else:
                test_result["p_value_counterpart"] = None
                test_result["mean_absolute_difference_counterpart"] = None

        # Base Condition Comparison
        base_condition_col = f"{supercondition}_rgb_calories"
        if predicted_col != base_condition_col and base_condition_col in df.columns:
            valid_data = df[[predicted_col, base_condition_col]].dropna()
            predictions = valid_data[predicted_col]
            base_predictions = valid_data[base_condition_col]
            abs_differences = np.abs(predictions - base_predictions)

            if len(abs_differences) > 1:  # Ensure sufficient data points
                t_stat, p_value = ttest_1samp(abs_differences, 0)
                mean_abs_diff = np.mean(abs_differences)
                test_result["p_value_base_condition"] = p_value
                test_result["mean_absolute_difference_base_condition"] = mean_abs_diff
            else:
                test_result["p_value_base_condition"] = None
                test_result["mean_absolute_difference_base_condition"] = None

        # Append the results for the current condition
        results.append(test_result)

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Save the results to CSV
results_df.to_csv(output_csv, index=False)

print(f"Statistical test results saved to {output_csv}")