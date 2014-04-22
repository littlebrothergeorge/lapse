#!/usr/bin/python
"""

"""
import glob
#import string
import os, sys,  subprocess
from encoder_functions import encoder_functions

class timelapse_revised:
    
    confirmSuccessful = False
    symlinkFolder = 'symlinks'
    
    def __init__(self,sysArgs):
        
        if (len(sysArgs) > 1):
                directory = sysArgs[1]
                directory = directory.strip()
                if directory[0] == "'" and directory[-1] == "'":
                    directory = directory[1:-1]
                if os.path.isdir(directory):
                    os.chdir(directory) 
                    print "\n\nChecking: " + directory
                    
                    # first level of directories
                    directoryFolders = [d for d in os.listdir(directory) if os.path.isdir(d)]
                    #sort the folders
                    directoryFolders.sort() 
                    for folder in directoryFolders:
                            print folder
                    if len(directoryFolders) == 0:
                        print directory                    
                        directoryFolders.append("") # this parent directory
                        
                    for folder  in directoryFolders:
                        path = os.path.join(directory, folder)
                        print "\nChecking " + path
                        os.chdir(path)
                        #print os.listdir(path).sort()
                        # if numbereing already done
                        if os.path.exists(os.path.join(path,'00001.jpg')):
                            print 'Found numbered files in "'+ path + '"'
                        else:
                            # and rename each file                                
                            if not self.confirmSuccessful:                                
                                self.doConfirm() 
                            if self.confirmSuccessful:  
                                self.renameFiles()
                                
                    createdClips = []

                    # now its time to create the videos
                    for folder in directoryFolders:
                        
                        os.chdir(os.path.join(directory, folder))
                        if folder == "":
                            folder = directory

                        videoNameAVI =  folder  + "-" + directory + ".mp4"
                        video = os.path.join(directory,videoNameAVI)
                        
                        # now its time to create the video 
                        self.createMovieParts(directory,videoNameAVI)
                        createdClips.append(video)
                    
                    if (len(createdClips) > 1):   
                        # now join all the clips together    
                        tmpVideo = os.path.join(directory,"tmp.mp4")
                        alltheVideos = ""
                        for elem in createdClips:
                            alltheVideos += ' %s ' % str(elem)
                        join = "cat " + alltheVideos + " > '" + tmpVideo + "'"
                        reindex = "mencoder '" + tmpVideo + "' -o '" + os.path.join(directory,"movieComplete.avi") + "' -forceidx -ovc copy -oac copy"
                        if  (self.askToJoin()):
                            print join
                            os.chdir(directory) 
                            subprocess.call(join, shell=True)
                            subprocess.call(reindex , shell=True)                    
                            os.remove(tmpVideo);
                        else:
                            print "Ok to do the join latter here are the commands"
                            print join
                            print reindex
                    
                    print "\ndone..\n"
                else:
                    print "directory does not exist"

        else:
                print "\n  usage: python goProTimelapse2AVI.py  /path/to/files/\n"
    
    def createMovieParts(self,directory,videoName):
            
            pathAndFile = os.path.join(directory,videoName)
            if not os.path.exists(pathAndFile):
                print "Will create " + pathAndFile                
            else:
                if(self.askToDelete(pathAndFile)):
                    os.remove(pathAndFile);
                else:
                    print "Not overwriting " + pathAndFile
                    return

            # http://rodrigopolo.com/ffmpeg/cheats.html
            # http://mariovalle.name/mencoder/mencoder.html
            # http://electron.mit.edu/~gsteele/ffmpeg/
            encoder_functions().makeFFmpegMovieFromFiles(pathAndFile)
            #encoder_functions().makeMencoderMovieFromFiles(pathAndFile)

    def renameFiles(self):
        #get all the jpg file names in the current folder
        files = glob.glob("*.JPG") 
        #files = glob.glob("*.jpg") 
        #sort the list
        files.sort()
        count = 0
        # and rename each file
        for f in files:
            count = count + 1
            n = str.zfill(str(count),5) + ".jpg"
            #n = str(count)+ ".jpg"
            print f + " => " + n 
            try:
                os.rename(f, n)
                #pass
            except:
                print "error: couldnt rename, check permissions"
                sys.exit()

    
    def doConfirm(self):
        if(self.confirm("\n   Are you sure? Rename all un-numbered jpg's in the above directories?", allow_empty=True)):
            self.confirmSuccessful = True
            return True
            
    def askToDelete(self,filename):
        if(self.confirm("\n   File " + filename + " Delete the file?", allow_empty=True)):            
            return True
        else:
            return False
            
    def askToJoin(self):
        """if(self.confirm("\n   Stitch up the files?", allow_empty=True)):            
            return True
        else:
            return False
        """
        return True
            
    
    def confirm(self,prompt_str="Confirm", allow_empty=False, default=False):
      fmt = (prompt_str, 'y', 'n') if default else (prompt_str, 'n', 'y')
      if allow_empty:
        prompt = '%s [%s]|%s: ' % fmt
      else:
        prompt = '%s %s|%s: ' % fmt
     
      while True:
        ans = raw_input(prompt).lower()
     
        if ans == '' and allow_empty:
          return default
        elif ans == 'y':
          return True
        elif ans == 'n':
          return False
        else:
              print 'Please enter y or n.'

if __name__=="__main__":
    timelapse_revised(sys.argv)


