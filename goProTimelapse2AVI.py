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
#import string
import os, sys,  subprocess

class goProTimelapse2AVI:
    
    confirmSuccessful = False
    
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
                                
                    createdClips = ""
                    singleFile = False # will there be many file needing stitching
                    # now its time to create the videos
                    # http://mariovalle.name/mencoder/mencoder.html
                    for folder in directoryFolders:
                        
                        os.chdir(os.path.join(directory, folder))
                        if folder == "":
                            folder = "movie"

                        videoNameAVI =  folder  +".avi"
                        video = os.path.join(directory,videoNameAVI)
                        print "\nCreating video " + video
                        createdClips += "'" +video + "' "
                        
                        # now its time to create the video 
                        self.createMovieParts(directory,videoNameAVI)
                        
                    # now join all the clips together    
                    tmpAvi = os.path.join(directory,"tmp.avi")
                    join = "cat " + createdClips + " > '" + tmpAvi + "'"
                    reindex = "mencoder '" + tmpAvi + "' -o '" + os.path.join(directory,"movieComplete.avi") + "' -forceidx -ovc copy -oac copy"
                    if  (self.askToJoin()):
                        print join
                        os.chdir(directory) 
                        subprocess.call(join, shell=True)
                        subprocess.call(reindex , shell=True)                    
                        os.remove(tmpAvi);
                    else:
                        print "Ok to do the join latter here are the commands"
                        print join
                        print reindex
                    
                    print "\ndone..\n"
                else:
                    print "directory does not exist"

        else:
                print "\n  usage: python goProTimelapse2AVI.py  ~/Desktop/\n"
    
    def createMovieParts(self,directory,videoNameAVI):
            
            pathAndFileAsAVI = os.path.join(directory,videoNameAVI)
            if not os.path.exists(pathAndFileAsAVI):
                print "Will create " + pathAndFileAsAVI                
            else:
                if(self.askToDelete(pathAndFileAsAVI)):
                    os.remove(pathAndFileAsAVI);
                else:
                    print "Not overwriting " + pathAndFileAsAVI
                    return

            # http://rodrigopolo.com/ffmpeg/cheats.html
            self.makeFFmpegMovie(pathAndFileAsAVI)
            #self.makeMencoderMovie(pathAndFileAsAVI)
                
    def makeFFmpegMovie(self,outputFile):
        width = 1080
        height = 720
        quality = 50 # The quality factor can vary between 40 and 60 to trade quality for size
        # compute the optimal bitrate 
        #	br = 50 * 25 * width * height / 256
        #
        # the 50 factor can vary between 40 and 60
        #
        optimal_bitrate =  width * height* quality * 25 / 256
        
        # for gopro videos
        makeMovieCommand = "ffmpeg  -loglevel verbose  -i %05d.jpg -vb 6400k -vcodec libx264 -s hd1080 -v 0 \
        -flags +loop -cmp +chroma -partitions +parti4x4+partp8x8+partb8x8 -subq 5 -me_range 16 \
        -g 250 -keyint_min 25 -sc_threshold 40 -i_qfactor 0.71 '" + outputFile + "'"

        # for olympus om-d
        #makeMovieCommand = "ffmpeg -loglevel verbose  -i  %05d.jpg -r 25 -vcodec libx264 -s hd1080 '" + outputFile + "'"

        #High quality 2 Pass

        #ffmpeg -y -i INPUT -r 30000/1001 -b 2M -bt 4M -vcodec libx264 -pass 1 -vpre fastfirstpass -an output.mp4
        # ffmpeg -y -i INPUT -r 30000/1001 -b 2M -bt 4M -vcodec libx264 -pass 2 -vpre hq -acodec libfaac -ac 2 -ar 48000 -ab 192k output.mp4

        


        print makeMovieCommand
        subprocess.call(makeMovieCommand, shell=True)
                
            
    def makeMencoderMovie(self,outputFile):
        # http://mariovalle.name/mencoder/mencoder.html
        # see mencoder on desktop      
        
        # def optimal_bitrate = quality * 25 * width * height / 256
        # ffmpeg -y -i %d.jpg -r 12 -s hd720 -vcodec ffv1 movie.avi
        width = 1920
        height = 1024
        quality = 60 # The quality factor can vary between 40 and 60 to trade quality for size
        # compute the optimal bitrate 
        #	br = 50 * 25 * width * height / 256
        #
        # the 50 factor can vary between 40 and 60
        #
        optimal_bitrate =  width * height* quality * 25 / 256
        
        #
        # set the MPEG4 codec options
        #	you have to experiment!
        #
        opt ="vbitrate=" + str(optimal_bitrate) + ":mbd=2:keyint=132:v4mv:vqmin=3:lumi_mask=0.07:dark_mask=0.2:scplx_mask=0.1:tcplx_mask=0.1:naq:trell"
        codec="mpeg4"
        
        #
        # set the Microsoft MPEG4 V2 codec options
        #
        #opt="vbitrate=$obr:mbd=2:keyint=132:vqblur=1.0:cmp=2:subcmp=2:dia=2:mv0:last_pred=3"
        #codec="msmpeg4v2"
        
        #
        # clean temporary files that can interfere with the compression phase        #        
        subprocess.call("rm -f divx2pass.log frameno.avi", shell=True)
        
        # first pass
        makeMovieCommand = "mencoder -ovc lavc -lavcopts vcodec=" + codec + ":vpass=1:" + opt + " -mf type=jpg:w=" + str(width) + ":h=" + str(height) + ":fps=25 -nosound -o /dev/null mf://" + os.getcwd() + "/\*.jpg"
        subprocess.call(makeMovieCommand, shell=True)
        
        # second pass
        makeMovieCommand = "mencoder  -ovc lavc -lavcopts vcodec=" + codec +  ":vpass=2:" + opt + " -mf type=jpg:w=" + str(width) + ":h=" + str(height) + ":fps=25 -nosound -o " +  outputFile + " mf://" + os.getcwd() + "/\*.jpg"
        subprocess.call(makeMovieCommand, shell=True)
        
        
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
    goProTimelapse2AVI(sys.argv)


