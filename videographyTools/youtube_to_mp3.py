from pytube import YouTube

def test(url:str) -> None:
    yt = YouTube(url=url)
    print(yt.fmt_streams)

test(url="https://www.youtube.com/watch?v=fCrxXlthvMY")