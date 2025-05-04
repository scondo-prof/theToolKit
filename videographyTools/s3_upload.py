import asyncio
import os
import re
import sys

import aioboto3
from boto3.s3.transfer import TransferConfig

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from utils.files_and_directories import list_files_recursively, move_file


async def upload_s3_obj(file_name: str, s3_key: str) -> str:

    config = TransferConfig(
        multipart_threshold=1024 * 8,
        max_concurrency=16,
        multipart_chunksize=1024 * 16,
        use_threads=True,
    )

    print(f"About to upload file with S3 key: {s3_key}")
    try:
        print("Inside Catch")
        session = aioboto3.Session()
        print("session made")
        async with session.client("s3") as s3_client:
            response = await s3_client.upload_file(
                Filename=file_name, Bucket=os.getenv("S3_BUCKET"), Key=s3_key, Config=config
            )
            print(f"Successfully Uploaded: {s3_key}")

    except Exception as e:
        return f"Failed Upload for {s3_key}: {e}"


async def bulk_s3_upload(s3_path: str) -> list[str]:
    dir_path = os.getcwd()
    all_files = list_files_recursively(dir_path)
    tasks = []
    results = []

    async def upload_task(file_path: str, s3_path: str):
        relative_path = os.path.relpath(file_path, start=dir_path)

        s3_key = relative_path.replace(os.sep, "/")  # S3 expects forward slashes
        s3_key = s3_path + s3_key

        print(
            f"""---
Gathered File: {file_path}
To be Uploaded To
S3 Key: {s3_key}"""
        )

        result = await upload_s3_obj(file_name=file_path, s3_key=s3_key)
        return result

    for file_path in all_files:
        if not ".git" in file_path:
            tasks.append(upload_task(file_path=file_path, s3_path=s3_path))
    # tasks = [upload_task(file_path=file_path, s3_path=s3_path) for file_path in all_files]
    print("Files Gathered and Ready For Upload")
    results = await asyncio.gather(*tasks)
    return results


if __name__ == "__main__":
    pattern = r"^(?:[\w\-]+/)+$"

    while True:
        user_s3_path = input("Enter the S3 path prefix (e.g., 'my-folder/'): ")
        if re.match(pattern, user_s3_path):
            break
        print(
            "Invalid format. Please ensure the path ends with '/' and contains only letters, digits, underscores, or hyphens."
        )

    asyncio.run(bulk_s3_upload(s3_path=user_s3_path))

# asyncio.run(upload_s3_obj(file_name="z.txt", s3_key="test/z.txt"))

# asyncio.run(bulk_s3_upload(s3_path="test/"))
