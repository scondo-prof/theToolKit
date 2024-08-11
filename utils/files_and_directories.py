import os
import shutil

def list_files_recursively(dir_path: str) -> dict:
    target_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            target_files.append(os.path.join(root, file))
    return target_files


def move_file(source_path: str, destination_path: str):
  
    try:
        shutil.move(source_path, destination_path)
        print(f"File moved from {source_path} to {destination_path}")

    except Exception as e:
        print(f"Failed to move file from {source_path} to {destination_path}: {e}")


