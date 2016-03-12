#! /usr/python

'''
///////////////////////////////////////////////////////////
//  Permission is hereby granted, free of charge,
//  to any person obtaining a copy of
//  this software and associated documentation files
//  (the "Software"), to deal in the Software without
//  restriction, including without limitation the rights
//  to use, copy, modify, merge, publish, distribute,
//  sublicense, and/or sell copies of the Software, and
//  to permit persons to whom the Software is furnished
//  to do so, subject to the following conditions:
//
//  The above copyright notice and this permission notice
//  shall be included in all copies or substantial portions
//  of the Software.
//
//  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF
//  ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
//  TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
//  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
//  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
//  CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
//  OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
//  IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
//  DEALINGS IN THE SOFTWARE.
'''

__author__ = 'RobertIan'
__version__ = '0.2.1'

import argparse
import pygame
import picamera
import time
import datetime
import netifaces

import RPi.GPIO as GPIO
import os.path


#KJW imports
import sys
import select
import os

class Trial:

    def __init__(self, stim, starttime, feedornot):
        # perhaps replace this with a bash script or RPC that controlls timing
        # of all servers
        #self.now = time.asctime()
        #self.when = when
        #assert self.when - self.now > 0
        #
        pygame.display.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)
        self.stimulus = stim
        #
        self.start = float(starttime)
        self.tLength = 30 #four minute trial, changed to 1 min KJW
        self.feedDelay = 15 #thirty seconds
        #
        GPIO.setmode(GPIO.BCM)

        self.feeder = 17 ##
        self.notfeeder = 5 ##
        self.feederin = 26 ##????
        self.notfeederin = 25 ##????
        if feedornot == 'feed':
            self.feederin = self.feederin
            self.feederout = self.feeder
        elif feedornot == 'notfeed':
            self.feederin = self.notfeederin
            self.feederout = self.notfeeder
        else:
            print 'feeder not assigned'
            self.safeQuit()
        GPIO.setup(self.feederin, GPIO.IN)
        GPIO.add_event_detect(self.feederin, GPIO.RISING)
        GPIO.setup(self.feederout, GPIO.OUT)
        GPIO.output(self.feederout, True)
        #GPIO.setup(self.notfeeder, GPIO.OUT)
        #PIO.output(self.notfeeder, False)
        #


        presented = False

    def checkPiIP(self):
       self.ip = netifaces.ifaddresses('eth0')[2][0]['addr']
       #print self.ip

    def whatStimulus(self):
        self.stim, extension = os.path.splitext(self.stimulus)

        if extension == '.png' or extension == '.PNG' or extension == '.jpg' \
        or extension == '.JPG':
        # still image
            try:
                self.image = pygame.image.load('/home/pi/ethoStim/individualtesting/src/10.png')
            except IOError:
                # currently a print, should be changed to send a message to
                #the client
                print 'are you sure this file exists? check the src folder \
                ony jpg/JPG, png/PNG formats'

        '''
        elif extension == '.mpg' or extension == '.MPG' or extension == '.avi' \
        or extension == '.AVI':
            try:
                self.video = pygame.image.load('src/',self.stimulus)
            except IOError:(KeyboardInterrupt           # currently a print should be changed to send a message to
                #the client
                print 'are you sure this file exists? check the src folder \
                ony jpg/JPG, ong/PNG, avi/AVI and mpg/MPG formats'
        '''
    def feed(self):
        GPIO.output(self.feeder, GPIO.HIGH)

    def notFeed(self):
        GPIO.output(self.notfeeder, GPIO.HIGH)
    def cameraInit(self):
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1920, 1080)
        self.camera.framerate = 30
        self.camera.autofocus = False
        self.camera.awb_mode = 'fluorescent'

    def videoFileName(self, species, tround, sl, sex, fishid, day, session,
                    conditionside):
        self.vidout = ('data/'+str(self.ip)+'/'+(str(species)+'_'+str(tround)
        +'_'+str(sl)+'_'+str(sex) +'_'+str(fishid)+'_'+str(day)+'_'+
        str(session)+'_' +str(self.stim)+'_'+str(conditionside)))
        print self.vidout
    def startRecording(self):
        print 'start recording'
        self.camera.start_recording(self.vidout+ '.h264')
        print 'recording'


    def stopRecording(self):
        self.camera.stop_recording()

    def cameraQuit(self):
        self.camera.close()

    def safeQuit(self):
	print'safeQuit'
        GPIO.output(self.feeder, True)#changed
        GPIO.cleanup()
        pygame.quit()
        exit()

    def mainLoop(self, camera):

        print 'feedornot'
        print 'main loop'
	#delaymet = False
        #presented = False

        while time.time()<self.start:
            print time.time()-self.start
            pass

	    self.startT = time.time()
        fed = False
        if camera == 'record':
            selft.startRecording()
        elif camera == 'notrecord':
            pass
        while ((time.time() - self.startT) < self.tLength):
            print (time.time()-self.startT)
	    pygame.display.flip()
	    self.screen.blit(self.image, (250,100))
	    #presented = True
            try:

               # if presented == True:
                #    pass
                if (time.time() -self.startT) >  self.feedDelay:
		    #if not fed:
                    #GPIO.setmode(BCM)
		    #GPIO.setmode(GPIO.BCM)
		    #GPIO.setup(17, GPIO.OUT)
		    #GPIO.output(17, False)

                 	#pygame.display.flip()
              	 	#self.screen.blit(self.image, (0,0))

                 	#presented = True
                    if fed:
                        pass
                    elif GPIO.event_detected(self.feederin):
		                time.sleep(1.0)
		                GPIO.output(self.feederout,True)
                        fed = True
   		    else:
                      # time.sleep(1.0)
                       GPIO.output(self.feederout, False)

                       #print time.time()
		  # pass

            except KeyboardInterrupt:
		print'KeyInterupt'
		self.safeQuit()



