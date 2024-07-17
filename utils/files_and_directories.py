import os

def list_files_recursively(dir_path: str) -> str:
    target_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            target_files.append(file)
    return target_files


