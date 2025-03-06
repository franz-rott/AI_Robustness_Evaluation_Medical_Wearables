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
    aggregates total calories by taking the most likely food per position, and returns a DataFrame of results.
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

                        # Aggregate total calories by selecting the most likely food per position
                        total_calories = 0
                        for item in json_data.get("items", []):
                            foods = item.get("food", [])
                            if not foods:
                                continue  # Skip if no food items

                            # Select the food with the highest confidence
                            top_food = max(foods, key=lambda x: x.get("confidence", 0))

                            # Extract nutrition and quantity
                            nutrition = top_food.get("food_info", {}).get("nutrition", {})
                            quantity = top_food.get("quantity", 0)

                            # Ensure calories_100g is present and valid
                            calories_per_100g = nutrition.get("calories_100g", 0)
                            if calories_per_100g is None:
                                calories_per_100g = 0

                            # Calculate calories
                            calories = (calories_per_100g * quantity) / 100
                            total_calories += calories

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

# Save the full dataset to CSV
full_data_csv = "demo/data/results/nutrition_evaluation_full.csv"
final_df.to_csv(full_data_csv, index=False)
print(f"Full data saved to {full_data_csv}")

# Save the summary table to CSV
summary_table_csv = "demo/data/results/nutrition_evaluation_summary.csv"
summary_table.to_csv(summary_table_csv, index=False)
print(f"Summary table saved to {summary_table_csv}")