import numpy as np
from stl import mesh

from neumannNormals import *
from subdivision import (subdivision,
						subdivide_reconstruct,
						calculate_centroid_of_triangle,
						search_triangles,)
from lengthSolver import *
from pointCollection import *
from mijMat import *
from outsideMat import *
from diagonalMat import *
from mallotImpact import *
from chimeVelocity import *


def calculateEigenvectors(filename, youngs, n, indexW):

	"""
	Calculate the desiredDerivs for a certain eigenvalue. This is used in the airsolver

	Input: filename needs to be in '.stl' format ex. filename = 'sphere.stl'
		   youngs = Young's modulus of the material
		   n = the number of the times of division
		   indexW = the index of eigenvalue and the corresponding index of the eigenvector

	Output: w[indexW] - the eigenvalue thatis corresponding to the eigenvector in the calculation
						This is also the wavelength we are using in the airsolver
			desiredDerivsMat - the matrix for desired derivatives
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

	return positions, triangleSet, triNormVecs, w, v


def desiredDerivs(positions, w, v, indexW, neumannNormals, initialImpact):

	"""
	Goal: calculate desiredDerivs for the airsolver function.

	Input: positions - a list of distinct points on the chime
		   w - eigenvalues coming from the bigMatrix
		   v - eigenvectors coming from the bigMatrix
		   indexW - the index of the eigenvalue we are using in this round of calculation
		 			w[indexW] is also the input wavelength in the airsolver
		   neumannNormals - the normal vectors corresponding to positions
		   initialImpact - the output of MallotImpoact function
		   				   The velocity of all the points on the chime at impact
		   				   It is currently 3len(positions)x1, need reshape

	Output: w[indexW] - the eigenvalue thatis corresponding to the eigenvector in the calculation
						This is also the wavelength we are using in the airsolver
			desiredDerivsMat - the matrix for desired derivatives
	"""
	

	# Need to reorganize the eigenvectors from having x, y, z on the same column
	# e.g. (if len(positions) = n, the current v is 3nx3n and each column is 3nx1)
	# to a matrix having each x, y, z on the same row (nx3)
	vMat = np.reshape(v[:,indexW], (len(positions), 3))

	# Add mallotImpact scaler
	# Need to test initialImpact cannot be all 0
	reshapedImpact = np.reshape(initialImpact, (len(positions), 3))

	# print(vMat.shape == reshapedImpact.shape) #True
	vMatScaler = np.zeros((len(positions), 1))

	for i in range(len(positions)):
		vMatScaler[i] = np.dot(vMat[i], reshapedImpact[i])

	# Elementwide multiplication between vMatScaler and vMat
	scaledVMat = vMat*vMatScaler
	# print("scaledVMat dimension = " + str(scaledVMat.shape))

	desiredDerivsMat = np.zeros((len(positions), 1))

	for i in range(len(positions)):
		desiredDerivsMat[i] = np.dot(scaledVMat[i], neumannNormals[i])
	#print(desiredDerivsMat)
	#print(desiredDerivsMat.shape)

	return w[indexW], desiredDerivsMat

positions, triangleSet, triNormVecs, w, v = calculateEigenvectors("newChimeR.0127D4.stl", 128*10**9, 1, 0)
neumannNormalVecs = neumannNormals(positions, triangleSet, triNormVecs)
v2 = chimeVelocity(0.043, 0.002, 0)
initialImpact = mallotImpact(positions, np.array([0, .0127, .0535]), v2, .015)
print("neumannNormal dimension = " + str(neumannNormalVecs.shape))
print(desiredDerivs(positions, w, v, 0, neumannNormalVecs, initialImpact))

