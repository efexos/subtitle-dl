
import os
import shutil
import zipfile
import requests
from .strings import *
from bs4 import BeautifulSoup


def subsceneParseSubLink(title, subs, links):
    link = 0
    for i in range(0, len(subs)):
        if (title == subs[i]):
            link = links[i]
            break
    return link


def subsceneParseMovieLink(searchstring, movies, links):
    link = 0
    for i in range(0, len(movies)):
        if (searchstring.split(" ") == removeSpecialChars(movies[i]).split(" ")[:-1]):
            link = links[i]
            break
    return link


def subsceneMovieSearch(searchstring):
    try:
        response = requests.get(
            "https://subscene.com/subtitles/searchbytitle?query=" + searchstring)
    except:
        raise Exception("Error while contacting Subscene.")
    soup = BeautifulSoup(response.content, features="html.parser")
    divs = soup.findAll("div", {"class": "title"})
    movies = []
    links = []
    for i in range(0, len(divs)):
        a = divs[i].find("a")
        movies.append(a.text)
        links.append(a.get("href").strip())
    return movies, links


def subsceneSubSearch(link):
    try:
        response = requests.get("https://subscene.com/" + link + "/english")
    except:
        raise Exception("Error while contacting Subscene.")
    soup = BeautifulSoup(response.content, features="html.parser")
    tds = soup.findAll("td", {"class": "a1"})
    subs = []
    links = []
    for i in range(0, len(tds)):
        subs.append(tds[i].findAll("span")[1].text.strip())
        links.append(tds[i].findAll("a")[0].get("href").strip())
    return subs, links


def subsceneDownloadSubtitle(sublink):
    try:
        response = requests.get("https://subscene.com/" + sublink)
    except:
        raise Exception("Error while contacting Subscene.")
    soup = BeautifulSoup(response.content, features="html.parser")
    downloadLink = soup.findAll("a", {"id": "downloadButton"})[0].get("href")
    try:
        response = requests.get("http://subscene.com" + downloadLink)
    except:
        raise Exception("Error while contacting Subscene.")
    return response


def subsceneWriteSubtitle(response, subtitlepath, rootpath):
    zippath = os.path.splitext(subtitlepath)[0] + ".zip"
    subzip = open(zippath, "wb")
    for chunk in response.iter_content(200000):
        subzip.write(chunk)
    subzip.close()
    subzip = zipfile.ZipFile(zippath)
    for filename in subzip.namelist():
        subzip.extract(filename, rootpath)
        shutil.move(rootpath + filename, subtitlepath)
    subzip.close()
    os.unlink(zippath)


# auto download for subscene
def subsceneDownload(searchstring, title, subtitlepath, rootpath, verbose):
    # verbose print
    def verbosePrint(msg):
        if (verbose):
            message(msg)

    # code flow
    verbosePrint("Searching for '" + searchstring + "' in Subscene.")
    movies, movielinks = subsceneMovieSearch(searchstring)
    movielink = subsceneParseMovieLink(searchstring, movies, movielinks)
    if (movielink == 0):
        message("Not found in subscene.")
        return False
    verbosePrint("Opening Link: " + movielink)
    subs, sublinks = subsceneSubSearch(movielink)
    sublink = subsceneParseSubLink(title, subs, sublinks)
    if (sublink == 0):
        message("Movie '" + searchstring +
                "' found but not for this specific title. I suggest download with --manual.")
        return False
    verbosePrint(
        "Subtitle found in subscene, downloading now from: " + sublink)
    response = subsceneDownloadSubtitle(sublink)
    verbosePrint("Extracting subtitle zip file and writing it.")
    subsceneWriteSubtitle(response, subtitlepath, rootpath)
    return True


# manual download for subscene
def subsceneDownloadManual(searchstring, subtitlepath, rootpath, verbose):
    # verbose print
    def verbosePrint(msg):
        if (verbose):
            message(msg)

    # code flow
    verbosePrint("Searching for '" + searchstring + "' in Subscene.")
    movies, movielinks = subsceneMovieSearch(searchstring)
    selectindex = choose(movies)
    if (selectindex > len(movies)):
        raise Exception("ValueError: Value is greater than expected.")
    movielink = movielinks[selectindex]
    subs, subslink = subsceneSubSearch(movielink)
    selectindex = choose(subs)
    if (selectindex > len(subs)):
        raise Exception("ValueError: Value is greater than expected.")
    sublink = subslink[selectindex]
    response = subsceneDownloadSubtitle(sublink)
    verbosePrint("Extracting subtitle zip file and writing it.")
    subsceneWriteSubtitle(response, subtitlepath, rootpath)
    return True
