import os
import re

from config import dp, bot
from aiogram.types import Message, InputFile
from aiogram.dispatcher.filters import Command
from pytube import YouTube
from moviepy.editor import AudioFileClip
from youtube_transcript_api import YouTubeTranscriptApi

@dp.message_handler(Command("/start"))
async def start(message: Message):
    await message.answer("Send me a link to the video.\nI will send you the video in mp4 format, mp3 audio and subtitles")


@dp.message_handler(lambda msg: msg.text.startswith("https://www.youtube.com/"))
async def video(message: Message):
    await message.answer("Загрузка...")

    video_link = message.text

    yt = YouTube(video_link)
    video_title = yt.title
    video_filename = f"video_({video_title}).mp4"
    audio_filename = f"audio_({video_title}).mp3"

    video_id = re.search('v=(.*)', video_link).group(1)
    video_captions_list = YouTubeTranscriptApi.get_transcript(video_id)
    video_captions = ""
    for caption in video_captions_list:
        video_captions += caption["text"] + "\n"

    captions_file = "../Captions.txt" 
    with open(captions_file, "w") as f:
        f.write(video_captions)

    yt = yt.streams.filter(res='360p', 
                           file_extension='mp4')

    yt.first().download(output_path='../videos', 
                        filename=video_filename)

    videofile_path = f"../videos/{video_filename}"
    audiofile_path = f"../audios/{audio_filename}"

    audio = AudioFileClip(videofile_path)
    audio.write_audiofile(audiofile_path)

    await bot.send_video(chat_id=message.chat.id,
                         video=InputFile(videofile_path))
    
    await bot.send_audio(chat_id=message.chat.id,
                         audio=InputFile(audiofile_path))
    
    await bot.send_document(chat_id=message.chat.id,
                            document=open(captions_file, "rb"),
                            caption="Captions")
    
    os.remove(videofile_path)
    os.remove(audiofile_path)