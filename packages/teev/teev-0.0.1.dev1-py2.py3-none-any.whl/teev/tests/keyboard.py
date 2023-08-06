import unittest

from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

from teev import Keyboard, InlineKey, ReplyKey


class TestKeyboard(unittest.TestCase):
    def test_simple_inline_keyboard(self):
        key = InlineKey(text="START", callback_data="/start")
        keyboard = Keyboard([key]).get()

        test_keyboard = InlineKeyboardMarkup()
        test_keyboard.add(key)

        self.assertEqual(keyboard, test_keyboard)

    def test_complex_inline_keyboard(self):
        key = InlineKey(text="START", callback_data="/start")
        keyboard = Keyboard([[key, key], key]).get()

        test_keyboard = InlineKeyboardMarkup()
        test_keyboard.row(key, key)
        test_keyboard.add(key)

        self.assertEqual(keyboard, test_keyboard)

    def test_simple_reply_keyboard(self):
        key = ReplyKey("START")
        keyboard = Keyboard([key]).get()

        test_keyboard = ReplyKeyboardMarkup()
        test_keyboard.add(key)

        self.assertEqual(keyboard, test_keyboard)

    def test_complex_reply_keyboard(self):
        key = ReplyKey("START")
        keyboard = Keyboard([[key, key], key]).get()

        test_keyboard = ReplyKeyboardMarkup()
        test_keyboard.row(key, key)
        test_keyboard.add(key)

        self.assertEqual(keyboard, test_keyboard)

    def test_simple_text_keyboard(self):
        key = "START"
        keyboard = Keyboard([key]).get()

        key = KeyboardButton("START")
        test_keyboard = ReplyKeyboardMarkup()
        test_keyboard.add(key)

        self.assertEqual(keyboard, test_keyboard)

    def test_complex_text_keyboard(self):
        key = "START"
        keyboard = Keyboard([[key, key], key]).get()

        key = KeyboardButton("START")
        test_keyboard = ReplyKeyboardMarkup()
        test_keyboard.row(key, key)
        test_keyboard.add(key)

        self.assertEqual(keyboard, test_keyboard)
