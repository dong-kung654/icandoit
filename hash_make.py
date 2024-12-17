import hashlib
import os
import json

def calculate_file_hash(file_path):
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as file:
        for byte_block in iter(lambda: file.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def generate_hashes_for_directory(directory_path):
    all_file_hashes = []
    for root, dirs, files in os.walk(directory_path):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_hash = calculate_file_hash(file_path)
            file_data = {
                "file_name": file_name,
                "file_path": file_path,
                "sha256_hash": file_hash
            }
            all_file_hashes.append(file_data)
    
    return all_file_hashes

def save_hashes_to_json(directory_path, json_file):
    hashes = generate_hashes_for_directory(directory_path)
    with open(json_file, "w") as json_output:
        json.dump(hashes, json_output, indent=4)
