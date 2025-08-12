from modules.python_downloader import download_live
from modules.extract_screenshots_decord import video_to_frames
from modules.extract_timestamp import process_images
from modules.edit_together import cut_video_by_timestamps
import argparse
import csv 

def confirm(prompt="Are you sure? (y/n): "):
    while True:
        choice = input(prompt).lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("Please enter y or n.")

def extract_time_columns(csv_file_path):
    result = []
    
    with open(csv_file_path, 'r', newline='') as file:
        # Create a CSV reader object
        csv_reader = csv.DictReader(file)
        
        # Extract start_time and end_time from each row
        for row in csv_reader:
            start_time = int(row['Start_time'])
            end_time = int(row['End_time'])
            result.append([start_time, end_time])
    
    return result

def orchestrate_all(video_url):
    file_name = download_live(video_url)
    if file_name ==0:
        return 0
    # duration = extract_screenshots(f"./video/{file_name}.mp4", f"./screenshots/{file_name}", interval_seconds=30)
    duration = video_to_frames(f"./video/{file_name}.mp4", "screenshots/", )
    duration = 13920
    process_images(f"./screenshots/{file_name}", duration, f"./timestamps/{file_name}.csv")
    # Example usage
    if confirm("Do you want to continue? \nEnsure that you have checked the timestamps CSV to ensure incorrect timestamps are not included.\n (y/n): "):
        print("Continuing...")
        # Perform actions if confirmed
    else:
        print("Cancelled.")
        return 0
        # Perform actions if cancelled

    timestamps= extract_time_columns(f"./timestamps/{file_name}.csv")
    cut_video_by_timestamps(f"video/{file_name}.mp4", timestamps, f"./outputs/{file_name}.mp4")
    return 1

   

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a URL.')
    parser.add_argument('url', help='The input URL to process')
    args = parser.parse_args()
    bool = orchestrate_all(args.url)
    #Example Video
    # bool = orchestrate_all("https://live.vkvideo.ru/tangerin/record/9f048ceb-6bee-4908-a6bb-258d36671ff1/records")
    if bool == 0:
        print("The task has failed")
    if bool == 1:
        print("The task has suceeded")