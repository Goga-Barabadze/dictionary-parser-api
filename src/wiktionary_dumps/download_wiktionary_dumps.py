"""
Visits wiktionary's dumps and downloads the dump language-specific
files defined in the configs file.
"""
import bz2
import concurrent.futures
import logging
import os
import re
import threading
from datetime import datetime
from itertools import repeat

import requests

from box import Box
from bs4 import BeautifulSoup
from tqdm import tqdm

CHUNK_SIZE = 1024
BLOCK_SIZE = 1024

BINARY_READ_WRITE_MODE = 'wb+'
BINARY_READ_MODE = 'rb'

BZ2_FILE_EXTENSION = '.bz2'
HTML_TAG_LINK = 'a'
WIKTIONARY_FILE_SUFFIX = '-pages-articles-multistream.xml.bz2'

thread_local = threading.local()

logging.basicConfig(format='%(asctime)s %(levelname)s %(thread)d %(lineno)d \t %(message)s')
logging.getLogger().setLevel(logging.INFO)

config = Box.from_yaml(filename='config.yaml')


def _download_dump_and_decompress(link, version_control):
    """
    Downloads a bz2 with the given url and decompresses it to xml
    """

    filename = link.split('/')[-1]
    dest = config.paths.downloadsFolder

    if version_control and os.path.exists(filename) and _date_from_filename(dest + filename) >= _date_from_filename(link):
        logging.info('Skipping over %s since we don\'t need this version.', link)
        return

    size = int(requests.head(link, allow_redirects=True).headers['Content-Length']) / float(1 << 20)

    file_name_and_path = os.path.join(dest + filename)
    session = _get_session()
    with session.get(link, stream=True) as download_request:
        download_request.raise_for_status()
        progress_bar = tqdm(desc='Downloading %s' % filename, total=size, unit='iB', unit_scale=True)

        try:
            with open(file_name_and_path, BINARY_READ_WRITE_MODE) as bz2_file:
                for chunk in download_request.iter_content(chunk_size=BLOCK_SIZE * CHUNK_SIZE):
                    bz2_file.write(chunk)
                    progress_bar.update(len(chunk))
        except Exception as e:
            progress_bar.close()
            logging.error(e)
            logging.error('Error while downloading file. %s will be removed as not to leave unfinished downloads.', filename)
            os.remove(file_name_and_path)
            return

        progress_bar.close()
        logging.info('🚀 Successfully downloaded %s 🚀', filename)

        _decompress_bz2(dest, file_name_and_path, filename, size)

        os.remove(file_name_and_path)
        logging.info('Temp file %s removed again.', filename)


def _get_session():
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session


def _decompress_bz2(destination, file_name_and_path, filename, size):
    progress_bar = tqdm(desc='Decompressing %s' % filename, total=size, unit='iB', unit_scale=True)

    try:
        with bz2.open(file_name_and_path) as file, open(destination + filename.replace(BZ2_FILE_EXTENSION, ''),
                                                        BINARY_READ_WRITE_MODE) as new_file:
            _copyfileobj(file, new_file, progress_bar, length=BLOCK_SIZE * CHUNK_SIZE)
    except Exception as e:
        progress_bar.close()
        logging.error(e)
        logging.error('Error while decompressing file. %s will be removed as not to leave unfinished decompression.', filename)
        os.remove(destination + filename.replace(BZ2_FILE_EXTENSION, ''))
        return

    progress_bar.close()
    logging.info('🚀 Successfully decompressed %s 🚀', filename)


def _copyfileobj(fsrc, fdst, progress_bar, length=BLOCK_SIZE*CHUNK_SIZE):
    fsrc_read = fsrc.read
    fdst_write = fdst.write
    while True:
        buf = fsrc_read(length)
        if not buf:
            break
        fdst_write(buf)
        progress_bar.update(length)


def _date_from_filename(filename):
    date_as_string = re.findall(r'(?<=-)[0-9]*?(?=-)', filename)[0]
    return datetime.strptime(date_as_string, '%Y%m%d')


def download_dump_files(version_control=True):
    """
    Downloads the dump files
    """

    links = []

    for lang in config.languages.supported:
        dictionary_dump_request = requests.get(config.links.wiktionary.dumps)
        soup = BeautifulSoup(dictionary_dump_request.content, 'html.parser')

        for link in soup.find_all(HTML_TAG_LINK):
            if str.__contains__(link.text, lang + "wiktionary"):
                base_url = config.links.wiktionary.base_url
                deep_link = base_url + link.__dict__["attrs"]["href"]

                dictionary_dump_request = _get_session().get(deep_link)
                soup = BeautifulSoup(dictionary_dump_request.content, 'html.parser')

                for bz2_link in soup.find_all(HTML_TAG_LINK):
                    if str.__contains__(bz2_link.text, WIKTIONARY_FILE_SUFFIX):
                        download_link_for_dump = deep_link + '/' + bz2_link.__dict__["contents"][0]
                        logging.info("Link for language %s: %s", lang, download_link_for_dump)

                        links.append(download_link_for_dump)

    _download_links(list(dict.fromkeys(links)), version_control)


def _download_links(links, version_control):
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        executor.map(_download_dump_and_decompress, links, repeat(version_control))


if __name__ == "__main__":
    download_dump_files(version_control=False)
