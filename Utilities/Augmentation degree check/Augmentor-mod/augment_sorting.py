import Augmentor
import os
from shutil import copyfile

# Define constants
constants = {
    'skew': {'min': 0.2, 'max': 1, 'step': 0.2},
    'skew_corner': {'min': 0.2, 'max': 1, 'step': 0.2},
    'random_distortion': {'grid_min': 4, 'grid_max': 10, 'grid_step': 2, 'magnitude_min': 2, 'magnitude_max': 10, 'magnitude_step': 2},
    'rotate': {'min': 5, 'max': 25, 'step': 5},
    'shear': {'min': 5, 'max': 25, 'step': 5},
    'crop_resize': {'min': 0.2, 'max': 0.8, 'step': 0.2}
}

# Function to apply crop and resize
def crop_and_resize(p, percentage_area):
    p.crop_random(probability=1, percentage_area=percentage_area, randomise_percentage_area=False)
    p.resize(probability=1, width=512, height=512)

# Helper function to generate a range of floating point numbers
def frange(start, stop, step):
    while start <= stop:
        yield round(start, 2)
        start += step

# Function to create augmentor pipelines for each operation
def create_pipelines(img_path):
    # Ensure the image exists
    if not os.path.isfile(img_path):
        raise FileNotFoundError(f"The image {img_path} does not exist.")
    
    # Create output directories if they do not exist
    output_base_dir = "output"
    if not os.path.exists(output_base_dir):
        os.makedirs(output_base_dir)

    # Copy test image to output directories
    for operation in constants:
        if operation == "random_distortion":
            for grid_size in range(constants[operation]['grid_min'], constants[operation]['grid_max']+1, constants[operation]['grid_step']):
                for magnitude in frange(constants[operation]['magnitude_min'], constants[operation]['magnitude_max'], constants[operation]['magnitude_step']):
                    output_dir = os.path.join(output_base_dir, f"{operation}_{grid_size}_{magnitude}")
                    if not os.path.exists(output_dir):
                        os.makedirs(output_dir)
                    copyfile(img_path, os.path.join(output_dir, os.path.basename(img_path)))
        else:
            for magnitude in frange(constants[operation]['min'], constants[operation]['max'], constants[operation]['step']):
                output_dir = os.path.join(output_base_dir, f"{operation}_{magnitude}")
                if not os.path.exists(output_dir):
                    os.makedirs(output_dir)
                copyfile(img_path, os.path.join(output_dir, os.path.basename(img_path)))

    # Skew
    for skew_magnitude in frange(constants['skew']['min'], constants['skew']['max'], constants['skew']['step']):
        output_dir = os.path.join(output_base_dir, f"skew_{skew_magnitude}")
        p = Augmentor.Pipeline(source_directory=output_dir, output_directory=output_dir)
        p.skew(probability=1, magnitude=skew_magnitude)
        p.sample(1)
    
    # Skew Corner
    for skew_corner_magnitude in frange(constants['skew_corner']['min'], constants['skew_corner']['max'], constants['skew_corner']['step']):
        output_dir = os.path.join(output_base_dir, f"skew_corner_{skew_corner_magnitude}")
        p = Augmentor.Pipeline(source_directory=output_dir, output_directory=output_dir)
        p.skew_corner(probability=1, magnitude=skew_corner_magnitude)
        p.sample(1)

    # Random Distortion
    for grid_size in range(constants['random_distortion']['grid_min'], constants['random_distortion']['grid_max']+1, constants['random_distortion']['grid_step']):
        for magnitude in frange(constants['random_distortion']['magnitude_min'], constants['random_distortion']['magnitude_max'], constants['random_distortion']['magnitude_step']):
            output_dir = os.path.join(output_base_dir, f"random_distortion_{grid_size}_{magnitude}")
            p = Augmentor.Pipeline(source_directory=output_dir, output_directory=output_dir)
            p.random_distortion(probability=1, grid_width=grid_size, grid_height=grid_size, magnitude=magnitude)
            p.sample(1)

    # Rotate
    for max_left_rotation in range(constants['rotate']['min'], constants['rotate']['max']+1, constants['rotate']['step']):
        output_dir = os.path.join(output_base_dir, f"rotate_{max_left_rotation}")
        p = Augmentor.Pipeline(source_directory=output_dir, output_directory=output_dir)
        p.rotate(probability=1, max_left_rotation=max_left_rotation, max_right_rotation=max_left_rotation)
        p.sample(1)

    # Shear
    for shear_magnitude in range(constants['shear']['min'], constants['shear']['max']+1, constants['shear']['step']):
        output_dir = os.path.join(output_base_dir, f"shear_{shear_magnitude}")
        p = Augmentor.Pipeline(source_directory=output_dir, output_directory=output_dir)
        p.shear(probability=1, max_shear_left=shear_magnitude, max_shear_right=shear_magnitude)
        p.sample(1)

    # Crop and Resize
    for percentage_area in frange(constants['crop_resize']['min'], constants['crop_resize']['max'], constants['crop_resize']['step']):
        output_dir = os.path.join(output_base_dir, f"crop_resize_{percentage_area}")
        p = Augmentor.Pipeline(source_directory=output_dir, output_directory=output_dir)
        crop_and_resize(p, percentage_area)
        p.sample(1)

if __name__ == "__main__":
    create_pipelines('input_image.jpg')