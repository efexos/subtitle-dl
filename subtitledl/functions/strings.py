
import sys
import click


def choose(items):
    click.echo(
        "####################################################################")
    for i in range(0, len(items)):
        j = i + 1
        click.echo(str(j) + ": " + items[i])
    click.echo(
        "####################################################################")
    try:
        selection = click.prompt("Enter your choice", type=click.INT)
        return selection - 1
    except click.Abort:
        return 0


def exitSuccess(msg):
    message(msg)
    message("Exiting.")
    sys.exit(0)


def message(msg):
    click.echo("Message: " + msg)


def removeSpecialChars(string):
    string = string.replace(".", "").replace(",", "").replace("(", "").replace(
        ")", "").replace("{", "").replace("}", "").replace("[", "").replace("]", "").replace(
        ":", "").replace(";", "").replace("'", "").replace("/", "").replace("|", "").replace(
        "<", "").replace(">", "").replace("-", "").replace("_", "").replace("=", "").replace("+", "")
    return string


def getRootPath(filepath):
    y = -1
    for x, slashes in enumerate(reversed(filepath)):
        if(slashes == "\\" or slashes == "/"):
            y = len(filepath) - 1 - x
            break
    return filepath[:1 + y]


def getTitle(filepath):
    y = -1
    for x, slashes in enumerate(reversed(filepath)):
        if(slashes == "\\" or slashes == "/"):
            y = len(filepath) - 1 - x
            break
    return filepath[y + 1:]


def getSearchString(movietitle):
    searchStr = ""
    movietitle = movietitle.replace(".", " ")
    movietitle = removeSpecialChars(movietitle)
    words = movietitle.split(" ")
    for word in words:
        try:
            if(any(w.isdigit() for w in word) == True and len(word) != 1):
                break
            else:
                searchStr += word + " "
        except ValueError:
            pass
    searchStr = searchStr[:-1]
    return searchStr
