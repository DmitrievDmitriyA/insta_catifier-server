
import sys, os, shutil
sys.path.append(os.path.abspath('..\\'))
import catifier.scraping as scraping
import dataBaseAdapter


def loadPhotosToMemory(sourceUserFolder):
    for filename in os.listdir(sourceUserFolder):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            continue
    return

def scrapePhotos(username):
    sys.argv[1] = username
    sys.argv.append('--maximum')
    sys.argv.append('15')
    sys.argv.append('--media-types')
    sys.argv.append('image')
    sourceUserFolder = dataBaseAdapter.sourceUserFolder(username)
    scraping.scrape_photos(sourceUserFolder)
    return loadPhotosToMemory(sourceUserFolder)

def removeSources(username):
    sourceUserFolder = dataBaseAdapter.sourceUserFolder(username)
    shutil.rmtree(sourceUserFolder)
