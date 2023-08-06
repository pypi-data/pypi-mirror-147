import random

from aiogram.types import WebAppInfo

from teev import Keyboard, InlineKey


async def handle_start(_, __, command_dict: dict):
    command_dict['text'] = command_dict['text'].format(random.randint(1, 100))


COMMANDS = [
    ["/start", "Make random"],
    ["/web", "Web test"],
]

PARSE_MODE = "HTML"

TOKEN = ""

SCHEME = {
    "/start": {
        "text": "Hi, here is your random number: {}",
        "keyboard":  Keyboard([InlineKey(text="RANDOM", callback_data="/start")]),
        "function": handle_start
    },
    "/web": {
        "text": "PUSH THE BUTTON",
        "keyboard":  Keyboard([InlineKey(text="PUSH ME",web_app=WebAppInfo(url="https://shop.startech.live/"))]),
        "function": None
    }
}