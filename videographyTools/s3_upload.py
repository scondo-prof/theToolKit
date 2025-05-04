import asyncio
import os
import sys

import aioboto3
import aioboto3.session
from boto3.s3.transfer import TransferConfig

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.files_and_directories import list_files_recursively, move_file


async def upload_s3_obj(file_name: str, s3_path: str) -> str:
    bucket_name = os.getenv("S3_BUCKET")

    config = TransferConfig(
        multipart_threshold=1024 * 8,
        max_concurrency=16,
        multipart_chunksize=1024 * 16,
        use_threads=True,
    )

    print(f"About to upload file with S3 key: {s3_path}")
    try:
        print("Inside Catch")
        session = aioboto3.Session()
        print("session made")
        async with session.client("s3") as s3_client:
            response = await s3_client.list_buckets()
            print(f"Response: {response}")
            for bucket in response["Buckets"]:
                print(bucket["Name"])

    #     async with aioboto3.client(
    #         "s3",
    #         config=aioboto3.session.Config(s3={"use_accelerate_endpoint": True}),
    #     ) as s3_client:
    #         print("Created the client")
    #         # Run the blocking upload_file in a thread to avoid blocking the event loop
    #         await asyncio.to_thread(
    #             s3_client.upload_file,
    #             Filename=file_name,
    #             Bucket=bucket_name,
    #             Key=s3_path,
    #             Config=config,
    #         )
    #     return f"Successfully Uploaded {s3_path}"
    except Exception as e:
        return f"Failed Upload for {s3_path}: {e}"


async def bulk_s3_upload(s3_path: str) -> list[str]:
    dir_path = os.getcwd()
    all_files = list_files_recursively(dir_path)
    results = []

    async def upload_task(file_path: str, s3_path: str):
        relative_path = os.path.relpath(file_path, start=dir_path)

        s3_key = relative_path.replace(os.sep, "/")  # S3 expects forward slashes
        s3_key = s3_path + s3_key

        result = await upload_s3_obj(file_name=file_path, s3_path=s3_key)
        return result

    tasks = [upload_task(file_path=file_path, s3_path=s3_path) for file_path in all_files]
    results = await asyncio.gather(*tasks)
    return results


asyncio.run(upload_s3_obj(file_name="z.txt", s3_path="test/z.txt"))

# asyncio.run(bulk_s3_upload(s3_path="test/"))
