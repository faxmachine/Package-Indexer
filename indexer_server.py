#!/usr/bin/env python3
import socketserver
import threading
import socket
import sys
import re

from graph import Graph

class IndexerServer:

	def __init__(self, host, port):
		"""
		Initializes the concurrency value, the regular expression, and the thread lock.
		Creates a socket then binds the host and port
		"""

		self.CONCURRENCY_VALUE = 100
		regex = "^(ADD|REMOVE|CHECK)[ ][a-zA-z0-9-_+]*[ ][a-zA-z0-9-_+]*([,][a-zA-z0-9-_+]*)*\r?\n$"
		self.comp_regex = re.compile(regex)
		self.lock = threading.Lock()


		self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		print("Socket created")

		self.index = Graph()
		print("index created")

		try:
			self.s.bind((host, port))
		except socket.error as err:
			print("Socket error: {}".format(err))
			sys.exit()

		print("Socket bound")

	def is_valid_input(self, message):
		"""
		This uses the regex compiled in __init__ to determine
		if the received message is valid
		"""

		return bool(self.comp_regex.match(message))

	def unpack(self, message):
		"""
		Turns a valid message from a string into an array with a set as it's
		last element
		"""

		message = message.replace("\n", "").replace("\r", "")
		aux_array = message.split(" ")
		aux_array[2] = aux_array[2].split(",")

		# This handles the no dependencies case
		if aux_array[2][0] == "":
			aux_array[2] = set()

		aux_array[2] = set(aux_array[2])

		return aux_array

	def client_thread(self, conn):
		"""
		The target method for the threads. If a connected user stops sending data,
		then the connection for that user is closed and the thread ends. A lock just before 
		the critical section prevents a race condition from happening.
		"""

		while True:
			data = conn.recv(1024)

			if not data:
				break
			elif not self.is_valid_input(data.decode()):
				conn.sendall("ERROR\n".encode())
			else:
				with self.lock:
					unpacked_message = self.unpack(data.decode())
					command, package = unpacked_message[0], unpacked_message[1]
					dependencies = unpacked_message[2]

					self.evaluate_message(command, package, dependencies, conn)
		
		conn.close()

	def evaluate_message(self, command, package, dependencies, conn):
		"""
		This method determines what the server does in response to a given message. It is a helper
		method to client_thread()
		"""

		if command == "ADD":
			# Check to see if the package can be indexed
			if self.index.check_indexable(package, dependencies) or self.index.check_package_exists(package):
				self.index.add_package(package, dependencies)
				conn.sendall("SUCCESS\n".encode())
			else:
				conn.sendall("FAILURE\n".encode())

		elif command == "REMOVE":
			if not self.index.check_package_exists(package):
				conn.sendall("SUCCESS\n".encode())
			elif self.index.check_if_dependency(package):
				conn.sendall("FAILURE\n".encode())
			else:
				self.index.remove_package(package)
				conn.sendall("SUCCESS\n".encode())

		elif command == "CHECK":
			if self.index.check_package_exists(package):
				conn.sendall("SUCCESS\n".encode())
			else:
				conn.sendall("FAILURE\n".encode())
		else:
			conn.sendall("ERROR\n".encode())

	def listen(self):
		"""
		Listens for new connections. Once a new connection is made a thread is created
		for that connection.
		"""

		self.s.listen(self.CONCURRENCY_VALUE)
		print("Socket now listening...")

		threads = []

		while True:
			conn, addr = self.s.accept()
			print("Connected with: {} , {}".format(str(addr[0]), str(addr[1])))
			
			#create threads
			t = threading.Thread(target = self.client_thread, args = (conn,))
			threads.append(t)
			t.start()

		self.s.close()
		sys.exit()

	def shutdown(self):
		"""
		A way to manually close the socket
		"""
		self.s.close()

if __name__ == '__main__':
	"""
	Driver for indexer_server. The KeyboardInterrupt exception is caught for
	a more graceful exit when shutting down. 
	"""

	try:
		server = IndexerServer("127.0.0.1", 8080)
		server.listen()
	except KeyboardInterrupt:
		print("\nExiting...")
		sys.exit()
