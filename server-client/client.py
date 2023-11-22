from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import socket

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

    # Terima kunci dari server
    server_key = client_socket.recv(24)

    while True:
        encrypted_message = client_socket.recv(1024)
        decrypted_message = decrypt_message(encrypted_message, server_key)
        print('Received from server:', decrypted_message.decode())

        message = input('Enter message for server: ')
        encrypted_response = encrypt_message(message.encode(), server_key)
        client_socket.send(encrypted_response)

        if message.lower() == 'exit':
            break

    client_socket.close()

if __name__ == "__main__":
    client_program()
