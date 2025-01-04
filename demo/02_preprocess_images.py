# .\demo\02_preprocess_images.py

import cv2
import os
import numpy as np

# Global constants for brightness, contrast, and saturation changes
brightness_change = 0.2  
contrast_change = 0.2    
saturation_change = 0.2  

def adjust_brightness(image, factor):
    """
    Adjusts the brightness of an image by a given factor.
    Positive factor -> increase brightness.
    Negative factor -> decrease brightness.
    """
    return np.clip(image * (1 + factor), 0, 255).astype(np.uint8)

def adjust_contrast(image, factor):
    """
    Adjusts the contrast of an image around its mean intensity value.
    Positive factor -> increase contrast.
    Negative factor -> decrease contrast.
    """
    mean = np.mean(image)
    return np.clip((1 + factor) * (image - mean) + mean, 0, 255).astype(np.uint8)

def adjust_saturation(image, factor):
    """
    Adjusts the saturation of an image in the HSV color space.
    Positive factor -> increase saturation.
    Negative factor -> decrease saturation.
    """
    hsv_img = cv2.cvtColor(image, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv_img[..., 1] = np.clip(hsv_img[..., 1] * (1 + factor), 0, 255)
    return cv2.cvtColor(hsv_img.astype(np.uint8), cv2.COLOR_HSV2BGR)

def create_image_variations(image_path, output_dir):
    """
    Reads an image from `image_path`, generates various augmented versions 
    (brightness, contrast, saturation), and saves them in `output_dir`.
    """
    image = cv2.imread(image_path)
    if image is None:
        print(f"Failed to load image: {image_path}")
        return

    # Dictionary of variation names and transformations
    variations = {
        "brightness_plus": adjust_brightness(image, brightness_change),
        "brightness_minus": adjust_brightness(image, -brightness_change),
        "contrast_plus": adjust_contrast(image, contrast_change),
        "contrast_minus": adjust_contrast(image, -contrast_change),
        "saturation_plus": adjust_saturation(image, saturation_change),
        "saturation_minus": adjust_saturation(image, -saturation_change),
    }

    # Save each variation
    for name, variation in variations.items():
        output_path = os.path.join(output_dir, f"rgb_{name}.png")
        cv2.imwrite(output_path, variation)

def process_all_images(input_folder):
    """
    Iterates over two subdirectories: 'overhead' and 'side_angle', 
    and applies image augmentation to any file named 'rgb.png'.
    
    Args:
        input_folder (str): Parent folder containing 'overhead' and 'side_angle' subfolders.

    Returns:
        None
    """
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
