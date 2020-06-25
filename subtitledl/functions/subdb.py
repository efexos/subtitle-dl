
import os
import sys
import hashlib
import urllib.request
import urllib.error
from subtitledl.functions.strings import message


def subdbHashMovie(moviepath):
    readSize = 64 * 1024
    with open(moviepath, "rb") as movie:
        data = movie.read(readSize)
        movie.seek(-readSize, os.SEEK_END)
        data += movie.read(readSize)
    return hashlib.md5(data).hexdigest()


def subdbWriteSubtitle(response, subpath):
    with open(subpath, "wb") as subFile:
        subFile.write(response)


def subdbSearch(hashtxt):
    header = {
        'User-Agent': 'SubDB/1.0 (subtitle-dl/1.0; http://github.com/efexos/subtitle-dl)'
    }
    subDB = "http://api.thesubdb.com/?action=download&hash=" + hashtxt + "&language=en"

    try:
        req = urllib.request.Request(subDB, None, header)
        response = urllib.request.urlopen(req).read()
        if (sys.getsizeof(response) < 400):
            return 0
        else:
            return response
    except urllib.error.URLError or urllib.error.HTTPError as error:
        raise Exception()


# auto download SubDB. No manual for this
def subdbDownload(moviepath, subtitlepath, verbose):
    # verbose
    def verbosePrint(msg):
        if (verbose):
            message(msg)

    verbosePrint("Hashing movie file.")
    hashtxt = subdbHashMovie(moviepath)
    verbosePrint("Searching for subtitle in SubDB.")
    try:
        response = subdbSearch(hashtxt)
        if (response != 0):
            verbosePrint("Subtitle found in SubDB. Saving it now.")
            subdbWriteSubtitle(response, subtitlepath)
            return True
        message("Not Found in SubDB.")
    except Exception:
        message("Not Found in SubDB.")
