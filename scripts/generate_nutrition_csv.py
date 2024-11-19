import os
import pandas as pd
import json

# Define paths
json_folder = "data/results/processed_results"
final_output_csv = "data/results/nutrition_evaluation.csv"
metadata_csv = "data/raw/metadata/dish_metadata_cafe1.csv"

# Load metadata (ground truth) and clean up potential whitespace in dish_id
metadata_columns = ["dish_id", "calories", "mass", "fat", "carb", "protein"]
metadata = pd.read_csv(metadata_csv, header=None, names=metadata_columns, usecols=[0, 1, 2, 3, 4, 5])
metadata["dish_id"] = metadata["dish_id"].str.strip()  # Remove leading/trailing whitespaces
metadata = metadata.drop_duplicates(subset=['dish_id'])

# Superconditions and conditions
superconditions = ["overhead", "side_angle"]
conditions = ["rgb", "rgb_brightness_minus", "rgb_brightness_plus", 
              "rgb_contrast_minus", "rgb_contrast_plus", 
              "rgb_saturation_minus", "rgb_saturation_plus"]

# Function to process a single supercondition
def process_supercondition(supercondition):
    supercondition_path = os.path.join(json_folder, supercondition)
    results = []

    if os.path.exists(supercondition_path):
        for dish_folder in os.listdir(supercondition_path):
            dish_path = os.path.join(supercondition_path, dish_folder)
            dish_id = dish_folder.strip()  # Trim any whitespace

            dish_data = {"dish_id": dish_id}
            for condition in conditions:
                json_file = os.path.join(dish_path, f"{condition}.json")
                if os.path.exists(json_file):
                    with open(json_file, 'r') as f:
                        json_data = json.load(f)

                    # Aggregate nutrition data for items with confidence > 0.5
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

                    # Store aggregated values in specified order
                    dish_data[f"{supercondition}_{condition}_calories"] = total_calories
                    dish_data[f"{supercondition}_{condition}_mass"] = total_mass
                    dish_data[f"{supercondition}_{condition}_fat"] = total_fat
                    dish_data[f"{supercondition}_{condition}_carb"] = total_carbs
                    dish_data[f"{supercondition}_{condition}_protein"] = total_protein
                else:
                    # Fill missing JSON entries with NaNs in specified order
                    for nutrient in ["calories", "mass", "fat", "carb", "protein"]:
                        dish_data[f"{supercondition}_{condition}_{nutrient}"] = None

            results.append(dish_data)

    return pd.DataFrame(results)

# Process both superconditions
overhead_df = process_supercondition("overhead")
side_angle_df = process_supercondition("side_angle")

# Trim whitespace in dish_id
overhead_df["dish_id"] = overhead_df["dish_id"].str.strip()
side_angle_df["dish_id"] = side_angle_df["dish_id"].str.strip()

# Perform inner joins for each DataFrame with metadata
groundtruth_df = metadata.copy()
overhead_merged = groundtruth_df.merge(overhead_df, on="dish_id", how="inner")
side_angle_merged = groundtruth_df.merge(side_angle_df, on="dish_id", how="inner")

# Merge all three DataFrames on dish_id
final_df = groundtruth_df.merge(overhead_merged, on="dish_id", how="inner").merge(side_angle_merged, on="dish_id", how="inner")

# Save final CSV
final_df.to_csv(final_output_csv, index=False)
print(f"Final nutrition evaluation saved to {final_output_csv}")