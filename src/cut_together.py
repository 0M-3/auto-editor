import csv 
from modules.edit_together import cut_video_by_timestamps
import argparse

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

def cut_vid(file_name):
    try:
        timestamps= extract_time_columns(f"./timestamps/{file_name}.csv")
        cut_video_by_timestamps(f"video/{file_name}.mp4", timestamps, f"./outputs/{file_name}.mp4")
        return 1
    except:  # noqa: E722
        return 0

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process a video.')
    parser.add_argument('video', help='The input video to process')
    args = parser.parse_args()
    success = cut_vid(args.video)
    if success==1:
        print("The task has suceeded")
    if success==0:
        print("The task has failed")
