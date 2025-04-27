import yt_dlp
import sys

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

    ydl_opts = {
        'format': 'bestvideo[height<=?720]+bestaudio/best[height<=?720]',
        'outtmpl': './video/%(title)s.%(ext)s',
        'restrictfilenames': True,
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
                info = ydl.extract_info(video_url, download=False)
                
                # Get filename from info
                filename = ydl.prepare_filename(info)
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
    video_url = "YOUR_VKVIDEO_URL_HERE"  # <--- Replace with the actual VK video URL