import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Define paths
metrics_input_path = os.path.join("data", "results", "metrics_analysis.csv")

# Load the metrics analysis data
metrics_df = pd.read_csv(metrics_input_path)

# Metrics of interest
metrics = ["calories", "mass", "fat", "carb", "protein"]

# Heatmap function
def plot_heatmap(data, title, metric, error_type):
    plt.figure(figsize=(10, 6))
    plt.title(f"{title} - {metric} ({error_type})", fontsize=14)
    plt.imshow(data, cmap="coolwarm", aspect="auto", interpolation="nearest")
    plt.colorbar(label=error_type)
    plt.xticks(range(data.shape[1]), data.columns, rotation=45, ha="right")
    plt.yticks(range(data.shape[0]), data.index)
    plt.tight_layout()
    plt.show()

# Iterate over each metric and visualize the results
for metric in metrics:
    # Filter data for current metric
    metric_data = metrics_df[["condition", f"mae_{metric}", f"mape_{metric}", f"prop_below_20_{metric}"]]
    
    # Extract supercondition and condition from `condition` column
    metric_data[['supercondition', 'condition']] = metric_data['condition'].str.split('_', n=1, expand=True)
    
    # Pivot tables for each metric and error type
    mae_table = metric_data.pivot(index='supercondition', columns='condition', values=f'mae_{metric}')
    mape_table = metric_data.pivot(index='supercondition', columns='condition', values=f'mape_{metric}')
    prop_below_20_table = metric_data.pivot(index='supercondition', columns='condition', values=f'prop_below_20_{metric}')

    # Print tables
    print(f"\n### {metric.upper()} METRIC ###")
    print("\nMean Absolute Error (MAE):")
    print(mae_table)
    print("\nMean Absolute Percentage Error (MAPE):")
    print(mape_table)
    print("\nProportion Below 20% (Prop<20%):")
    print(prop_below_20_table)

    # Plot heatmaps
    plot_heatmap(mae_table, "Heatmap", metric, "MAE")
    plot_heatmap(mape_table, "Heatmap", metric, "MAPE")
    plot_heatmap(prop_below_20_table, "Heatmap", metric, "Prop<20%")