import os
import shutil
from sys import argv

# Specify the directory
category = argv[1]
directory = f"amazon_{category}_review"

# Define the folders to keep
folders_to_keep = ["data", "pic"]

# Get a list of all items in the directory
items = os.listdir(directory)

# Iterate over the items and delete the unwanted ones
for item in items:
    item_path = os.path.join(directory, item)
    if os.path.isfile(item_path):
        os.remove(item_path)
    elif os.path.isdir(item_path) and item not in folders_to_keep:
        shutil.rmtree(item_path)