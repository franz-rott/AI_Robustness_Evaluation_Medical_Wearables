# .\demo\src\utils\api_connector.py

import requests
import os
import json
from pathlib import Path

# Replace with your actual API key and endpoint
API_KEY = "t9LoOWu1.wJgxTb2EYOIkjePAcAC2zYTRBU0XE4Q9"
API_URL = "https://vision.foodvisor.io/api/1.0/en/analysis/"
HEADERS = {"Authorization": f"Api-Key {API_KEY}"}

def analyze_image(image_path):
    """
    Sends an image to the Foodvisor API and returns the JSON response.

    Args:
        image_path (str): File path to the image.

    Returns:
        dict or None: JSON response from the API if successful, otherwise None.
    """
    if not os.path.exists(image_path):
        print(f"Image file not found: {image_path}")
        return None

    try:
        with open(image_path, "rb") as image:
            response = requests.post(API_URL, headers=HEADERS, files={"image": image})
            response.raise_for_status()
            return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

def save_json(data, output_path):
    """
    Saves the API response data to a JSON file.

    Args:
        data (dict): The JSON-serializable data to be saved.
        output_path (str): Path where the JSON file should be saved.

    Returns:
        None
    """
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    with open(output_path, "w") as json_file:
        json.dump(data, json_file, indent=4)
    print(f"Saved JSON to {output_path}")

def process_image(image_path, angle, dish, condition, results_root="demo/data/results/processed_results"):
    """
    Processes an image by analyzing it via the Foodvisor API and saves
    the response to a JSON file. Skips processing if the JSON file already exists.

    Args:
        image_path (str): Path to the image file.
        angle (str): Perspective of the image (e.g., 'overhead' or 'side_angle').
        dish (str): Unique identifier or name of the dish.
        condition (str): Condition label for the image (e.g., 'rgb', 'rgb_plus_brightness').
        results_root (str): Root directory to store the processed JSON results.

    Returns:
        None
    """
    output_path = os.path.join(results_root, angle, dish, f"{condition}.json")

    # Skip if file already exists
    if os.path.exists(output_path):
        print(f"Skipping {image_path}, JSON already exists.")
        return

    response = analyze_image(image_path)
    if response:
        save_json(response, output_path)
    else:
        print(f"Failed to process image: {image_path}")
