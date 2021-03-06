import cv2
import os
from PIL import Image
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
import glob

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('--input_folder', help='input folder')
parser.add_argument('--out_folder', help='output folder')
parser.add_argument('--img_size', help='image pixel size', type=int)
param = parser.parse_args()


def facecrop(image, out_im_dir):
    facedata = "haarcascade_frontalface_alt.xml"
    #https://github.com/opencv/opencv/tree/master/data/haarcascades
    cascade = cv2.CascadeClassifier(facedata)

    img = cv2.imread(image)

    minisize = (img.shape[1],img.shape[0])
    miniframe = cv2.resize(img, minisize)

    faces = cascade.detectMultiScale(miniframe)

    for f in faces:
        x, y, w, h = [ v for v in f ]
        cv2.rectangle(img, (x,y), (x+w,y+h), (255,255,255))

        sub_face = img[y:y+h, x:x+w]
        fname, ext = os.path.splitext(image)
        cv2.imwrite(out_im_dir, sub_face)

    return None

#facecrop('../../data/my_face/me_with_others/UNADJUSTEDNONRAW_thumb_c98.jpg', '../../data/my_face/me_with_others/UNADJUSTEDNONRAW_thumb_c98__.jpg')

def facecrop_all_in_folder(im_dir_path, out_dir_path):

    it = 0

    for filename in os.listdir(im_dir_path):
        if filename.endswith(".jpg"):

            print(str(it) + ': ' + filename)

            image_dir = im_dir_path + '/' + filename
            out_im_dir = out_dir_path + '/' + filename

            facecrop(image_dir, out_im_dir)

            it += 1

#facecrop_all_in_folder('../../data/my_face/me_with_others', '../../data/my_face/faces_1')

def crop_image(original):
    width, height = original.size

    if width == height:
        return original

    # The shortest side length
    min_side = min(width, height)

    # Get the width values
    excess_width = (width - min_side) / 2.
    left = excess_width
    right = left + min_side

    # Get height values
    excess_height = (height - min_side) / 2.
    top = excess_height
    bottom = top + min_side

    cropped_img = original.crop((left, top, right, bottom))

    return cropped_img


def scale_images(in_dir, out_dir, file_type_str, img_size=(256,256)):
    it = 0
    for filepath in glob.iglob(in_dir + '/*' + file_type_str):
        # print(filepath)

        try:
            img = Image.open(filepath)
            # img.crop((0, 0, img_width, img_height)).save(out_dir+'/'+str(it)+file_type_str)
            img = crop_image(img)
            img.resize(img_size, Image.ANTIALIAS).save(out_dir + '/' + str(it) + file_type_str)
            it += 1
        except OSError as e:
            print(e)

#scale_images('../../data/my_face/faces_1', '../../data/my_face/faces_1_scaled', '.jpg')

def scale_images_in_folders(in_dir, out_dir, img_size=256):
    print(in_dir)
    # Iterate all artist folders
    for filepath in glob.iglob(in_dir + '/*'):
        print(filepath)
        artist = filepath.split('/')[-1]

        # Check that file is a directory
        if os.path.isdir(filepath):

            # Create folder in target dir
            if not os.path.isdir(out_dir + '/' + artist):
                os.mkdir(out_dir + '/' + artist)

            # Scale images in dir
            scale_images(filepath, out_dir + '/' + artist, '.jpg', (img_size, img_size))

if __name__ == '__main__':

    #scale_images('../../data/elephants/original', '../../data/elephants/scaled', '.jpg')
    scale_images_in_folders(param.input_folder, param.out_folder, param.img_size)
    #scale_images(param.input_folder, param.out_folder, '.jpg')
