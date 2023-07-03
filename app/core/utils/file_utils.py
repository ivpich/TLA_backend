import os
from fastapi import UploadFile


def save_upload_file(upload_file: UploadFile, directory: str):
    try:
        os.makedirs(directory, exist_ok=True)
    except OSError as error:
        print(f"Error creating directory {directory}: {error}")
        return None

    filename = os.path.join(directory, upload_file.filename)
    with open(filename, "wb+") as file_object:
        file_object.write(upload_file.file.read())
    return filename
