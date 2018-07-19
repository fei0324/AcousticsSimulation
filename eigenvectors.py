import math
import numpy as np
from stl import mesh

from subdivision import *
from lengthSolver import *
from pointCollection import *
from mijMat import *
from outsideMat import *
from diagonalMat import *

from neumannNormals import *

def eigenvectors(filename, youngs, n):

	"""
	Plot the magnitude of eigenvector on points of the original shape

	Input: filename needs to be in '.stl' format ex. filename = 'sphere.stl'
		   youngs = Young's modulus of the material
		   n = the number of the times of division

	Output: The plot of the first four eigenvectors, color coded by the impact
			on each point of the objected 
	"""

	file_mesh = mesh.Mesh.from_file(filename)

	oriTriangleSet = file_mesh.vectors
	#triNormVecs = file_mesh.normals

	triangleSet = []
	triNormVecs = []

	for i in range(len(oriTriangleSet)):
		points, singleTriangleSet, singleNorVecSet = subdivision(oriTriangleSet[i][0], oriTriangleSet[i][1], oriTriangleSet[i][2],n)

		for j in range(len(singleTriangleSet)):
			triangleSet.append(singleTriangleSet[j])
			triNormVecs.append(singleNorVecSet[j])


	forceVecs = np.zeros((len(triNormVecs),3))

	for i in range(len(forceVecs)):
		forceVecs[i] = -1*triNormVecs[i]*3

	Llist, Lmat = lengthSolver(triangleSet,triNormVecs,forceVecs)

	positions = pointCollection(triangleSet)

	Mijmatrix = mijMat(youngs,Llist,triangleSet,positions)
	OTMat = outsideMat(positions,Mijmatrix)
	Dmat = diagonalMat(positions,Mijmatrix)

	BigMatrix = OTMat + Dmat

	w, v = np.linalg.eig(BigMatrix)

	neumannNormalVecs = neumannNormals(positions, triangleSet, triNormVecs)

	#print(np.dot(v, neumannNormalVecs))

	return v, neumannNormalVecs



v, neumannNormalVecs = eigenvectors("newChimeR.0127D4.stl", 128*10**9, 0)

print v.shape
print neumannNormalVecs.shape