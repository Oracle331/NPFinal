# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 10:30:08 2019
Chat client
@author: Anthony Salaris, Andrew Galvin, Endi Caushie 
"""

import socket
def client_program():
    host = socket.gethostname()
    port = 5089
    client_socket = socket.socket()
    client_socket.connect((host, port))
    #address = client_socket
    print('Connecting to: ' + socket.gethostbyname(host))
    message = input(" -> ")
    while message.lower().strip() != 'disconnect':
        client_socket.send(message.encode())
        data = client_socket.recv(1024).decode()
        if data == "disconnect":
            print('Host disconnected')
            break
        print('Host: ' + data)
        message = input(" -> ")
    client_socket.close()
if __name__ == '__main__':
    client_program()
