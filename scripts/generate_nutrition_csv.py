# .\scripts\generate_nutrition_csv.py

import os
import pandas as pd
import json

# Paths for JSON data, final output CSV, and metadata
json_folder = "data/results/processed_results"
final_output_csv = "data/results/nutrition_evaluation.csv"
metadata_csv = "data/raw/metadata/dish_metadata_cafe1.csv"

# Define columns for the metadata CSV
metadata_columns = ["dish_id", "calories", "mass", "fat", "carb", "protein"]
metadata = pd.read_csv(
    metadata_csv,
    header=None,
    names=metadata_columns,
    usecols=[0, 1, 2, 3, 4, 5]
)

# Clean dish_id by stripping whitespace
metadata["dish_id"] = metadata["dish_id"].str.strip()
metadata = metadata.drop_duplicates(subset=['dish_id'])

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
    Aggregates nutritional data from JSON results for a specific supercondition 
    (overhead or side_angle). Returns a DataFrame of aggregated data.
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

                        total_calories = total_mass = total_fat = total_carbs = total_protein = 0
                        for item in json_data.get("items", []):
                            for food in item.get("food", []):
                                if food.get("confidence", 0) > 0.5:
                                    nutrition = food.get("food_info", {}).get("nutrition", {})
                                    quantity = food.get("quantity", 0)

                                    total_calories += (nutrition.get("calories_100g", 0) * quantity) / 100
                                    total_mass += quantity
                                    total_fat += (nutrition.get("fat_100g", 0) * quantity) / 100
                                    total_carbs += (nutrition.get("carbs_100g", 0) * quantity) / 100
                                    total_protein += (nutrition.get("proteins_100g", 0) * quantity) / 100

                        # If absolutely no data was added, set them to None
                        if all(val == 0 for val in [total_calories, total_mass, total_fat, total_carbs, total_protein]):
                            total_calories = total_mass = total_fat = total_carbs = total_protein = None

                        dish_data[f"{supercondition}_{condition}_calories"] = total_calories
                        dish_data[f"{supercondition}_{condition}_mass"] = total_mass
                        dish_data[f"{supercondition}_{condition}_fat"] = total_fat
                        dish_data[f"{supercondition}_{condition}_carb"] = total_carbs
                        dish_data[f"{supercondition}_{condition}_protein"] = total_protein

                    except json.JSONDecodeError:
                        print(f"Error reading JSON file: {json_file}")
                        for nutrient in ["calories", "mass", "fat", "carb", "protein"]:
                            dish_data[f"{supercondition}_{condition}_{nutrient}"] = None
                else:
                    print(f"File {json_file} not found.")
                    for nutrient in ["calories", "mass", "fat", "carb", "protein"]:
                        dish_data[f"{supercondition}_{condition}_{nutrient}"] = None

            results.append(dish_data)

    return pd.DataFrame(results)

# Process overhead and side_angle data
overhead_df = process_supercondition("overhead")
side_angle_df = process_supercondition("side_angle")

# Clean dish IDs
overhead_df["dish_id"] = overhead_df["dish_id"].str.strip()
side_angle_df["dish_id"] = side_angle_df["dish_id"].str.strip()

# Merge overhead, side_angle with metadata
print("Merging metadata with overhead data...")
overhead_merged = metadata.merge(overhead_df, on="dish_id", how="inner")
print(overhead_merged.head())

print("Merging metadata with side_angle data...")
side_angle_merged = metadata.merge(side_angle_df, on="dish_id", how="inner")
print(side_angle_merged.head())

# Merge all data
print("Merging all data...")
final_df = (
    metadata
    .merge(overhead_merged, on="dish_id", how="inner")
    .merge(side_angle_merged, on="dish_id", how="inner")
)

print("Final DataFrame:")
print(final_df.head())

# Save the final DataFrame
final_df.to_csv(final_output_csv, index=False)
print(f"Final nutrition evaluation saved to {final_output_csv}")