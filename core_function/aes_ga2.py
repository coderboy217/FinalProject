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
    iv = os.urandom(AES.block_size)  # Generate a random initialization vector
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    encrypted_message = cipher.encrypt(padded_message)

    return iv + encrypted_message


def decrypt_message(encrypted_message, aes_key):
    # Split the initialization vector and encrypted message
    iv = encrypted_message[:AES.block_size]
    encrypted_data = encrypted_message[AES.block_size:]

    # Create a new AES cipher using the provided key and initialization vector, and decrypt the encrypted message
    cipher = AES.new(aes_key, AES.MODE_CBC, iv)
    decrypted_data = cipher.decrypt(encrypted_data)

    # Remove the padding from the decrypted data
    unpadded_data = decrypted_data.rstrip(b"\0")

    return unpadded_data


# Generate an RSA key pair
(pubkey, privkey) = rsa.newkeys(2048)

# Get the message from the user
message = input("Enter a message to encrypt: ").encode()

# Generate a random AES key
aes_key = generate_aes_key(16)

# Encrypt the AES key using the genetic algorithm
encrypted_aes_key = encrypt_aes_key(aes_key, pubkey)

# Encrypt the message using the AES key
encrypted_message = encrypt_message(message, aes_key)

# Decrypt the message using the AES key
decrypted_message = decrypt_message(encrypted_message, aes_key)

print("Encrypted AES key:", encrypted_aes_key)
print("Encrypted message:", encrypted_message)
print("Decrypted message:", decrypted_message.decode())
