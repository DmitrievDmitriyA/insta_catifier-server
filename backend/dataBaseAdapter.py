import sys, os
databasePath = os.path.abspath('..\\') + 'database\\'

def sourceUserFolder(username):
    return databasePath + 'sources\\' + username + '\\'


def resultUserFolder(username):
    return databasePath + 'results\\' + username + '\\'