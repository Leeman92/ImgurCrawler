__author__ = 'Patrick'
from urllib import request
from os import path

from bs4 import BeautifulSoup
import requests


skipping = 0
base_url = "http://imgur.com"
sub_url = ""  # link to the album you want to download. example /r/Girls_smiling


def web_spider(max_pictures, start_picture=1):
    pictures = 1
    global skipping
    url = base_url + sub_url
    source_code = requests.get(url)
    # just get the code, no headers or anything
    plain_text = source_code.text
    # BeautifulSoup objects can be sorted through easy
    soup = BeautifulSoup(plain_text)
    for link in soup.findAll('a', {'class': 'image-list-link'}):
        if pictures <= max_pictures:
            href = link.get('href')
            # print(href)
            if pictures < start_picture:
                pictures += 1
            if skipping == 1:
                skipping = 0
                pictures -= 1
                continue
            download_picture(base_url + href, "")
            pictures += 1
            left = max_pictures - pictures
            print("There are %s pictures left to download!" % left)


def download_picture(url, name):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    global skipping

    for title in soup.findAll('h2', {'id': 'image-title'}):
        name = title.string
    for image in soup.findAll('link', {'rel': 'image_src'}):
        image_source = image.get('href')
        filename = name.replace(',', '_').replace(' ', '_').lower().replace('?', '') + str(image_source)[-4:]
        if path.isfile(filename):
            skipping = 1
            print("Skipping.. Already downloaded...")
            continue
        if str(image_source).endswith(".jpg") or str(image_source).endswith(".JPG") or str(image_source).endswith(
                ".gif"):
            request.urlretrieve(image_source, filename)
            print("Successfully downloaded", filename)


web_spider(start_picture=1, max_pictures=100)
