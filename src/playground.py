"""
Playing around
"""

import logging
import shutil
from bs4 import BeautifulSoup
from box import Box
import requests


WIKTIONARY_FILE_SUFFIX = '-pages-articles-multistream.xml.bz2'


logging.getLogger().setLevel(logging.INFO)
config = Box.from_yaml(filename="../config.yaml")


def download_file(url):
    """
    downloads a file with the given url
    """
    local_filename = '../' + config.paths.downloadsFolder + url.split('/')[-1]
    with requests.get(url, stream=True) as download_request:
        with open(local_filename, 'wb') as file:
            shutil.copyfileobj(download_request.raw, file)


for lang in config.languages.supported:
    dictionary_dump_request = requests.get(config.links.wiktionary.dumps)
    soup = BeautifulSoup(dictionary_dump_request.content, 'html.parser')

    for link in soup.find_all('a'):
        if str.__contains__(link.text, lang + "wiktionary"):
            base_url = config.links.wiktionary.base_url
            deep_link = base_url + link.__dict__["attrs"]["href"]

            dictionary_dump_request = requests.get(deep_link)
            soup = BeautifulSoup(dictionary_dump_request.content, 'html.parser')

            for bz2_link in soup.find_all('a'):
                if str.__contains__(bz2_link.text, WIKTIONARY_FILE_SUFFIX):
                    download_link = deep_link + '/' + bz2_link.__dict__["contents"][0]
                    logging.info("Found download link for language %s: %s", lang, download_link)

                    # download_file('https://mir-s3-cdn-cf.behance.net/project
                    #_modules/max_1200/101ad363237205.5aa9feaddf1f7.gif')
