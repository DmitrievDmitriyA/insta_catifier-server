import sys, os
import catifier.enhancement as enhancement
import catifier.scraping as scraping
import server.dataBaseAdapter as dataBaseAdapter


def add_cats(username):
    sourceUserFolder = dataBaseAdapter.sourceUserFolder(username)
    resultUserFolder = dataBaseAdapter.resultUserFolder(username)
    results = enhancement.add_cats_and_return_paths(sourceUserFolder, resultUserFolder, 10)

    # Load results to bucket
    dataBaseAdapter.load_results_to_bucket([photo['resultPath'] for photo in results ], username)

    # Clean temporary folders
    dataBaseAdapter.remove_temporary_folders(username)


def _loadPhotosToMemory(sourceUserFolder):
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
    return _loadPhotosToMemory(sourceUserFolder)
