## Description: This script will transfer files from the downloads folder to the relevant folders according to the file type
from os import scandir, rename
from os.path import splitext, exists, join
from shutil import move
from time import sleep

import logging

## The watchdog module is used to monitor file system changes
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


# ! FILL IN THE PATHS TO THE FOLDERS
download_dir = "PATH_TO_DOWNLOADS_FOLDER"
dest_dir_softwares = "PATH_TO_SOFTWARES_FOLDER"
dest_dir_video = "PATH_TO_VIDEOS_FOLDER"
dest_dir_image = "PATH_TO_IMAGES_FOLDER"
dest_dir_documents = "PATH_TO_DOCUMENTS_FOLDER"

## Image types
image_extensions = [".jpg", ".jpeg", ".jpe", ".jif", ".jfif", ".jfi", ".png", ".gif", ".webp", ".tiff", ".tif", ".psd", ".raw", ".arw", ".cr2", ".nrw",
                    ".k25", ".bmp", ".dib", ".heif", ".heic", ".ind", ".indd", ".indt", ".jp2", ".j2k", ".jpf", ".jpf", ".jpx", ".jpm", ".mj2", ".svg", ".svgz", ".ai", ".eps", ".ico"]
## Video types
video_extensions = [".webm", ".mpg", ".mp2", ".mpeg", ".mpe", ".mpv", ".ogg",
                    ".mp4", ".mp4v", ".m4v", ".avi", ".wmv", ".mov", ".qt", ".flv", ".swf", ".avchd"]
## Software types
softwares_extensions = [".dmg", ".pkg", "zip", ".bin", ".app", ".aae" ".cnf", ".exe", ".msi"]

## Document types
document_extensions = [".doc", ".docx", ".odt",
                       ".pdf", ".xls", ".xlsx", ".ppt", ".pptx"]

## This function will make a change to the file name if the file already exists in the destination folder
def make_a_change(dest, name):
    filename, extension = splitext(name)
    counter = 1
    ## This loop will keep running until the file name is unique
    while exists(f"{dest}/{name}"):
        name = f"{filename}({str(counter)}){extension}"
        counter += 1

    return name

## This function will move the file to the relevant folder
def move_file_func(dest, entry, name):
    if exists(f"{dest}/{name}"):
        unique_name = make_a_change(dest, name)
        oldName = join(dest, name)
        newName = join(dest, unique_name)
        rename(oldName, newName)
    move(entry, dest)


class MoverManger(FileSystemEventHandler):
    ## This function will be called when a file is created in the download folder
    def on_modified(self, event):
        with scandir(download_dir) as entries:
            for entry in entries:
                name = entry.name
                self.check_if_its_softwares_files(entry, name)
                self.check_if_its_video_files(entry, name)
                self.check_if_its_image_files(entry, name)
                self.check_if_its_document_files(entry, name)

    ## This function will check if the file is a software file
    def check_if_its_softwares_files(self, entry, name):  
        for softwares_extension in softwares_extensions:
            if name.endswith(softwares_extension) or name.endswith(softwares_extension.upper()):
                dest = dest_dir_softwares
                move_file_func(dest, entry, name)
                logging.info(f"Moved software file: {name}")

    ## This function will check if the file is a video file
    def check_if_its_video_files(self, entry, name):  
        for video_extension in video_extensions:
            if name.endswith(video_extension) or name.endswith(video_extension.upper()):
                move_file_func(dest_dir_video, entry, name)
                logging.info(f"Moved video file: {name}")

    ## This function will check if the file is a image file
    def check_if_its_image_files(self, entry, name):  
        for image_extension in image_extensions:
            if name.endswith(image_extension) or name.endswith(image_extension.upper()):
                move_file_func(dest_dir_image, entry, name)
                logging.info(f"Moved image file: {name}")

    ## This function will check if the file is a document file
    def check_if_its_document_files(self, entry, name):  
        for documents_extension in document_extensions:
            if name.endswith(documents_extension) or name.endswith(documents_extension.upper()):
                move_file_func(dest_dir_documents, entry, name)
                logging.info(f"Moved document file: {name}")


# ! DO NOT CHANGE BELOW CODE
if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')
    path = download_dir
    event_handler = MoverManger()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        while True:
            sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()