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
	ttMat1, fftt1, fafotr1['fftt1'] = syntheticAperture(start, end, slow, fast, (read(fillist[0])), SampleRateRedux)
	ttMat2, fftt2, fafotr1['fftt2'] = syntheticAperture(start, end, slow, fast, (read(fillist[1])), SampleRateRedux)

	print '  '
	print "the number of files in the full directory is: {0}".format(nbr)
	print 'the first file : {0}'.format(fillist[0])
	print 'the the second file: {0}'.format(fillist[1])

	f , axarr = plt.subplots(2, 3, sharex=False)
	eMat, eAvg = compareAperture(start, end, slow, fast, SampleRateRedux, (read(fillist[0])), (read(fillist[1])))
	axarr[0,0].imshow(abs(ttMat1))
	axarr[0,1].imshow(abs(fftt1)) 
	axarr[1,0].imshow(abs(ttMat2))
	axarr[1,1].imshow(abs(fftt2)) 
	axarr[0,2].imshow(abs(eMat))
	plt.suptitle('Compare Two files', fontsize=30)
	plt.show()

if __name__ == '__main__':
	main()

