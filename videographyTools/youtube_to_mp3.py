from pytubefix import YouTube
from pytubefix.cli import on_progress

url = "https://www.youtube.com/watch?v=MMihPT3-ADg"

yt = YouTube(url, on_progress_callback=on_progress)
print(yt.title)

ys = yt.streams.get_audio_only()
ys.download(output_path="Q:\\strokeNotPoke\\thePremier\\moosePond\\assets")
