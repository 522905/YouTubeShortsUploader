import os
import subprocess

def check_ffmpeg():
    """Checks if FFmpeg is installed and accessible."""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        print("❌ FFmpeg is not installed or not in PATH. Install it from https://ffmpeg.org/download.html")
        exit()

def sanitize_filename(filename):
    """Removes special characters from filenames to avoid file errors."""
    return "".join(c if c.isalnum() or c in (" ", "_", "-") else "_" for c in filename).rstrip()
