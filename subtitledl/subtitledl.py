
# imports
import os
import sys
import click
import subtitledl


# mainFunc
@click.command()
@click.option("--verbose", "-v", is_flag=True, default=False, help=subtitledl.helpVerbose())
@click.option("--manual", "-m", is_flag=True, default=False, help=subtitledl.helpManual())
@click.argument("moviepath", type=click.Path(exists=True), required=True)
def cli(verbose, manual, moviepath):
    # verbose print
    def verbosePrint(msg):
        if (verbose):
            subtitledl.message(msg)

    # checks
    verbosePrint("Checking things up.")
    moviepathnoext, extension = os.path.splitext(moviepath)
    subtitlepath = moviepathnoext + ".srt"
    try:
        subtitledl.checkConnection()
        subtitledl.checkExtension(extension)
        subtitledl.checkExists(subtitlepath)
    except Exception as error:
        click.echo(error)
        sys.exit(1)

    # searches
    verbosePrint("Movie file loaded. Trying to download subtitles.")
    rootpath = subtitledl.getRootPath(moviepath)
    movietitle = subtitledl.getTitle(moviepathnoext)
    searchstr = subtitledl.getSearchString(movietitle)
    try:
        # if manual
        if (manual):
            if (subtitledl.subsceneDownloadManual(searchstr, subtitlepath, rootpath, verbose)):
                subtitledl.exitSuccess("Subtitle Downloaded from Subscene.")
            subtitledl.message("No subs downloaded.")
            sys.exit(0)

        # if auto
        subtitledl.message("Trying SubDB.")
        if (subtitledl.subdbDownload(moviepath, subtitlepath, verbose)):
            subtitledl.exitSuccess("Subtitile Downloaded from SubDB.")
        subtitledl.message("Tring Subscene.")
        if (subtitledl.subsceneDownload(searchstr, movietitle, subtitlepath, rootpath, verbose)):
            subtitledl.exitSuccess("Subtitle Downloaded from Subscene.")
        subtitledl.message("No Subs, maybe try manually with --manual option.")
        sys.exit(0)
    except Exception as error:
        click.echo(error)
        sys.exit(1)


# first line of code written
if __name__ == "__main__":
    cli()
