#!/usr/bin/env python3

class Graph:
	def __init__(self):
		self.graph = {}

	def add_package(self, package, dependencies):
		"""
		Add a package, possibly with dependencies, to the graph
		Supports updating depenencies
		"""

		self.graph[package] = dependencies

		for p in dependencies:
			if p not in self.graph.keys():
				self.graph[p] = set()

	def remove_package(self, package):
		"""
		Remove all occurrences of the package in question from the adjacency list
		"""

		del self.graph[package]

		for p, dependencies in self.graph.items():
			if package in dependencies:
				dependencies.remove(package)

	def check_indexable(self, package, dependencies):
		"""
		Check if the dependencies for a given package have been indexed
		"""

		return dependencies.issubset(self.graph.keys())
	
	def check_package_exists(self, package):
		return package in self.graph.keys()

	def check_if_dependency(self, package):
		"""
		Check if a given package is a dependency
		"""

		for p, dependencies in self.graph.items():
			if package in dependencies:
				return True

		return False

	def cycle_check(self, package):
		"""
		Checks the graph for a dependency cycle using iterative Depth First Search
		"""
		visited = set()
		stack = []
		stack.append(package)

		while stack:
			package = stack.pop()
			if package not in visited:

				visited.add(package)
				stack.extend(self.graph[package])
			else:
				return True

		return False

	def print_dic(self):
		"""
		Prints the adjecency list
		"""

		for package, dependencies in self.graph.items():
			print(package, "->", dependencies)
