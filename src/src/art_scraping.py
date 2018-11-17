
import time
import os
import re
import random
import argparse
import pickle
import urllib
import urllib.request
import itertools
import bs4
from bs4 import BeautifulSoup
import multiprocessing
from multiprocessing.dummy import Pool

base_url = 'https://www.wikiart.org'
all_works_url = '/all-works/text-list'
#https://www.wikiart.org/en/wassily-kandinsky/all-works/text-list

parser = argparse.ArgumentParser()
parser.add_argument("--out_dir", help="Path to output directory", type=str, default="")
parser.add_argument("--mode", help="If you want to download artist links or get the artwork", type=str, default="artist")

def get_artist_list(url):
    soup = BeautifulSoup(urllib.request.urlopen(url), features="html5lib")
    list_soup = soup.find("div", class_="masonry-text-view masonry-text-view-all")
    li_list = list_soup.find_all('li')
    link_name_list = [(x.a.get('href'), x.a.get_text()) for x in li_list]
    return link_name_list

def get_artwork_list(url):
    try:
        soup = BeautifulSoup(urllib.request.urlopen(url), features="html5lib")
        paintings_list = soup.find_all('li', class_="painting-list-text-row")
        link_painting_name_list = [(x.a.get('href'), x.a.get_text()) for x in paintings_list]
        print(str(len(link_painting_name_list)) + " artwork links found")
    except AttributeError as e:
        print("No artwork found")
        #print("URL: " + str(url))
        #print(e)
        link_painting_name_list = None

    return link_painting_name_list

def get_all_artwork_links(out_dir):
    artists_url = 'https://www.wikiart.org/en/artists-by-genre/abstract/text-list'
    artist_list = get_artist_list(artists_url)
    artist_artwork_dict = {}

    it = 0
    # Iterate artists
    for (artist_url, name) in artist_list:
        time.sleep(random.random())
        print(str(it) + ' artist: ' + name)
        url = base_url + artist_url + all_works_url
        artwork_list = get_artwork_list(url)
        if artwork_list != None:
            artist_artwork_dict[name] = (base_url + artist_url, artwork_list)
        it += 1

    pickle.dump(artist_artwork_dict, open(out_dir + "/" + "artist_artwork_dict.p", "wb"))

def download_artwork(url, artist_name, out_dir):
    print(url)
    soup = BeautifulSoup(urllib.request.urlopen(url), features="html5lib")

    img_soup = soup.find("img", {"itemprop":"image"})
    img_name = img_soup['title']
    img_link = img_soup['src']
    urllib.request.urlretrieve(img_link, out_dir + '/' + artist_name + '_' + img_name + '.jpg')

def download_one_artists_artworks():
    pass

def download_all_artwork(out_dir):

    artist_artwork_dict = pickle.load(open(out_dir + "/" + "artist_artwork_dict.p", "rb"))
    it = 0

    # Iterate all artists in dict
    for name in artist_artwork_dict.keys():
        art_list = artist_artwork_dict[name][1]
        url_artist = artist_artwork_dict[name][0]

        # Create artist dir
        if not os.path.isdir('%s/%s' % (out_dir, name)):
            os.mkdir('%s/%s' % (out_dir, name))

        # Iterate all artworks for artist
        for art_link, art_name in art_list:
            print(str(it) + ' artwork: ' + art_name)
            url = base_url + art_link
            download_artwork(url, name, out_dir)
            it += 1

        del artist_artwork_dict[name]
        pickle.dump(artist_artwork_dict, open("artist_artwork_dict.p", "wb"))


if __name__ == '__main__':
    #get_artist_list('https://www.wikiart.org/en/artists-by-genre/abstract/text-list')
    #artwork_list = get_artwork_list('https://www.wikiart.org/en/wassily-kandinsky/all-works/text-list')
    #download_artwork('https://www.wikiart.org/en/wassily-kandinsky/poster-for-the-abrikosov-company-1898', 'Kdski')

    #print(artwork_list)

    args = parser.parse_args()

    if args.mode == "artist":
        get_all_artwork_links(args.out_dir)
    if args.mode == "artwork":
        download_all_artwork(args.out_dir)