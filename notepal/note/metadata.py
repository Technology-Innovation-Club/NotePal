import re
from ninja.files import UploadedFile
from django.utils import timezone


def get_file_type(filename):
    # Define a regular expression pattern to match filename and file type
    pattern = r"^(.*)\.([a-zA-Z0-9]+)$"

    # Use re.match() to find the match
    match = re.match(pattern, filename)

    if match:
        filetype_part = match.group(2)
        return filetype_part
    else:
        return None


def get_file_name(filename):
    # Define a regular expression pattern to match filename and file type
    pattern = r"^(.*)\.([a-zA-Z0-9]+)$"

    # Use re.match() to find the match
    match = re.match(pattern, filename)

    if match:
        filename_part = match.group(1)
        return filename_part
    else:
        return None


def get_metadata(file: UploadedFile):
    metadata = {}
    metadata["file_name"] = get_file_name(file.name)
    metadata["file_size"] = file.size
    metadata["file_type"] = get_file_type(file.name)
    metadata["date_created"] = timezone.now().isoformat()
    metadata["date_modified"] = timezone.now().isoformat()
    return metadata
