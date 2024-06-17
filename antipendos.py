import asyncio
import sys
from datetime import datetime
import re
import os

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message, FSInputFile
from aiogram import Router

CAPITAL_BEGIN = 65
CAPITAL_END = 90

lower_begin = 97
lower_end = 122

TOKEN = sys.argv[1]

VIDEO_PATH = 'gif/higurashi.mp4'

LOG_FILE = 'log.txt'


def log_message(username: str, message: str) -> None:
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if not os.path.exists(LOG_FILE):
        open(LOG_FILE, 'w').close()
    with open(LOG_FILE, 'a', encoding='utf-8') as f:
        f.write(f'{timestamp} - @{username}: {message}\n')

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
url_pattern = re.compile(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+')

dp = Dispatcher()
router = Router(name=__name__)
dp.include_router(router)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Привет, этот бот создан чтобы унижать пендосов")
    log_message(message.from_user.username, f"Пользователь {message.from_user.id} запустил бота.")

@dp.message()
async def message_handler(message: Message) -> None:
    if message.text:
        contains_lowercase = any(lower_begin <= ord(char) <= lower_end for char in message.text)
        contains_url = url_pattern.search(message.text)
        
        if contains_lowercase and not contains_url:
            await message.delete()
            log_message(message.from_user.username, f"Видалено повідомлення від користувача {message.from_user.id}, яке містить літери.")
            video = FSInputFile(VIDEO_PATH)
            sent_message = await bot.send_video(chat_id=message.chat.id, video=video, duration=10)
            await asyncio.sleep(10)
            await bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)

            
async def main() -> None:
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

