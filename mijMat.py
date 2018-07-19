import math
import numpy as np
from stl import mesh

import matplotlib.pyplot as plt

def triangleArea(triangleSet):

	"""
	Calculate areas of subdivided triangles

	Input: the set of subdivided triangles

	Output: a list of the areas with corresponding idices with the the triangleSet
	"""

	triangleAreaSet = []

	for i in range(len(triangleSet)):
		v1 = triangleSet[i][1] - triangleSet[i][0]
		v2 = triangleSet[i][2] - triangleSet[i][0]
		area = np.linalg.norm(np.cross(v1, v2))/2
		triangleAreaSet.append(area)

	return triangleAreaSet



def sameTriangle(indexI,indexJ,positions,triangleSet):

	"""
	Test if two points are in the same triangle

	Input: indexI = the index of the first point in positions
		   indexJ = the index of the second point in positions (indexI has to be different from indexJ)
		   positions = the list of all unique points from the STL file
		   triangleSet = the STL file or the triangle set generated after
	Output: triIndex = a list of 0 to 2 elements, indices of the triangles that contain the two point from input
	"""

	triIndex = []

	if indexI != indexJ:
		for m in range(len(triangleSet)):
			triangleI = -2
			triangleJ = -3
			for n in range(len(triangleSet[m])):
				if abs(np.linalg.norm(positions[indexI] - triangleSet[m][n]))<1e-5:
					triangleI = m
				if abs(np.linalg.norm(positions[indexJ] - triangleSet[m][n]))<1e-5:
					triangleJ = m
			if triangleI == triangleJ:
				triIndex.append(m)

	return triIndex


def mijMat(elastic,l,triangleSet,positions):

	"""
	Calculating Mij, a matrix of spring constants over length of strings
	Input: elastic = elastic modulus/Young's modulus
		   l = the length calculated by the L solver based on force
		   triangleSet = the entire set of triangles after necessary subdivision
	Output: A matrix of spring constants for each string
	"""

	Mij = np.zeros((len(positions),len(positions)))
	triangleAreaSet = triangleArea(triangleSet)

	weirdPoints = []

	for i in range(len(positions)):
		for j in range(len(positions)):

			triIndex = sameTriangle(i,j,positions,triangleSet)
			#print(triIndex)

			if i == j:
				Mij[i,j] = 0
			elif len(triIndex) == 0:
				Mij[i,j] = 0
			elif len(triIndex) == 1:
				print("Two points only present in one triangle." + " i = " + str(i) + " j = " + str(j))
				# weirdPoints.append(positions[i])
				# weirdPoints.append(positions[j])
			elif len(triIndex) == 2:

				# k needs to be arbitrary. Need to fix that later
				
				k1 = triangleAreaSet[triIndex[0]]*elastic/l[triIndex[0]]
				k2 = triangleAreaSet[triIndex[1]]*elastic/l[triIndex[1]]
				k = (k1+k2)/2
				Mij[i,j] = k/np.linalg.norm(positions[j]-positions[i])

	return Mij