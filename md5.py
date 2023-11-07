import os
import hashlib

def calculate_hash(file_path, hash_algorithm):
    """Calculate the hash sum of a file."""
    try:
        hasher = hashlib.new(hash_algorithm)
        with open(file_path, "rb") as file:
            while True:
                data = file.read(65536)  # Read in 64k chunks
                if not data:
                    break
                hasher.update(data)
        return hasher.hexdigest()
    except Exception as e:
        return f"Error: {str(e)} (File: {file_path})"

def hash_files_in_directory(directory, hash_algorithm):
    """Calculate hash sums for all files in a directory."""
    hash_sums = {}
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            file_hash = calculate_hash(file_path, hash_algorithm)
            hash_sums[file_path] = file_hash
    return hash_sums

if __name__ == "__main__":
    directory = "/"  # Use '/' to start from the root directory
    hash_algorithm = "md5"  # You can use "md5", "sha1", "sha256", etc.

    hash_sums = hash_files_in_directory(directory, hash_algorithm)

    output_directory = "/home/sysadmin/Md5sum"
    os.makedirs(output_directory, exist_ok=True)

    output_file = os.path.join(output_directory, f"{hash_algorithm}_hashes.txt")

    with open(output_file, "w") as output:
        for file_path, file_hash in hash_sums.items():
            output.write(f"{file_path}: {file_hash}\n")

    print(f"Hashes saved to {output_file}")
