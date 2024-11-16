import cv2
import os
import zipfile

def extract_frame(video_path, output_path, frame_number):
    # Open the video file
    cap = cv2.VideoCapture(video_path)
    
    # Set the video position to the desired frame number
    cap.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
    
    # Read the specified frame
    success, frame = cap.read()
    if success:
        # Flip the frame vertically
        flipped_frame = cv2.flip(frame, 0)
        
        # Save the flipped frame as an image
        cv2.imwrite(output_path, flipped_frame)
    else:
        print(f"Failed to read frame {frame_number} from {video_path}")
    
    # Release the video capture object
    cap.release()

def zip_h264_file(folder_path):
    # Path to the camera_a.h264 file
    h264_file = os.path.join(folder_path, "camera_a.h264")
    
    if os.path.exists(h264_file):
        # Path to the zip file
        zip_file = os.path.join(folder_path, "camera_a.zip")
        
        # Create a zip file containing the camera_a.h264 file
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(h264_file, os.path.basename(h264_file))
        
        # Remove the original .h264 file after zipping
        os.remove(h264_file)
        print(f"Zipped and removed {h264_file}")

def process_all_videos(input_folder, output_folder, frame_number):
    for folder_name in os.listdir(input_folder):
        folder_path = os.path.join(input_folder, folder_name)
        video_path = os.path.join(folder_path, "camera_A.h264")
        
        if os.path.isdir(folder_path) and os.path.exists(video_path):
            # Define the output directory and image path
            output_dir = os.path.join(output_folder, folder_name)
            os.makedirs(output_dir, exist_ok=True)
            output_image_path = os.path.join(output_dir, "rgb.png")
            
            # Extract and save the specified frame
            extract_frame(video_path, output_image_path, frame_number)
            print(f"Frame {frame_number} extracted and flipped for {folder_name}")
            
            # Zip the camera_a.h264 file after extracting the frame
            zip_h264_file(folder_path)

if __name__ == "__main__":
    input_folder = "data/raw/side_angle/"
    output_folder = "data/final/side_angle/"
    
    # Set the frame number you want to extract (e.g., 10th frame)
    frame_number = 0  # Change this to your desired frame index
    
    process_all_videos(input_folder, output_folder, frame_number)