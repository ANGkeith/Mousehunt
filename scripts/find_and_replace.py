#!/usr/bin/env python3
# Standard Library
import re
import sys


def find_and_replace(old_value: str, new_value: str, file_path: str) -> None:
    with open(file_path, "r") as file:
        file_content = file.read()
    with open(file_path, "w") as file:
        modified_file_content = re.sub(old_value, new_value, file_content)
        file.write(modified_file_content)


find_and_replace(sys.argv[1], sys.argv[2], sys.argv[3])
