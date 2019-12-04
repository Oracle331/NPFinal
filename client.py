from socket import *
import sys
import threading

host = "10.220.82.40"#127.0.0.1
port = 5089


class listen(threading.Thread):
    def __init__(self, client):
        threading.Thread.__init__(self)
        self.client = client
        self.setDaemon(True)

    def run(self):
        connected = True
        while connected:
            try:
                data = self.client.recv(2048).decode()
                if data == "exit":
                    sys.exit(1)
                elif data.startswith("/filetransfer"):
                    fileTransfer(self)
                else:
                    print(data)

            except Exception as e:
                connected = False
                print("You have disconnected")


if __name__ == "__main__":
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((host, port))
    try:
        print("Welcome to chat!")
        print("Type your message and press 'Enter' to send.")
        print("Send '/name' command to change your username.")
        print("Send '/quit' command to quit.")
    except error as e:
        if clientSocket:
            clientSocket.close()
        print("Could not open a socket: " + str(e))
        sys.exit(1)

    l = listen(clientSocket)
    l.start()
    message = input()
    while message != "/quit":
        # sys.stdout.flush()
        clientSocket.send(message.encode())
        # data = self.clientSocket.recv(1024)
        # data = data.decode()
        # print("Recieved: "+str(data))
        message = input()
    clientSocket.close()

    def fileTransfer(self):

        filename = input(str("Please enter a filename for the incoming file: "))
        file = open(filename, 'wb')
        file_data = self.client.recv(4096).decode()
        file.write(file_data)
        file.close()
        print("File has been received successfully.")