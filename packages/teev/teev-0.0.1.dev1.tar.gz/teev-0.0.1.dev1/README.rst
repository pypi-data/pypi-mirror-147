teev
====
.. image:: https://img.shields.io/badge/test-pass-00d200.svg
    :target: nono

.. image:: https://img.shields.io/badge/build-pass-00d200.svg
    :target: nono

.. image:: https://img.shields.io/badge/license-BSD-blue.svg?style=flat-square
    :target: https://en.wikipedia.org/wiki/BSD_License

.. image:: https://img.shields.io/badge/code%20style-black-000000.svg
    :target: https://github.com/ambv/black

Teev is an open source asynchronous Python telegram bots module designed \
for humans mainly inspired by `Eve <https://github.com/pyeve/eve>`_ and made as a wrapper around
`aiogram <https://github.com/aiogram/aiogram>`_ module.
It allows setting up telegram bot using settings file, making its logic more readable
and easy to upgrade.

Teev is Simple
--------------
.. code-block:: python

    from teev import Teev

    app = Teev()
    app.run()

Bot is now alive and ready to process messages.
You need to provide proper telegram token in settings.py file.

.. code-block:: python

    TOKEN = ""

    COMMANDS = [
        ["/start", "Say Love"]
    ]

    SCHEME = {
        "/start": {
            "text": "I love Teev!"
        }
    }


You can see `examples <https://github.com/startech-live/teev/examples>`_ to find out more.

`Check out the teev Website <https://teev.startech.live/>`_ (Not yet available)

Features
--------
* Full support of all aiogram methods.
* Keyboard made in one instruction.
* Text logic made simple in scheme.
* Statuses logic to handle user answers.

To Do
-----
* Native Mongodb support.
* Buffer responses.
* Different message send types.

License
-------
teev is a `Stepan Starovoitov`_ open source project,
distributed under the `BSD license
<https://github.com/startech-live/teev/blob/master/LICENSE>`_.

.. _`Stepan Starovoitov`: https://starovoitov.startech.live
