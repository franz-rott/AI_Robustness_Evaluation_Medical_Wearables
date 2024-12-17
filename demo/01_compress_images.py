from PIL import Image
import os

def compress_image_to_target(input_path, max_size_mb=2):
    """
    Compresses an image to ensure its size is below max_size_mb.
    Reduces quality, and if necessary, resizes the image.
    """
    max_size_bytes = max_size_mb * 1024 * 1024  # Convert MB to bytes
    file_size = os.path.getsize(input_path)

    if file_size <= max_size_bytes:
        print(f"Skipping {input_path}, size already below {max_size_mb} MB")
        return

    quality = 95  # Start with high quality
    with Image.open(input_path) as image:
        image = image.convert("RGB")  # Ensure compatibility with JPEG compression

        # Compress by reducing quality
        while file_size > max_size_bytes and quality > 10:
            image.save(input_path, optimize=True, quality=quality)
            file_size = os.path.getsize(input_path)
            quality -= 5

        # If still too large, reduce dimensions
        if file_size > max_size_bytes:
            print(f"Resizing {input_path} to meet size requirements...")
            scale_factor = 0.9  # Start with 90% of original size
            while file_size > max_size_bytes:
                new_width = int(image.width * scale_factor)
                new_height = int(image.height * scale_factor)
                image = image.resize((new_width, new_height), Image.LANCZOS)
                image.save(input_path, optimize=True, quality=quality)
                file_size = os.path.getsize(input_path)
                scale_factor -= 0.05  # Gradually reduce size

    final_size_mb = file_size / (1024 * 1024)
    print(f"Compressed {input_path} to {final_size_mb:.2f} MB at quality {quality}")

def compress_images_in_folder(root_folder, max_size_mb=2):
    """
    Recursively compresses all images in the root folder and its subfolders.
    Ensures each image is below the specified max_size_mb.
    """
    for subdir, _, files in os.walk(root_folder):
        for filename in files:
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                file_path = os.path.join(subdir, filename)
                compress_image_to_target(file_path, max_size_mb)

# Set your root folder (e.g., "data/final/side_angle/" or "data/final/overhead/")
root_folder = "demo/data/final/"  # Change this as needed

# Run compression on all images within the folder structure
compress_images_in_folder(root_folder, max_size_mb=2)