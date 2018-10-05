# Test based on what I currently have in Mij matrix.

import unittest
import numpy as np
from stl import mesh

from pointCollection import pointCollection
from mijMat import sameTriangle


class TestMijMat(unittest.TestCase):

	def setUp(self):

		self.chime_mesh = mesh.Mesh.from_file("newChimeR.0127D4.stl")
		self.oriTriangleSet = self.chime_mesh.vectors
		self.positions = pointCollection(self.oriTriangleSet)

		"""
		triIndex_dict: key - the i and j index pair in positions,
					   value - output from the sameTriangle functionn
							   indices of the triangles that contain both of teh points
		"""
		self.triIndex_dict = {
			(0,1):[0,1],
			(0,3):[1,18],
			(1,3):[1,20],
			(3,21):[21,38],
			(3,19):[19,38],
			(25,9):[28,29],
			(10,26):[30,31],
			(28,38):[55,56],
			(47,38):[74,75],
			(43,2):[],
			(45,40):[],
			}


	def test_same_triangle(self):

		for key in self.triIndex_dict:

			triIndex = sameTriangle(key[0],key[1],self.positions,self.oriTriangleSet)
			self.assertEqual(triIndex, self.triIndex_dict[key])


if __name__ == '__main__':
	unittest.main()