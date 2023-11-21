import socket
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

def pad(data):
    length = 8 - (len(data) % 8)
    return data + bytes([length] * length)

def encrypt_message(message, key):
    cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    padded_message = pad(message)
    encrypted_message = encryptor.update(padded_message) + encryptor.finalize()
    return encrypted_message

def decrypt_message(encrypted_message, key):
    cipher = Cipher(algorithms.TripleDES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_message = decryptor.update(encrypted_message) + decryptor.finalize()
    return decrypted_message

def client_program():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('127.0.0.1', 12345))

    # Menggunakan kunci acak dengan panjang 24 byte (192 bit) untuk 3DES
    key = os.urandom(24)
    client_socket.send(key)

    while True:
        message = input('Enter message for server: ')
        encrypted_message = encrypt_message(message.encode(), key)
        client_socket.send(encrypted_message)

        encrypted_response = client_socket.recv(1024)
        decrypted_response = decrypt_message(encrypted_response, key)
        print('Received from server:', decrypted_response.decode())

    client_socket.close()

if __name__ == "__main__":
    client_program()
