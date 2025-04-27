from modules.python_downloader import download_live
from modules.extract_screenshots import extract_screenshots
from modules.extract_timestamp import extract_timestamp
from modules.edit_together import cut_video_by_timestamps

def orchestrate_all(video_url):
    file_name = download_live(video_url)
    print(f"Filename: {file_name}")
    

if __name__ == "__main__":
    # orchestrate_all("https://live.vkvideo.ru/tangerin/record/8498f588-c24a-4338-bd15-8b5c9ad7d9bb/video")
    file_name = orchestrate_all("https://live.vkvideo.ru/tangerin/record/5e0983f7-c4eb-42b6-97bb-8f3c74cac370/records")
    
