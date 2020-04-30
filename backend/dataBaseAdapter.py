import sys, os, shutil
databasePath = os.path.abspath('..\\') + 'database\\'

def sourceUserFolder(username):
    return databasePath + 'sources\\' + username + '\\'


def resultUserFolder(username):
    return databasePath + 'results\\' + username + '\\'


def removeSources(username):
    shutil.rmtree(sourceUserFolder(username))
    

def removeResults(username):
    shutil.rmtree(resultUserFolder(username))