# .\src\data_preprocessing\extract_first_frame.py

import cv2
import os
import zipfile

def extract_frame(video_path, output_path, frame_number):
    """
    Extracts a specified frame from a video file, flips it vertically, 
    and saves it as an image.

    Args:
        video_path (str): Path to the input video file.
        output_path (str): Path to save the extracted frame as an image.
        frame_number (int): Index of the frame to extract.

    Returns:
        None
    """
    cap = cv2.VideoCapture(video_path)

    # Move to the desired frame
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    
    success, frame = cap.read()
    if success:
        # Flip vertically
        flipped_frame = cv2.flip(frame, 0)
        cv2.imwrite(output_path, flipped_frame)
    else:
        print(f"Failed to read frame {frame_number} from {video_path}")
    
    cap.release()

def zip_h264_file(folder_path):
    """
    Zips the 'camera_a.h264' file located in `folder_path` and removes the 
    original .h264 file after successful zipping.

    Args:
        folder_path (str): Directory containing the camera_a.h264 file.

    Returns:
        None
    """
    h264_file = os.path.join(folder_path, "camera_a.h264")
    
    if os.path.exists(h264_file):
        zip_file = os.path.join(folder_path, "camera_a.zip")
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(h264_file, os.path.basename(h264_file))
        
        os.remove(h264_file)
        print(f"Zipped and removed {h264_file}")

def process_all_videos(input_folder, output_folder, frame_number):
    """
    For each subfolder in `input_folder`, looks for 'camera_A.h264', extracts
    the specified frame, flips it, saves it to `output_folder`, and then zips
    the original .h264 file.

    Args:
        input_folder (str): Source directory containing video folders.
        output_folder (str): Destination directory to save extracted frames.
        frame_number (int): Frame index to extract from each video.

    Returns:
        None
    """
    for folder_name in os.listdir(input_folder):
        folder_path = os.path.join(input_folder, folder_name)
        video_path = os.path.join(folder_path, "camera_A.h264")

        if os.path.isdir(folder_path) and os.path.exists(video_path):
            # Create output directory if needed
            output_dir = os.path.join(output_folder, folder_name)
            os.makedirs(output_dir, exist_ok=True)
            output_image_path = os.path.join(output_dir, "rgb.png")

            extract_frame(video_path, output_image_path, frame_number)
            print(f"Frame {frame_number} extracted and flipped for {folder_name}")

            zip_h264_file(folder_path)

if __name__ == "__main__":
    input_folder = "data/raw/side_angle/"
    output_folder = "data/final/side_angle/"
    frame_number = 0  # Example: extract the first frame
    process_all_videos(input_folder, output_folder, frame_number)
