import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import wave
import sys
from scipy.io.wavfile import read
from scipy import fftpack, ndimage
import math 
import re
 
"""
Compute the synthetic appeture matrix
	Input:  start = the starting time of the sinal (seconds) 
		end = the end time of the sinal (seconds)  
		slow = the slow time of the sinal (seconds)  
		fast = the fast time of the sinal (1xP seconds)  
		sound = wave file 
Output: matrix of pressures (NxP)
		matrix of fast fourier transform in both directions of pressures (NxP)
		matrix of log of fast fourier transform in both directions of pressures (NxP)
"""
def syntheticAperture(start, end, slow, fast, sound, SampleRateRedux):
	# the frequency will always be 44100 when using wave files 
	hz = 44100 
	samplerate = 44100/SampleRateRedux
	# convert varibles from seconds to indices in file
	iterations = int(float((end-start-fast)*(1/slow)))    
	StStart = int(float(start*samplerate))
	StSlow = int(float(slow*samplerate))
	StFast = int(float(fast*samplerate))

	# imports the wave file
	l = np.array(sound[1],dtype=float)
	b = l[0::SampleRateRedux]
	col3 = StFast
	ttMat = np.zeros((iterations, col3), dtype=complex)
	for j in range(0, iterations):
		for i in range(0, col3):
			ttMat[j,i] = b[i+(j*StSlow)] 
	fftt = fftpack.fft2(ttMat) 
	fftlog = np.array(np.log10(fftt), dtype=complex) 
	return ttMat, fftt, fftlog # forPlotBetweenPositions #return fftlog # was for AnalysisBeRdMaOp4 , now has been modified

