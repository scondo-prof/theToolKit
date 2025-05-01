import os
import sys
import re

import boto3
from boto3.s3.transfer import TransferConfig
import pendulum


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.files_and_directories import list_files_recursively, move_file


def upload_s3_obj(file_name, s3_path) -> str:
    bucket_name = os.getenv("S3_BUCKET")

    s3_client = boto3.client(
        "s3",
        config=boto3.session.Config(s3={"use_accelerate_endpoint": True}),
    )

    config = TransferConfig(
        multipart_threshold=1024 * 8,  # 8 MB
        max_concurrency=16,  # 16 threads
        multipart_chunksize=1024 * 16,  # 16 MB
        use_threads=True,
    )

    print(f"About to upload file with S3 key: {s3_path}")
    try:
        response = s3_client.upload_file(
            Filename=file_name,
            Bucket=bucket_name,
            Key=s3_path,
            Config=config,
        )
        return f"Successfully Uploaded {s3_path}"
    except Exception as e:
        return f"Failed Upload for {s3_path}: {e}"


def bulk_s3_upload(dir_path):
    