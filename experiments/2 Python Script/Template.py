############################
# Original Author: Peter Liu
# Purpose:


#######################################################
# Importing Packages
import requests
import pandas as pd
import numpy as np
import os
import pathlib

# Reference: https://arrow.apache.org/docs/python/feather.html
import pyarrow.feather as feather

# User Define Functions
from utilities.import_files.import_recursive_csv_files import import_recursive_csv_files
from utilities.import_files.import_recursive_files import import_recursive_files


#######################################################
# User define functions
# recursive inmporting csv
def import_recursive_csv_files(directory):
    csv_files = {}
    for file in pathlib.Path(directory).rglob("*.csv"):
        file_name = file.stem
        csv_files[file_name] = pd.read_csv(file)
    return csv_files


# recursive inmporting file
def import_recursive_files(directory, file_extensions=["csv"]):
    # Loading the files list
    files = {}

    # Ensure file_extensions is a list
    if isinstance(file_extensions, str):
        file_extensions = [file_extensions]

    # Create pattern for globbing
    patterns = [f"*.{ext.strip('.')}" for ext in file_extensions]

    print(patterns)

    for pattern in patterns:
        for file in pathlib.Path(directory).rglob(pattern):
            # Use the full path as the key to avoid overwriting
            file_name = file.stem
            print(file_name)
            ext = pattern
            # Use appropriate loader based on extension
            try:
                if ext == "*.csv":
                    files[file_name] = pd.read_csv(file)
                elif ext == "*.feather":
                    files[file_name] = feather.read_feather(file)
                elif ext == "*.xlsx":
                    files[file_name] = pd.read_excel(file, sheet_name=None)
                else:
                    print(f"Warning: Could not load {file} with default CSV loader")
            except Exception as e:
                print(f"Error loading {file}: {str(e)}")

    return files


#######################################################
# Current directory
current_dir = os.getcwd()
parent_dir = os.path.dirname(current_dir)


########################################################
# Input folder
folder_name = os.path.join(parent_dir, "1 Input Files")

# Single File
df = pd.read_csv(folder_name + "\\XXXXNAMEXXX.csv")
df = feather.read_feather(folder_name + "\\XXXXNAMEXXXX.feather")

# Recursive Reading Files
# Read CSV Files
csv_files = import_recursive_csv_files(folder_name)
files = import_recursive_files(folder_name, ["feather", "csv"])
# Read feather Files


#######################################################
# Operations


############## Intermediate data ###############
folder_name = os.path.join(parent_dir, "2.1 Intermediate Files")

name = ""
filename = f"{folder_name}\\{name}.csv"

# write the file into the folder
# dataframe.to_csv(filename,sep= ';',index=False)

# read the file from the folder
# df = pd.read_csv(filename, sep = ';')

############### Output data ###################
folder_name = os.path.join(parent_dir, "3 Output Files")

name = ""
filename = f"{folder_name}\\{name}.csv"

# write the file into the folder
# dataframe.to_csv(filename,sep= ';',index=False)

# read the file from the folder
# df = pd.read_csv(filename, sep = ';')

############## Results ########################
folder_name = os.path.join(parent_dir, "4 Results")

name = ""
filename = f"{folder_name}\\{name}.csv"

# write the file into the folder
# dataframe.to_csv(filename,sep= ';',index=False)

# read the file from the folder
# df = pd.read_csv(filename, sep = ';')


############## Shared ########################
folder_name = os.path.join(parent_dir, "5 Shared")

name = ""
filename = f"{folder_name}\\{name}.csv"

# write the file into the folder
# dataframe.to_csv(filename,sep= ';',index=False)

# read the file from the folder
# df = pd.read_csv(filename, sep = ';')
