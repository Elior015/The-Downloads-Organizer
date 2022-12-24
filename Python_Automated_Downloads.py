import os



os.listdir()
os.scandir()

source_dir = "PATH_TO_DOWNLOADS_FOLDER"

with os.scandir(source_dir) as entries:
    for entry in entries:
        print(entry.name)