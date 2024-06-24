import sys
import os 
import asyncio
import re

from aiohttp import web
from aiogram import Bot, Dispatcher, Router
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram.utils.markdown import hbold
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application

TOKEN = os.getenv('TELEGRAM_TOKEN')
WEB_SERVER_HOST = "127.0.0.1"
WEB_SERVER_PORT = 8080
WEBHOOK_PATH = "/webhook"
WEBHOOK_SECRET = "my-secret"

#your localhost tunnel URL here
BASE_WEBHOOK_URL = ""

VIDEO_PATH = 'gif/higurashi.mp4'
CAPITAL_BEGIN = 65
CAPITAL_END = 90
LOWER_BEGIN = 97 
LOWER_END = 122

router = Router()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')
tag_pattern = re.compile(r'.*\B@(?=\w{5,32}\b)[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*.*')

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Привет, этот бот создан чтобы унижать пендосов") 

@router.message()
async def message_handler(message: Message) -> None:
    if message.text:
        contains_lowercase = any(LOWER_BEGIN <= ord(char) <= LOWER_END for char in message.text)
        contains_uppercase = any(CAPITAL_BEGIN <= ord(char) <= CAPITAL_END for char in message.text)
        contains_url = url_pattern.search(message.text)
        contains_tag = tag_pattern.search(message.text)
        if contains_lowercase or contains_uppercase and not contains_url and not contains_tag:
            await message.delete()
            video = FSInputFile(VIDEO_PATH)
            sent_message = await bot.send_video(chat_id=message.chat.id, video=video, duration=10)
            await asyncio.sleep(10)
            await bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)

async def on_startup(bot: Bot) -> None:
    await bot.set_webhook(f"{BASE_WEBHOOK_URL}{WEBHOOK_PATH}", secret_token=WEBHOOK_SECRET)

def main() -> None:
    dp = Dispatcher()
    dp.include_router(router)
    dp.startup.register(on_startup)
    app = web.Application()
    webhook_reqeuests_handler = SimpleRequestHandler(
            dispatcher=dp,
            bot=bot,
            secret_token=WEBHOOK_SECRET,
    )
    webhook_reqeuests_handler.register(app, path=WEBHOOK_PATH)
    setup_application(app, dp, bot=bot)
    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)

if __name__ == "__main__":
    main()
