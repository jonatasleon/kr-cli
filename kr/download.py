import sys
from os import path

import requests
from bs4 import BeautifulSoup


def download(url, output_dir="/tmp", output_filename=None, chunk_size=1024):
    if output_filename is None:
        output_filename = url.split("/")[-1]

    filename = path.join(output_dir, output_filename)

    res = requests.get(url, stream=True)
    yield int(res.headers.get("Content-Length", 0))

    with open(filename, "wb") as f:
        chunks = res.iter_content(chunk_size=chunk_size)
        for chunk in chunks:
            f.write(chunk)
            yield len(chunk)


def retrieve_file_url(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    download_url = soup.select('a[itemprop="downloadUrl"]')[0]["href"]
    return download_url
