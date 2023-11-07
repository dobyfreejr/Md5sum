import hashlib
import os

def generate_hash(file_path, algorithm='sha256'):
    """Generate a hash for the given file using the specified algorithm."""
    hasher = hashlib.new(algorithm)
    with open(file_path, 'rb') as file:
        while True:
            data = file.read(65536)
            if not data:
                break
            hasher.update(data)
    return hasher.hexdigest()

def calculate_hash_sum(directory_path, algorithm='sha256'):
    """Calculate the sum of hash values for all files in the specified directory."""
    hash_sum = 0
    for root, _, files in os.walk(directory_path):
        for file in files:
            file_path = os.path.join(root, file)
            file_hash = generate_hash(file_path, algorithm)
            hash_sum += int(file_hash, 16)  # Convert hexadecimal hash to integer

    return hex(hash_sum).rstrip('L')

if __name__ == "__main__":
    directory_path = 'path_to_directory'  # Replace with the path to your directory
    stored_hash_sum = 'your_stored_hash_sum'  # Replace with the previously computed hash sum

    calculated_hash_sum = calculate_hash_sum(directory_path)

    if calculated_hash_sum == stored_hash_sum:
        print("The hash sum of all files in the directory matches the stored hash sum. No tampering detected.")
    else:
        print("The hash sum of files in the directory doesn't match the stored hash sum. Tampering may have occurred.")
