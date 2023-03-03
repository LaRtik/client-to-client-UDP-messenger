import socket
import threading
import random
import time
import sys


CLIENT_CONFIG = "localhost", 9999
ALTER_CLIENT_CONFIG = "localhost", 9998
MESSAGES = []


class Client():
	def __init__(self, name: str) -> None:
		self.USE_ALTER = False
		self.client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		try:
			self.client.bind(CLIENT_CONFIG)
		except:
			self.client.bind(ALTER_CLIENT_CONFIG)
			self.USE_ALTER = True
		self.name = name
		self.t = threading.Thread(target = self.recieve)
		self.t.start()
		self.send("[SMMESSAGES]", tim = False)


	def recieve(self):
		while True:
			try:
				
				message, _ = self.client.recvfrom(1024)
				#name = message.decode().split('[')[1]
				#name = message.split(']')[0]
				#print(name)
				message = message.decode()
				if message == "[SMMESSAGES]":
					for msg in MESSAGES:
						self.restore_messages(msg)
				else:
					print(message)
					MESSAGES.append(message)
			except:
				pass

	def send(self, message: str, tim = True):
		if message == "!q":
			sys.exit(0)
		else:
			try:
				if tim:
					self.client.sendto(f"{time.ctime()} - [{self.name}]: {message}".encode(), CLIENT_CONFIG)
					self.client.sendto(f"{time.ctime()} - [{self.name}]: {message}".encode(), ALTER_CLIENT_CONFIG)
				else:
					self.client.sendto(message.encode(), CLIENT_CONFIG)
					self.client.sendto(message.encode(), ALTER_CLIENT_CONFIG)
			except Exception as e:
				print("Error sending message", e)
	

	def restore_messages(self, message: str):
		try:
			self.client.sendto(message.encode(), CLIENT_CONFIG if self.USE_ALTER else ALTER_CLIENT_CONFIG)
		except Exception as e:
			print(e)
	


print("Enter your name: ")
name = input()
client = Client(name)
print(client.client)

while True:
	message = input()
	client.send(message)