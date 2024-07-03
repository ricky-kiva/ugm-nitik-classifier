import os
import shutil
import re

# Define the source and target directory paths
source_dir = 'Batik Nitik 960 Images'
target_dir = 'Nitik'

# Function to extract item name from the filename, making rotation part optional
def extract_item_name(filename):
    # Adjusted pattern to optionally match rotation information
    # Also handles filenames without rotation part
    match = re.match(r'(\d+)\s+(.*?)\s+(\d+)(?:_rotate_\d+)?', filename)
    if match:
        item_name = match.group(2).strip()  # Trim any leading/trailing spaces from the item name
        return ' '.join(item_name.split())  # Replace multiple spaces with a single space
    return None

# Ensure the target directory exists
os.makedirs(target_dir, exist_ok=True)

# Iterate over each file in the source directory
for filename in os.listdir(source_dir):
    item_name = extract_item_name(filename)
    if item_name:
        # Ensure a directory for this item name exists
        item_dir = os.path.join(target_dir, item_name)
        os.makedirs(item_dir, exist_ok=True)
        
        # Copy the file into the item directory
        src_file = os.path.join(source_dir, filename)
        dst_file = os.path.join(item_dir, filename)
        shutil.copy2(src_file, dst_file)
