import pandas as pd
import os

# Load the constructed CSV
csv_input_path = os.path.join("data", "results", "metrics_analysis.csv")
output_dir_metrics = os.path.join("data", "results", "subtables_metrics")
output_dir_nutrients = os.path.join("data", "results", "subtables_nutrients")

# Create output directories if they don't exist
os.makedirs(output_dir_metrics, exist_ok=True)
os.makedirs(output_dir_nutrients, exist_ok=True)

# Load the data
df = pd.read_csv(csv_input_path)

# Define metrics and the columns that belong to each metric
metrics = {
    "mae": [col for col in df.columns if "mae_" in col],
    "mape": [col for col in df.columns if "mape_" in col],
    "prop_below_20": [col for col in df.columns if "prop_below_20_" in col],
    "avg_error": [col for col in df.columns if "avg_error_" in col],
    "avg_rel_error": [col for col in df.columns if "avg_rel_error_" in col]
}

# Define nutrient criteria and the columns that belong to each nutrient
nutrients = {
    "calories": [col for col in df.columns if "calories" in col],
    "mass": [col for col in df.columns if "mass" in col],
    "fat": [col for col in df.columns if "fat" in col],
    "carb": [col for col in df.columns if "carb" in col],
    "protein": [col for col in df.columns if "protein" in col]
}

# Save sub-tables for each metric
for metric_name, metric_cols in metrics.items():
    metric_df = df[["condition"] + metric_cols]
    metric_output_path = os.path.join(output_dir_metrics, f"{metric_name}_table.csv")
    metric_df.to_csv(metric_output_path, index=False)
    print(f"Saved {metric_name} table to {metric_output_path}")

# Save sub-tables for each nutrient criterion
for nutrient_name, nutrient_cols in nutrients.items():
    nutrient_df = df[["condition"] + nutrient_cols]
    nutrient_output_path = os.path.join(output_dir_nutrients, f"{nutrient_name}_table.csv")
    nutrient_df.to_csv(nutrient_output_path, index=False)
    print(f"Saved {nutrient_name} table to {nutrient_output_path}")