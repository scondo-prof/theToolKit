import boto3
from boto3.s3.transfer import TransferConfig
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.files_and_directories import list_files_recursively

# Initialize a session using Amazon S3
s3_client = boto3.client('s3')

def upload_s3_obj(dir_path, object_name, s3_path) -> str:

    config = TransferConfig(
        multipart_threshold=1024 * 25,  # 25MB
        max_concurrency=10,
        multipart_chunksize=1024 * 25,  # 25MB
        use_threads=True
    )

    try:
        response = s3_client.upload_file(
            Filename = dir_path + "\\" + object_name, 
            Bucket = os.getenv("S3_BUCKET"), 
            Key = s3_path+object_name,
            Config = config
        )
        print(f"Response: {response}")
    except Exception as e:
        print(f"Upload failed: {e}")


def bulk_s3_upload(dir_path):

    identifiers = {
        "avata" : "raw/avata/",
        "m3p" : "raw/m3p/",
        "gp" : "raw/gp/",
        "gpa" : "raw/gpa/"
    }

    files = list_files_recursively(dir_path = dir_path)

    print(files)

    for file in files:
        print(file)
        s3_path = ""
        for key in identifiers:
            if key in file:
                s3_path = identifiers[key]
                print(s3_path)
                break
        
        if s3_path:
            print(f"About to upload: {file}")
            response = upload_s3_obj(dir_path=dir_path, object_name=file, s3_path=s3_path)
            print(f"Response: {response}")

bulk_s3_upload(dir_path="C:\\Users\\scott\\OneDrive\\Documents\\drones\\raw")