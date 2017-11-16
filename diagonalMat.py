import numpy as np 


def diagonalMat(positions,Mij):

	"""
	goal: to take the position vectors and the constant matrix and output the diagonal terms for the eigen value problem
	input: position vectors in a 3XN matrix
		   constant terms in a NXN matrix
	output: a 3NX3N matrix with zeros everywhere but the diagonal 3 by 3 blocks
	"""

	n = len(positions)
	dim = len(positions[0])

	#n is the number of masses
	#dim is the number of terms in the vectors
	nn = dim*n
	diagonalMat = np.zeros((nn,nn),dtype=complex)
	for i in range(0,nn):
		if i % dim == 0:
			#k is what block we are in
			k = i/dim
			#cooi is the coordinate of the effected mass
			for cooi in range(0,dim):
				#cooj is the coordinate of the effecting mass
				for cooj in range(0,dim):
					b = 0
					#effmass is which mass is doing the effecting
					for effmass in range(0,n):
						#the algorythmn should run through all the different masses for each term with the coorisponding coordinates
						a = Mij[k,effmass]*((positions[k][cooi]-positions[effmass][cooi])*(positions[k][cooj]-positions[effmass][cooj]))
						b= b+a
					diagonalMat[i+cooi][i+cooj] = b

	return diagonalMat