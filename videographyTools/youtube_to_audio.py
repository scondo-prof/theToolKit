import os
import re
import subprocess

from dotenv import load_dotenv
from pytubefix import YouTube
from pytubefix.cli import on_progress

load_dotenv()

# Warning, Need ffmpeg to use conversion portion of script

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

    if os.getenv("CONVERTED_AUDIO_FORMAT"):
        new_audio_file: str = f'{output_path}\\{file_name}{os.getenv("CONVERTED_AUDIO_FORMAT")}'

        if os.getenv("CONVERTED_AUDIO_FORMAT") == ".wav":
            subprocess.run(["ffmpeg", "-i", output_file, "-vn", "-ab", "192k", "-ar", "44100", "-y", new_audio_file])
            cleanup: bool = True

        elif os.getenv("CONVERTED_AUDIO_FORMAT") == ".mp3":
            subprocess.run(["ffmpeg", "-i", output_file, "-vn", "-ar", "44100", "-ac", "2", "-y", new_audio_file])
            cleanup: bool = True

        else:
            print(f'No Logic for Audio Format: {os.getenv("CONVERTED_AUDIO_FORMAT")}')
            cleanup: bool = False

        if cleanup:
            print(f"Converted | {output_file}  ->  {new_audio_file} |")
            os.remove(path=output_file)
            print(f"Removed: {output_file}")
