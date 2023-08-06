#!/usr/bin/env python
import io
import re

from setuptools import setup, find_packages
from collections import OrderedDict

DESCRIPTION = "Asynchronous Telegram Bot Framework."
with open("README.rst") as f:
    LONG_DESCRIPTION = f.read()

with io.open("teev/__init__.py", "rt", encoding="utf8") as f:
    VERSION = re.search(r"__version__ = \"(.*?)\"", f.read()).group(1)

INSTALL_REQUIRES = [
    "aiogram",
    "flask"
]

EXTRAS_REQUIRE = {
    "docs": ["sphinx", "alabaster", "doc8"],
    "tests": ["testfixtures", "pytest", "tox"],
}
EXTRAS_REQUIRE["dev"] = EXTRAS_REQUIRE["tests"] + EXTRAS_REQUIRE["docs"]

setup(
    name="teev",
    version=VERSION,
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/x-rst",
    author="Stepan Starovoitov",
    author_email="stepan@startech.live",
    url="http://teev.startech.live",
    project_urls=OrderedDict(
        (
            ("Documentation", "http://teev.startech.live"),
            ("Code", "https://github.com/startech-live/teev"),
            ("Issue tracker", "https://github.com/startech-live/teev/issues"),
        )
    ),
    license="BSD",
    platforms=["any"],
    packages=find_packages(),
    test_suite="teev.tests",
    install_requires=INSTALL_REQUIRES,
    extras_require=EXTRAS_REQUIRE,
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
