import os.path
import hashlib


def is_folder_exists(working_dir: str, folder_name: str) -> bool:
    """Function to check is folder to connect exists in local storage or not"""

    return os.path.exists(f'{working_dir}/{folder_name}')


def generate_hash(data: bytes) -> str:
    """Function to generate sha256 hash"""

    return hashlib.sha256(data).hexdigest()


def get_all_files(working_dir: str) -> list:
    """Get all files from working_dir"""

    output = []

    for root, dirs, files in os.walk(working_dir):
        for file in files:
            output.append(f'{root}/{file}'.replace(working_dir, ''))

    return output


def get_file_hashes(working_dir: str, folder_name: str) -> list:
    """Function to get file hashes"""

    if is_folder_exists(working_dir, folder_name):
        return []

    output = []
    files = get_all_files(f'{working_dir}/{folder_name}')
    for file in files:
        filename_hash = generate_hash(file.encode())
        file_data_hash = generate_hash(open(f'{working_dir}/{folder_name}/{file}', 'rb').read())
        output.append({file: [filename_hash, file_data_hash]})
    return output
