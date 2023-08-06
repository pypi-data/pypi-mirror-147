# -*- coding: utf-8 -*-

"""
    Basic.
    ~~~~~~~~~~~~~~~~~~~~~~~~~~

    This example shows basic usage of Teev.
    To start using Teev, define the application first.

    Checkout teev at https://github.com/startech-live/teev

    This snippet by Stepan Starovoitov can be used freely for anything you like.
    Consider it public domain.
"""
import aiogram.types

from teev import Teev

app = Teev()

"""
Example of using aiogram methods in addition to Teev handling.
"""
@app.dp.message_handler(content_types=['location'])
async def handle_location(message: aiogram.types.Message):
    await message.answer(f"COORDINATES : {message.location.latitude},{message.location.longitude}")

if __name__ == "__main__":
    app.run()
