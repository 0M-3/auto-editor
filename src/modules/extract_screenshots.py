import cv2
import os
import argparse
from datetime import timedelta

def extract_screenshots(video_path, output_dir, interval_seconds=60):
    """
    Extract screenshots from a video at specified time intervals
    
    Parameters:
        video_path (str): Path to the MP4 file
        output_dir (str): Directory to save screenshots
        interval_seconds (int): Interval in seconds between screenshots
    """
    # Create output directory if it doesn't exist
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # Open the video file
    video = cv2.VideoCapture(video_path)
    
    if not video.isOpened():
        print(f"Error: Could not open video file {video_path}")
        return
    
    # Get video properties
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = total_frames / fps
    
    print(f"Video FPS: {fps}")
    print(f"Total frames: {total_frames}")
    print(f"Video duration: {timedelta(seconds=int(duration))}")
    
    # Calculate frame intervals
    frame_interval = int(fps * interval_seconds)
    
    current_frame = 0
    screenshot_count = 0
    
    while current_frame < total_frames:
        # Set the frame position
        video.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
        
        # Read the frame
        success, frame = video.read()
        
        if not success:
            print(f"Failed to read frame at position {current_frame}")
            break
        
        # Calculate timestamp
        time_seconds = current_frame / fps
        timestamp = str(timedelta(seconds=int(time_seconds)))
        
        # Save the screenshot
        filename = f"screenshot_{screenshot_count:04d}_{timestamp.replace(':', '-')}.jpg"
        output_path = os.path.join(output_dir, filename)
        cv2.imwrite(output_path, frame)
        
        print(f"Saved {output_path}")
        
        # Move to next interval
        current_frame += frame_interval
        screenshot_count += 1
    
    video.release()
    print(f"Extracted {screenshot_count} screenshots")
    return duration

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract screenshots from a video at specified intervals")
    parser.add_argument("video_path", help="Path to the MP4 file")
    parser.add_argument("--output", "-o", default="screenshots", help="Output directory to save screenshots")
    parser.add_argument("--interval", "-i", type=int, default=60, help="Interval in seconds between screenshots")
    
    args = parser.parse_args()
    
    extract_screenshots(args.video_path, args.output, args.interval)
