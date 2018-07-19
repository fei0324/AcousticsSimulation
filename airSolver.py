import math
import numpy as np
import scipy.io.wavfile
from stl import mesh

from pointCollection import *
from neumannNormals import *
from desiredDerivs import *


def airSolver(wavelength,sourcePoints,neumannPoints,neumannNormals,desiredDerivs):

	"""
	Construct a solution for the scalar Helmholtz equation with mixed Dirichlet-Neumann 
	boundary conditions using the boundary element method. There is a close relationship
	between the airsolver and the eigenvalues and eigen vectors we obtain from the elstic
	solver. If there are n distince points on the object, we would obtain 3n eigenvalues
	and eigenvectors, then we need to reorganize the eigenvectors for each eigenvalue and
	run airsolver 3n times. Wavelength are the eigenvalues and desiredDerivs are the dot
	product of the neumann normals and the eigenvecots.

	Input: wavelength    = operating wavelength (meters)
	     sourcePoints    = location of point sources to solve (PxD, meters)
	     neumannPoints   = locations of points where normal derivatives are specified (NxD, meters)
	     neumannNormals  = normal vectors at each Neumann point (NxD, unit vector)
	     desiredDerivs   = the value of the derivative of the field at each Neumann point (Nx1, field/meter)

	Output: sources = values of each source (Px1)
	"""

	# Wavenumber
	k = 2*math.pi/wavelength

	# Neumann subproblem
	if neumannPoints.size != 0:
		# Normalize supplied normal vectors (NxD)
		for i in range(len(neumannNormals)):
			neumannNormals[i] = neumannNormals[i]/np.linalg.norm(neumannNormals[i])

		# Construct vectors from each source point to each Neumann point (NxPxD)
		neumannRangeVector = np.zeros(shape=(len(neumannPoints),len(sourcePoints),len(neumannPoints[0])), dtype=complex)
		for i in range(len(neumannPoints)):
			for j in range(len(sourcePoints)):
				neumannRangeVector[i,j] = neumannPoints[i] - sourcePoints[j]

		# Distance source to Neumann points (NxP)
		neumannRange = np.zeros((len(neumannRangeVector[:,0]),len(neumannRangeVector[0,:])), dtype=complex)
		for i in range(len(neumannRangeVector[:,0])):
			for j in range(len(neumannRangeVector[0,:])):
				neumannRange[i,j] = np.linalg.norm(neumannRangeVector[i,j])

		# Vector source to Neumann, projected onto local normals (NxP)
		neumannProj = np.zeros((len(neumannRangeVector[:,0]),len(neumannRangeVector[0,:])), dtype=complex)
		for i in range(len(neumannRangeVector[:,0])):
			for j in range(len(neumannRangeVector[0,:])):
				neumannProj[i,j] = np.dot(neumannRangeVector[i,j],neumannNormals[i])

		# Construct Neumann submatrix (NxP)
		neumannMat = np.zeros((len(neumannRangeVector[:,0]),len(neumannRangeVector[0,:])), dtype=complex)
		for i in range(len(neumannRangeVector[:,0])):
			for j in range(len(neumannRangeVector[0,:])):
				neumannMat[i,j] = np.exp(-1j*k*neumannRange[i,j])/(4*math.pi*neumannRange[i,j]**2)*neumannProj[i,j]*(1-1/neumannRange[i,j])

	if neumannPoints.size != 0:
		print(neumannMat.shape)
		print(desiredDerivs.shape)
		sources = np.linalg.lstsq(neumannMat,desiredDerivs)[0]
	return sources

"""
wavelength1 = 1 
sourcepoints1 = np.array([[0,0],[1,0],[-1,0]])
neumanpoints1 = np.array([[0,1],[1,1],[-1,1]])
neumannormals1 = np.array([[-1,0],[-1,0],[-1,0]])
desiredderivs1 = np.array([[1],[0],[0]])
"""
file_mesh = mesh.Mesh.from_file("newChimeR.0127D4.stl")
positions = pointCollection(file_mesh.vectors)
wavelength1, desiredderivs1 = desiredDerivs("newChimeR.0127D4.stl", 128*10**9, 0, 0)

sourcepoints1 = np.array([[-0.2,0,-0.3535],[-0.1,-0.1*np.sqrt(3),-0.3535],[0,-0.2,-0.3535],[0.1,-0.1*np.sqrt(3),-0.3535],[0.2,0,-0.3535]])
neumannpoints1 = np.array(positions)
neumannnormals1 = neumannNormals(positions, file_mesh.vectors, file_mesh.normals)

print(airSolver(wavelength1, sourcepoints1, neumannpoints1, neumannnormals1, desiredderivs1))

# All the dimensions seem to match up okay but the result is odd 6/27/2018

# wavelength is eigen values
# run 150 times
