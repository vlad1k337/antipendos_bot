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
import imgui
import glfw
import OpenGL.GL as gl
from imgui.integrations.glfw import GlfwRenderer


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
tag_pattern = re.compile(r'.*\B@(?=\w{5,32}\b)[a-zA-Z0-9]+(?:_[a-zA-Z0-9]+)*.*')

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
        contains_tag = tag_pattern.search(message.text)
        if contains_lowercase and not contains_url and not contains_tag:
            await message.delete()
            log_message(message.from_user.username, f"Видалено повідомлення від користувача {message.from_user.id}, яке містить літери.")
            video = FSInputFile(VIDEO_PATH)
            sent_message = await bot.send_video(chat_id=message.chat.id, video=video, duration=10)
            await asyncio.sleep(10)
            await bot.delete_message(chat_id=sent_message.chat.id, message_id=sent_message.message_id)

            
async def main() -> None:
    await dp.start_polling(bot)

async def stop() -> None:
    await dp.stop_polling(bot)

def impl_glfw_init(window_name="minimal ImGui/GLFW3 example", width=1280, height=720):
    if not glfw.init():
        print("Could not initialize OpenGL context")
        exit(1)

    # OS X supports only forward-compatible core profiles from 3.2
    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, gl.GL_TRUE)

    # Create a windowed mode window and its OpenGL context
    window = glfw.create_window(int(width), int(height), window_name, None, None)
    glfw.make_context_current(window)

    if not window:
        glfw.terminate()
        print("Could not initialize Window")
        exit(1)

    return window


class GUI(object):
    def __init__(self):
        super().__init__()
        self.backgroundColor = (0, 0, 0, 1)
        self.window = impl_glfw_init()
        gl.glClearColor(*self.backgroundColor)
        imgui.create_context()
        self.impl = GlfwRenderer(self.window)

        self.string = ""
        self.f = 0.5

        self.loop()

    def loop(self):
        while not glfw.window_should_close(self.window):
            glfw.poll_events()
            self.impl.process_inputs()
            imgui.new_frame()
            imgui.begin("Custom window", True)

            if imgui.button("START"):
                asyncio.run(main()) 
            if imgui.button("STOP"):
                asyncio.run(stop())

            imgui.end()

            imgui.render()

            gl.glClearColor(*self.backgroundColor)
            gl.glClear(gl.GL_COLOR_BUFFER_BIT)

            self.impl.render(imgui.get_draw_data())
            glfw.swap_buffers(self.window)

        self.impl.shutdown()
        glfw.terminate()

if __name__ == "__main__":
   gui = GUI()
