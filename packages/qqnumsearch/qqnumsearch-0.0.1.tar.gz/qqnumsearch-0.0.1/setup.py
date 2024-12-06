import codecs
import os

from setuptools import find_packages, setup



VERSION = '0.0.1'
DESCRIPTION = 'A light weight command line menu that supports Windows, MacOS, and Linux'
long_description = 'qqnumsearch is a light weight command line menu. Supporting Windows, MacOS, and Linux. It has support for hotkeys'

# Setting up
setup(
    name="qqnumsearch",
    version=VERSION,
    author="xiaoqhjerry",
    author_email="",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    packages=find_packages(),
    install_requires=[
        'getch; platform_system=="Unix"',
        'getch; platform_system=="MacOS"',
    ],
    keywords=['python', 'menu', 'dumb_menu', 'windows', 'mac', 'linux'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)