#!/usr/bin/env python3
import unittest
import socket
import subprocess 
from indexer_server import IndexerServer

class TestIndexerServerMethods(unittest.TestCase):
	def testIsValidInput(self):
		self.server = IndexerServer("127.0.0.1", 8080)
		self.assertTrue(self.server.is_valid_input("ADD python \n"))
		self.server.shutdown()

	def testUnpack(self):
		self.server = IndexerServer("127.0.0.1", 8080)
		correct_unpacking = ["INDEX", "aubio", {"C"}]
		test_unpacking = self.server.unpack("ADD aubio C\n")
		
		self.assertEqual(test_unpacking, correct_unpacking)

		test_unpacking = self.server.unpack("CHECK aubio \n")
		self.assertNotEqual(test_unpacking, correct_unpacking)
		self.server.shutdown()		

if __name__ == "__main__":
	unittest.main()
	