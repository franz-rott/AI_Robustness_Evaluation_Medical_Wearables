# .\scripts\visualize_metrics.py

import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Path to the metrics analysis CSV
metrics_input_path = os.path.join("data", "results", "metrics_analysis.csv")

# Load the data
metrics_df = pd.read_csv(metrics_input_path)

# Define which columns to look at
metrics = ["calories", "mass", "fat", "carb", "protein"]

def plot_heatmap(data, title, metric, error_type):
    """
    Plots a simple heatmap using matplotlib's imshow for the given data.

    Args:
        data (pd.DataFrame): Data to be displayed in the heatmap (2D).
        title (str): Title of the heatmap.
        metric (str): Nutrient or metric name (e.g., 'calories').
        error_type (str): Type of error (e.g., 'MAE', 'MAPE', etc.).
    
    Returns:
        None
    """
    plt.figure(figsize=(10, 6))
    plt.title(f"{title} - {metric} ({error_type})", fontsize=14)
    plt.imshow(data, cmap="coolwarm", aspect="auto", interpolation="nearest")
    plt.colorbar(label=error_type)
    plt.xticks(range(data.shape[1]), data.columns, rotation=45, ha="right")
    plt.yticks(range(data.shape[0]), data.index)
    plt.tight_layout()
    plt.show()

# Iterate over each metric and visualize results
for metric in metrics:
    metric_data = metrics_df[["condition", f"mae_{metric}", f"mape_{metric}", f"prop_below_20_{metric}"]]

    # Split supercondition and condition
    metric_data[['supercondition', 'condition']] = metric_data['condition'].str.split('_', n=1, expand=True)

    # Pivot tables for each error measure
    mae_table = metric_data.pivot(index='supercondition', columns='condition', values=f'mae_{metric}')
    mape_table = metric_data.pivot(index='supercondition', columns='condition', values=f'mape_{metric}')
    prop_below_20_table = metric_data.pivot(index='supercondition', columns='condition', values=f'prop_below_20_{metric}')

    # Print the pivot tables
    print(f"\n### {metric.upper()} METRIC ###")
    print("\nMean Absolute Error (MAE):")
    print(mae_table)
    print("\nMean Absolute Percentage Error (MAPE):")
    print(mape_table)
    print("\nProportion Below 20% Error (Prop<20%):")
    print(prop_below_20_table)

    # Plot the heatmaps
    plot_heatmap(mae_table, "Heatmap", metric, "MAE")
    plot_heatmap(mape_table, "Heatmap", metric, "MAPE")
    plot_heatmap(prop_below_20_table, "Heatmap", metric, "Prop<20%")