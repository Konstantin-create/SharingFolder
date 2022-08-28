import os
import hashlib


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


def get_file_hashes(working_dir: str) -> list:
    """Function to get file hashes"""

    output = []

    files = get_all_files(working_dir)
    for file in files:
        filename_hash = generate_hash(file.encode())
        file_data_hash = generate_hash(open(f'{working_dir}/{file}', 'rb').read())
        output.append({file: [filename_hash, file_data_hash]})
    return output


print(get_file_hashes('/home/hacknet/Kostua/Flask/hacknet_web'))
