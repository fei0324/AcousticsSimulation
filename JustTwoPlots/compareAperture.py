import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import wave
import sys
from scipy.io.wavfile import read
from scipy import fftpack, ndimage
import math
import cmath
from SyntheticAperture import syntheticAperture
import pylab

"""
Compute the synthetic appeture matrix
Input:  start = the starting time of the sinal (seconds) 
		end = the end time of the sinal (seconds)  
		slow = the slow time of the sinal (seconds)  
		fast = the fast time of the sinal (1xP seconds)  
	sound1 = simulated wave file
	sound2 = real world wave file 
Output: matrix of pressures (Px )
"""
def compareAperture(start, end, slow, fast, SampleRateRedux, sound1, sound2):

	cc1, fftt1, fftlog1 = syntheticAperture(start, end, slow, fast, sound1, SampleRateRedux)
	cc2, fftt2, fftlog2 = syntheticAperture(start, end, slow, fast, sound2, SampleRateRedux)

	row1 = fftt1.shape[0] 
	col1 = fftt1.shape[1]
	row2 = fftt2.shape[0]
	col2 = fftt2.shape[1]

	energyMat = np.zeros((row1,col1), dtype=complex)
	for i in range(0, row1):	
		for j in range(0, col1):
			energyMat[i,j] = 20*np.abs((np.log10(np.linalg.norm(fftt1[i,j]))-np.log10(np.linalg.norm(fftt2[i,j]))))
	energyAvg = np.average(energyMat)
	return energyMat, energyAvg
	#return energyAvg


