import telebot
import glob
import yt_dlp
import os
TOKEN = "7788543723:AAFysq3jARWLSf1ol8CDHd4V0ICfxVc8fKk" #TOKEN
bot = telebot.TeleBot(TOKEN)

AUDIO_DIR = "audio"
AUDIO_SONGS = {i.replace(f"{AUDIO_DIR}\\","").replace("_"," ").replace(".mp3","") : i for i in glob.glob(f"{AUDIO_DIR}/*.mp3")}
START_MSG = "Лабораторная работа №1"

START_BTNS = [
    ("Работа с изображениями (выслать сгенерированное или готовое по запросу)", "image_button"),# image button
    ("Работа с аудиофайлами (выслать сгенерированный или готовый по запросу)", "audio_button"), # audio button
    ("Получить ссылку на публичный репозиторий с исходниками бота", "source_button") # source button
]

IMG_BTNS = [
    ("Сгенерировать изображение по запросу", "generate_img"),
    ("Отправить изображение по ссылке", "link_img"),
    ("Назад на главную", "back_to_main")
            ]

AUDIO_BTNS = [
    ("Сгенерировать text-to-speech", "generate_audio"),
    ("Отправить аудио по запросу", "link_sound"),
    ("Назад на главную", "back_to_main")
]

REP_URL = ""    # ссылка на гитхаб


def audio_yt(query):
    ydl_opts = {
        'format': 'm4a/bestaudio/best',  # Best audio quality
        'noplaylist': True,  # Don't download playlists
        # 'skip-download': True
        # 'quiet': True,  # Suppress output for cleaner logs
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Search for the query and get the first result
        info = ydl.extract_info(f"ytsearch1:{query}", download=False)
        url = "https://www.youtube.com/watch?v=" + info['entries'][0]['id']  # Return the URL of the first video
        ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'audio/tmp',  # Save in current directory
        'quiet': True,
    }

    # Download the audio
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        filename = f"{info['title']}.mp3"  # Construct filename

    # Send the audio file to Telegram
    with open('audio/tmp.mp3', 'rb') as audio_file: return (audio_file.read(), filename)


# audio_yt("Всё идет по плану")
# Пример использования
