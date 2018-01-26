import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import wave
import sys   # used for  sys.path.append()
from scipy.io.wavfile import read  # reading wav files
import scipy.io.wavfile
import math
import cmath
import pylab
import os # for opeining files in loop #change working diectory, count files in directory
import os.path
import glob # looping throught all files in folder
from autocropper import autoCropper
from transferFile import transfer
"""
Crop .wav files and rename them
Input:  roundno = the number of the round of recording 
		startP = the position in the round to start on
		endP = the position in the round to end on
""" 
def main():
	
	print "number of positions?, 1, 2, ... 10 (type 4) "
	posno = input()    
	startR = 1
	print "number of rounds?, 1, 2, 3, ... (type 3)"  
	endR = input()  

	startRn = startR -1
	endRn = endR

	# Tells program to look in folder where program is saved
	current_file_path = __file__ #import os  
	cfd = os.path.abspath(__file__)	#
	current_file_dir = os.path.relpath(__file__) #

	# Removes last part of string and attaches name of raw data folder
	baseP= cfd 
	basePa = str(baseP.split('\\')[0:-1])
	basePat = '\\'.join(baseP.split('\\')[0:-1])
	basepath = os.path.join(basePat,"DataBefore")	#basepath = basePat

	# creates fillist of files in raw data folder
	nbr=len([name for name in os.listdir(basepath) 
		if os.path.isfile(os.path.join(basepath, name))])  # 
	os.chdir(basepath) #
	fillist =  os.listdir(basepath) 

	# creates a dictionary/list? named "positions" out of files in the folder located at path named "fillist"
	positions = {}
	for x in range(1,5):
		positions[x]=[k for k in fillist if 'p{0}'.format(x) in k] #sub = positions[posno]
	
	print "the number of files in the full directory is: {0}".format(nbr)
	print 'the names of files in full directory are:'
	print fillist
	print 'the contense of the dictionary positions:'
	print positions
	#
	fs = 44100
	
	# reads the raw files into a dictionary named "lfile1"
	lfile1 = {}
	for k in range(0, posno): # loops through positions (pXseries.wav files in folder) # for k in range(0, 4):
		print "the file is:" #print sub
		print fillist[k]
		lfile1['log{0}'.format(k+1)] = scipy.io.wavfile.read(fillist[k]) 
	print " the fillist is:"
	print fillist
	print " the fillist is:"
	print fillist[0]
	print fillist[1]
	print fillist[2]
	print fillist[3]
	print " the lfile1 is:"
	print lfile1['log1']
	print lfile1['log2']
	print lfile1['log3']
	print lfile1['log4']

	# creates cropped versions of the raw files and puts them in same folder
	# unnecessarly?? creates a dictionary named "cropFile"
	cropFile = {}
	for o in range(0, posno): # loop through positions # for o in range(0, 4): # for o in range(startPosNo, endPosNo): # for o in range(startRn, endRn): 
		cropFile['cropedP{0}'.format(o+1)] = autoCropper(fs, lfile1['log{0}'.format(o+1)], (o+1), posno, startRn, endRn, positions) 
	print ' the dictinoary just ....'  #print 'the dictionary just created is as follows: {0}'.format(cropFile) 
	
	#transfers the cropped files to new folder
	for s in range(0, posno): #loop through possitions # for s in range(0, 4):
		for q in range(startRn+1, endRn+1): # loop through rounds # for q in range(0+1, 3+1): # for q in range(startRn+1, endRn+1):
			transfer('triMr{0}p{1}.wav'.format(q, s+1), basepath) # transfer('triMr{0}{1}.wav'.format(q, posno), basepath) 

if __name__ == '__main__':
	main()


