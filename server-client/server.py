import socket

s = socket.socket()
print('socket successfully created')
port = 12345
s.bind(('',port))
print(f'socket binded to port{port}')
s.listen(5)
print('socket is listening')
while True:
    c, addr = s.accept()
    print('got connection from', addr)
    message = ('Thank you for connecting')
    c.send(message.encode())
    c.close
