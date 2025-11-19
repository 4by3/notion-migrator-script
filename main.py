#!/usr/bin/env python3
"""
Notion MD file migrator/renamer

Simple script that renames and copies the migrated Notion MD files by date in the format: YYYY-DD-MMTHHMM_Title.md
"""

from datetime import datetime
import shutil
import os
from pathlib import Path


def file_search(old_folder_destination, new_folder_name):
    os.makedirs(new_folder_name, exist_ok=True)

    for filepath in Path(old_folder_destination).glob("*.md"):
        parse_and_copy(filepath, new_folder_name)


def parse_and_copy(filepath, new_folder_name):
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
        date_line = lines[2]
        title_line = lines[0]

        date = date_line.split(":", 1)[1].strip()
        dt = datetime.strptime(date, "%B %d, %Y %I:%M %p")
        formatted_dt = dt.strftime("%Y-%m-%dT%H%M_")

        title_name = (
            title_line.split("#", 1)[1].strip().replace(" ", "_").replace("/", "-")
        )

        destination = new_folder_name + "/" + formatted_dt + title_name + ".md"
        print(destination)
        shutil.copy2(filepath, destination)

    except Exception as e:
        print(f"Error processing {filepath}: {e}")


def main():
    old_folder_destination = input("Your folder's destination: ")
    new_folder_name = input("Name of new folder: ")
    file_search(old_folder_destination, new_folder_name)


if __name__ == "__main__":
    main()
