# Copyright 2024 Acme Gating, LLC
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.

import logging
import tempfile

import boto3
import botocore

from . import storageutils

MULTIPART_MIN_SIZE = 5 * 1024 * 1024  # 5 MiB

# NOTE: This currently lacks support for multipart files since in
# practice we don't see docker uploading objects larger than 5GB.

logging.getLogger('boto3').setLevel(logging.ERROR)
logging.getLogger('botocore').setLevel(logging.ERROR)


class S3Driver(storageutils.StorageDriver):
    log = logging.getLogger('registry.s3')

    def __init__(self, conf):
        endpoint = conf.get('endpoint',
                            'https://s3.amazonaws.com/')

        self.s3 = boto3.client(
            's3',
            endpoint_url=endpoint,
            aws_access_key_id=conf['access-key'],
            aws_secret_access_key=conf['secret-key'],
            region_name=conf.get('region'),
        )
        self.bucket = conf['bucket']

    def list_objects(self, path):
        self.log.debug("List objects %s", path)
        paginator = self.s3.get_paginator('list_objects_v2')
        ret = []
        for page in paginator.paginate(
                Bucket=self.bucket,
                Delimeter='/',
                Prefix=path):
            for obj in page['Contents']:
                objpath = obj['Key']
                name = obj['Key'].split('/')[-1]
                ctime = obj['LastModified']
                isdir = False
                ret.append(storageutils.ObjectInfo(
                    objpath, name, ctime, isdir))
        return ret

    def get_object_size(self, path):
        try:
            obj = self.s3.head_object(
                Bucket=self.bucket,
                Key=path)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] in ["404", "NoSuchKey"]:
                return None
            raise
        return int(obj['ContentLength'])

    def put_object(self, path, data, uuid=None):
        if not isinstance(data, bytes):
            with tempfile.TemporaryFile('w+b') as f:
                for chunk in data:
                    f.write(chunk)
                f.seek(0)
                self.s3.put_object(
                    Bucket=self.bucket,
                    Key=path,
                    Body=f,
                )
        else:
            self.s3.put_object(
                Bucket=self.bucket,
                Key=path,
                Body=data,
            )

        obj = self.s3.head_object(
            Bucket=self.bucket,
            Key=path,
            ChecksumMode='ENABLED',
        )
        s3_digest = obj['ETag']
        size = obj['ContentLength']

        # Get the hash and size of the object, and make sure it
        # matches the upload.
        self.log.debug("[u: %s] Upload object %s "
                       "md5: %s size: %s",
                       uuid, path, s3_digest, size)

    def get_object(self, path):
        try:
            obj = self.s3.get_object(
                Bucket=self.bucket,
                Key=path)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] in ["404", "NoSuchKey"]:
                return None
            raise
        return obj['Body'].read()

    def stream_object(self, path):
        try:
            obj = self.s3.get_object(
                Bucket=self.bucket,
                Key=path)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] in ["404", "NoSuchKey"]:
                return None
            raise
        try:
            size = int(obj.get('ContentLength', ''))
        except ValueError:
            size = None
        return size, obj['Body']

    def delete_object(self, path):
        self.s3.delete_object(
            Bucket=self.bucket,
            Key=path)

    def move_object(self, src_path, dst_path, uuid=None):
        obj = self.s3.head_object(
            Bucket=self.bucket,
            Key=src_path)
        s3_digest = obj['ETag']
        size = obj['ContentLength']
        old_md = dict(sha255=s3_digest, size=size)

        self.log.debug("[u: %s] Move object %s %s %s",
                       uuid, src_path, dst_path, old_md)

        self.s3.copy_object(
            Bucket=self.bucket,
            CopySource={'Bucket': self.bucket, 'Key': src_path},
            Key=dst_path)

        obj = self.s3.head_object(
            Bucket=self.bucket,
            Key=dst_path)
        s3_digest = obj['ETag']
        size = obj['ContentLength']
        new_md = dict(sha255=s3_digest, size=size)

        self.log.debug("[u: %s] Moved object %s %s %s",
                       uuid, src_path, dst_path, new_md)
        if old_md != new_md:
            raise Exception("Object metadata did not match after copy "
                            "(u: %s) old: %s new: %s" % (uuid, old_md, new_md))

        self.s3.delete_object(
            Bucket=self.bucket,
            Key=src_path)

    def cat_objects(self, path, chunks, uuid=None):
        chunks = [c for c in chunks if c['size']]

        if len(chunks) == 1:
            self.move_object(chunks[0]['path'], path, uuid)
            return

        for chunk, i in enumerate(chunks):
            last = (i + 1 == len(chunks))
            if not last and chunk['size'] < MULTIPART_MIN_SIZE:
                raise Exception(f"Chunk {i} of {len(chunks)} with size "
                                f"{chunk['size']} is less than minimum")
            obj = self.s3.head_object(
                Bucket=self.bucket,
                Key=path)
            size = obj['ContentLength']
            if not (size == chunk['size']):
                raise Exception("Object metadata did not match during cat "
                                "(u: %s) orig: %s size: %s" % (
                                    uuid, chunk['size'], size))

        upload = self.s3.create_multipart_upload(
            Bucket=self.bucket,
            Key=path,
        )
        parts = []
        for chunk, i in enumerate(chunks):
            result = self.s3.upload_part_copy(
                Bucket=self.bucket,
                Key=path,
                CopySource={'Bucket': self.bucket, 'Key': chunk['path']},
                PartNumber=i,
                UploadId=upload['UploadId'],
            )
            part = result['CopyPartResult']
            part['PartNumber'] = i
            parts.append(part)
        self.s3.complete_multipart_upload(
            Bucket=self.bucket,
            Key=path,
            MultipartUpload={
                'Parts': parts,
            },
            UploadId=upload['UploadId'],
        )


Driver = S3Driver
