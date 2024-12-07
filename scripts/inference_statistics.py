import pandas as pd
import numpy as np
from scipy.stats import ttest_1samp, wilcoxon

# Load the dataset
input_csv = "data/results/nutrition_evaluation.csv"
output_csv = "data/results/statistical_tests_abs_diff_calories.csv"
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

# Test each condition
for supercondition in superconditions:
    for condition in conditions:
        test_result = {
            "condition": f"{supercondition}_{condition}",
            "p_value_abs_diff_ttest": None,
            "mean_abs_diff": None,
            "p_value_abs_diff_wilcoxon": None,
            "median_abs_diff": None
        }

        # Get the predicted calories column
        predicted_col = f"{supercondition}_{condition}_calories"
        if predicted_col in df.columns and ground_truth_col in df.columns:
            # Drop rows with NaN values
            valid_data = df[[ground_truth_col, predicted_col]].dropna()
            aligned_gt = valid_data[ground_truth_col]
            aligned_pred = valid_data[predicted_col]

            if len(aligned_gt) > 1:  # Ensure sufficient data points
                abs_diff = np.abs(aligned_pred - aligned_gt)

                # Perform one-sample t-test on absolute differences
                t_stat, p_value_ttest = ttest_1samp(abs_diff, 0)
                mean_abs_diff = np.mean(abs_diff)

                # Perform Wilcoxon Signed-Rank Test on absolute differences
                if len(abs_diff) >= 10:  # Wilcoxon requires more than a few samples
                    t_stat_wilcoxon, p_value_wilcoxon = wilcoxon(abs_diff)
                    median_abs_diff = np.median(abs_diff)
                else:
                    p_value_wilcoxon, median_abs_diff = None, None

                # Store results
                test_result["p_value_abs_diff_ttest"] = p_value_ttest
                test_result["mean_abs_diff"] = mean_abs_diff
                test_result["p_value_abs_diff_wilcoxon"] = p_value_wilcoxon
                test_result["median_abs_diff"] = median_abs_diff

        results.append(test_result)

# Convert results to a DataFrame
results_df = pd.DataFrame(results)

# Save the results to CSV
results_df.to_csv(output_csv, index=False)
print(f"Statistical test results for absolute differences saved to {output_csv}")