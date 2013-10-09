#!/usr/bin/python
import os, os.path, sys, subprocess
import argparse
from encoder_functions import encoder_functions

#i = 0	
parser = argparse.ArgumentParser(description='Covert video files matching input type to encoder_functions.py output type in the directory')
parser.add_argument('directory', help='The folder to find the video files')
parser.add_argument('-inputFilesExt','--inputFileExt', default="avi", dest="fileInExt", help='The video file extension to convert')
args = parser.parse_args()

directory = args.directory
fileInExt = args.fileInExt

if directory[0] == "'" and directory[-1] == "'":
	directory = directory[1:-1]

if os.path.exists(directory):
	
	print "Checking the directory: " + directory
	for root, dirs, files in os.walk(directory):
		for name in files:
			if name.endswith(fileInExt):
				fAsExpected = os.path.splitext(name)[0] + '.mp4'
				fAsExpected = os.path.join(root, fAsExpected)
				if not os.path.exists(fAsExpected):
					theFile = os.path.join(root, name)
					print "will create " + fAsExpected
					encoder_functions().ffmpeg(theFile,fAsExpected)
					
				else:
					print "Ignoring existing " + fAsExpected
			else:
				pass
				#print "ignoring: " + name

	print "\n\ndone..\n"
else:
	print "\n\n'" + directory + "' cannot be found\n"


