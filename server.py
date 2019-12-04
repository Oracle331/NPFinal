from socket import *
import select
import sys
import threading
import time

QUIT = False


class Server:
    def __init__(self):
        self.host = "10.220.82.40"
        self.port = 5089
        self.threads = []
        self.backlog = 10

    def run(self):

        while True:
            try:
                all_good = False
                self.sock = socket(AF_INET, SOCK_STREAM)
                self.sock.bind((self.host, self.port))
                self.sock.listen(self.backlog)

                print("Server started at " + self.host + ":" + str(self.port))
                break
            except Exception as err:
                print('Socket connection error... ')
                self.sock.close()
        try:
            while True:
                try:
                    client, addr = self.sock.accept()
                except socket.timeout:
                    continue
                new_thread = Client(client)

                print("Connected by ", addr)
                msg = ("User: %s connected from: %s" % (new_thread.name, addr)).encode()
                for each in self.threads:
                    each.client.send(msg)

                self.threads.append(new_thread)
                new_thread.start()

                for thread in self.threads:
                    if not thread.is_alive():
                        self.threads.remove(thread)
                        thread.join()
                        # time.sleep(1)
        except KeyboardInterrupt:
            print("Terminating by Ctrl+C")
        except Exception as err:
            print("Exception: %s\nClosing" % err)
        for thread in self.threads:
            thread.join()
        self.sock.close()


class Client(threading.Thread):

    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client
        time.sleep(1)

        self.done = False

    def run(self):

        while not self.done:
            try:
                cmd = self.client.recv(1024).decode()
                if cmd.startswith("/name"):
                    self.client.send("Enter your username: ".encode())
                    old_name = self.name
                    self.name = self.client.recv(1024).decode()
                    msg = "%s has changed his username to %s" % (old_name, self.name)
                    for each in server.threads:
                        if each != self and each.is_alive():
                            each.client.send(msg.encode())
                    self.client.send(("Your username has been changed to %s" % self.name).encode())
                elif cmd == "/quit":
                    self.remove()
                elif cmd.startswith("/filetransfer"):
                    self.client.send("Please enter the filename of the file: ".encode())
                    filename = self.client.recv(1024).decode()
                    file = open(filename, 'rb')
                    file_data = file.read(4096)
                    for each in server.threads:
                        if each != self and each.is_alive():
                            self.fileTransfer(each)
                    print("Data has been transmitted successfully")
                else:
                    msg = "%s: %s" % (self.name, cmd)
                    for each in server.threads:
                        if each != self:
                            each.client.send(msg.encode())
            except Exception as e:
                print("Connection lost", e)
                # self.remove()
                break
                # continue
        server.threads.remove(self)
        self.client.close()
        return

    def remove(self):
        self.client.send("exit".encode())
        server.threads.remove(self)
        QUIT = True
        self.done = True

    def fileTransfer(self, user):
        # filename = input(str("Please enter a filename for the incoming file: "))
        user.client.send("Please enter a filename for the incoming file: ".encode())
        filename = user.client.recv(1024).decode()
        with open(filename, 'wb') as file:
            file_data = user.client.recv(4096)
            file.write(file_data)
        # file = open(filename, 'wb')

        # file.close()
        print("File has been received successfully.")


if __name__ == "__main__":
    server = Server()
    server.run()

    print("Terminated")
