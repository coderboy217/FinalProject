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
    # Generate a new Initialization Vector (IV) for CBC mode
    iv = os.urandom(AES.block_size)

    # Create a new AES cipher using the provided key and IV, and encrypt the padded message
    cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)
    encrypted_message = cipher.encrypt(_pad(message))

    # Include the IV in the encrypted message to enable proper decryption
    encrypted_message = iv + encrypted_message

    return encrypted_message


def decrypt_message(encrypted_message, aes_key):
    # Get the IV from the encrypted message
    iv = encrypted_message[:AES.block_size]

    # Create a new AES cipher using the provided key and IV, and decrypt the encrypted message
    cipher = AES.new(aes_key, AES.MODE_CBC, iv=iv)
    decrypted_message = cipher.decrypt(encrypted_message[AES.block_size:])

    # Remove the padding from the decrypted message
    unpadded_message = _unpad(decrypted_message)

    return unpadded_message


def _pad(s):
    # Pad the message so its length is a multiple of 16 bytes
    padding_size = AES.block_size - len(s) % AES.block_size
    padding = bytes([padding_size] * padding_size)
    return s + padding


def _unpad(s):
    # Remove the padding from the decrypted message
    padding_size = s[-1]
    return s[:-padding_size]


# Generate an RSA key pair
(pubkey, privkey) = rsa.newkeys(2048)

# Generate a random AES key
aes_key = generate_aes_key(16)

# Encrypt the AES key using the genetic algorithm
encrypted_aes_key = encrypt_aes_key(aes_key, pubkey)

# Read plaintext message from file
with open('message.txt', 'rb') as f:
    plaintext_message = f.read()

# Encrypt the message using the AES key
encrypted_message = encrypt_message(plaintext_message, aes_key)

# Decrypt the message using the AES key
decrypted_message = decrypt_message(encrypted_message, aes_key)

# Print the results
print("Encrypted AES key:", encrypted_aes_key)
print("Plaintext message:", plaintext_message)
print("Encrypted message:", encrypted_message)
print("Decrypted message:", decrypted_message)
