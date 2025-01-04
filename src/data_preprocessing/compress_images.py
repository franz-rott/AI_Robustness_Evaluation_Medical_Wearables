# .\src\data_preprocessing\compress_images.py

from PIL import Image
import os

def compress_image_to_target(input_path, max_size_mb=2):
    """
    Compresses an image to ensure its size remains below `max_size_mb`.
    Reduces quality in steps, and if necessary, resizes the image dimensions.

    Args:
        input_path (str): Path to the image file.
        max_size_mb (int): Maximum allowed file size in MB.

    Returns:
        None
    """
    max_size_bytes = max_size_mb * 1024 * 1024  # Convert MB to bytes
    file_size = os.path.getsize(input_path)

    # If the file is already within the size limit, skip
    if file_size <= max_size_bytes:
        print(f"Skipping {input_path}, size already below {max_size_mb} MB")
        return

    quality = 95  # Start with high quality
    with Image.open(input_path) as image:
        image = image.convert("RGB")  # Ensure compatible format

        # Step 1: Reduce image quality
        while file_size > max_size_bytes and quality > 10:
            image.save(input_path, optimize=True, quality=quality)
            file_size = os.path.getsize(input_path)
            quality -= 5

        # Step 2: If still too large, resize the image
        if file_size > max_size_bytes:
            print(f"Resizing {input_path} to meet size requirements...")
            scale_factor = 0.9
            while file_size > max_size_bytes and scale_factor > 0:
                new_width = int(image.width * scale_factor)
                new_height = int(image.height * scale_factor)
                image = image.resize((new_width, new_height), Image.LANCZOS)
                image.save(input_path, optimize=True, quality=quality)
                file_size = os.path.getsize(input_path)
                scale_factor -= 0.05

    final_size_mb = file_size / (1024 * 1024)
    print(f"Compressed {input_path} to {final_size_mb:.2f} MB at quality {quality}")

def compress_images_in_folder(root_folder, max_size_mb=2):
    """
    Recursively compresses all .jpg, .jpeg, and .png files in the `root_folder`
    so that each is below the given `max_size_mb`.

    Args:
        root_folder (str): The folder in which to search for images.
        max_size_mb (int): Desired maximum file size in MB.

    Returns:
        None
    """
    for subdir, _, files in os.walk(root_folder):
        for filename in files:
            if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                file_path = os.path.join(subdir, filename)
                compress_image_to_target(file_path, max_size_mb)

if __name__ == "__main__":
    root_folder = "data/final/side_angle/"  # Example path
    compress_images_in_folder(root_folder, max_size_mb=2)
