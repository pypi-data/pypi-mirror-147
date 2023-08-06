from setuptools import setup, find_packages
import codecs
import os

VERSION = ''
DESCRIPTION = 'talob'
LONG_DESCRIPTION = 'A package that make sending emails easily!'

# Setting up
setup(
    name="talob",
    version=VERSION,
    author="Ahmedd",
    author_email="itztaloptalop@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['arithmetic', 'math', 'mathematics', 'python tutorial', 'avi upadhyay'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)