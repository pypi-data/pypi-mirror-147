#!/usr/bin/env python

import codecs
from setuptools import setup

# Version info -- read without importing
_locals = {}
with open("alabester/_version.py") as fp:
    exec(fp.read(), None, _locals)
version = _locals["__version__"]

# README into long description
with codecs.open("README.rst", encoding="utf-8") as f:
    readme = f.read()

setup(
    name="alabester",
    version=version,
    description="A mobile-friendlier almost-drop-in replacement Alabaster",
    long_description=readme,
    author="introt",
    author_email="introt@koti.fimnet.fi",
    url="https://github.com/introt/alabester",
    packages=["alabester"],
    include_package_data=True,
    entry_points={"sphinx.html_themes": ["alabester = alabester"]},
    classifiers=[
        "Framework :: Sphinx",
        "Framework :: Sphinx :: Theme",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: Implementation :: CPython",
        "Programming Language :: Python :: Implementation :: PyPy",
        "Topic :: Documentation",
        "Topic :: Documentation :: Sphinx",
        "Topic :: Software Development :: Documentation",
    ],
)
