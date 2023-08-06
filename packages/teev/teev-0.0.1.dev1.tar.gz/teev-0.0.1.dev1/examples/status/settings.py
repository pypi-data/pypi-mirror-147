import aiogram
from teev import Keyboard, InlineKey, Teev


async def handle_wait(app: Teev, message: aiogram.types.Message, command_dict: dict):

    command_dict['text'] = command_dict['text'].format(message.text)

    if "Some text" in message.text:
        await message.answer("Send something more interesting!")
        await app.set_status(message.chat.id, 'wait')
    else:
        await message.answer(command_dict['text'], reply_markup=Keyboard([InlineKey("AGAIN", callback_data="/start")]).get())


COMMANDS = [
    ["/start", "Set status"]
]

PARSE_MODE = "HTML"

TOKEN = ""

SCHEME = {
    "/start": {
        "text": "Send me some text.",
        "keyboard":  Keyboard(["Some text", "I love you Teev!"]),
        "status": "wait"
    },
    "wait": {
        "text": "Gotcha '{}' from you!",
        "function": handle_wait,
        "send": False
    }
}