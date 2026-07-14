# import csv
# import xml.etree.ElementTree as ET
import requests
from bs4 import BeautifulSoup
import gzip
import io
from pathlib import Path


def default_html_parser(text):
    return BeautifulSoup(text, "html.parser")


def default_http_getter(*args, **kwargs):
    return requests.get(*args, **kwargs)


def default_gzip_decompressor(data):
    file_object = io.BytesIO(data)
    with gzip.GzipFile(fileobj=file_object) as decompressor:
        decompressed_data = decompressor.read().decode('utf-8')
    return decompressed_data

def default_directory_creator(directory_path):
    dir_path_path = Path(directory_path)
    dir_path_path.mkdir(parents=True, exist_ok=True)

class StoreStorage:
    def __init__(self, directory_creator, base_directory):
        self._base_directory = base_directory
        directory_creator(self._base_directory)

    def save(self, filename, content):
        with open('/'.join([self._base_directory, filename]), 'w', encoding='utf-8') as file:
            file.write(content)


def extract_filename_from_url(url):
    try:
        clean_url = url.split('?')[0]
        filename_with_ext = clean_url.split('/')[-1]
        filename = filename_with_ext.split('.gz')[0]
        return filename if filename else None
    except (IndexError, AttributeError):
        return None

def get_stores_xml_urls(base_url, **kwargs):
    path = kwargs.get("path", "")
    params = kwargs.get("params", dict())
    html_parser = kwargs.get("html_parser", default_html_parser)
    http_getter = kwargs.get("http_getter", default_http_getter)

    response = http_getter("/".join([base_url, path]), params)
    response.raise_for_status()
    parsed_html = html_parser(response.text)

    urls = []
    for link in parsed_html.select("tbody a"):
        url = link.get("href")
        if url:
            urls.append(url)
    return urls


def get_stores_info_xml(url, **kwargs):
    http_getter = kwargs.get("http_getter", default_http_getter)
    decompressor = kwargs.get("gzip_decompressor", default_gzip_decompressor)

    response = http_getter(url, stream=True)
    response.raise_for_status()

    filename = extract_filename_from_url(url)

    return (filename, decompressor(response.content))


def main(base_url, path, params, store_storage):
    urls = get_stores_xml_urls(base_url, path=path, params=params)
    for url in urls:
        filename, data = get_stores_info_xml(url)
        store_storage.save(filename, data)

print(__name__)
if __name__ == '__main__':
    base_url = "https://prices.shufersal.co.il"
    path = "FileObject/UpdateCategory"
    params = dict(catID=5, storeId=0)
    store_storage = StoreStorage(default_directory_creator, "./raw/stores")
    main(base_url, path, params, store_storage)