if __name__ == '__main__':


    print'Place1'

    ap = argparse.ArgumentParser()
    ap.add_argument("-f","--fish", help="ID of fish in tank")
    ap.add_argument("-ts", "--trainedStim",help="numerosity stimulus the individual is being trained to, e.g. 12")
    ap.add_argument("-ps", "--presentedStim", help="stimulus being presented with this raspberry pi")
    ap.add_argument("-d","--day", help="experiment day, e.g. 1-7")
    ap.add_argument("-s","--session", help="trial session, e.g. 1-4")
    ap.add_argument("-fs","--fedSide", help="side(self.ip feed on/conditioned side")
    ap.add_argument("-x","--sex", help="fish sex")
    ap.add_argument("-p","--proportion", help="training ratio")
    ap.add_argument("-sp", "--species", help="species name")
    ap.add_argument("-sl","--fishstandardlength", help="standard length of the")
    ap.add_argument("-r","--round", help="training round")
    ap.add_argument("-fd", "--feed", help="feed with this stimulus",action="store_true")
    ap.add_argument("-c", "--camera",help="do you want to record using this pi?",action="store_true")
    ap.add_argument("-m:", "--startTime", help="time since epoch that you want to start your trial")
    args = vars(ap.parse_args())



    print 'Place2'
    if args.["feed"]:
        T = Trial(args["presentedStim"], args["startTime"], 'feed')
    else:
        T = Trial(args["presentedStim"], args["startTime"], 'notfeed'))

    #T.safeQuit()

    T.checkPiIP()
    T.whatStimulus()
    T.videoFileName(args["species"], args["round"], args["fishstandardlength"],
                    args["sex"], args["fish"], args["day"], args["session"], args["fedSide"])

    if args["camera"]:
        T.cameraInit()

    #if args["camera"]:
        #T.startRecording()
    else:
        pass
  #if args["feed"]:
    if args["camera"]:
        T.mainLoop('record')
    else:
        T.mainLoop('notrecord')
    #else:
      #T.mainLoop(False)
    if args["camera"]:
        T.stopRecording()
    else:
        pass

    if args["camera"]:
	T.cameraQuit()

    T.safeQuit()
