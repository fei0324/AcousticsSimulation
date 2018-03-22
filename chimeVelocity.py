import math
import numpy as np
import scipy.constants


def chimeVelocity(m1, m2, u2):

	"""
	Goal: Calculate the velocity of the chime when struck by the mallot

	Input: m1 = mass of the pendulum (kg)
		   m2 = mass of the piece of the chime that is hit by the pendulum (kg)
		   u2 = initial velocity of the chime
	Output: v2 = velocity of the chime at impact
	"""

	# u1 calculates the velocity of the pendulum at impact 
	u1 = calculateu1(.4572, 0.043, np.radians(20.), np.radians(-60.))

	v2 = (u2*(m2-m1) + 2*m1*u1)/(m1+m2)

	return v2

def calculateu1(l, m1, theta, theta0):

	"""
	Goal: calculate the velocity of the pendulum at impact

	Input: l = length of the pendulum string (m)
		   m1 = mass of the pendulum (kg)
		   theta0 = initial angle (radian)
		   theta = angle at impact (radian)
	Output: u1 = velocity of pendulum at impact
	"""

	# using the scipy constant standard acceleration of gravity

	u1 = np.sqrt(2*scipy.constants.g*l*(np.cos(theta)-np.cos(theta0))/m1)

	return u1


#print chimeVelocity(0.043, 0.002, 0)