import numpy as np
from stl import mesh

from neumannNormals import *
from subdivision import *
from lengthSolver import *
from pointCollection import *
from mijMat import *
from outsideMat import *
from diagonalMat import *
from mallotImpact import *


def desiredDerivs(filename, youngs, n, indexW):

	"""
	Calculat the desiredDerivs for a certain eigenvalue. This is used in the airsolver

	Input: filename needs to be in '.stl' format ex. filename = 'sphere.stl'
		   youngs = Young's modulus of the material
		   n = the number of the times of division
		   indexW = the index of eigenvalue and the corresponding index of the eigenvector

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
	#print("eigenvalues = " + str(v))
	#print(w.shape)
	#print(v.shape)

	# reorganize eigenvectors

	vMat = np.zeros((len(positions), 3))

	for i in range(len(v[:,indexW])):
		if i%3 == 0:
			xyz = np.array([v[i,indexW], v[i+1,indexW], v[i+2,indexW]])
			vMat[i/3] = xyz

	#print(vMat)
	#print(vMat.shape)

	# Need to scale the vMat with initial impact
	


	neumannNormalVecs = neumannNormals(positions, triangleSet, triNormVecs)
	print(neumannNormalVecs.shape)

	desiredDerivsMat = np.zeros((len(positions),1))

	for i in range(len(positions)):
		desiredDerivsMat[i] = np.dot(vMat[i], neumannNormalVecs[i])
	print(desiredDerivsMat)
	print(desiredDerivsMat.shape)

	return w[indexW], desiredDerivsMat

desiredDerivs("newChimeR.0127D4.stl", 128*10**9, 0, 0)