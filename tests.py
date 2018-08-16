import unittest
import numpy as np

from subdivision import subdivision

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

		

if __name__ == '__main__':
	unittest.main()