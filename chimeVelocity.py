import math
import numpy as np
import scipy as sp


def u1(l, m1, theta0, theta):

	"""
	Goal: calculate the velocity of the pendulum at impact

	Input: l = length of the pendulum string (cm)
		   m1 = mass of the pendulum (kg)
		   theta0 = initial angle (degree)
		   theta = angle at impact (degree)
	Output: u1 = velocity of pendulum at impact
	"""

	# using the scipy constant standard acceleration of gravity
	u1 = np.sqrt(2*sp.g*l*(np.cos(theta)-np.cos(theta0))/m1)

	return u1

def chimeVelocity(m1, m2, u2):

	"""
	Goal: Calculate the velocity of the chime when struck by the mallot

	Input: m1 = mass of the pendulum (kg)
		   m2 = mass of the piece of the chime that is hit by the pendulum (kg)
		   u2 = initial velocity of the chime
	Output: v2 = velocity of the chime at impact
	"""

	# u1 calculates the velocity of the pendulum at impact 
	u1 = u1(45.72, 0.043, 20, -60)

	v2 = (u2*(m2-m1) + 2*m1*u1)/(m1+m2)

	return v2


print chimeVelocity(0.043, 0.002, 0)