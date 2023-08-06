from aiogram.types import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardMarkup,
)


class Keyboard:
    keyboard = None

    def __init__(self, keys: list):
        self.build_keyboard(keys)

    def set_keyboard(self, keyboard_type):
        self.keyboard = keyboard_type()

    def check_and_set_keyboard(self, key):
        if not self.keyboard:
            if isinstance(key, InlineKeyboardButton):
                self.set_keyboard(InlineKeyboardMarkup)
            elif isinstance(key, KeyboardButton):
                self.set_keyboard(ReplyKeyboardMarkup)
            elif isinstance(key, str):
                self.set_keyboard(ReplyKeyboardMarkup)
            else:
                raise TypeError(f"Type {type(key)} not supported as keyboard key.")

    def verify_or_format_key(self, key):
        if isinstance(self.keyboard, ReplyKeyboardMarkup):
            if isinstance(key, str):
                return KeyboardButton(key)
            elif isinstance(key, KeyboardButton):
                return key
            else:
                TypeError(
                    f"Keyboard type set to {type(self.keyboard)} and a key is {type(key)}. Keyboard is not consistent."
                )
        elif isinstance(self.keyboard, InlineKeyboardMarkup):
            if isinstance(key, InlineKeyboardButton):
                return key
            else:
                TypeError(
                    f"Keyboard type set to {type(self.keyboard)} and a key is {type(key)}. Keyboard is not consistent."
                )

    def build_keyboard(self, keys: list):
        for row in keys:
            if isinstance(row, list):
                formatted_row = []
                for col in row:
                    self.check_and_set_keyboard(col)
                    col = self.verify_or_format_key(col)
                    formatted_row.append(col)
                self.keyboard.row(*formatted_row)
            else:
                self.check_and_set_keyboard(row)
                row = self.verify_or_format_key(row)
                self.keyboard.row(row)

    def get(self):
        return self.keyboard


InlineKey = InlineKeyboardButton
ReplyKey = KeyboardButton
