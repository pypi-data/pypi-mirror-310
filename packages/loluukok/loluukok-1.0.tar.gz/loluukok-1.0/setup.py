from setuptools import setup, find_packages

NAME = "loluukok"
VERSION = "1.0"
DESCRIPTION = "A simple library for file and directory management."
AUTHOR = "Luuk M. Mastbroek"
AUTHOR_EMAIL = "luukm@mastbroek.nl"
URL = "https://pypi.org/loluukok/loluukok"
LONG_DESCRIPTION = open("README.md", "r").read()

setup(
    name=NAME,
    version=VERSION,
    packages=find_packages(),
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    url=URL,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    python_requires=">=3.6",
    include_package_data=True,
)
