import yt_dlp
from datetime import datetime

def get_vk_video_date(url):
    """
    Extracts the upload date of a VK video using yt-dlp and formats it as 'dd_mm_yy'.

    Args:
        url (str): The URL of the VK video.

    Returns:
        str or None: The formatted date string 'dd_mm_yy', or None if extraction fails.
    """
    ydl_opts = {
        'simulate': True,           # Don't download the video
        'quiet': True,              # Suppress standard output
        'force_generic_extractor': False, # Allow specific VK extractor
        'extract_flat': True,       # Only extract metadata, don't follow playlists/channels
        'skip_download': True,      # Skip the download
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
            
            # The date is usually stored under the 'upload_date' key in YYYYMMDD format
            upload_date_str = info_dict.get('release_date')
            
            if upload_date_str:
                # Parse the YYYYMMDD string into a datetime object
                date_object = datetime.strptime(upload_date_str, '%Y%m%d')
                
                # Format the datetime object to 'dd_mm_yy'
                formatted_date = date_object.strftime('%d_%m_%y')
                return formatted_date
            else:
                return "Date not found in metadata."
                
    except Exception as e:
        return f"An error occurred: {e}"

if __name__=='__main__':
# The URL to process
    video_url = "https://live.vkvideo.ru/tangerin/record/5683d7b9-cdbc-4397-aa64-0b51523b8048?tab=video"

# Get the date
    result_date = get_vk_video_date(video_url)

    print(f"Extracted Date: {result_date}")
