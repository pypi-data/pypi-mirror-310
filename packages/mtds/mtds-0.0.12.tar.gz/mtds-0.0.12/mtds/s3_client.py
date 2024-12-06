import logging
import os
from pathlib import Path

import boto3
from botocore.exceptions import NoCredentialsError


# TODO 单例模式
class S3Client:
    def __init__(self, **kwargs):
        self.s3_client = boto3.client('s3', **kwargs)
        try:
            self.s3_client.list_buckets()
        except NoCredentialsError:
            raise Exception('No AWS credentials found')

    @classmethod
    def create_from_env(cls):
        aws_access_key_id = os.environ.get('aws_access_key_id')
        aws_secret_access_key = os.environ.get('aws_secret_access_key')

        if not aws_access_key_id or not aws_secret_access_key:
            raise Exception('AWS credentials not found in environment variables')

        return cls(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    def upload_file(self, file_path, s3_key, bucket_name='sing-strong', extra_args=None):
        source_path = Path(file_path)
        if not source_path.exists():
            raise FileNotFoundError(f'File {file_path} does not exist')
        self.s3_client.upload_file(
            file_path,
            bucket_name,
            s3_key,
            extra_args,
        )

    def upload_bytes(self, body, s3_key, bucket_name='sing-strong', **kwargs):
        self.s3_client.put_object(Bucket=bucket_name, Key=s3_key, Body=body, **kwargs)

    def download_file(self, s3_key, file_path, bucket_name, **kwargs):
        dest_path = Path(file_path)
        if not dest_path.parent.exists():
            dest_path.parent.mkdir(parents=True, exist_ok=True)
        self.s3_client.download_file(bucket_name, s3_key, file_path, **kwargs)
