from socket import *
import sys
import threading

# @authors Andrew Galvin, Endi Caushi, Anthony Salaris
# @version 1.0.0 - Simple client per class assignment
# @version 2.0.0 - Added constant send/receive messages from other clients

# the server IP is manually set here for the local host
host = "127.0.0.1"  # IP can be found in cmd prompt by typing 'ipconfig'
port = 5089


# Creates a new thread when a user connects
class listen(threading.Thread):
    # Method to initialize the thread for the client

    def __init__(self, client):
        # create a new thread
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
                #  elif data.startswith("/filetransfer"):
                #     fileTransfer(self)
                else:
                    print(data)

            except Exception as e:
                connected = False
                print("You have disconnected")


# Main module to run everything
if __name__ == "__main__":
    # initialize TCP socket #
    clientSocket = socket(AF_INET, SOCK_STREAM)
    # connect the socket to the given host and port #
    clientSocket.connect((host, port))
    # display welcome messsage to client #
    try:
        print("----------Welcome to our chat-----------------------------------")
        print("----------Type your message and press 'Enter' to send.----------")
        print("----------Send '/name' command to change your username.---------")
        print("----------Send '/quit' command to quit.-------------------------")
    except error as e:
        # if unable to open a socket #
        if clientSocket:
            # close the socket #
            socket.close(clientSocket)
        # error message to print out if unable to open  the socket #
        print("Unable to open a socket: " + str(e))
        # shutdown the client #
        sys.exit(1)

    connection = listen(clientSocket)
    connection.start()
    message = input()
    while message != "/quit":
        clientSocket.send(message.encode())
        message = input()
    clientSocket.close()
