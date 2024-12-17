import cv2
import os
import numpy as np

# Adjust these values to change the percentage for brightness, contrast, and saturation modifications
brightness_change = 0.2  
contrast_change = 0.2    
saturation_change = 0.2  

def adjust_brightness(image, factor):
    # Clip to avoid overflow after adjustment
    return np.clip(image * (1 + factor), 0, 255).astype(np.uint8)

def adjust_contrast(image, factor):
    # Mean value for RGB image to adjust around the center intensity
    mean = np.mean(image)
    return np.clip((1 + factor) * (image - mean) + mean, 0, 255).astype(np.uint8)

def adjust_saturation(image, factor):
    # Convert to HSV to adjust saturation
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv_img[..., 1] = np.clip(hsv_img[..., 1] * (1 + factor), 0, 255)
    return cv2.cvtColor(hsv_img.astype(np.uint8), cv2.COLOR_HSV2BGR)

def create_image_variations(image_path, output_dir):
    # Load image
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image: {image_path}")
        return

    # Create variations and save
    variations = {
        "brightness_plus": adjust_brightness(image, brightness_change),
        "brightness_minus": adjust_brightness(image, -brightness_change),
        "contrast_plus": adjust_contrast(image, contrast_change),
        "contrast_minus": adjust_contrast(image, -contrast_change),
        "saturation_plus": adjust_saturation(image, saturation_change),
        "saturation_minus": adjust_saturation(image, -saturation_change),
    }

    # Save variations in output directory
    for name, variation in variations.items():
        output_path = os.path.join(output_dir, f"rgb_{name}.png")
        cv2.imwrite(output_path, variation)

def process_all_images(input_folder):
    # Iterate over both 'overhead' and 'side_angle' subdirectories
    for subfolder in ['overhead', 'side_angle']:
        subfolder_path = os.path.join(input_folder, subfolder)
        for folder_name in os.listdir(subfolder_path):
            dish_path = os.path.join(subfolder_path, folder_name)
            image_path = os.path.join(dish_path, "rgb.png")
            if os.path.isfile(image_path):
                print(f"Processing {image_path}")
                create_image_variations(image_path, dish_path)
            else:
                print(f"No image found in {dish_path}")

if __name__ == "__main__":
    input_folder = "demo/data/final/"
    process_all_images(input_folder)