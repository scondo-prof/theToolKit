import os
import re
import subprocess

from dotenv import load_dotenv
from pytubefix import YouTube
from pytubefix.cli import on_progress

load_dotenv()

if __name__ == "__main__":

    url: str = input("Enter Desired Video Url: ")

    yt: YouTube = YouTube(url, on_progress_callback=on_progress)
    print(f"Going to Download: {yt.title}")

    ys = yt.streams.get_audio_only()

    if os.getenv("OUTPUT_PATH"):
        output_path: str = os.getenv("OUTPUT_PATH")

    else:
        output_path: str = input("Enter Location of Audio Output: ")

    print(f"Output Location: {output_path}")

    file_name: str = yt.title
    file_name = file_name.lower()
    file_name = file_name.replace(" ", "_")
    file_name = re.sub(r"[^a-z0-9_]", "", file_name)

    output_file: str = ys.download(output_path=output_path, filename=f"{file_name}.m4a")

    print(f"Downloaded Video: {yt.title} | To location: {output_file}")
