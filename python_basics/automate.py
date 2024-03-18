''' Automate tasks with Python '''
import os
import logging
import random
import string
from shutil import move
from urllib.parse import urlparse
import bz2
import zipfile
import requests
from requests.exceptions import RequestException
from tqdm import tqdm

from data_science.time_data import seconds_2_date


def file_identifier(filepath: str) -> str:
    '''Identify fie types'''
    extension = os.path.splitext(filepath)[1]

    # supported image types
    image_extensions = [".jpg", ".jpeg", ".jif", ".png", ".gif", ".webp",
                        ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2",
                        ".nrw", ".k25", ".bmp", ".dib", ".heif", ".heic",
                        ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm",
                        ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
    # supported Video types
    video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv",
                        ".ogg", ".mp4", ".mp4v", ".m4v", ".avi", ".wmv",
                        ".mov", ".qt", ".flv", ".swf", ".avchd"]
    # supported Audio types
    audio_extensions = [".m4a", ".flac", ".mp3", ".wav", ".wma", ".aac"]
    # supported Document types
    document_extensions = [".doc", ".docx", ".odt", ".pdf", ".xls", ".xlsx",
                           ".ppt", ".pptx"]

    # Map extensions to their categories
    extension_categories = {
        **{ext: 'image' for ext in image_extensions},
        **{ext: 'video' for ext in video_extensions},
        **{ext: 'audio' for ext in audio_extensions},
        **{ext: 'document' for ext in document_extensions}
    }

    return extension_categories.get(extension.lower(), 'other')


def sort_files(dir_path: str) -> str:
    '''Sort files in a given directory'''
    if not os.path.isdir(dir_path):
        logging.info("Path not exist: %s", dir_path)
        return None

    for entry in os.scandir(dir_path):
        if entry.is_file():
            category = file_identifier(entry.name)
            subdir = os.path.join(dir_path, category)
            os.makedirs(subdir, exist_ok=True)
            move(entry.path, os.path.join(subdir, entry.name))

    return f"{dir_path} scanned successfully"


def list_files(
        dir_path: str,
        file_type: str
        ) -> (tuple[None, None] | tuple[list, dict]):
    '''Get the list of given file type from a directory'''

    if not os.path.isdir(dir_path):
        logging.info("Path not exist: %s", dir_path)
        return (None, None)

    files = []
    file_info = {}

    for entry in os.scandir(dir_path):
        if entry.is_file() and (os.path.splitext(entry.name)[1] == file_type):
            files.append(entry)
            file_stat = entry.stat()
            file_info[entry.name] = {
                "File size(MB)": (file_stat.st_size/(1024*1024)),
                "Last modified": seconds_2_date(file_stat.st_mtime)
                }

    return files, file_info


def generate_unique_name(length=10) -> str:
    '''Generate unique names'''
    characters = string.ascii_letters + string.digits
    unique_name = ''.join(random.choice(characters) for _ in range(length))
    return unique_name


def download_files(url_list: dict, downloads_dir: str) -> None:
    '''Download the content from a url list to a given location
    input = {
        "file_name": "url"
    }'''
    # create downloads dir
    os.makedirs(downloads_dir, exist_ok=True)

    # validate urls
    for file_name, url in url_list.items():
        if (urlparse(url).scheme and urlparse(url).netloc):
            with requests.Session() as se:
                chunk_size = 1024 * 1024  # 1 MB chunk size
                response = se.get(url, stream=True)
                total_size = int(response.headers.get('content-length', 0))

                # display progress bar
                with tqdm(total=total_size,
                          unit='B',
                          unit_scale=True,
                          desc=url.split('/')[-1],
                          ascii=True,
                          miniters=1) as progress:
                    download_path = os.path.join(downloads_dir, file_name)
                    with open(download_path, 'wb') as f:
                        try:
                            for chunk in response.iter_content(chunk_size):
                                if chunk:
                                    f.write(chunk)
                                    progress.update(len(chunk))
                        except RequestException as e:
                            logging.info("Download failed: %e", e)
                            os.remove(download_path)

                if total_size != 0 and progress.n != total_size:
                    logging.info("Download failed: %s", url)
                    os.remove(download_path)
                else:
                    logging.info("Download success: %s", url)
        else:
            logging.info("Invalid URL : %s", url)


def check_url(url: str) -> str | None:
    '''Check the content type of a URL'''
    # check the header
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)

        # check if the request was successful (status code 2xx)
        if response.status_code // 100 == 2:
            logging.info("URL is accessible: %s", url)

            # check if the response indicates a downloadable file
            content_type = response.headers.get('content-type', '')
            return content_type

        else:
            logging.info("URL not accessible: %s", url)
            logging.info("status code: %s", response.status_code)
            return
    except RequestException as e:
        logging.info("URL not accessible: %e", e)
        return


def extract_bz2(file_path: str) -> None:
    '''Extract bz2 compressed files'''
    # check if the file exists
    if not os.path.isfile(file_path):
        logging.info("File not exists: %s", file_path)
        return

    # open the .bz2 file in binary read mode
    with open(file_path, 'rb') as f:
        compressed_data = f.read()

    # decompress the data
    try:
        data = bz2.decompress(compressed_data)

        output_path = os.path.splitext(file_path)[0]
        with open(output_path, 'wb') as f:
            f.write(data)

        logging.info("Extraction success: %s", output_path)
    except OSError as e:
        logging.info("Extraction failed: %e", e)


def extract_zip(file_path: str, extract_dir: str) -> None:
    '''Extract .zip compressed files'''
    # check if the file exists
    if not os.path.isfile(file_path):
        logging.info("File not exists: %s", file_path)
        return

    # extract the file
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            z.extractall(extract_dir)

        logging.info("Extraction success: %s", extract_dir)
    except OSError as e:
        logging.info("Extraction failed: %e", e)
