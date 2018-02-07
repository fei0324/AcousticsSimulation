import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import wave
import sys
from scipy.io.wavfile import read  # reading wav files
import math
import cmath
import pylab
from compareAperture import compareAperture
from SyntheticAperture import syntheticAperture
import os # for opeining files in loop #change working diectory, count files in directory
import glob # looping throught all files in folder

"""
Compare wave files from adjacent positions
Input:  start = the starting time of the sinal (seconds) 
		end = the end time of the sinal (seconds)  
		slow = the slow time of the sinal (seconds)  
		fast = the fast time of the sinal (1xP seconds)  
Output: energy difference between points
"""

def main():
	
	#print "what is start time?, 0"
	start = 0 # input()
	#print "what is end time?, 1"
	end = 1 # input()
	#print "what is slow time?, .01"
	slow = 0.01 # input()
	#print "what is fast time?, .001"
	fast = 0.001 # input()
	#print "what is sample rate?, 1, 6"
	SampleRateRedux = 1 # input()    

	cfd = os.path.abspath(__file__)	# gets the path to this current file
	baseP= cfd 
	basePa = str(baseP.split('\\')[0:-1])# removes the last folder of the path
	basePat = '\\'.join(baseP.split('\\')[0:-1])
	basepath = os.path.join(basePat,"DataJustTwo")
	print "  "
	print "the data is taken from:"
	print basepath
	
	os.chdir(basepath)  
	fillist =  os.listdir(basepath) 
	
	nbr = len([name for name in os.listdir(basepath) if os.path.isfile(os.path.join(basepath,name))]) 
	print "  "
	print 'the files in the folder are:'
	print fillist
	print "  "
	print "start time: {0}".format(start)
	print "end time: {0}".format(end)
	print "slow time: {0}".format(slow)
	print "fast time: {0}".format(fast)
	print "sample rate redux: {0}".format(SampleRateRedux)
	
	fafotr1 = {}
	ttMat, fftt, fafotr1['fftt1'] = syntheticAperture(start, end, slow, fast, (read(fillist[0])), SampleRateRedux)
	ttMat, fftt, fafotr1['fftt2'] = syntheticAperture(start, end, slow, fast, (read(fillist[1])), SampleRateRedux)

	print '  '
	print "the number of files in the full directory is: {0}".format(nbr)
	print 'the first file : {0}'.format(fillist[0])
	print 'the the second file: {0}'.format(fillist[1])

	row1 = fafotr1['fftt1'].shape[0] 
	col1 = fafotr1['fftt1'].shape[1]  
	
	energyMat = np.zeros((row1,col1), dtype=complex)
	for i in range(0, row1):	
		for j in range(0, col1):  
			mat1 = fafotr1['fftt1'] 
			mat2 = fafotr1['fftt2'] 
			energyMat[i,j] = 20*np.abs((np.log10(np.linalg.norm(mat1[i,j]))-np.log10(np.linalg.norm(mat2[i,j]))))
	eAvgMatn = np.average(energyMat) 
	print '  '
	print 'the energy difference is:'
	print eAvgMatn

if __name__ == '__main__':
	main()

