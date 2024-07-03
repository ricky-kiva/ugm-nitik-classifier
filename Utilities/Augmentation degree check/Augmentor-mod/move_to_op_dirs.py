import os
import shutil

operations = [
    'skew',
    'skew_corner',
    'random_distortion',
    'rotate',
    'shear',
    'crop_resize'
]

def process_directories(root_dir):
    # List all first-layer directories in the root directory
    layer_1_dirs = [d for d in os.listdir(root_dir) if os.path.isdir(os.path.join(root_dir, d))]

    for layer_1_dir in layer_1_dirs:
        layer_1_path = os.path.join(root_dir, layer_1_dir)
        output_path = os.path.join(layer_1_path, 'output')
        
        if os.path.exists(output_path):
            layer_2_dirs = [d for d in os.listdir(output_path) if os.path.isdir(os.path.join(output_path, d))]
            
            for layer_2_dir in layer_2_dirs:
                layer_2_path = os.path.join(output_path, layer_2_dir)
                
                # Process each image file in the second-layer directory
                for file_name in os.listdir(layer_2_path):
                    file_path = os.path.join(layer_2_path, file_name)
                    
                    # Check if the file name starts with any operation name
                    for operation in operations:
                        if file_name.startswith(operation):
                            # Ensure the operation directory exists in the root directory
                            operation_dir = os.path.join(root_dir, operation)
                            if not os.path.exists(operation_dir):
                                os.makedirs(operation_dir)
                            
                            # Determine the new file name by removing the suffix after "_original" and appending ".jpg"
                            base_name = file_name.split('_original')[0]
                            new_file_name = base_name + ".jpg"
                            new_file_path = os.path.join(operation_dir, new_file_name)
                            
                            # Copy the file to the operation directory with the new name
                            shutil.copy(file_path, new_file_path)
                            print(f"Copied {file_path} to {new_file_path}")
                            break
            
            # After processing and copying, delete the first-layer directory
            shutil.rmtree(layer_1_path)
            print(f"Deleted {layer_1_path}")

if __name__ == "__main__":
    root_directory = os.getcwd()  # Set this to the root directory path
    process_directories(root_directory)
