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


def subdivide_reconstruct(oriTriangleSet,oriNormVecSet,indices,n):

	"""
	Goal: Subdivide the triangles of given indices n times, replace the
		  subdivided triangles with new points.
	
	Input: oriTriangleSet = Original triangle set after reading the stl file
		   oriNormVecSet = Original triangle normals from the stl file
		   indices = a list of indices of the triangles that need to be divided
		   n = the number of times of subdivision
	Output: a new triangle set in the same format as stl file vectors.
	"""
	numberOfTriangleSets = len(oriTriangleSet) + len(indices)*(4**n) - len(indices)
	newTriangleSet = np.zeros((numberOfTriangleSets, 3, 3))
	newNormVecSet = np.zeros((numberOfTriangleSets, 3))

	# listIndex is the index in the list "indices"
	listIndex = 0
	# i is the index in oriTriangleSet
	i = 0
	# counter is the pointer to the current position to be filled in the newTriangleSet
	counter = 0

	while i < len(oriTriangleSet):

		if listIndex == len(indices):

			newTriangleSet[counter] = oriTriangleSet[i]
			newNormVecSet[counter] = oriNormVecSet[i]

			i += 1
			counter += 1

		elif i == indices[listIndex]:
			# subdivide
			points, triangleSet, norVecSet = subdivision(oriTriangleSet[listIndex][0], oriTriangleSet[listIndex][1], oriTriangleSet[listIndex][2], n)
			# replace the old triangle with subdivided triangles
			for k in range(counter, counter+4**n):
				newTriangleSet[k] = triangleSet[k-counter]
				newNormVecSet[k] = norVecSet[k-counter]
			
			listIndex += 1
			i += 1
			counter += 4**n

		else:

			# Need to shift indices over based on how many subdivisions we've done already 
			# listIndex is the number of subdivisions we have completed
			# Since we are replacing the old instead of only adding, we are subtracting
			# the number of subdivisions after the shifting over 4**n

			newTriangleSet[counter] = oriTriangleSet[i]
			newNormVecSet[counter] = oriNormVecSet[i]

			i += 1
			counter += 1

	return newTriangleSet, newNormVecSet

def calculate_centroid_of_triangle(pt1, pt2, pt3):

	centroid = np.zeros(3)

	centroid[0] = (pt1[0] + pt2[0] + pt3[0])/3
	centroid[1] = (pt1[1] + pt2[1] + pt3[1])/3
	centroid[2] = (pt1[2] + pt2[2] + pt3[2])/3

	return centroid

def search_triangles(oriTriangleSet, impactCoor):

	"""
	Goal: Serach for the 6 closest triangles around the impact coordinate to subdivide.
	
	Input: oriTriangleSet = Original triangle set after reading the stl file
	       impactCoor = the coordinate of the impact point
	Output: a list of indices of the 6 triangles we would like to subdivide
	"""


	# Calculate the center of the triangle
	# Create a dictionary {'index': 'distance'} where the value is the distance
	# between the center of the triangle and the impact coordinate
	distanceDict = {}

	for i in range(len(oriTriangleSet)):

		centroid = calculate_centroid_of_triangle(oriTriangleSet[i][0], oriTriangleSet[i][1], oriTriangleSet[i][2])
		distanceDict[i] = np.linalg.norm(centroid - impactCoor)

	# Sort the dictionary based on distance
	sortedIndices = sorted(distanceDict, key=distanceDict.__getitem__)

	# Pick the minimum 6 indices and return them in a list
	return sortedIndices[:6]



# chime_mesh = mesh.Mesh.from_file("newChimeR.0127D4.stl")
# oriTriangleSet = chime_mesh.vectors
# oriNormVecSet = chime_mesh.normals

# indices = search_triangles(oriTriangleSet, np.array([0,0,0]))

# newTriangleSet, newNormVecSet = subdivide_reconstruct(oriTriangleSet, oriNormVecSet, indices, 1)
# print(len(newTriangleSet))
# print(len(newNormVecSet))