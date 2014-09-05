__author__ = 'Patrick'
from urllib import request
from os import path

from bs4 import BeautifulSoup
import requests


skipping = 0
base_url = "http://imgur.com"
# link to the album you want to download. example /r/Girls_smiling
sub_url = input("Please define where to download the pictures from: ")
pictures = 1

if sub_url.startswith(base_url):
    sub_url = sub_url[16:]


def web_spider(max_pictures):
    global pictures
    global skipping
    url = base_url + sub_url
    source_code = requests.get(url)
    # just get the code, no headers or anything
    plain_text = source_code.text
    # BeautifulSoup objects can be sorted through easy
    soup = BeautifulSoup(plain_text)
    for link in soup.findAll('a', {'class': 'image-list-link'}):
        if pictures <= max_pictures:
            print(href)
            if skipping == 1:
                skipping = 0
                pictures -= 1
            download_picture(base_url + href, max_pictures)
    print("No more pictures to download on this site")


def download_picture(url, max_pictures):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text)
    global skipping
    global pictures

    for title in soup.findAll('h2', {'id': 'image-title'}):
        name = title.string
    for image in soup.findAll('link', {'rel': 'image_src'}):
        image_source = image.get('href')
        filename = name.replace(',', '_').replace(' ', '_').lower().replace('?', '') + str(image_source)[-4:]
        if path.isfile(filename):
            skipping = 1
            print("Skipping.. Already downloaded...")
            continue
        elif str(image_source).endswith(".jpg") or str(image_source).endswith(".JPG") or str(image_source).endswith(
                ".gif") or str(image_source).endswith(".png") or str(image_source).endswith(".PNG") or str(image_source).endswith(".GIF"):
            request.urlretrieve(image_source, filename)
            print("Successfully downloaded", filename)
            left = max_pictures - pictures
            print("There are %s pictures left to download!" % left)
            pictures += 1

def start():
    max_download = input ("How many pictures should be downloaded at most? ")
    if max_download.isnumeric():
        web_spider(max_pictures=int(max_download))
    else:
        print("Error! You need to insert a numeric value!")
        start()

start()
