#!/usr/bin/python
"""

"""
import glob
#import string
import os, sys,  subprocess

class encoder_functions:
    
    # def ffmpeg(self,input,outputFile):

    #     if (len(input) == 0):
    #         input = " %05d.jpg "
    #     else:
    #         input = "'" + input + "'"


    #     width = 1920
    #     height = 1080
    #     quality = 50 # The quality factor can vary between 40 and 60 to trade quality for size
    #     # the 50 factor can vary between 40 and 60
    #     #
    #     optimal_bitrate =  width * height* quality * 25 / 256

    #     ######################################################
    #     ## online ffmpeg creator
    #     ##  http://rodrigopolo.com/ffmpeg/
    #     # http://rodrigopolo.com/ffmpeg/cheats.html
    #     # http://mariovalle.name/mencoder/mencoder.html
    #     # http://electron.mit.edu/~gsteele/ffmpeg/
    #     ######################################################

    #     # list all possible internal presets/tunes for FFmpeg by specifying no preset or tune option at all:
    #     # ffmpeg -i input -c:v libx264 -preset -tune dummy.mp4

        
    #     # for gopro videos
    #     #makeMovieCommand = "ffmpeg  -loglevel verbose  -i %05d.jpg -vb 6400k -vcodec libx264 -s hd1080 -v 0 \
    #     #-flags +loop  -partitions +parti4x4+partp8x8+partb8x8 -subq 5 -me_range 16 \
    #     #-g 250 -keyint_min 25 -sc_threshold 40 -i_qfactor 0.71 '" + outputFile + "'"

    #     options = '-s ' + str(width) + 'x' + str(height) + ' -aspect 16:9 -r 30000/1001 -b ' + str(optimal_bitrate) + ' -bt 4M -vcodec libx264'

    #     makeMovieCommand = " ffmpeg -i " + input + " " + options + " -pass 1 -preset medium -an -ss 0 '" + outputFile + "' && \
    #       ffmpeg -y -i " + input + " " + options + "  -pass 2 -preset slow -acodec libfaac -ac 2 -ar 44100 -ab 128k -ss 0 '" + outputFile + "'"
        

    #     print makeMovieCommand
        
    #     subprocess.call(makeMovieCommand, shell=True)

                
    # def makeFFmpegMovieFromFiles(self,inputFolder,outputFile):

    #     os.chdir(inputFolder)
    #     self.ffmpeg(null,outputFile) 

    def makeFFmpegMovieFromFiles(self,inputFolder,outputFile):

        os.chdir(inputFolder)
        print "\n\nRendering all the files in " + inputFolder + "\n"
        
        width = 1920
        height = 1080
        quality = 50 # The quality factor can vary between 40 and 60 to trade quality for size
        # the 50 factor can vary between 40 and 60
        #
        optimal_bitrate =  width * height* quality * 25 / 256

        ######################################################
        ## online ffmpeg creator
        ##  http://rodrigopolo.com/ffmpeg/
        ######################################################

        # list all possible internal presets/tunes for FFmpeg by specifying no preset or tune option at all:
        # ffmpeg -i input -c:v libx264 -preset -tune dummy.mp4

        
        # for gopro videos
        #makeMovieCommand = "ffmpeg  -loglevel quiet  -i %05d.jpg -vb 6400k -vcodec libx264 -s hd1080 -v 0 \
        #-flags +loop -cmp +chroma -partitions +parti4x4+partp8x8+partb8x8 -subq 5 -me_range 16 \
        #-g 250 -keyint_min 25 -sc_threshold 40 -i_qfactor 0.71 '" + outputFile + "'"

        options = '-y -i %05d.jpg -s ' + str(width) + 'x' + str(height) + ' -loglevel quiet -aspect 16:9 -r 30000/1001 -b ' + str(optimal_bitrate) + ' -bt 4M -vcodec libx264'

        makeMovieCommand = " ffmpeg " + options + " -pass 1 -preset medium -an -ss 0 " + outputFile + " && \
         ffmpeg " + options + "  -pass 2 -preset slow -acodec libfaac -ac 2 -ar 44100 -ab 128k -ss 0 " + outputFile 

        # for olympus om-d
        #makeMovieCommand = "ffmpeg -loglevel verbose  -i  %05d.jpg -r 25 -vcodec libx264 -s hd1080 '" + outputFile + "'"
       


        print makeMovieCommand
        subprocess.call(makeMovieCommand, shell=True)
                
            
    def makeMencoderMovieFromFiles(self,inputFolder,outputFile):

        os.chdir(inputFolder)

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
	        
