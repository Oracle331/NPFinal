from socket import *
import select
import sys
import threading
import time


# @authors Andrew Galvin, Endi Caushi, Anthony Salaris
# @version 1.0.0 - Simple client per class assignment
# @version 2.0.0 - Adjusted for multiple clients


# Manage threads per user
class Server:

    # declare variables
    def __init__(self):

        # manually set server on local host
        self.host = "127.0.0.1"
        self.port = 5089
        self.threads = []
        self.backlog = 10

    # start and run the server
    def run(self):
        while True:
            # start the server if the port is available
            try:
                user = socket(AF_INET, SOCK_STREAM)
                user.bind((self.host, self.port))
                user.listen(self.backlog)

                print("Server started at " + self.host + ":" + str(self.port))
                break
            except Exception as err:
                print('Socket connection error... ')
                self.user.close()
        try:
            # create a new thread for each user  that connects
            while True:
                try:
                    client, addr = self.user.accept()
                except socket.timeout:
                    continue
                new_thread = Client(client)

                print("Connected by ", addr)
                msg = ("User: %s connected from: %s" % (new_thread.name, addr)).encode()
                for each in self.threads:
                    each.client.send(msg)

                # add the user to the array of threads
                self.threads.append(new_thread)
                new_thread.start()

                # remove inactive threads
                for thread in self.threads:
                    if not thread.is_alive():
                        self.threads.remove(thread)
                        thread.join()
        except KeyboardInterrupt:
            print("Terminating by Ctrl+C")
        except Exception as err:
            print("Exception: %s\nClosing" % err)
        for thread in self.threads:
            thread.join()
        self.sock.close()


# permissions for clients connecting
class Client(threading.Thread):

    # declare variables
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client
        time.sleep(1)

        self.done = False

    # hold a connection with the client
    def run(self):
        while not self.done:
            # if a command is received
            try:
                cmd = self.client.recv(1024).decode()
                # change username
                if cmd.startswith("/name"):
                    self.client.send("Enter your username: ".encode())
                    old_name = self.name
                    self.name = self.client.recv(1024).decode()
                    msg = "%s has changed his username to %s" % (old_name, self.name)
                    for each in server.threads:
                        if each != self and each.is_alive():
                            each.client.send(msg.encode())
                    self.client.send(("Your username has been changed to %s" % self.name).encode())
                # disconnect from server
                elif cmd == "/quit":
                    self.remove()
                    # below is the attempt at file transfer
                # elif cmd.startswith("/filetransfer"):
                #     self.client.send("Please enter the filename of the file: ")
                #     filename = self.client.recv(1024)
                #     file = open(filename, 'rb')
                #     file_data = file.read(4096).decode()
                #
                #     for each in server.threads:
                #         if each != self and each.is_alive():
                #             each.fileTransfer(file_data)
                #     print("Data has been transmitted successfully")

                # send message
                else:
                    msg = "%s: %s" % (self.name, cmd)
                    for each in server.threads:
                        if each != self:
                            each.client.send(msg.encode())
            except Exception as e:
                print("Connection lost", e)
                break

        # user disconnects, remove thread
        server.threads.remove(self)
        self.client.close()
        return

    def remove(self):
        self.client.send("exit".encode())
        server.threads.remove(self)
        self.done = True
    # attempt at file transfer
    # def fileTransfer(self, file_data):
    #     # filename = input(str("Please enter a filename for the incoming file: "))
    #     # user.client.send("Please enter a filename for the incoming file: ".encode())
    #     filename = self.client.recv(1024).decode()
    #     # file_data = self.client.recv(4096).decode()
    #
    #     # with open(filename, 'wb') as file:
    #     file = open(filename, 'wb')
    #     # file.write(file_data)
    #     self.client.send(file_data)
    #
    #     file.close()
    #     print("File has been received successfully.")


# run server
if __name__ == "__main__":
    server = Server()
    server.run()

    print("Terminated")
