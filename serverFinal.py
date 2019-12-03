#!/usr/bin/python3
import socket, sys, threading, queue,time


'''
kody wiadomosci:
0 logowanie
'''

PORT = 5089
HOST = socket.gethostname()
newUserComes = queue.Queue()
newMesages = queue.Queue()
activeUsers = []
#If someone logs in, they have a login at the beginning of the message
#if he sends it he has a message for you

class Server:
	users = []
	
	def __init__(self):
		self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			address = HOST, PORT
			self.server.bind(address)
		except socket.error:
			print("Binding failed")
			return
		self.server.listen()
		
	def exit(self):
		self.server.close()
	
	def run(self):
		print("Waiting for connection")
		while True:
			conn, addr = self.server.accept()
			threading.Thread(target=self.run_thread, args=(conn, addr)).start()
	
	def handleMessage(self):
		while not newMesages.empty():
			newMessage = newMesages.get()
			if newMessage[0] == "0":
				newMessage = newMessage.split(" ", 1)
				print ("I sent information that has arrived",newMessage[1])
				newUserComes.put(newMessage[1])
		while not newUserComes.empty():
			newUser = newUserComes.get()
			activeUsers.append(newUser)
			print("He came", newUser)
		
	
	def run_thread(self, conn, addr):
		while True:
			message = conn.recv(1024)
			if(message.decode() != ""):
				newMesages.put(message.decode() )
			if(not newMesages.empty()):
				print("message came to me")
				self.handleMessage()
			time.sleep(1)
			

newServer = Server()
newServer.run()
Server.exit()
