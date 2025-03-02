import os
from download_split import download_video, get_latest_video, split_and_add_headers
from upload_shorts import authenticate_youtube, upload_all_shorts
from utils import check_ffmpeg

def main():
    # Ensure FFmpeg is installed
    check_ffmpeg()
    
    # Ask if user wants to download a new video or use the latest downloaded one.
    choice = input("Do you want to download a new video (Y/N)? ").strip().lower()
    video_path = None
    if choice == "y":
        url = input("Enter YouTube URL: ")
        video_path = download_video(url)
    else:
        video_path = get_latest_video()
    
    # If a video is available, split and process it into shorts
    if video_path:
        split_and_add_headers(video_path)
    else:
        print("No video available for processing.")
    
    # Authenticate and then upload all shorts from the shorts folder.
    youtube = authenticate_youtube()
    shorts_folder = r"C:\Users\om\DemoProject\shorts"
    upload_all_shorts(youtube, shorts_folder)

if __name__ == "__main__":
    main()

























# import os
# import yt_dlp
# import subprocess
# from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip

# # Directories
# OUTPUT_DIR = "processed_videos"
# SHORTS_DIR = "shorts"
# os.makedirs(OUTPUT_DIR, exist_ok=True)
# os.makedirs(SHORTS_DIR, exist_ok=True)

# def check_ffmpeg():
#     """Checks if FFmpeg is installed and accessible."""
#     try:
#         subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#     except FileNotFoundError:
#         print("❌ FFmpeg is not installed or not in PATH. Install it from https://ffmpeg.org/download.html")
#         exit()

# def sanitize_filename(filename):
#     """Removes special characters from filenames to avoid file errors."""
#     return "".join(c if c.isalnum() or c in (" ", "_", "-") else "_" for c in filename).rstrip()

# def get_latest_video():
#     """Gets the latest downloaded video from the processed_videos folder."""
#     files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".mp4")]
#     if not files:
#         print("❌ No videos found in processed_videos folder!")
#         return None
#     latest_file = max(files, key=lambda f: os.path.getmtime(os.path.join(OUTPUT_DIR, f)))
#     return os.path.join(OUTPUT_DIR, latest_file)

# def download_video(youtube_url):
#     """Downloads the best quality video with audio using yt-dlp."""
#     ydl_opts = {
#         'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
#         'outtmpl': os.path.join(OUTPUT_DIR, '%(title)s.%(ext)s'),
#         'merge_output_format': 'mp4',
#         'noplaylist': True,
#     }

#     with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#         try:
#             info = ydl.extract_info(youtube_url, download=True)
#             video_title = sanitize_filename(info.get('title', 'video'))
#             video_path = os.path.join(OUTPUT_DIR, f"{video_title}.mp4")
#             print(f"✅ Video downloaded successfully: {video_path}")
#             return video_path
#         except Exception as e:
#             print(f"❌ Error downloading video: {e}")
#             return None

# def split_and_add_headers(video_path, clip_duration=29):
#     """Splits video into 29-second clips, forces a 9:16 aspect ratio, and adds headers."""
#     if not os.path.exists(video_path):
#         print(f"❌ File not found: {video_path}")
#         return
    
#     try:
#         video = VideoFileClip(video_path)
#     except Exception as e:
#         print(f"❌ Error loading video: {e}")
#         return

#     duration = int(video.duration)  # Total duration in seconds
#     base_name = sanitize_filename(os.path.splitext(os.path.basename(video_path))[0])

#     for i, start in enumerate(range(0, duration, clip_duration)):
#         output_path = os.path.join(SHORTS_DIR, f"{base_name}_part{i+1}.mp4")
#         temp_path = output_path.replace(".mp4", "_temp.mp4")
        
#         # Split the video using FFmpeg and force a vertical 9:16 output.
#         subprocess.run([
#             "ffmpeg", "-y", "-i", video_path, "-ss", str(start), "-t", str(clip_duration),
#             "-vf", "scale=w=1080:h=1920:force_original_aspect_ratio=decrease,pad=1080:1920:(ow-iw)/2:(oh-ih)/2",
#             "-c:v", "libx264", "-c:a", "aac", "-strict", "experimental", "-b:a", "192k", temp_path
#         ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

#         # Ensure temp file exists before proceeding
#         if not os.path.exists(temp_path):
#             print(f"❌ Error: FFmpeg failed to create {temp_path}")
#             continue

#         # Add header (Part 1, Part 2, etc.)
#         try:
#             video_clip = VideoFileClip(temp_path)
#             txt_clip = TextClip(f"Part {i+1}", fontsize=70, color='white', bg_color='black', method='caption')
#             txt_clip = txt_clip.set_position(("center", "top")).set_duration(video_clip.duration)

#             final_video = CompositeVideoClip([video_clip, txt_clip])
#             final_video.audio = video_clip.audio  # Ensure audio is preserved
#             final_video.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=video_clip.fps)

#             os.remove(temp_path)  # Clean up temporary file
#             print(f"🎬 Processed: {output_path}")
#         except Exception as e:
#             print(f"❌ Error adding header to video part {i+1}: {e}")

# if __name__ == "__main__":
#     check_ffmpeg()  # Ensure FFmpeg is available

#     choice = input("Do you want to download a new video (Y/N)? ").strip().lower()
    
#     if choice == "y":
#         url = input("Enter YouTube URL: ")
#         video_path = download_video(url)
#     else:
#         video_path = get_latest_video()

#     if video_path:
#         split_and_add_headers(video_path)
