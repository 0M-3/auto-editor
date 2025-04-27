import yt_dlp
import sys
import os

def get_next_filename(folder_path, base_name="file"):
    # Ensure the folder exists
    if not os.path.exists(folder_path):
        raise FileNotFoundError(f"The folder '{folder_path}' does not exist.")
    
    # Get the list of files in the folder
    files = os.listdir(folder_path)
    
    # Extract the numeric part from filenames that match the base name pattern
    max_number = -1
    for file in files:
        if file.startswith(base_name):
            # Split the filename to extract the number
            name, ext = os.path.splitext(file)
            if name[len(base_name):].isdigit():  # Check if the remaining part is a number
                number = int(name[len(base_name):])
                if number > max_number:
                    max_number = number
    
    # Determine the next available number
    next_number = max_number + 1 if max_number != -1 else 1
    
    # Generate the next filename
    next_filename = f"{base_name}{next_number}"
    
    return next_filename

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

    filename = get_next_filename("video/", "Tangerin_vid")

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
        print(f"\nThe User has interrupted the process.")

    except yt_dlp.utils.DownloadError as e:
        print(f"\nAn error occurred during download: {e}")
        return 0
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        return 0

if __name__ == '__main__':
    # --- Configuration ---
    video_url = "YOUR_VKVIDEO_URL_HERE"# <--- Replace with the actual VK video URL
    print(get_next_filename("video/", "Tangerin_vid"))