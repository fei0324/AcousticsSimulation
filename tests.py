import unittest
import numpy as np
from stl import mesh

from subdivision import subdivision, subdivide_reconstruct

class TestSubdivision(unittest.TestCase):

	def setUp(self):

		self.points1, self.triangleSet1, self.norVecSet1 = subdivision(np.array([0,0,0]), np.array([0,1,0]), np.array([1,0,0]), 1)
		self.points3, self.triangleSet3, self.norVecSet3 = subdivision(np.array([0,0,0]), np.array([0,1,0]), np.array([1,0,0]), 3)

	def test_number_of_triangles(self):

		self.assertEqual(len(self.triangleSet1), 4)
		self.assertEqual(len(self.triangleSet3), 64)

	def test_number_of_points(self):

		self.assertEqual(len(self.points1), 6)
		self.assertEqual(len(self.points3), 45)

class TestSubdivisionReconstruct(unittest.TestCase):

	def setUp(self):

		self.oriTriangoSet = mesh.Mesh.from_file("newChimeR.0127D4.stl").vectors
		self.indices = [0, 1, 10, 13, 56]
		self.n = 1

		self.newTriangleSet = subdivide_reconstruct(self.oriTriangoSet, self.indices, self.n)

	def test_size_of_new_triangle_set(self):

		self.assertEqual(len(self.oriTriangoSet), 80, msg="The size of the original triangle set is not as expected.")
		self.assertEqual(len(self.indices), 5, msg="The size of the list of triangles we want to subdivide is not as expected.")

		self.assertEqual(len(self.newTriangleSet), 95, msg="The size of the newTriangleSet is not the same as calculated.")

	def test_insertion_index_of_new_triangles(self):

		"""
		Test if the subdivided new triangles are inserted into the correct spot in the new triangle set.
		"""

		# The triangle at oriTriangleSet[2] should to inserted into newTriangleSet[8] after shifting the indices
		# based on subdivision of triangles 0 and 1.
		self.assertTrue(np.array_equal(self.oriTriangoSet[2], self.newTriangleSet[8]),
						msg="Subdivided triangles are not inserted in the correct positions in the new triangle set.")

		self.assertTrue(np.array_equal(self.oriTriangoSet[14], self.newTriangleSet[26]),
						msg="Subdivided triangles are not inserted in the correct positions in the new triangle set.")

		
class TestSearchTriangles(unittest.TestCase):

	def setUp(self):

		self.test_dict = {2:'a', 1:'a', 3:'d', 5:'f', 4:'e', 6:'b', 7:'c', 8:'e'}
		self.sorted_dict = {1:'a', 2:'a', 6:'b', 7:'c', 3:'d', 4:'e', 8:'e', 5:'f'}

	def test_sort_dictionary_based_on_values_algorithm(self):

		test_dict = self.test_dict
		sorted_keys = sorted(test_dict, key=test_dict.__getitem__)
		sorted_values = sorted(test_dict.values())
		sorted_dict = dict(zip(sorted_keys, sorted_values))

		self.assertEqual(sorted_dict, self.sorted_dict)



if __name__ == '__main__':
	unittest.main()