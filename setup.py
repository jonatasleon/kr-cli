import pathlib

from setuptools import setup

README = (pathlib.Path(__file__).parent / "README.md").read_text()

setup(
    name="kr-cli",
    version="0.1.0",
    description="CLI tool to search and download roms from Killers Roms",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/jonatasleon/kr-cli",
    author="Jonatas Leon",
    author_email="j@jonatasleon.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
    ],
    packages=["kr"],
    install_requires=[
        "Click",
        "beautifulsoup4",
        "requests",
        "tabulate",
    ],
    entry_points="""
        [console_scripts]
        kr=kr:cli
    """,
)
