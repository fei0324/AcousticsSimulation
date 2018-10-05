import unittest
import numpy as np
from stl import mesh

from subdivision import (
	subdivision,
	subdivide_reconstruct,
	calculate_centroid_of_triangle,
	search_triangles,
	)

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

		self.chime_mesh = mesh.Mesh.from_file("newChimeR.0127D4.stl")
		self.oriTriangoSet = self.chime_mesh.vectors
		self.oriNormVecSet = self.chime_mesh.normals
		self.indices = [0, 1, 10, 13, 20, 56]
		self.n = 1

		self.newTriangleSet, self.newNormVecSet = subdivide_reconstruct(self.oriTriangoSet, self.oriNormVecSet, self.indices, self.n)

	def test_size_of_new_triangle_set(self):

		self.assertEqual(len(self.oriTriangoSet), 80, msg="The size of the original triangle set is not as expected.")
		self.assertEqual(len(self.indices), 6, msg="The size of the list of triangles we want to subdivide is not as expected.")

		self.assertEqual(len(self.newTriangleSet), 98, msg="The size of the newTriangleSet is not the same as calculated.")

	def test_size_of_new_normvecset(self):

		self.assertEqual(len(self.oriNormVecSet), 80, msg="The size of the original normal vector set is not as expected.")
		self.assertEqual(len(self.newNormVecSet), 98, msg="The size of the newNormVecSet is not the same as calculated. ")

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
		self.sorted_keys = [1, 2, 6, 7, 3, 4, 8, 5]
		self.triangle = np.array([np.array([1.,2.,3.]), np.array([-3.,9.,5.]), np.array([5.,2.,-3.])])

		self.chime_mesh = mesh.Mesh.from_file("newChimeR.0127D4.stl")
		self.ori_triangle_set = self.chime_mesh.vectors
		self.impact_coor = np.array([0.,0.,0.])
		self.output_indices = [25, 35, 44, 54, 23, 33]

	def test_sort_dictionary_based_on_values_algorithm(self):

		test_dict = self.test_dict
		sorted_keys = sorted(test_dict, key=test_dict.__getitem__)

		self.assertEqual(sorted_keys, self.sorted_keys)
		self.assertEqual(test_dict[sorted_keys[0]], min(sorted(test_dict.values())))

	def test_centroid_of_triangle(self):

		# Test the centroid is in the same plane as the triangle

		pt1 = self.triangle[0]
		pt2 = self.triangle[1]
		pt3 = self.triangle[2]

		v1 = pt2 - pt1
		v2 = pt3 - pt1

		centroid = calculate_centroid_of_triangle(pt1, pt2, pt3)

		v3 = centroid - pt1

		# find the normal vector of the plane
		normalVec = np.cross(v1, v2)

		# take the dot product of the normal vector and v3, expecting 0
		dot_product = np.dot(v3, normalVec)

		self.assertTrue(abs(dot_product)<10e-5, msg="The centroid is not on the same plane as the triangle.")

	def test_correct_ordered_output(self):

		indices = search_triangles(self.ori_triangle_set, self.impact_coor)
		self.assertEqual(len(indices), 6, msg="The number of triangles in the output of the search function is incorrect.")
		self.assertTrue(np.array_equal(indices, self.output_indices), msg="The search function is not outputing the correct triangles.")



if __name__ == '__main__':
	unittest.main()