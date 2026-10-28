import pathlib
import pandas as pd
import pyarrow.feather as feather


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
