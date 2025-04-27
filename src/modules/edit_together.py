import os
from moviepy.editor import *
# from moviepy.video.io.VideoFileClip import VideoFileClip # type: ignore
# from moviepy.video.compositing.CompositeVideoClip import concatenate_videoclips  # type: ignore

def cut_video_by_timestamps(video_path, timestamps, output_path=None):
    """
    Cuts a video file according to the specified timestamps and combines the segments.
    
    Args:
        video_path (str): Path to the input video file (.mp4)
        timestamps (list): List of [start, end] timestamp pairs in seconds
        output_path (str, optional): Path for the output video. If None, creates a file in the same directory
                                    with "_edited" appended to the original name.
    
    Returns:
        str: Path to the output video file
    """
    # Validate input
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video file not found: {video_path}")
    
    if not timestamps or not isinstance(timestamps, list):
        raise ValueError("Timestamps must be a non-empty list of [start, end] pairs")
    
    # Generate output path if not provided
    if output_path is None:
        base_name, ext = os.path.splitext(video_path)
        output_path = f"{base_name}_edited{ext}"
    
    try:
        # Load the video file
        video = VideoFileClip(video_path)
        
        # Cut segments according to timestamps
        segments = []
        for start, end in timestamps:
            if not (isinstance(start, (int, float)) and isinstance(end, (int, float))):
                raise ValueError(f"Invalid timestamp format: [{start}, {end}]. Must be numbers.")
            if start >= end:
                raise ValueError(f"Start time ({start}) must be less than end time ({end})")
            if end > video.duration:
                print(f"Warning: End time {end} exceeds video duration {video.duration}. Clipping to video end.")
                end = video.duration
            
            segment = video.subclipped(start, end)
            segments.append(segment)
        
        # Combine segments
        if segments:
            final_clip = concatenate_videoclips(segments)
            final_clip.write_videofile(output_path, codec="libx264", threads=7)
            final_clip.close()
        else:
            raise ValueError("No valid segments were extracted from the video")
        
        # Close the original video to free resources
        video.close()
        
        return output_path
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        # Make sure to close any open clips to prevent resource leaks
        if 'video' in locals() and video is not None:
            video.close()
        if 'segments' in locals():
            for segment in segments:
                if segment is not None:
                    segment.close()
        if 'final_clip' in locals() and final_clip is not None:
            final_clip.close()
        raise

if __name__ == "__main__":

    Timestamps_lst=[
        [14*60, 18*60+10],
        [24*60+30, 3600+12*60+35],
        [3600+28*60+48, 3600+34*60],
        [3600+54*60+30, 2*3600+9*60*15],
        [2*3600+37*60, 2*3600+45*60+10],
        [3*3600+7*60+10, 3*3600+12*60+19],
        [4*3600+20*60+38, 4*3600+30*60+48],
        [4*3600+42*60+55, 4*3600+48*60],
        [5*3600+13*60+40, 5*3600+16*60+15],
        [5*3600+18*60+30, 5*3600+21*60],
        [6*3600+8*60+33, 6*3600+12*60+36],
        [6*3600+23*60+25, 6*3600+27*60+10],
        [6*3600+47*60+54, 7*3600+45*60+10],
        [7*3600+56*60+32, 7*3600+59*60+7],
        [8*3600+4*60, 8*3600+14*60+30]
    ]
    output_path = cut_video_by_timestamps("C:/Users/Omkar2/Documents/Hackathon/auto_editor/tangerin_vid_nochapters.mp4", Timestamps_lst)