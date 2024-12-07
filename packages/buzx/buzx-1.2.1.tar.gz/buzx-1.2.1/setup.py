from setuptools import setup, find_packages

setup(
    name="buzx",
    version="1.2.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "tqdm",
    ],
    entry_points={
        "console_scripts": [
            "buzx = buzx.downloader:download_file",
        ],
    },
    python_requires=">=3.6",
)
