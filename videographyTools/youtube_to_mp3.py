from pytube import YouTube
import os
from pydub import AudioSegment
import subprocess

def download_video_as_mp3(youtube_url, output_path):
    # Download video
    yt = YouTube(youtube_url)
    video = yt.streams.filter(only_audio=True).first()

    # Generate MP3 filename directly
    mp3_filename = video.default_filename.replace(".mp4", ".mp3")

    # Download directly as MP3
    out_file = video.download(output_path=output_path, filename=mp3_filename)

    print(f"Downloaded and saved as MP3: {out_file}")
    return out_file



def convert_mp3_to_wav_ffmpeg(mp3_file_path, wav_file_path):
    # Command to convert MP3 to WAV using ffmpeg
    cmd = ['ffmpeg', '-i', mp3_file_path, wav_file_path]

    try:
        # Execute the command
        subprocess.run(cmd, check=True)
        print(f"Successfully converted {mp3_file_path} to {wav_file_path}")
    except subprocess.CalledProcessError as e:
        # Handle errors
        print(f"Error occurred while converting file: {e}")


def convert_mov_to_mp4(mov_file_path, mp4_file_path):
    # Command to convert MOV to MP4 using ffmpeg
    cmd = ['ffmpeg', '-i', mov_file_path, '-codec', 'copy', mp4_file_path]

    try:
        # Execute the command
        subprocess.run(cmd, check=True)
        print(f"Successfully converted {mov_file_path} to {mp4_file_path}")
    except subprocess.CalledProcessError as e:
        # Handle errors in the conversion process
        print(f"Error occurred while converting file: {e}")
    except Exception as e:
        # Handle other exceptions such as invalid input paths
        print(f"An error occurred: {e}")

# Example usage



def main(transform):

    if transform == ".mov":
        mov_file_path = 'C:\\Users\\scott\\Documents\\github\\tools\\theToolKit\\Trimmed_Lesson_2_4.mov'
        mp4_file_path = 'C:\\Users\\scott\\Documents\\github\\tools\\theToolKit\\Trimmed_Lesson_2_4.mp4'

        convert_mov_to_mp4(mov_file_path, mp4_file_path)    

    elif transform == "yt-wav":
        youtube_url = 'https://www.youtube.com/watch?v=EvL_nlrUCrY'
        output_path = 'C:\\Users\\scott\\OneDrive\\Documents\\drones\\syzygy' 
        print('before mp3') # Specify your output path
        mp3_file_name = download_video_as_mp3(youtube_url, output_path)
        print('post mp3')
        
        wav_file_path = mp3_file_name.replace('mp3', 'wav')

        print('before ffmpeg')
        convert_mp3_to_wav_ffmpeg(mp3_file_name, wav_file_path)

main("yt-wav")