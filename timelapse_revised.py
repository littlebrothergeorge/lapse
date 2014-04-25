#!/usr/bin/python
"""

"""
import glob, os, sys, subprocess, shutil
from encoder_functions import encoder_functions

class timelapse_revised:
    
    videoExtension = ".mov"
    symlinkFolder = 'symlinks'
    ignoreFolders = [symlinkFolder,'raw','render']
    movieParts = []
    directory = ""
    codec = "libx264"

    
    def __init__(self,sysArgs):
        
        if (len(sysArgs) > 1):

            # this directory
            self.directory = sysArgs[1]

            # codec, libx264 for web , prores for editing
            if sysArgs[2]:
                self.codec = sysArgs[2]

            self.directory = self.directory.strip()
            if self.directory[0] == "'" and self.directory[-1] == "'":
                self.directory = self.directory[1:-1]
            if os.path.isdir(self.directory):
                os.chdir(self.directory) 
                print "\n\nChecking: " + self.directory
                
                # first level of directories
                self.directoryFolders = [d for d in os.listdir(self.directory) if os.path.isdir(d) and d not in self.ignoreFolders]
                #sort the folders
                self.directoryFolders.sort() 
                if len(self.insensitive_glob("*.JPG")) > 0:                
                    self.directoryFolders.append("") # the parent self.directory
                
                # Create the symlink directories 
                for folder in self.directoryFolders:
                    path = os.path.join(self.directory, folder)
                    symlinkPath = os.path.join(path, self.symlinkFolder)
                    
                    if os.path.exists(os.path.join(symlinkPath,'00001.jpg')):
                        print 'Found numbered files in "'+ symlinkPath + '"'
                    else: 
                        self.createSymlinks(symlinkPath)
                            
                createdClips = []

                # List up the videos
                for folder in self.directoryFolders:
                    if folder == "":
                        folder = os.path.split(os.path.dirname(self.directory))[1]

                    videoName =  folder + self.videoExtension
                    video = os.path.join(self.directory,videoName)
                    print "handling video " + video
                    #os.chdir(os.path.join(self.directory, folder))
                    
                    self.movieParts.append({'video':video,'folder':os.path.join(self.directory, folder)})
                    createdClips.append(video)

                # Create the videos
                self.createMovieParts()


                # Join all videos together
                if (len(createdClips) > 1):   

                    tmpVideo = os.path.join(self.directory,os.path.split(os.path.dirname(self.directory))[1] + "-tmp" + self.videoExtension)
                    alltheVideos = ""
                    for elem in createdClips:
                        alltheVideos += ' %s ' % str(elem)
                    join = "cat " + alltheVideos + " > '" + tmpVideo + "'"
                    finalVideo = os.path.join(self.directory,"movieComplete"+ self.videoExtension) 
                    reindex = "mencoder '" + tmpVideo + "' -o '" + finalVideo + "' -forceidx -ovc copy -oac copy"

                    # now join all the clips together    
                    if  (self.askToJoin()):

                        os.chdir(self.directory) 
                        subprocess.call(join, shell=True)
                        subprocess.call(reindex , shell=True)                    
                        os.remove(tmpVideo);
                        print "\ndone.. " +  finalVideo + "\n"

                    else:
                        print "\n\nOk to do the join latter.\nHere are the commands:\n-----------------------------------------\n"
                        print join
                        print reindex
                        print "\n\n"
                
                
            else:
                print "self.directory does not exist"

        else:
            print "\n  usage: python goProTimelapse2AVI.py  /path/to/files/ [codec (prores only supported) ]\n"
    
    def createMovieParts(self):

        listToRender = []

        for destFile in self.movieParts:
            render = True
            if not os.path.exists(destFile['video']):
                print "Will create " + destFile['video']               
            else:
                if(self.askToDelete(destFile['video'])):
                    os.remove(destFile['video']);
                else:
                    print "Not overwriting " + destFile['video']
                    render = False

            if render:
                listToRender.append(destFile)

        for selected in listToRender:
            sourceSymlinks = os.path.join(os.path.dirname(selected['folder']), self.symlinkFolder)
            encoder_functions().makeFFmpegMovieFromFiles(sourceSymlinks,selected['video'],self.codec)


    def createSymlinks(self,symlinkPath):
        
        if not os.path.exists(symlinkPath):
            print "Creating symlinkFolder " + symlinkPath
        else:
            shutil.rmtree(symlinkPath)
        
        try:
            print "\nPopulating symlink folder " + symlinkPath
            os.makedirs(symlinkPath)
        except:
            print "ERROR:!!! couldnt create symlinks folder, check permissions"
            sys.exit()

        os.chdir(symlinkPath)
        os.chdir('..')

        #get all the jpg file names in the current folder
        files = self.insensitive_glob("*.JPG") 
        files.sort()

        count = 0
        # Create symlink to each file
        for f in files:
            count += 1
            n = str.zfill(str(count),5) + ".jpg"
    
            os.symlink(
                os.path.join(os.getcwd(),f),
                os.path.join(self.symlinkFolder,n)
            )
    
            
    def askToDelete(self,filename):
        if(self.confirm("\n   File " + filename + " Delete the file?", allow_empty=True)):   
            return True
        else:
            return False

    def insensitive_glob(self, pattern):
        def either(c):
            return '[%s%s]'%(c.lower(),c.upper()) if c.isalpha() else c
        return glob.glob(''.join(map(either,pattern)))
            
    def askToJoin(self):
        if(self.confirm("\n   Stitch up the files?", allow_empty=True)):            
            return True
        else:
            return False
        
    
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


