from __future__ import unicode_literals
import yt_dlp
import ffmpeg
import sys
import base64
import speech_recognition as sr
from pathlib import Path
from datetime import datetime
import sys

from Youtube_Scrapper.utility_functions.wavSplitter import wavDivider
# from utility_functions.wavSplitter import wavDivider

r = sr.Recognizer()
def audioToText():

    with sr.AudioFile("audio1.wav") as source:  # use "audio1.wav" as the audio source
        audio = r.record(source)             

    try:
        print("Transcription: " + r.recognize_google(audio))  # recognize speech using Google Speech Recognition
    except sr.UnknownValueError:                            
        print("Could not understand audio")
    except sr.RequestError as e:                               # Could not request results from Google Speech Recognition service
        print(f"Could not request results; {e}")

ydl_opts = {
    'format': 'bestaudio/best',
    'ffmpeg_location': r'C:\Users\azad\OneDrive\Documents\ffmpeg-2024-05-20-git-127ded5078-full_build\bin',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'wav',
    }],
}

def download_from_url(url):
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # print(ydl)
        # sys.exit()
        result = ydl.extract_info(url, download=True)
        # print(result)
        
        
        original_filename = ydl.prepare_filename(result)
        print(original_filename)
    # Ensure the input file exists
    input_file = Path(original_filename)
    # if not input_file.exists():
    #     print(f"Error: The file {input_file} does not exist.")
    #     return
    
    # Change the file extension to wav
    # output_file = input_file.with_suffix('.wav')
    
    # Convert the downloaded audio to wav format
    # stream = ffmpeg.input(str(input_file))
    # stream = ffmpeg.output(stream, str(output_file))
    # ffmpeg.run(stream)
    
    # Pass the path and filename to wavDivider
    # current_dir = Path(__file__).parent.resolve()
    current_dir=r"C:\Users\azad\OneDrive\Desktop\Git\decoy backend 2"
    wav_file_path = f"{current_dir}/{original_filename.replace('.webm', '.wav')}"
    transcription=  wavDivider(wav_file_path)
    print(f"{transcription}")
    return transcription
    

# print(datetime.now())
# def initiateConvert(link):
# args = sys.argv[1:]
# if len(args) > 1:
#     print("Too many arguments.")
#     print("Usage: python videoToAudioConverter.py <optional link>")
#     print("If a link is given it will automatically convert it to .wav. Otherwise a prompt will be shown")
#     exit()
# if len(args) == 0:
#     url = input("Enter Youtube URL: ")
#     download_from_url(url)
# #    return result
# else:
#     download_from_url(args[0])
# download_from_url("https://www.youtube.com/shorts/eZV_Pmf1Psc")