from pytubefix import YouTube
from pytubefix.cli import on_progress


if __name__ == "__main__":

    url: str = input("Enter Desired Video Url: ")

    yt: YouTube = YouTube(url, on_progress_callback=on_progress)
    print(f"Going to Download: {yt.title}")

    ys = yt.streams.get_audio_only()

    output_path: str = input("Enter Location of Audio Output: ")
    ys.download(output_path=output_path)

    print(f"Downloaded Video: {yt.title} | To location: {output_path}")

    # https://www.youtube.com/watch?v=MMihPT3-ADg
    # ./
