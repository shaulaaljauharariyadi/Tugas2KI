from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import socket
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

def server_program():
    # Tentukan kunci secara statis di sini
    static_key = b'StaticKey12345678'

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('', 12345))
    server_socket.listen(5)

    print("Server listening...")

    while True:
        client_socket, addr = server_socket.accept()
        print('Got connection from', addr)

        # Kirim kunci statis ke klien
        client_socket.send(static_key)

        while True:
            message = input('Enter message for client: ')
            encrypted_message = encrypt_message(message.encode(), static_key)
            client_socket.send(encrypted_message)

            if message.lower() == 'exit':
                break

            encrypted_response = client_socket.recv(1024)
            decrypted_response = decrypt_message(encrypted_response, static_key)
            print('Received from client:', decrypted_response.decode())

        client_socket.close()

if __name__ == "__main__":
    server_program()
