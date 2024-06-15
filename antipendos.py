import asyncio 
import sys
import re
import json 

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.methods.delete_message import DeleteMessage
from aiogram import Router
from aiogram.types import Chat
from aiogram.methods.send_message import SendMessage
from aiogram.types import ChatPermissions

TOKEN = sys.argv[1]
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

dp = Dispatcher()
router = Router(name=__name__)
dp.include_router(router)

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Привет, этот бот создан что бы унижать пендосов")

@dp.message()
async def message_handler(message: Message) -> None:
    permission = ChatPermissions(can_send_messages = False, can_send_audios = False, can_send_photos=False, can_send_documents = False, can_send_videos = False, can_send_other_messages=False, can_send_polls=False)
    cnt = len(re.findall('[a-zA-Z]', message.text))/len(message.text)
    tag = len(re.findall('.*\B@(?=\w{5,32}\b)[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*.*'))
    if cnt > 0.2 and tag != len(message.text):
        await message.delete()
        await bot.restrict_chat_member(message.chat.id, message.from_user.id, permissions=permission, until_date=600)
        SendMessage(chat_id=message.from_user.id, text="Отдыхай, пендос")

async def main() -> None:
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())
    
