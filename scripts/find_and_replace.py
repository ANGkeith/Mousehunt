#!/usr/bin/env python3
# Standard Library
import re
import sys


def find_and_replace(old_value: str, new_value: str, file_path: str) -> None:
    with open(file_path, "r") as file:
        file_content = file.read()
    with open(file_path, "w") as file:
        modified_file_content = re.sub(old_value, new_value, file_content)
        if file_content != modified_file_content:
            print(
                f"{file_name(file_path)}: Success `{old_value} -> f{new_value}`"
            )
        else:
            print(f"{file_name(file_path)}: Failed `{old_value}`")
        file.write(modified_file_content)


def file_name(file_path: str) -> str:
    return file_path.split("/")[-1]


find_and_replace(sys.argv[1], sys.argv[2], sys.argv[3])
