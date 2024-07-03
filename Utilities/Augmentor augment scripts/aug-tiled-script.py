import os
import shutil
import random
import Augmentor
from PIL import Image
from tqdm import tqdm
import time

def create_2x2_tile(image_path):
    original_image = Image.open(image_path) # open the image using PIL
    resized_image = original_image.resize((original_image.width // 2, original_image.height // 2)) # resize the image to `1/4` of the image
    new_image = Image.new('RGB', original_image.size) # make new blank canvas of Image
    for i in range(2):
        for j in range(2):
            new_image.paste(resized_image, (i * resized_image.width, j * resized_image.height)) # paste the resized image as tiles in the blank canvas of Image
    return new_image

def augment_images(parent_directory):
    class_directories = [os.path.join(parent_directory, d) 
                         for d in os.listdir(parent_directory) 
                         if os.path.isdir(os.path.join(parent_directory, d))]
    
    for class_dir in class_directories:
        print(f"Processing {class_dir}...")
        
        # Step 1: Create 2x2 tiles for all images in the class directory and save them
        images = [f for f in os.listdir(class_dir) 
                  if os.path.isfile(os.path.join(class_dir, f)) 
                  and f.lower().endswith(('png', 'jpg', 'jpeg'))] # make list of image within the class directory 

        for image_name in tqdm(images, desc="Creating 2x2 tiles"): # loop and show progress with tqdm
            image_path = os.path.join(class_dir, image_name) # getting full image path
            tiled_image = create_2x2_tile(image_path) # make tiled image for the specified image
            tiled_image_path = os.path.splitext(image_path)[0] + '_tiled' + os.path.splitext(image_path)[1] # rename the tiled image
            tiled_image.save(tiled_image_path) # save the tiled image
        
        # Step 2: Rescan the directory to include both original and newly created tiled images
        updated_images = [f for f in os.listdir(class_dir) if os.path.isfile(os.path.join(class_dir, f)) and f.lower().endswith(('png', 'jpg', 'jpeg'))]

        # Initialize Augmentor Pipeline for each class directory
        p = Augmentor.Pipeline(class_dir)
        
        # Step 3: Apply augmentations to all images (original + tiled)
        for image_name in tqdm(updated_images, desc="Augmenting images"):
            augmentations = [
                lambda p: p.skew(probability=1, magnitude=0.6),
                lambda p: p.skew_corner(probability=1, magnitude=0.8),
                lambda p: p.random_distortion(probability=1, grid_width=10, grid_height=10, magnitude=8),
                lambda p: p.rotate(probability=1, max_left_rotation=15, max_right_rotation=15),
                lambda p: p.shear(probability=1, max_shear_left=15, max_shear_right=15),
            ] # create list of augmentor functions
            
            # combine crop & resize augmentor
            def crop_and_resize(p):
                p.crop_random(probability=1, percentage_area=random.uniform(0.6, 0.8))
                p.resize(probability=1, width=512, height=512)

            # execute data augmentation in `augmentations` list 1 by 1
            for augmentation in augmentations:
                augmentation(p)
                p.sample(1)
                
            # execute data augmentation with `crop_and_resize` function
            crop_and_resize(p)
            p.sample(1)

            p.operations = [] # removes previous operations added to the Augmentor pipeline

        # move all augmented images in `output` directory to the class's directory
        output_dir = os.path.join(class_dir, "output")
        for file in os.listdir(output_dir):
            shutil.move(os.path.join(output_dir, file), class_dir)
        
        os.rmdir(output_dir) # delete `output` directory

        print(f"Finished processing {class_dir}.")

if __name__ == "__main__":
    start_time = time.time()
    parent_directory = 'Nitik960'
    augment_images(parent_directory)
    elapsed_time = time.time() - start_time
    print(f"Total processing time: {elapsed_time:.2f} seconds")
