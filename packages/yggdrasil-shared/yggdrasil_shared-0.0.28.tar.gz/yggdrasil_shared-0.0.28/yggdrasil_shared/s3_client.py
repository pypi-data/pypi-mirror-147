import mimetypes
import os
import uuid
import boto3, botocore
from nameko import config
from marshmallow import fields, exceptions
from werkzeug.datastructures import FileStorage
from yggdrasil_shared.exceptions import BadRequest
import logging


_logger = logging.getLogger(__name__)

MAX_FILE_UPLOAD_SIZE = config.get('MAX_FILE_UPLOAD_SIZE')
PRE_SIGNED_URL_EXPIRE_TIME = config.get('PRE_SIGNED_URL_EXPIRE_TIME')


def get_s3_resource():
    return boto3.resource(
        's3',
        endpoint_url=config.get('S3_ADDRESS_URL'),
        aws_access_key_id=config.get('S3_ACCESS_KEY_ID'),
        aws_secret_access_key=config.get('S3_SECRET_ACCESS_KEY'),
    )


def get_s3_client():
    return boto3.client(
        's3',
        endpoint_url=config.get('S3_ADDRESS_URL'),
        aws_access_key_id=config.get('S3_ACCESS_KEY_ID'),
        aws_secret_access_key=config.get('S3_SECRET_ACCESS_KEY'),
    )


def upload_on_s3(request, bucket_name=config.get("S3_PUBLIC_BUCKET_NAME")):
    files_data = files_preprocessing(request)
    for file_data in files_data:
        _logger.debug(f"Uploading file : {file_data}")
        get_s3_resource().Bucket(bucket_name).put_object(**file_data)
    return [file['Key'] for file in files_data]


def files_preprocessing(request):
    files_data = []
    for file in request.files.items():
        _, file_storage = file
        file_name = '_'.join([str(uuid.uuid4().hex[:6]), file_storage.filename])
        mime_type, _ = mimetypes.guess_type(file_name)

        files_data.append(dict(
            Key=file_name,
            Body=file_storage,
            ContentType=mime_type,
            ContentLength=file_size(file_storage),
        ))

    return files_data


def file_size(file: FileStorage):
    """
    validate and return file size
    :return: file size
    """
    file.seek(0, os.SEEK_END)
    size = file.tell()
    if size > MAX_FILE_UPLOAD_SIZE:
        raise BadRequest(
            {file.filename:
                ["You cant upload any file more that {} bytes".format(
                    MAX_FILE_UPLOAD_SIZE)]
             }
        )
    file.seek(0)
    return size


def get_public_link(file_name, bucket_name=config.get("S3_PUBLIC_BUCKET_NAME")):
    url = get_s3_client().generate_presigned_url('get_object',
                                                 Params={'Bucket': bucket_name,
                                                         'Key': file_name},
                                                 ExpiresIn=PRE_SIGNED_URL_EXPIRE_TIME)
    return url


def object_exits(file_name, bucket_name=None):
    bucket_name = bucket_name or config.get("S3_PUBLIC_BUCKET_NAME")
    try:
        get_s3_resource().Object(bucket_name, file_name).load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
            return False
        raise
    return True


class MediaField(fields.String):
    def _deserialize(self, value, attr, data, **kwargs):
        return_value = super(MediaField, self)._deserialize(value, attr, data, **kwargs)
        if not object_exits(return_value):
            raise exceptions.ValidationError('no file with this name')
        return return_value

    def _serialize(self, value, attr, obj, **kwargs):
        return get_public_link(value)
