from setuptools import setup, find_packages

def readme():
    with open("README.md") as file_name:
        return file_name.read()

def lic():
    with open("LICENSE") as file_name:
        return file_name.read()

setup(
    name="subtitle-dl",
    version="1.0.0",
    description="Subtitle Downloader",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="efexos",
    author_email="efexos@protonmail.com",
    url="https://github.com/efexos/subtitle-dl",
    license=lic(),
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "subtitle-dl=subtitledl.subtitledl:cli"
        ]
    },
    include_package_data=True,
    install_requires=[
        "click",
        "bs4",
        "requests"
    ]
)