from setuptools import setup, find_packages


def readme():
    with open("readme.md", "r") as f:
        return f.read()


setup(
    name="moe-parsers",
    version="2024.11.4",
    author="nichind",
    author_email="nichinddev@gmail.com",
    description="Async aniboom/kodik player parser",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/nichind/moe-parsers",
    packages=find_packages(),
    install_requires=["aiohttp", "python-dotenv", "beautifulsoup4"],
    classifiers=[
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
    keywords=["aniboom", "kodik", "animego", "moe", "parser", "anime", "async"],
)
