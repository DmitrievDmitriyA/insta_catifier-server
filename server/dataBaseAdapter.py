import sys, os, shutil, json, ntpath
temporaryDatabasePath = os.path.abspath('./') + '/temporary/'
from minio import Minio
from minio.error import (ResponseError, BucketAlreadyOwnedByYou, BucketAlreadyExists)
from pkg_resources import resource_filename


access_key = None
secret_key = None

filePath = resource_filename(__name__, 'secret.json')
with open(filePath, 'r') as json_file:
    data = json.load(json_file)
    server = data['server']
    bucket = data['bucket']
    access_key = data['access_key']
    secret_key = data['secret_key']


minioClient = Minio(server, access_key=access_key, secret_key=secret_key)


def _path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def sourceUserFolder(username):
    return temporaryDatabasePath + 'sources/' + username + '/'


def resultUserFolder(username):
    return temporaryDatabasePath + 'results/' + username + '/'


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
        minioClient.fput_object(bucket, objectName, photo)
        photosCount += 1


def remove_results_from_bucket(username):
    # logger.info(f'Going to remove {username}')

    # Remove multiple objects in a single library call.
    try:
        objects = minioClient.list_objects_v2(bucket, prefix=username + '/')
        objects_to_delete = [obj.object_name for obj in objects]
        # force evaluation of the remove_objects() call by iterating over
        # the returned value.
        for del_err in minioClient.remove_objects(bucket, objects_to_delete):
            # logger.error(f"Deletion Error: {del_err}")
            pass
    except ResponseError as err:
        # logger.error(err)
        pass


def get_results_from_bucket(username):
    urls = []
    results = minioClient.list_objects_v2(bucket, prefix=username + '/')

    for instance in results:
        presignedURL = minioClient.presigned_get_object(bucket, instance.object_name)
        urls.append(presignedURL)

    return json.dumps(urls)


def get_accounts_from_bucket():
    objects = minioClient.list_objects_v2(bucket)
    return [_path_leaf(obj.object_name) for obj in objects]