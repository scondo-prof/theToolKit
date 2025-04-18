import boto3
from boto3.s3.transfer import TransferConfig
import os
import sys
import re
import pendulum


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.files_and_directories import list_files_recursively, move_file

# Initialize a session using Amazon S3
s3_client = boto3.client('s3')

def upload_s3_obj(file_name, object_name, s3_path) -> str:

    config = TransferConfig(
        multipart_threshold=1024 * 25,  # 25MB
        max_concurrency=10,
        multipart_chunksize=1024 * 25,  # 25MB
        use_threads=True
    )

    
    print(f"About to upload file with s3 key: {s3_path}")
    try:
        response = s3_client.upload_file(
            Filename = file_name,
            Bucket = os.getenv("S3_BUCKET"), 
            Key = s3_path,
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

    todays_date = pendulum.today().format("MM-DD-YYYY")
    print(f"Today is: {todays_date}")

    for file in files:
        print(file)
        s3_path = ""
        for key in identifiers:
            if key in file:
                file_name = file.split("\\")[-1]
                file_name = todays_date + "_" + file_name
                s3_path = identifiers[key] + file_name
                print(s3_path)
                break
        
        if s3_path:
            print(f"About to upload: {file}")
            response = upload_s3_obj(file_name=file, object_name=file, s3_path=s3_path)
            new_path = re.sub(r"\\raw.*", rf"\\processed\\{file_name}", file)
            print(f"New Path: {new_path}")
            move_file(source_path=file, destination_path=new_path)
            print(f"Response: {response}")




bulk_s3_upload(dir_path="C:\\Users\\scott\\OneDrive\\Documents\\drones\\raw")