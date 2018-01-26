import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import wave
import sys
from scipy.io.wavfile import read  # reading wav files
import scipy.io.wavfile
import math
import cmath
import pylab
import os # for opeining files in loop #change working diectory, count files in directory
import os.path
import glob # looping throught all files in folder
import shutil
#from autocropper import autoCropper
"""
transfer the new files created from autocroper
Input:  datafile = the name of the original file to be moved
Output: datafile = identical file in new location 
		also deletes original file
""" 
def transfer(datafile, location):
	
	print "starting transfer"

	basepath = location  
	#print " the location is:"
	#print location
	#print basepath
	
	# gets the path to this current file
	cfd = os.path.abspath(__file__)	
	#print " the cfd is:"
	#print cfd
	baseP= cfd 

	# removes the last folder of the path
	basePa = str(baseP.split('\\')[0:-1])
	basePat = '\\'.join(baseP.split('\\')[0:-1])

	# adds "\DataRa" to the end of the base path
	basepath = os.path.join(basePat,"DataBefore")	
	# adds "\DataCr" to the end of the base path
	folderPath = os.path.join(basePat,"DataAfter")

	# copies the cropped file to a new folder
	shutil.copy(os.path.join(basepath, datafile), folderPath) 

	# removes the file that has just been coppied
	os.remove(os.path.join(basepath, datafile))

	print "the file has been transfered"





