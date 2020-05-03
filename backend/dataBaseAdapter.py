import sys, os, shutil, json, ntpath, logging
databasePath = os.path.abspath('..\\') + '\\temporary\\'
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou, BucketAlreadyExists)


# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


minioClient = Minio('127.0.0.1:9000', access_key='minioadmin', secret_key='minioadmin', secure=False)


def _path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


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


def remove_results_from_bucket(username):
    logger.info('Going to remove ' + username)

    # Remove multiple objects in a single library call.
    try:
        objects = minioClient.list_objects_v2('results', prefix=username + '/')
        objects_to_delete = [obj.object_name for obj in objects]
        # force evaluation of the remove_objects() call by iterating over
        # the returned value.
        for del_err in minioClient.remove_objects('results', objects_to_delete):
            print("Deletion Error: {}".format(del_err))
    except ResponseError as err:
        print(err)


def get_results_from_bucket(username):
    urls = []
    results = minioClient.list_objects_v2('results', prefix=username + '/')

    for instance in results:
        presignedURL = minioClient.presigned_get_object('results', instance.object_name)
        urls.append(presignedURL)

    return json.dumps(urls)


def get_accounts_from_bucket():
    objects = minioClient.list_objects_v2('results')
    return [_path_leaf(obj.object_name) for obj in objects]


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