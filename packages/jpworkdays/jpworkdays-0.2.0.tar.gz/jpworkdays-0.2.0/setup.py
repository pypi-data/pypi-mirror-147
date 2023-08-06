# -*- coding: utf-8 -*-
from codecs import open
import os
import re
from setuptools import setup

with open(os.path.join("jpworkdays", "__init__.py"), "r", encoding="utf8") as f:
    version = re.compile(r".*__version__ = '(.*?)'", re.S).match(f.read()).group(1)

setup(
    name="jpworkdays",
    packages=["jpworkdays"],
    version=version,
    license="MIT License",
    platforms=["POSIX", "Windows", "Unix", "MacOS"],
    description="Generate Japan's Workdays Taking Account for Public Holidays",
    author="Kohei Ohno",
    author_email="discus0434@gmail.com",
    url="https://github.com/discus0434/jp-workdays",
    keywords=["Japan", "Workdays"],
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Japanese",
        "Operating System :: MacOS",
        "Operating System :: Microsoft",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    data_files=[("", ["README.md"])],
    long_description="{}".format((open("README.md", encoding="utf8").read())),
    long_description_content_type="text/markdown",
)
