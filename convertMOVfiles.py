#!/usr/bin/python
import os, os.path, sys, subprocess

#i = 0
if (len(sys.argv) > 1):
	directory = sys.argv[1]
	directory = directory.strip()
	if directory[0] == "'" and directory[-1] == "'":
	    directory = directory[1:-1]
	print "Checking: " + directory
	for root, dirs, files in os.walk(directory):
	    print dirs
	    for f in files:
		#i += 1
		if f.endswith('.MOV'):
			fAsAVI = os.path.splitext(f)[0] + '.avi'
			fAsAVI = os.path.join(root, fAsAVI)
			if not os.path.exists(fAsAVI):
				fullpath = os.path.join(root, f)
				print "will create " + fAsAVI
				p = subprocess.call("ffmpeg -i '" + fullpath + "' -b 3000k -vcodec mjpeg  -flags +loop -cmp +chroma -partitions +parti4x4+partp8x8+partb8x8 -subq 5 -me_range 16 -g 250 -keyint_min 25 -sc_threshold 40 -i_qfactor 0.71 '" + fAsAVI + "'", shell=True)
				#p.wait()
				#os.system("ls -la '" + fullpath + "'")
			else:
				print "Ignoring existing " + fAsAVI
		else:
			pass
			#print "ignoreing: " + fullpath
else:
    print "\n\n     usage: python convertMOVfiles.py '/media/BigFarger/My Videos/CREATED VIDEOS/'\n"

print "\n\ndone..\n"



