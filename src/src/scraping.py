from google_images_download import google_images_download  # importing the library
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import os
import json
from urllib.request import *
import sys
import time
import urllib.request

# adding path to geckodriver to the OS environment variable
os.environ["PATH"] += os.pathsep + os.getcwd()
download_path = "dataset/"


def get_google_full_images():
    response = google_images_download.googleimagesdownload()  # class instantiation

    arguments = {"keywords": "Polar bears,baloons,Beaches",
                 "limit": 2,
                 "print_urls": True,
                 "thumbnail": True}  # creating list of arguments
    paths = response.download(arguments)  # passing the arguments to the function
    print(paths)  # printing absolute paths of the downloaded images


def scroll_down_page(driver, number_of_scrolls):
    print('n scrolls: ' + str(int(number_of_scrolls)))
    for i in range(int(number_of_scrolls)):
        print(i)

        for _ in range(10):
            # multiple scrolls needed to show all 400 images
            driver.execute_script("window.scrollBy(0, 1000)")
            time.sleep(0.5)
        # to load next 400 images
        time.sleep(0.5)
        try:
            #driver.find_element_by_xpath("//input[@value='Show more results']").click()
            driver.find_element_by_xpath("//input[@value='Visa fler resultat']").click()
            #driver.find_element_by_class_name("ksb").click()
        except Exception as e:
            print("Less images found: {}".format(e))
            #break


def scrape_google_thumbnails(query, n_images):

    number_of_scrolls = n_images / 400 + 1
    # number_of_scrolls * 400 images will be opened in the browser

    if not os.path.exists(download_path + query.replace(" ", "_")):
        os.makedirs(download_path + query.replace(" ", "_"))

    url = "https://www.google.co.in/search?q=" + query + "&source=lnms&tbm=isch"
    # driver = webdriver.Firefox()
    driver = webdriver.Safari()
    driver.get(url)

    headers = {}
    headers[
        'User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
    extensions = {"jpg", "jpeg", "png", "gif"}
    img_count = 0
    downloaded_img_count = 0

    scroll_down_page(driver, number_of_scrolls)

    full_dl_path = download_path + query.replace(" ", "_") + "/"
    save_files(full_dl_path, driver)
    driver.close()


def save_files(download_path, driver):
    img_type = "jpg"
    images = driver.find_elements_by_tag_name('img')
    print(images)
    img_count = 0
    failed_img_loads = 0

    for image in images:
        print(image.get_attribute('src'))
        #print(image.get_attribute("class"))

        if image.get_attribute("class") == "rg_ic rg_i":

            try:
                file_path = download_path + str(img_count) + "." + img_type
                urllib.request.urlretrieve(image.get_attribute('src'), file_path)
                img_count += 1

            except TypeError:
                print("Image not done loading")
                failed_img_loads += 1
                #print(image.get_attribute("class"))



    print("Images downloaded: " + str(img_count))
    print("Images not done loading: " + str(failed_img_loads))

if __name__ == '__main__':

    scrape_google_thumbnails('elephant', 100000)

    #get_google_full_images()