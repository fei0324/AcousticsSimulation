import math
import numpy as np

from stl import mesh


def subdivision(pt1, pt2, pt3, n):

	"""
	Convert STL data into unit normal vectors and points on the triangles

	Input: Triangles (three 3d points) (3 numpy arrays)
		   a number of subdivisions to perform
	Output: Points on those triangles
			unit normal vectors points
	"""

	# find unit normal vector given three points on a plane
	vectorU = pt2 - pt1
	vectorV = pt3 - pt1
	normalVector = np.cross(vectorU, vectorV)
	#print(normalVector)
	unitNorVec = normalVector/np.linalg.norm(normalVector)
	#print(unitNorVec)

	# find subdivision points in barycentric coordinates
	points = [] #points includes the vertices of the original triangle
	for i in range(0, 2**n+1):
		for j in range(0, 2**n+1-i):
			points.append(pt1 + (i/2.**n)*vectorU + (j/2.**n)*vectorV)

	triangleSet = []
	x = 0
	y = 2**n

	for i in range(2**n+1, 1, -1):
		for j in range(x,y):

			tri = []
			tri.append(points[j])
			tri.append(points[j+1])
			tri.append(points[j+i])
			triangleSet.append(tri)

		x = x+i
		y = y+i-1

		for k in range(x,y):

			tri = []
			tri.append(points[k])
			tri.append(points[k+1])
			tri.append(points[k+1-i])
			triangleSet.append(tri)

	norVecSet = []

	for i in range(len(triangleSet)):
		norVecSet.append(unitNorVec)


	return points, triangleSet, norVecSet


def subdivide_reconstruct(oriTriangleSet,indices,n):

	"""
	Goal: Subdivide the triangles of given indices n times, replace the
		  subdivided triangles with new points.
	
	Input: oriTriangleSet = Original triangle set after reading the stl file
		   indices = a list of indices of the triangles that need to be divided
		   n = the number of times of subdivision
	Output: a new triangle set in the same format as stl file vectors.
	"""
	numberOfTriangleSets = len(oriTriangleSet) + len(indices)*(4**n) - len(indices)
	newTriangleSet = np.zeros((numberOfTriangleSets, 3, 3))
	
	# for j in range(len(indices)):
	# 	index = indices[j]
		
	# 	for i in range(len(oriTriangleSet))
			
	# 		if i == index:
	# 			# subdivide
	# 			points, triangleSet, norVecSet = subdivision(oriTriangleSet[index][0], oriTriangleSet[index][1], oriTriangleSet[index][2], n)
	# 			# replace the old triangle with subdivided triangles
	# 			for k in range(i, i+4**n):
	# 				newTriangleSet[k] = triangleSet[k-i]

	# 		# fill the rest with old triangles
	# 		else:

	# 			# Need to shift indices over based on how many subdivisions we've done already 
				
	# 			# j+1 is the number of subdivisions we have completed
	# 			# Since we are replacing the old instead of only adding, we are subtracting
	# 			# the number of subdivisions after the shifting over 4**n

	# 			newTriangleSet[i+4**n-j-1] = oriTriangleSet[i]


	listIndex = 0
	i = 0
	counter = 0

	while i < len(oriTriangleSet):

		if listIndex == len(indices):

			newTriangleSet[counter] = oriTriangleSet[i]

			i += 1
			counter += 1
			# print("counter = " + str(counter))
			# print("listIndex = " + str(listIndex))
			# print("i = " + str(i))

		elif i == indices[listIndex]:
			# subdivide
			points, triangleSet, norVecSet = subdivision(oriTriangleSet[listIndex][0], oriTriangleSet[listIndex][1], oriTriangleSet[listIndex][2], n)
			# replace the old triangle with subdivided triangles
			for k in range(counter, counter+4**n):
				newTriangleSet[k] = triangleSet[k-counter]
			
			listIndex += 1
			i += 1
			counter += 4**n
			# print("subdivided triangle: " + str(i) + " counter = " + str(counter))
			# print("i = " + str(i))

		else:

			# Need to shift indices over based on how many subdivisions we've done already 
			# listIndex is the number of subdivisions we have completed
			# Since we are replacing the old instead of only adding, we are subtracting
			# the number of subdivisions after the shifting over 4**n

			newTriangleSet[counter] = oriTriangleSet[i]

			i += 1
			counter += 1
			# print("counter = " + str(counter))
			# print("listIndex = " + str(listIndex))
			# print("i = " + str(i))

	return newTriangleSet

# chime_mesh = mesh.Mesh.from_file("newChimeR.0127D4.stl")
# oriTriangleSet = chime_mesh.vectors

# newTriangleSet = subdivide_reconstruct(oriTriangleSet,[0, 1, 10, 13, 56], 1)
# print(newTriangleSet)
# print(newTriangleSet.shape)
# print(oriTriangleSet.shape)









