from setuptools import setup, find_packages


def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()
    
setup(
    name="StreamingCommunity",
    version="1.7.2",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Lovi-0",
    url="https://github.com/Lovi-0/StreamingCommunity",
    packages=["StreamingCommunity"],
    install_requires=[
        "httpx",
        "bs4",
        "rich",
        "tqdm",
        "m3u8",
        "psutil",
        "unidecode",
        "jsbeautifier",
        "pathvalidate",
        "fake-useragent",
        "qbittorrent-api",
        "python-qbittorrent",
        "googlesearch-python"
    ],
    python_requires='>=3.8',
    entry_points={
        "console_scripts": [
            "streamingcommunity=StreamingCommunity.run:main",
        ],
    },
    include_package_data=True,
    keywords="streaming community",
    project_urls={
        "Bug Reports": "https://github.com/Lovi-0/StreamingCommunity/issues",
        "Source": "https://github.com/Lovi-0/StreamingCommunity",
    }
)
