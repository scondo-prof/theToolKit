import os
import shutil
import argparse


def list_files_recursively(dir_path: str):
    """Recursively list all files in a directory."""
    for root, _, files in os.walk(dir_path):
        for file in files:
            print(os.path.join(root, file))


def move_file(source_path: str, destination_path: str):
    """Move a file from source to destination."""
    try:
        shutil.move(source_path, destination_path)
        print(f"File moved from {source_path} to {destination_path}")
    except Exception as e:
        print(f"Failed to move file from {source_path} to {destination_path}: {e}")


def filename_prefix_append(method: str, prefix: str, filename: str = None):
    """Appends a Prefix to designated file/files."""
    if method == "file":
        os.rename(src=filename, dst=f"{prefix}{filename}")
        print(f"{filename} -> {prefix}{filename}")
    elif method == "cwd":
        file_list: list[str] = []
        for f in os.listdir():
            if os.path.isfile(f):
                file_list.append(f)
        for file_name in file_list:
            os.rename(src=file_name, dst=f"{prefix}{file_name}")
            print(f"{file_name} -> {prefix}{file_name}")
    elif method == "recursive":
        pass
    else:
        raise Exception("method Argument must be file, cwd, or recursive")


def main():
    # parser = argparse.ArgumentParser(description="Utility for working with files and directories.")
    # subparsers = parser.add_subparsers(dest="command", required=True)

    # # list_files_recursively command
    # parser_list = subparsers.add_parser("list_files_recursively", help="Recursively list all files in a directory.")
    # parser_list.add_argument("dir_path", help="Path to the target directory.")
    # parser_list.set_defaults(func=list_files_recursively)

    # # move_file command
    # parser_move = subparsers.add_parser("move_file", help="Move a file from source to destination.")
    # parser_move.add_argument("source_path", help="Path to the file to move.")
    # parser_move.add_argument("destination_path", help="Path to the destination directory.")
    # parser_move.set_defaults(func=move_file)

    # args = parser.parse_args()
    # args.func(**vars(args))  # Calls the selected function
    filename_prefix_append(method="cwd", prefix="test_")


if __name__ == "__main__":
    main()
