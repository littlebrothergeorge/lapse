#!/usr/bin/python
import os, os.path, sys, subprocess
from encoder_functions import encoder_functions

#i = 0
if (len(sys.argv) > 1):
	theFile = sys.argv[1]
	print theFile
	if os.path.isfile(theFile):
		fAsMP4 = theFile.split('.')[0] + '.mp4'
		print "will create " + fAsMP4
		encoder_functions().ffmpeg(theFile,fAsMP4)
			
else:
    print "\n\n    Usage: python convertSingleFile.py '/media/BigFarger/My\ Videos/CREATED\ VIDEOS/somevideofile.ext'\n"
    print "\n    Converts a single file into a MP4 file using makeFFmpegMovie'\n"

print "\n\ndone..\n"



