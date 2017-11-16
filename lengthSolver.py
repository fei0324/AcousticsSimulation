import math
import numpy as np
from stl import mesh

def lengthSolver(triangles,triNormVecs,forceVecs):

	"""
	Preparation for Young's Modulus:
		Find the intersection of the extension of the force
		and a triangle on the other side of the object.
		Compute the distance.
	Input: triangles = triangle vectors from the input stl file
		   triNormVecs = normal vectors for each triangle from the stl file
		   forceVecs = a list of force vectors on every triangle
	Output: The length of L for Young's Modulus
	"""

	u = np.zeros((len(triangles),3))
	v = np.zeros((len(triangles),3))
	centroid = np.zeros((len(triangles),3))
	Lmat = np.zeros((len(triangles),len(triangles)))
	Llist = np.zeros(len(triangles))
	#Xmat = np.zeros((len(triangles),len(triangles)))

	# Vector u, vector v and force vector starting point (approximating with the centroid of triangles)
	for i in range(len(triangles)):
		u[i] = triangles[i][1] - triangles[i][0]
		v[i] = triangles[i][2] - triangles[i][0]
		centroid[i] = triangles[i][0] + (1/3)*u[i] + (1/3)*v[i]

	for i in range(len(forceVecs)):
		for j in range(len(triNormVecs)):

			# If the force vector is parallel to the triangle plane, assign -10
			if abs(np.dot(forceVecs[i], triNormVecs[j])-0.)<1e-05:
				Lmat[i,j] = -10
			
			else:
				# Find intersection point on the plane
				numer = np.dot(triNormVecs[j],triangles[j][0]-centroid[i])
				denom = np.dot(triNormVecs[j],forceVecs[i])
				t = numer/denom
				intersectPoint = centroid[i] + t*forceVecs[i]

				# Verify if the point is in the triangle
				q = intersectPoint - triangles[j][0]

				a = np.transpose(np.array([u[j],v[j]]))

				x = np.linalg.lstsq(a,q)[0]

				if -1e-05<=x[0]<=1+1e-05 and -1e-05<=x[1]<=1+1e-05 and -1e-05<=x[0]+x[1]<=1+1e-05:
					l = np.linalg.norm(intersectPoint - centroid[i])
					Lmat[i,j] = l

				# If the intersection point if outside of the triangle, assign -20
				else:
					Lmat[i,j] = -20

	for i in range(len(triangles)):
		Llist[i] = max(Lmat[i])

	return Llist, Lmat