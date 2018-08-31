import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

from stl import mesh

from subdivision import (subdivision,
						subdivide_reconstruct,
						calculate_centroid_of_triangle,
						search_triangles,)
from pointCollection import pointCollection


chime_mesh = mesh.Mesh.from_file("newChimeR.0127D4.stl")
oriTriangleSet = chime_mesh.vectors
oriNormVecSet = chime_mesh.normals

impact_coord = np.array([0, .0127, .0535])
indices, centroids = search_triangles(oriTriangleSet, impact_coord)
#print(centroids)
newTriangleSet, newNormVecSet = subdivide_reconstruct(oriTriangleSet, oriNormVecSet, indices, 2)
new_points = pointCollection(newTriangleSet)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

xs = []
ys = []
zs = []

# plot subdivided triangles
for point in new_points:
	xs.append(point[0])
	ys.append(point[1])
	zs.append(point[2])
ax.scatter(xs, ys, zs)

plt.hold(True)

# plot centroids
cxs = []
cys = []
czs = []


ax.scatter(impact_coord[0], impact_coord[1], impact_coord[2], s=200)

test_centroids = [centroids[24], centroids[25], centroids[27]]
for centroid in test_centroids:
	cxs.append(centroid[0])
	cys.append(centroid[1])
	czs.append(centroid[2])

	linexs = [impact_coord[0]]
	lineys = [impact_coord[1]]
	linezs = [impact_coord[2]]

	linexs.append(centroid[0])
	lineys.append(centroid[1])
	linezs.append(centroid[2])

	ax.plot(linexs, lineys, linezs, color='r')
	plt.hold(True)


ax.scatter(cxs, cys, czs, s=80, c='#FFFF33')
plt.hold(True)

# Plot the searched trianbles

point_order = [0,1,2,0]
test_indices = [24,25,27]

for index in test_indices:
	triangle = oriTriangleSet[index]
	triangle_outline_xs = [triangle[i][0] for i in point_order]
	triangle_outline_ys = [triangle[i][1] for i in point_order]
	triangle_outline_zs = [triangle[i][2] for i in point_order]
	ax.plot(triangle_outline_xs, triangle_outline_ys, triangle_outline_zs, color='g')
	plt.hold(True)

	
plt.show()