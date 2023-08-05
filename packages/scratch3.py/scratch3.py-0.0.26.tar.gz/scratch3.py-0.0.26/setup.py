from setuptools import setup, find_packages
import codecs
import os

VERSION = '0.0.26'
DESCRIPTION = 'A Scratch API wrapper'
LONG_DESCRIPTION = 'A Scratch API wrapper. Still under development.'

# Setting up
setup(
    name="scratch3.py",
    version=VERSION,
    author="TimMcCool",
    author_email="timmccool.scratch@gmail.com",
    description=DESCRIPTION,
    long_description_content_type="text/x-rst",
    long_description=open('README.rst').read(),
    packages=find_packages(),
    install_requires=["websocket-client"],
    keywords=['scratch api', 'scratch api python', 'scratch python', 'scratch for python', 'scratch', 'scratch cloud', 'scratch cloud variables', 'scratch bot'],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
