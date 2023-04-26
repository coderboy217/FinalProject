import rsa
import os
from Crypto.Cipher import AES
import ga

def generate_aes_key(length):
    # Generate a random AES key
    return os.urandom(length)

def encrypt_aes_key(aes_key, pubkey):
    # Convert the AES key to a string
    aes_key_str = aes_key.hex()

    # Use the genetic algorithm to encrypt the AES key
    ga_algorithm = ga.GeneticAlgorithm(aes_key_str, 0.05, 50)

    # Evolve the genetic algorithm for 100 generations
    for i in range(100):
        ga_algorithm.evolve()

    # Get the best key from the genetic algorithm and convert it to bytes
    best_key_str = ga_algorithm.get_best_key()
    best_key = bytes.fromhex(best_key_str)

    # Use RSA to encrypt the best key
    encrypted_key = rsa.encrypt(best_key, pubkey)

    return encrypted_key

def encrypt_message(message, aes_key):
    # Pad the message so its length is a multiple of 16 bytes
    padded_message = message + b"\0" * (AES.block_size - len(message) % AES.block_size)

    # Create a new AES cipher using the provided key and encrypt the padded message
    cipher = AES.new(aes_key, AES.MODE_ECB)
    encrypted_message = cipher.encrypt(padded_message)

    return encrypted_message

# Generate an RSA key pair
(pubkey, privkey) = rsa.newkeys(2048)

# Get a message from the user
message = input("Enter a message to encrypt: ").encode()

# Generate a random AES key
aes_key = generate_aes_key(16)

# Encrypt the AES key using the genetic algorithm
encrypted_aes_key = encrypt_aes_key(aes_key, pubkey)

# Encrypt the message using the AES key
encrypted_message = encrypt_message(message, aes_key)

print("Encrypted AES key:", encrypted_aes_key)
print("Encrypted message:", encrypted_message)
