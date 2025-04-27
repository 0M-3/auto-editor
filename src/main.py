from modules.python_downloader import download_live
from modules.extract_screenshots import extract_screenshots
from modules.extract_timestamp import process_images
from modules.edit_together import cut_video_by_timestamps

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
            start_time = row['start_time']
            end_time = row['end_time']
            result.append([start_time, end_time])
    
    return result

def orchestrate_all(video_url):
    file_name = download_live(video_url)
    file_name = file_name[6:]
    duration = extract_screenshots(f"video/{file_name}", f"./screenshots/{file_name}", interval_seconds=30)
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
    cut_video_by_timestamps(f"video/{file_name}", timestamps, f"./outputs/{file_name}")
    return 1

   

if __name__ == "__main__":
    #Example Video
    bool = orchestrate_all("https://live.vkvideo.ru/tangerin/record/8498f588-c24a-4338-bd15-8b5c9ad7d9bb/video")
    if bool == 0:
        print("The task has failed")
    if bool == 1:
        print("The task has suceeded")
