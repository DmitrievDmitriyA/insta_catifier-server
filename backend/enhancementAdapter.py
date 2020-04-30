
import sys, os
sys.path.append(os.path.abspath('..\\'))
import catifier.enhancement as enhancement
import dataBaseAdapter


def add_cats(username):
    sourceUserFolder = dataBaseAdapter.sourceUserFolder(username)
    resultUserFolder = dataBaseAdapter.resultUserFolder(username)
    enhancement.add_cats(False, username, sourceUserFolder, resultUserFolder)
