# -*- coding: utf-8 -*-
"""
    teev.app
    ~~~~~~~~~~~~
    This module implements the central bot app object as an aiogram wrapper.

    :copyright: (c) 2022 by Stepan Starovoitov.
    :license: BSD, see LICENSE for more details.
"""

import asyncio
import fnmatch
import os.path
import sys
import traceback
from copy import deepcopy
from threading import Lock
from typing import Union

import aiogram
from aiogram.types import BotCommand
from aiogram.utils import executor

from flask.config import Config

from teev.errors import error_handler
from teev.log import logger
from teev.keyboard import *


class Teev:
    """
    The main Teev object. On initialization it will load Teev settings from settings.py, then
    configure and enable the bot itself. The bot is launched by executing
    the code below:::

        app = Teev()
        app.run()

    :param settings: the name of the settings file.  Defaults to `settings.py`.

    """

    def __init__(self, settings="settings.py"):
        """
        Teev bot main app is implemented as an aiogram wrapper. On initialization it loads config
        and sets up base handlers for text and callbacks.
        """

        self.settings = settings
        self._load_config()
        self._setup_bot()

        self.scheme = self.config["SCHEME"]

        self.statuses = {}
        self.statuses_mutex = Lock()

        self._setup_handlers()

    def _load_config(self):
        self.config = Config(__package__)
        self.config.from_object("teev.default_settings")

        if not self.settings:
            return

        if isinstance(self.settings, dict):
            self.config.update(self.settings)
        else:
            if os.path.isabs(self.settings):
                pyfile = self.settings
            else:

                def find_settings_file(file_name):
                    # check if we can locate the file from sys.argv[0]
                    abspath = os.path.abspath(os.path.dirname(sys.argv[0]))
                    settings_file = os.path.join(abspath, file_name)
                    if os.path.isfile(settings_file):
                        return settings_file
                    else:
                        # try to find settings.py in one of the
                        # paths in sys.path
                        for p in sys.path:
                            for root, dirs, files in os.walk(p):
                                for f in fnmatch.filter(files, file_name):
                                    if os.path.isfile(os.path.join(root, f)):
                                        return os.path.join(root, file_name)

                # try to load file from environment variable or settings.py
                pyfile = find_settings_file(
                    os.environ.get("TEEV_SETTINGS") or self.settings
                )

            if not pyfile:
                raise IOError("Could not load settings.")

            try:
                self.config.from_pyfile(pyfile)
            except:
                raise

    def _setup_bot(self):
        try:
            self.bot = aiogram.Bot(
                token=self.config["TOKEN"], parse_mode=self.config["PARSE_MODE"]
            )
            self.dp = aiogram.Dispatcher(self.bot)
            self._setup_commands()
        except Exception:
            logger.error(traceback.format_exc())

    def _setup_commands(self):
        commands = self.config["COMMANDS"]
        commands_formatted = []
        if commands:
            for command in commands:
                commands_formatted.append(BotCommand(*command))
            asyncio.get_event_loop().run_until_complete(
                self.bot.set_my_commands(commands_formatted)
            )

    def _setup_handlers(self):
        if not self.bot:
            return

        @error_handler
        @self.dp.message_handler(content_types=["text"])
        async def answer_inline(message: aiogram.types.Message):
            user_id = message.chat.id
            status = self.get_status(user_id)
            if status:
                await self.handle_command(message, self.scheme[status], user_id)
                return

            message_command = message.text.split("_")[0]
            if message_command in self.scheme:
                await self.handle_command(
                    message, self.scheme[message_command], user_id
                )

        @error_handler
        @self.dp.callback_query_handler(lambda callback_query: True)
        async def handle_callback(call: aiogram.types.CallbackQuery):
            user_id = call.message.chat.id
            status = self.get_status(user_id)
            if status:
                await self.handle_command(call, self.scheme[status], user_id)
                return

            command = call.data.split("_")[0]
            await self.handle_command(call, self.scheme[command], user_id)

    async def handle_command(
        self,
        message: Union[aiogram.types.Message, aiogram.types.CallbackQuery],
        command_dict: dict,
        user_id: int,
    ):
        """
        Each handled command erases user status. During handling proper aiogram
        keyboard is made and command function is called if exists. If there is no
        function specified for command, then specified text and keyboard will be
        sent straight away. If function id specified it looks to 'send' flag to
        understand whether to send it or not. Yet it only supports sending new
        message, editing and deleting will be added in newer versions.

        Function is provided with app itself, message and command dict from scheme.

        :param message:
        :param command_dict:
        :param user_id:
        :return:
        """
        await self.set_status(user_id, "")
        command_dict = deepcopy(command_dict)
        if "status" in command_dict and command_dict["status"]:
            await self.set_status(user_id, command_dict["status"])
        if "keyboard" in command_dict and isinstance(
            command_dict["keyboard"], Keyboard
        ):
            command_dict["keyboard"] = command_dict["keyboard"].get()
        if "function" in command_dict and command_dict["function"]:
            await command_dict["function"](self, message, command_dict)
            if "send" in command_dict and not command_dict["send"]:
                return
        if isinstance(message, aiogram.types.Message):
            await message.answer(
                command_dict["text"], reply_markup=command_dict["keyboard"]
            )
        elif isinstance(message, aiogram.types.CallbackQuery):
            await message.message.answer(
                command_dict["text"], reply_markup=command_dict["keyboard"]
            )

    async def set_status(self, user_id: int, status: str):
        with self.statuses_mutex:
            self.statuses[user_id] = status

    def get_status(self, user_id: int):
        if user_id in self.statuses:
            return self.statuses[user_id]
        else:
            return None

    def run(self, skip_updates=True, on_startup=None) -> None:
        """
        Function that runs the app.

        :param skip_updates: defines whether to handle updates came while bot was down
        :param on_startup: defines function that runs background tasks
        """
        if not self.bot:
            raise ValueError("Bot token invalid or not specified.")

        executor.start_polling(
            self.dp, skip_updates=skip_updates, on_startup=on_startup
        )
