import math
import numpy as np
from stl import mesh

from pointCollection import *
from chimeVelocity import *
from subdivision import *
from stl import mesh

def mallotImpact(positions, impactCoor, v2, r):

	"""
	Goal: Generate the initial impact of every point on the object.

	Input: positions = a list of distinct points of the object after subdivision.
	       impactCoor = the coordinte of the impact position, based on the STL file coordinate system [x, y, z]
	       v2 = chime velocity at impact, which gives us a measurement of the magnitude of the impact
	       r = radius of impact

	Output: A list of initial impacts for every point on the object.
	"""
	# use positions from pointCollection

	initialImpact = np.zeros(len(positions)*3)

	for i in range(0, len(positions)):

		#print str(i) + "  " + str(np.linalg.norm(positions[i] - impactCoor))
		# Give a value for initial impact for points that are in a 5mm radius of the impact coordinate
		if np.linalg.norm(positions[i] - impactCoor) < r:

			# Hitting on the y-axis
			initialImpact[3*i] = 0
			initialImpact[3*i+1] = v2
			initialImpact[3*i+2] = 0

		else:
			initialImpact[3*i] = 0
			initialImpact[3*i+1] = 0
			initialImpact[3*i+2] = 0

		#print "{}   {}".format(i, initialImpact[3*i+1])

	return initialImpact

"""
file_mesh = mesh.Mesh.from_file("chimeH507R12.7.stl")

oriTriangleSet = file_mesh.vectors
#triNormVecs = file_mesh.normals

triangleSet = []
triNormVecs = []

for i in range(len(oriTriangleSet)):
	points, singleTriangleSet, singleNorVecSet = subdivision(oriTriangleSet[i][0], oriTriangleSet[i][1], oriTriangleSet[i][2], 3)

	for j in range(len(singleTriangleSet)):
		triangleSet.append(singleTriangleSet[j])
		triNormVecs.append(singleNorVecSet[j])


cylinder_mesh = mesh.Mesh.from_file("chimeH507R12.7.stl")
#print cylinder_mesh.vectors
positions = pointCollection(triangleSet)
#print "length of positions = " + str(len(positions))
v2 = chimeVelocity(0.043, 0.002, 0)
print "v2 = " + str(v2)
mallotImpact(positions, np.array([0, 12.7, 53.5]), v2, 25)
"""