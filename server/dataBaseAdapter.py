import sys, os, shutil, json, ntpath
databasePath = os.path.abspath('..\\') + '\\temporary\\'
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou, BucketAlreadyExists)


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
    # logger.info(f'Going to remove {username}')

    # Remove multiple objects in a single library call.
    try:
        objects = minioClient.list_objects_v2('results', prefix=username + '/')
        objects_to_delete = [obj.object_name for obj in objects]
        # force evaluation of the remove_objects() call by iterating over
        # the returned value.
        for del_err in minioClient.remove_objects('results', objects_to_delete):
            # logger.error(f"Deletion Error: {del_err}")
            pass
    except ResponseError as err:
        # logger.error(err)
        pass


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