# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 10:30:08 2019
Chat server
@author: Anthony Salaris, Andrew Galvin, Endi Caushie 
"""
import socket

def server_program():
    host = socket.gethostname()
    port = 5089
    server_socket = socket.socket()
    server_socket.bind((host,port))
    server_socket.listen(2)
    while True:
        conn, address = server_socket.accept()
        print("Connection from: " + str(address))
        message = "Waiting for message from user"
        while message.lower().strip() != 'disconnect':
            data = conn.recv(1024).decode()
            if not data:
                break
            print("from connected user: " + str(data))
            message = input(' -> ')
            conn.send(message.encode())
            if(message == "stop"):
                exit()
        conn.close()
        print("User disconnected")
        message = input('(press enter to continue, or type shutdown to stop) ')
        if message == 'shutdown':
            break
    server_socket.close()
if __name__ == '__main__':
    server_program()
