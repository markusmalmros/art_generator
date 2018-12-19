import Augmentor
import argparse
import random
import glob
from PIL import Image

def flatten_RGBA(in_dir, out_dir, file_type_str):
    it = 0
    for filepath in glob.iglob(in_dir + '/*' + file_type_str):
        # print(filepath)
        if it % 200 == 0:
            print(it)
            
        try:
            img = Image.open(filepath)
            img = img.convert("RGB")
            img.save(out_dir + '/' + str(it) + file_type_str)

            it += 1
        except OSError as e:
            print(e)
            
            
            
def augment(p, n_samples):
    p.flip_left_right(probability=0.5)
    
    def rot_func():
        p.rotate(probability=1, max_left_rotation=20, max_right_rotation=20)
        
    def crop_func():
        p.crop_random(probability=1, percentage_area=0.7)
        
    def skew_func():
        p.skew(probability=1)
    
    #Run one of the augmentation functions
    random.choice([rot_func, crop_func, skew_func])()
    
    p.sample(n_samples)
    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--img_dir", help="Path to image directory", type=str)
    parser.add_argument("--out_dir", help="Path to output directory", type=str)
    parser.add_argument("--n_samples", help="Amount of images to generate", type=int)
    args = parser.parse_args()
    
    p = Augmentor.Pipeline(args.img_dir, output_directory=args.out_dir, save_format="jpg")
    
    
    augment(p, args.n_samples)
    
# Usage example
# python augment_dataset.py --img_dir=/home/markus/Desktop/art_generator/data/abstract_art/color_same_dir --out_dir=/home/markus/Desktop/art_generator/data/abstract_art/color_augmented/orig_size --n_samples=100 --res=256
