# setup.py
# Copyleft (c) 2024 daysant - nisshi
# This file is licensed under the terms of the daysant license v2.
# daysant@proton.me

from setuptools import setup

setup(
    name="nisshi",
    version="0.1.1",
    packages=["nisshi"],
    author="daysant",
    author_email="daysant@proton.me",
    license="daysant license v2",
    description="another logger library for python",
    long_description=open("README.md", "r").read(),
    long_description_content_type="text/markdown",
    url="https://codeberg.org/daysant/nisshi",
)