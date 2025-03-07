# .\scripts\generate_nutrition_heatmaps.py

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# File paths for input CSV and output directories
csv_input_path = os.path.join("data", "results", "metrics_analysis.csv")
output_dir_heatmaps_metrics = os.path.join("data", "results", "heatmaps_metrics")
output_dir_heatmaps_nutrients = os.path.join("data", "results", "heatmaps_nutrients")

# Create output directories if they don't exist
os.makedirs(output_dir_heatmaps_metrics, exist_ok=True)
os.makedirs(output_dir_heatmaps_nutrients, exist_ok=True)

# Load the metrics data
df = pd.read_csv(csv_input_path)

# Define which columns belong to which metric
metrics = {
    "mae": [col for col in df.columns if "mae_" in col],
    "mape": [col for col in df.columns if "mape_" in col],
    "prop_below_20": [col for col in df.columns if "prop_below_20_" in col],
    "avg_error": [col for col in df.columns if "avg_error_" in col],
    "avg_rel_error": [col for col in df.columns if "avg_rel_error_" in col]
}

# Define which columns belong to which nutrient
nutrients = {
    "calories": [col for col in df.columns if "calories" in col],
    "mass": [col for col in df.columns if "mass" in col],
    "fat": [col for col in df.columns if "fat" in col],
    "carb": [col for col in df.columns if "carb" in col],
    "protein": [col for col in df.columns if "protein" in col]
}

def rank_and_sort(data):
    """
    Normalizes data by assigning ranks within each column, then sorts rows by
    their total rank. This ensures the best overall performance is at the top.
    
    Args:
        data (pd.DataFrame): The DataFrame containing metric or nutrient data.

    Returns:
        pd.DataFrame: The sorted DataFrame based on overall rank sum.
    """
    ranked_data = data.rank(axis=0, method="average", ascending=True)
    ranked_data["rank_sum"] = ranked_data.sum(axis=1)
    sorted_data = data.loc[ranked_data.sort_values("rank_sum").index]
    return sorted_data

def plot_heatmap(data, title, output_path):
    """
    Plots and saves a heatmap for the given DataFrame, using rank-based values.

    Args:
        data (pd.DataFrame): Data to be plotted in the heatmap.
        title (str): Title of the heatmap.
        output_path (str): File path to save the heatmap figure.
    """
    plt.figure(figsize=(10, 8))
    ranked_data = data.rank(axis=0, method="min", ascending=True)
    sns.heatmap(ranked_data, annot=data, fmt=".2f", cmap="coolwarm", cbar_kws={"label": "Rank Order"})
    plt.title(title)
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(output_path)
    plt.close()
    print(f"Saved heatmap to {output_path}")

# Generate heatmaps for each metric
for metric_name, metric_cols in metrics.items():
    metric_df = df[["condition"] + metric_cols].set_index("condition")
    metric_heatmap_path = os.path.join(output_dir_heatmaps_metrics, f"{metric_name}_heatmap.png")
    sorted_metric_df = rank_and_sort(metric_df)
    plot_heatmap(sorted_metric_df, f"Heatmap for {metric_name.upper()}", metric_heatmap_path)

# Generate heatmaps for each nutrient
for nutrient_name, nutrient_cols in nutrients.items():
    nutrient_df = df[["condition"] + nutrient_cols].set_index("condition")
    nutrient_heatmap_path = os.path.join(output_dir_heatmaps_nutrients, f"{nutrient_name}_heatmap.png")
    sorted_nutrient_df = rank_and_sort(nutrient_df)
    plot_heatmap(sorted_nutrient_df, f"Heatmap for {nutrient_name.upper()}", nutrient_heatmap_path)