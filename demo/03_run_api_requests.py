import sys
import os

# Dynamically set the path to include the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from src.utils.api_connector import process_image

# Define paths
image_dirs = [os.path.normpath('demo/data/final/side_angle/'), os.path.normpath('demo/data/final/overhead/')]

for image_dir in image_dirs:
    angle = os.path.basename(image_dir.strip(os.sep))

    for dish_folder in os.listdir(image_dir):
        dish_path = os.path.join(image_dir, dish_folder)

        if os.path.isdir(dish_path):
            dish = dish_folder

            for image_file in os.listdir(dish_path):
                if image_file.endswith(('.png', '.jpg', '.jpeg')):
                    condition = os.path.splitext(image_file)[0]
                    image_path = os.path.join(dish_path, image_file)

                    print(f"Processing: {image_path}")
                    process_image(image_path, angle, dish, condition)

print("All images processed.")