from setuptools import setup, find_packages

from codecs import open
from os import path

HERE = path.abspath(path.dirname(__file__))

with open(path.join(HERE, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name="runclock",
    version="1.0.0",
    description="With this library you can set time for running your code",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ali-Hosseinverdi/run-clock",
    author="Ali Hosseinverdi",
    author_email="alihv5000@email.com",
    license="GPLv3",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    packages=["runclock"],
    include_package_data=True,
)
