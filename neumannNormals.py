import numpy as np
from stl import mesh

#from pointCollection import *

def neumannNormals(positions, triangleSet, triangleNorms):

	"""
	Goal: Calculating the neumannNormals for the airSolver.

	Input: positions - distinct points from the triangle set
		   triangleSet - the triangle set after subdivision
		   triangleNorms - a list of normal vectors corresponding to the triangle sets
	Output: a list of normal vectors corresponding to the positions
	"""

	normals = np.zeros((len(positions),3))

	for i in range(len(positions)):

		count = 0
		sumOfNormals = [0., 0., 0.]
		#print("i = " + str(i))

		for j in range(len(triangleSet)):
			for point in triangleSet[j]:
				if np.array_equal(point, positions[i]):
					sumOfNormals = np.add(sumOfNormals, triangleNorms[j])
					#print(triangleNorms[j])
					count += 1
		#print("count = " + str(count))
		#print("sum = " + str(sumOfNormals))
		#print(type(sumOfNormals))
		aveNormal = (1./count)*sumOfNormals
		#print("ave = " + str(aveNormal))
		normals[i] = aveNormal

	return normals

"""
file_mesh = mesh.Mesh.from_file("newChimeR.0127D4.stl")
positions = pointCollection(file_mesh.vectors)
triangleSet = file_mesh.vectors
triangleNorms = file_mesh.normals

print(neumannNormals(positions, triangleSet, triangleNorms))
"""