import math
import numpy as np
from stl import mesh

from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib import cm

from subdivision import *
from lengthSolver import *
from pointCollection import *
from mijMat import *
from outsideMat import *
from diagonalMat import *


def eigenvectorLength(BigMatrix, indexW, positions):

	"""
	Preparation for plotting eigenvectors

	Input: BigMatrx = outsideMatrix + diagonalMatrx
		   indexW = the index of eigenvalue and the corresponding index of the eigenvector
		   positions = list of all unique points
	Output: A list of lengths of eigenvectors
	"""

	w, v = np.linalg.eig(BigMatrix)
	listOfLength = np.zeros(len(positions))
	indexOfList = 0

	for i in range(len(v[:,indexW])):
		if i%3 == 0:
			xyz = np.array([v[i,indexW], v[i+1,indexW], v[i+2,indexW]])

			listOfLength[indexOfList] = np.linalg.norm(xyz)
			indexOfList += 1

	return listOfLength

def plot(filename, youngs, n):

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

	listOfLength0 = eigenvectorLength(BigMatrix, 0, positions)
	listOfLength1 = eigenvectorLength(BigMatrix, 1, positions)
	listOfLength2 = eigenvectorLength(BigMatrix, 2, positions)
	listOfLength3 = eigenvectorLength(BigMatrix, 3, positions)


	fig = plt.figure()
	ax0 = fig.add_subplot(221, projection='3d')
	ax0.set_title("Eigenvector 0")
	ax1 = fig.add_subplot(222, projection='3d')
	ax1.set_title("Eigenvector 1")
	ax2 = fig.add_subplot(223, projection='3d')
	ax2.set_title("Eigenvector 2")
	ax3 = fig.add_subplot(224, projection='3d')
	ax3.set_title("Eigenvector 3")
	
	xs = []
	ys = []
	zs = []

	for i in range(len(positions)):
		xs.append(positions[i][0])
		ys.append(positions[i][1])
		zs.append(positions[i][2])


	ax0.scatter(xs, ys, zs, c=listOfLength0, cmap=cm.cool, s=50)
	ax1.scatter(xs, ys, zs, c=listOfLength1, cmap=cm.cool, s=50)
	ax2.scatter(xs, ys, zs, c=listOfLength2, cmap=cm.cool, s=50)
	ax3.scatter(xs, ys, zs, c=listOfLength3, cmap=cm.cool, s=50)

	w, v = np.linalg.eig(BigMatrix)
	print("eigenvalues = " + str(v))
	
	plt.show()
