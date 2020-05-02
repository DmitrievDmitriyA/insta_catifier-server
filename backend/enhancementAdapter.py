
import sys, os
sys.path.append(os.path.abspath('..\\'))
import catifier.enhancement as enhancement
import dataBaseAdapter
import json


def add_cats(username):
    sourceUserFolder = dataBaseAdapter.sourceUserFolder(username)
    resultUserFolder = dataBaseAdapter.resultUserFolder(username)
    results = enhancement.add_cats_and_return_paths(sourceUserFolder, resultUserFolder, 10)

    # Load results to bucket
    dataBaseAdapter.load_results_to_bucket([photo['resultPath'] for photo in results ], username)
