# .\demo\04_generate_nutrition_csv.py

import os
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns

# Paths for JSON folder and final output
json_folder = "demo/data/results/processed_results"
final_output_csv = "demo/data/results/nutrition_evaluation.csv"

# Superconditions and conditions of interest
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

def process_supercondition(supercondition):
    """
    Reads JSON files for each condition under a specific supercondition (overhead/side_angle),
    aggregates total calories, and returns a DataFrame of results.
    """
    supercondition_path = os.path.join(json_folder, supercondition)
    results = []

    if os.path.exists(supercondition_path):
        for dish_folder in os.listdir(supercondition_path):
            dish_path = os.path.join(supercondition_path, dish_folder)
            dish_id = dish_folder.strip()

            dish_data = {"dish_id": dish_id}
            for condition in conditions:
                json_file = os.path.join(dish_path, f"{condition}.json")
                if os.path.exists(json_file):
                    try:
                        with open(json_file, 'r') as f:
                            json_data = json.load(f)

                        # Aggregate total calories for items with confidence > 0.5
                        total_calories = 0
                        for item in json_data.get("items", []):
                            for food in item.get("food", []):
                                if food.get("confidence", 0) > 0.5:
                                    nutrition = food.get("food_info", {}).get("nutrition", {})
                                    quantity = food.get("quantity", 0)

                                    total_calories += (nutrition.get("calories_100g", 0) * quantity) / 100

                        dish_data[f"{supercondition}_{condition}_calories"] = total_calories

                    except json.JSONDecodeError:
                        print(f"Error reading JSON file: {json_file}")
                        dish_data[f"{supercondition}_{condition}_calories"] = None
                else:
                    print(f"File {json_file} not found.")
                    dish_data[f"{supercondition}_{condition}_calories"] = None

            results.append(dish_data)

    return pd.DataFrame(results)

# Process overhead and side_angle
overhead_df = process_supercondition("overhead")
side_angle_df = process_supercondition("side_angle")

# Trim whitespace in dish_ids
overhead_df["dish_id"] = overhead_df["dish_id"].str.strip()
side_angle_df["dish_id"] = side_angle_df["dish_id"].str.strip()

# Merge both DataFrames
print("Merging all data...")
final_df = side_angle_df.merge(overhead_df, on="dish_id", how="inner")
print("Final DataFrame:")
print(final_df.head())

# Save to CSV
final_df.to_csv(final_output_csv, index=False)
print(f"Final nutrition evaluation saved to {final_output_csv}")

def create_summary_table(df):
    """
    Creates a summary table for the average calories for each condition
    across overhead and side_angle.
    """
    summary_data = []
    for condition in conditions:
        row = {
            "Condition": condition,
            "Overhead Calories": df[f"overhead_{condition}_calories"].mean(skipna=True),
            "Side Angle Calories": df[f"side_angle_{condition}_calories"].mean(skipna=True)
        }
        summary_data.append(row)
    summary_df = pd.DataFrame(summary_data)
    return summary_df

summary_table = create_summary_table(final_df)
print("\nSummary Table:")
print(summary_table)

# Plot a heatmap of the summary
plt.figure(figsize=(10, 6))
summary_heatmap = summary_table.set_index("Condition").rename(columns={
    "Overhead Calories": "Overhead",
    "Side Angle Calories": "Side Angle"
})
sns.heatmap(summary_heatmap, annot=True, cmap="coolwarm", fmt=".2f")
plt.title("Average Calories Across Conditions and Superconditions")
plt.show()

# Save the data to an Excel file with two sheets
output_excel = "demo/data/results/nutrition_evaluation_summary.xlsx"
with pd.ExcelWriter(output_excel, engine='xlsxwriter') as writer:
    final_df.to_excel(writer, sheet_name='Full Data', index=False)
    summary_table.to_excel(writer, sheet_name='Summary Table', index=False)

print(f"Nutrition evaluation with summary saved to {output_excel}")
