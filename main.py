#!/usr/bin/env python3
"""
Notion MD file migrator/renamer

Simple script that renames and copies migrated Notion MD files by date in the format: YYYY-DD-MMTHHMM_Title.md
"""

from datetime import datetime
import shutil
import os
from pathlib import Path


def parse(filepath):
    try:
        with open(filepath, "r") as f:
            lines = f.readlines()
        if len(lines) < 3 or lines[2].split()[0] != "Created:":
            raise ValueError(f"File {filepath} is in invalid MD format")

        date_line = lines[2]
        title_line = lines[0]

        date = date_line.split(":", 1)[1].strip()
        dt_raw = datetime.strptime(date, "%B %d, %Y %I:%M %p")
        dt = dt_raw.strftime("%Y-%m-%dT%H%M")

        title = "__" + title_line[2:].strip()

        tags = ""
        if (
            len(lines) > 4
            and len(lines[3].split()) > 1
            and lines[3].split()[0] == "Tags:"
        ):
            tags_line = lines[3]
            tags = "__" + tags_line.split(":", 1)[1].strip().replace(" ", "")

        title = clean(title)
        tags = clean(tags)
        return dt, title, tags

    except Exception as e:
        raise ValueError(f"Error processing {filepath}: {e}")


def clean(string):
    safe_string = (
        string.replace(" ", "_")
        .replace("/", "-")
        .replace(":", "-")
        .replace("?", "")
        .replace('"', "'")
        .replace("<", "")
        .replace(">", "")
        .replace("|", "")
        .replace("*", "")
    )
    return safe_string


def main():
    old_folder_destination = input("Your folder's destination: ")
    new_folder_name = input("Name of new folder: ")
    os.makedirs(new_folder_name, exist_ok=True)

    successful_files = 0
    for filepath in Path(old_folder_destination).glob("*.md"):
        dt, title, tags = parse(filepath)
        try:
            new_filename = f"{new_folder_name}/{dt}{title}{tags}.md"
            shutil.copy2(filepath, new_filename)
            successful_files += 1
            print(f"Successfully copied {new_filename}")
        except Exception as e:
            raise ValueError(
                f"Error copying file: {e}\nExiting with {successful_files} successful files"
            )
    print(f"Finished with {successful_files} successful files")


if __name__ == "__main__":
    main()
