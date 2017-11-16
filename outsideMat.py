import math
import numpy as np

def outsideMat(positions, Mij):

	"""
	Input: positions = all the points after subdivision
		   Mij = Mij matrix calculated from the function mijMat

	Output: OutsideMat

	"""

	outsideMat = np.zeros((3*len(Mij),3*len(Mij)),dtype=complex)

	# i, j for Mij index, a, b for OTMat index
	for a in range(3*len(Mij)):
		for b in range(3*len(Mij)):
			i = a/3
			j = b/3
			outsideMat[a,b] = (-1)*Mij[i,j]*(positions[i][a%3]-positions[j][a%3])*(positions[i][b%3]-positions[j][b%3])

	return outsideMat


