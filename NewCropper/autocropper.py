import numpy as np
import math
#import wave  # one way to write wave files, may not be necessary? (I think this is if we are generating it from raw info)
from scipy import signal as sg # to do convolution
import scipy.io.wavfile # write wave files.  I think this is the better way?\
import os.path # this is for changeing path to save it to

"""
Crop .wav files and rename them
Input:  start = the starting time of the sinal (seconds) 
		sound = the .wav file to be cropped
Output: soundOut = cropped .wav file

###### below is explination for algorithum that selects point to crop ####
1000 is a number b/c the first few seconds or so data points are 
zero and so any number is going to be infinitly higher then the moving average
7.4 is the ratio that works with 1000, nn is the length in seconds of the 
window for which the moving average is taken

""" 
def autoCropper(lrate, sound, o, posno, startRn, endRn, positions):
	print "sound looks like:"
	print sound
	soundMatt= sound[1]  
	lenSound=len(soundMatt) 
	soundMat=abs(soundMatt) #this takes the absulute value
	lenSound=len(soundMat)
	print lenSound
	
	nn = 1 # nn = 0.5
	oo = 44100 * nn
	mm = int(oo)
	crDictionary = {}
	n=0
	j=0
	p=0
	qq=0  #
	for r in range (startRn+1, endRn+1):  # loops through each round  # for r in range (1, 5):
		print "  "  #
		print "(j) last break at:{0}".format(j) # j is iteration of loop 2 that trigers break 
		print "(p) take up at:{0}".format(p) #
		p = p*qq #  
		print "(p after 1 iteration) take up at:{0}".format(p)  #
		print '2nd loop r={0}, j={1}, p={2}'.format(r,j,p)
		for j in range(p, lenSound-mm): 
			moAv = np.mean(soundMat[j:j+mm-1]) #mean of nn second long moving interval
			if soundMat[j+mm-1] > 7.4*(moAv+1000): # determind from r1p1 & r1p2 spreadsheet
				qq = 1  
				p = j 
				print "the {0}th break is at:{1}".format(r, j) #
				k = j+22049  # sets k as the end point of the 1/2 sec interval from which the mean was taken
				crMat = soundMatt[k:k+88200] # creates a takes a 2 second long window
				scipy.io.wavfile.write('triMr{0}p{1}.wav'.format(r, o),44100,crMat)  
				p = j + 88200 # this should make the loop skip the next 2 seconds 
				print "should take up at:{0}".format(p)	
				break
