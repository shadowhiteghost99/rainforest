from bs4 import BeautifulSoup
import gzip
import io
import requests
from pathlib import Path


def default_gzip_decompressor(data):
    file_object = io.BytesIO(data)
    with gzip.GzipFile(fileobj=file_object) as decompressor:
        decompressed_data = decompressor.read().decode("utf-8")
    return decompressed_data


def default_html_parser(text):
    return BeautifulSoup(text, "html.parser")


def default_http_getter(*args, **kwargs):
    return requests.get(*args, **kwargs)


def default_directory_creator(directory_path):
    dir_path_path = Path(directory_path)
    dir_path_path.mkdir(parents=True, exist_ok=True)
