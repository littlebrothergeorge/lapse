#!/usr/bin/python
"""
Just a small script that renames all the JPEG files
in a folder as 0.jpg, 1.jpg etc. Initial order
is retained.


Note that this has possible error conditions that
are not handled at all:
- what if the folder has files already numbered?
- while renaming, it fails if the target file exists
"""
import glob
import shutil
import os, sys,  subprocess

class TimelapseSeriesExtend:
    
    confirmRename = False 
    extendedFilesCount = 0
    frames = 5
    extendedDir = ""
    extendedDirName = "extendedDir"
    
    def __init__(self,sysArgs):
        
        if (len(sysArgs) > 1):

                # Get the supplied params
                directory = sysArgs[1] # argv[0] is the script name
                directory = directory.strip()
                if (len(sysArgs) > 2):
                    self.frames = sysArgs[2]

                self.extendedDir = os.path.join(directory, self.extendedDirName)
                self.createExtendedDirectory()
                
                
                if directory[0] == "'" and directory[-1] == "'":
                    directory = directory[1:-1]
                if os.path.exists(directory):

                    os.chdir(directory)
                    directoryFolders = self.getDirectories()

                    if len(directoryFolders) == 0:
                        print directory                    
                        directoryFolders.append("") # this parent directory
                        
                    for folder  in directoryFolders:
                        path = os.path.join(directory, folder)
                        print "\nChecking " + path
                        os.chdir(path)

                        # if numbereing already done
                        if not self.areFilesSorted:                            
                            # rename each file?   
                            if self.confirmRename:  
                                self.renameFiles()
                            else:                              
                                if self.doConfirm("Are you sure? Rename all un-numbered jpg's in all directories?"):
                                    self.confirmRename = True 
                                    self.renameFiles()
                            

                        self.extendTheseImages()
                                
                   
                    
                print "\ndone..\n"
        else:
                print "\n  usage: python sysArgs[1].py  ~/Desktop/ 5 \n"



    def extendTheseImages(self):
        print "extending " +  os.getcwd()
        files = self.getJpegsCWD()
        # and create
        for f in files:

            for x in range(0, self.frames):

                self.extendedFilesCount += 1
                n = str.zfill(str(self.extendedFilesCount),5) + ".jpg"
                
                print f + " => " + self.extendedDir + "/" + n 
                try:
                    shutil.copyfile(f, self.extendedDir + "/" + n )
                    #pass
                except:
                    print "error: couldnt copy, check permissions"
                    sys.exit()


    def areFilesSorted(self):
        if os.path.exists(os.path.join(os.getcwd(),'00001.jpg')):
            #print 'Found correctly numbered files in "'+ os.getcwd() + '"' 
            return True

    def getDirectories(self):

        print "\n\nChecking root directory: " + os.getcwd()
        # get the first level of directories in cwd. may return only cwd
        directoryFolders = [d for d in os.listdir(os.getcwd()) if os.path.isdir(d)]
        #sort the folders
        directoryFolders.sort()

        # remove the extendedDir from list
        try:
            directoryFolders.remove(self.extendedDirName)
        except ValueError:
            print "couldnt delete extendedDirName from list"

        for folder in directoryFolders:
                print folder

        return directoryFolders


    def createExtendedDirectory(self):
        if os.path.exists(self.extendedDir):
            if self.doConfirm("Delete the existing extended files in " + self.extendedDir):
                shutil.rmtree(self.extendedDir) 
                os.mkdir(self.extendedDir)
            else:
                print "No point continuing then.."
                sys.exit()
        else:
            os.mkdir(self.extendedDir)
    
   
    def getJpegsCWD(self):
        #get all the jpg file names in the current folder
        files = glob.glob("*.[jJ][pP][gG]") 
        #sort the list
        files.sort()
        return files  
        
    def renameFiles(self):
        
        print "renaming " + str(len(files)) + " jpeg files in " + os.getcwd()
        count = 0
        files = self.getJpegsCWD()
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

    
    def doConfirm(self,message):
        if(self.confirm("\n   " + message, allow_empty=True)):
            print "\n"
            return True
            
    def askToDelete(self,filename):
        if(self.confirm("\n   File " + filename + " Delete the extended series folder?", allow_empty=True)):            
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
        print "\n"
     
        if ans == '' and allow_empty:
          return default
        elif ans == 'y':
          return True
        elif ans == 'n':
          return False
        else:
              print 'Please enter y or n.'

if __name__=="__main__":
    TimelapseSeriesExtend(sys.argv)


