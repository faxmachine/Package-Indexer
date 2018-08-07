#!/usr/bin/env python3

import unittest
from graph import Graph

class TestGraphMethods(unittest.TestCase):
	
	def test_empty_graph(self):
		g = Graph()
		self.assertEqual(len(g.graph), 0)

	def test_add_package(self):
		g = Graph()
		correct_graph = {"A": {"B", "C"},
		"B": set(),
		"C": set()}

		g.add_package("A", {"B", "C"})
		self.assertEqual(g.graph, correct_graph)

	def test_remove_package(self):
		g = Graph()
		correct_graph = {"A" : {"B"},
		"B": set()}

		g.add_package("A", {"B", "C"})
		g.remove_package("C")
		self.assertEqual(g.graph, correct_graph)

		g = Graph()
		correct_graph = {"B": set(),
		"C": set()}

		g.add_package("A", {"B", "C"})
		g.remove_package("A")
		self.assertEqual(g.graph, correct_graph)

	def test_check_indexable(self):
		g = Graph()
		g.add_package("A", set())
		g.add_package("B", set())
		self.assertEqual(g.check_indexable("C", {"A", "B"}), True)

		g = Graph()
		g.add_package("A", {"D", "E"})
		self.assertEqual(g.check_indexable("F", {"D", "C"}), False)

	def test_check_package_exists(self):
		g = Graph()
		g.add_package("A", set())
		g.add_package("B", set())
		self.assertEqual(g.check_package_exists("A"), True)

		g = Graph()
		g.add_package("B", set())
		self.assertEqual(g.check_package_exists("A"), False)

	def test_update_dependencies(self):
		g = Graph()
		g.add_package("A", {"B", "C"})
		correct_graph = {"A": {"B", "C", "D"},
		"B": set(),
		"C": set(),
		"D": set()}

		g.add_package("A", {"B", "C", "D"})
		self.assertEqual(g.graph, correct_graph)

	def test_cyclic_check(self):
		g = Graph()
		g.add_package("A", {"C"})
		g.add_package("B", {"A"})
		g.add_package("C", {"D"})
		g.add_package("D", {"B"})
		self.assertEqual(g.cycle_check("A"), True)

		g.add_package("B", set())
		self.assertEqual(g.cycle_check("A"), False)

if __name__ == "__main__":
	unittest.main()
