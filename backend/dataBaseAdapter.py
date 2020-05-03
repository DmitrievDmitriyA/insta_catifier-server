import sys, os, shutil, json
databasePath = os.path.abspath('..\\') + '\\temporary\\'
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou, BucketAlreadyExists)

minioClient = Minio('127.0.0.1:9000', access_key='minioadmin', secret_key='minioadmin', secure=False)


def sourceUserFolder(username):
    return databasePath + 'sources\\' + username + '\\'


def resultUserFolder(username):
    return databasePath + 'results\\' + username + '\\'


def _removeSources(username):
    shutil.rmtree(sourceUserFolder(username))
    

def _removeResults(username):
    shutil.rmtree(resultUserFolder(username))


def remove_temporary_folders(username):
    _removeSources(username)
    _removeResults(username)


def load_results_to_bucket(photos, username):
    photosCount = 0

    for photo in photos:
        _, file_extension = os.path.splitext(photo)
        objectName = username + '/' + str(photosCount) + file_extension
        minioClient.fput_object('results', objectName, photo)
        photosCount += 1


def get_results_from_bucket(username):
    urls = []
    results = minioClient.list_objects_v2('results', prefix=username + '/')

    for instance in results:
        presignedURL = minioClient.presigned_get_object('results', instance.object_name)
        urls.append(presignedURL)

    return json.dumps(urls)

# def foo():
#     # Make a bucket with the make_bucket API call.
#     try:
#         minioClient.make_bucket("maylogs")
#     except BucketAlreadyOwnedByYou as err:
#         pass
#     except BucketAlreadyExists as err:
#         pass
#     except ResponseError as err:
#         raise

#     # Put an object 'pumaserver_debug.log' with contents from 'pumaserver_debug.log'.
#     try:
#         minioClient.fput_object('maylogs', 'pumaserver_debug.log', '/tmp/pumaserver_debug.log')
#     except ResponseError as err:
#         print(err)