import yt_dlp
import sys
import os
from datetime import datetime

def get_next_filename(folder_path, url, base_name="file"):
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder '{folder_path}' does not exist.")
    
    # Get the username in str format
    next_filename = get_vk_video_date(url)
    
    return next_filename


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
                return f"{info_dict.get('uploader')}_vid_{formatted_date}"
            else:
                return "Date not found in metadata."
                
    except Exception as e:
        return f"An error occurred: {e}"


def download_live(video_url):
    # --- yt-dlp Options ---
    # Explanation of options:
    # 'format': Selects the best video stream with height <= 720 pixels
    #           and the best audio stream. If separate streams aren't available,
    #           it falls back to the best combined stream with height <= 720.
    #           Requires ffmpeg for merging separate streams.
    # 'outtmpl': Defines the output filename template. '%(title)s' is the video title,
    #            '%(ext)s' is the extension.
    # 'restrictfilenames': Replaces spaces and special characters in the filename
    #                      with underscores or other safe characters. This ensures
    #                      no spaces.
    # 'postprocessors': An array of actions to perform after downloading.
    #   - 'key': 'FFmpegVideoConvertor' - Uses FFmpeg to convert the video.
    #   - 'preferedformat': 'mp4' - Specifies the target format as MP4.
    #     Requires ffmpeg.
    # Optional: uncomment and set if ffmpeg is not in your PATH
    # 'ffmpeg_location': '/path/to/your/ffmpeg/bin',

    filename = get_next_filename("video/", video_url, "Tangerin_vid")

    ydl_opts = {
        'format': 'bestvideo[height<=?720]+bestaudio/best[height<=?720]',
        'outtmpl': f'./video/{filename}.%(ext)s',
        # 'restrictfilenames': True,
        # 'windowsfilenames': True,
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }],
        # 'ffmpeg_location': 'C:/ffmpeg/bin', # Example for Windows
    }

    # --- Input Validation ---
    if not video_url.startswith(('http://live.vkvideo.ru', 'https://live.vkvideo.ru')):
        print("Error: Please replace 'YOUR_VKVIDEO_URL_HERE' with a valid VK video URL.")
        sys.exit(1)


    # --- Download Process ---
    print(f"Attempting to download: {video_url}")
    print("Using options:")
    for key, value in ydl_opts.items():
        print(f"  {key}: {value}")

    try:
        # Using a 'with' statement ensures resources are cleaned up properly
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            error_code = ydl.download([video_url])
            if error_code == 0:
                print("\nDownload successful!")
                
                return filename
            else:
                print(f"\nDownload finished with errors (error code: {error_code}). Check output above.")
                return 0
    
    except KeyboardInterrupt:
        print("\nThe User has interrupted the process.")

    except yt_dlp.utils.DownloadError as e:
        print(f"\nAn error occurred during download: {e}")
        return 0
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        return 0

if __name__ == '__main__':
    # --- Configuration ---
    video_url = "https://live.vkvideo.ru/tangerin/record/94c883b7-85dd-4f2a-8cbe-fd53c956e960?tab=video"# <--- Replace with the actual VK video URL
    print(get_next_filename("video/", video_url,"Tangerin_vid"))