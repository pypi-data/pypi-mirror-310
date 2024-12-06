from setuptools import setup, find_packages

setup(
    name="demucs_acapella",
    version="1.0.1",
    description="A CLI tool for extracting acapellas using Demucs and managing audio metadata.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="komly",
    author_email="komly@yandex.ru",
    url="https://github.com/komly/demucs_acapella",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "demucs_acapella=demucs_acapella.cli:main",
        ],
    },
    install_requires=[
        "demucs==4.0.0",
        "pydub==0.25.1",
        "eyed3==0.9.7",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
)