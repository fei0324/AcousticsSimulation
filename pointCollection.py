import numpy as np
from stl import mesh

def pointCollection(triangleSet):

	"""
	Decomposing the given triangle set, creating a new list containing only unique points removing duplicates

	Input: triangleSet = the set of triangles from the STL file
	Output: positions = a list of unique points from the triangleSet without duplicates
	"""

	temp = []

	for triangle in triangleSet:
		temp.append(triangle[0])
		temp.append(triangle[1])
		temp.append(triangle[2])

	positions = [temp[0]]

	for i in range(1, len(temp)):
		if all(abs(np.linalg.norm(temp[i]-element))>1e-5 for element in positions):
			positions.append(temp[i])

	return positions