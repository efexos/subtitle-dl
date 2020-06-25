
import os
import urllib.request
import urllib.error

EXTENSIONS = [
    ".avi",
    ".mp4",
    ".mkv",
    ".mpg",
    ".wmv",
    ".mov",
    ".3gp",
    ".vob",
    ".rm",
    ".flv",
    ".3g2",
    ".mpeg"
]


def checkConnection():
    try:
        urllib.request.urlopen("http://google.com/", timeout=1)
    except urllib.error.URLError or urllib.error.HTTPError:
        raise Exception(
            "ConnectionError: Cannot connect to Internet. Check Connection.")


def checkExtension(extension):
    if extension not in EXTENSIONS:
        raise Exception(
            "ExtensionError: Given file is not a valid movie file.")


def checkExists(filepath):
    if (os.path.exists(filepath) == True):
        raise Exception("FileExistsError: Subtitle file already exists.")
