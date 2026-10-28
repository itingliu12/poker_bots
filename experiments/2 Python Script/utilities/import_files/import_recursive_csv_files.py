import pandas as pd
import pathlib

# recursive inmporting csv


def import_recursive_csv_files(directory):
    csv_files = {}
    for file in pathlib.Path(directory).rglob("*.csv"):
        file_name = file.stem
        csv_files[file_name] = pd.read_csv(file)
    return csv_files
