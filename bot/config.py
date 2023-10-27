import os
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher

load_dotenv(find_dotenv(".env"))
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot)