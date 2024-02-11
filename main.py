import requests
import os
import argparse
import sys


def get_filename_from_url(url):
    url_parts = url.split("/")
    file_name = url_parts[-1]
    return file_name


def download_file_chain(
    url_template: str,
    destination_folder: str,
    start_number: int,
    padding: int,
) -> None:
    current_number = start_number
    file_exists = True
    while file_exists:
        url = url_template.format(str(current_number).zfill(padding))
        filename = get_filename_from_url(url)
        file_exists = download_file(url, destination_folder, filename)
        current_number += 1


def download_file(url: str, destination_folder: str, filename: str) -> bool:
    """
    Download an individual file and save it to the specified folder.
    """
    destination_path = f"{destination_folder}/{filename}"
    response = requests.get(url)
    if response.status_code == 200:
        with open(destination_path, "wb") as f:
            f.write(response.content)
        print(f"Downloaded '{filename}'")
        return True
    else:
        print(f"'{filename}' not found. Stopping download.")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Download multiple consecutively numbered files from a given URL."
    )
    parser.add_argument(
        "url_template",
        help="URL template with {} as placeholder for the number",
    )
    parser.add_argument(
        "destination_folder", help="Destination folder for downloaded files"
    )
    parser.add_argument("start_number", type=int, help="Starting file number")
    parser.add_argument(
        "--padding",
        help="Size of the padded number (default: 1)",
        default=1,
        type=int,
    )
    args = parser.parse_args()
    destination_folder = os.path.expanduser(args.destination_folder)
    if not os.path.exists(destination_folder):
        os.makedirs(destination_folder)

    download_file_chain(
        args.url_template, destination_folder, args.start_number, args.padding
    )
    sys.exit(0)


if __name__ == "__main__":
    main()
