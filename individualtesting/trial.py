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
__version__ = '0.2.5'

import argparse
import pygame
import picamera
import time
import datetime
import netifaces
import RPi.GPIO as GPIO
import os.path
import sys
import select
import os

class Trial:

    def __init__(self, stim, starttime, feedornot):

        ## initialize display
        pygame.display.init()
        pygame.mouse.set_visible(False)
        self.screen = pygame.display.set_mode((0,0),pygame.FULLSCREEN)

        ## assign stimulus
        self.stimulus = stim

        ## timing
        self.start = float(starttime)
        self.tLength = 4*60 #four minute trial
        self.feedDelay = 30 #thirty second delay

        ## GPIO setup
        GPIO.setmode(GPIO.BCM)
        self.feeder = 17 ##????
        self.notfeeder = 5 ##????
        self.feederin = 26 ##????
        self.notfeederin = 25 ##????
        if feedornot == 'feed':
            self.feederin = self.feederin
            self.feederout = self.feeder
        elif feedornot == 'notfeed':
            self.feederin = self.notfeederin
            self.feederout = self.notfeeder
        else:
            ## currently a print, should be changed to send a message to
            #the client
            print 'feeder not assigned'
            self.safeQuit()
        GPIO.setup(self.feederin, GPIO.IN)
        GPIO.add_event_detect(self.feederin, GPIO.RISING)
        GPIO.setup(self.feederout, GPIO.OUT)
        GPIO.output(self.feederout, True)

    def checkPiIP(self):

        ## query IP address from system
        self.ip = netifaces.ifaddresses('eth0')[2][0]['addr']

    def whatStimulus(self):

        ## locate stimulus in src folder
        self.stim, extension = os.path.splitext(self.stimulus)
        if extension == '.png' or extension == '.PNG' or extension == '.jpg' \
        or extension == '.JPG':

        ## still image
            try:
                self.image = pygame.image.load('/home/pi/ethoStim/individualtesting/src/10.png')
            except IOError:
                ## currently a print, should be changed to send a message to
                #the client
                print 'are you sure this file exists? check the src folder \
                ony jpg/JPG, png/PNG formats'
                self.safeQuit()

    def cameraInit(self):

        ## adjust camera settings here
        self.camera = picamera.PiCamera()
        self.camera.resolution = (1920, 1080)
        self.camera.framerate = 30
        self.camera.autofocus = False
        self.camera.awb_mode = 'fluorescent'

    def videoFileName(self, species, tround, sl, sex, fishid, day, session,
                    conditionside):

        ## adjust video naming convention here
        self.vidout = ('data/'+str(self.ip)+'/'+(str(species)+'_'+str(tround)
        +'_'+str(sl)+'_'+str(sex) +'_'+str(fishid)+'_'+str(day)+'_'+
        str(session)+'_' +str(self.stim)+'_'+str(conditionside)))

    def startRecording(self):
        self.camera.start_recording(self.vidout+ '.h264') #output video

    def stopRecording(self):
        self.camera.stop_recording()

    def cameraQuit(self):
        self.camera.close()

    def safeQuit(self):
        GPIO.output(self.feeder, True) #reset feeder ????
        GPIO.output(self.notfeeder, True) #reset notfeeder ????
        GPIO.cleanup() #reset all GPIOs
        pygame.quit()
        exit()

    def mainLoop(self, camera):

        ## hang until assigned start time
        while time.time()<self.start:
            print time.time()-self.start
            pass

        ## start timer
	    self.startT = time.time()
        fed = False # feed delay control variable

        ## start recording
        if camera == 'record':
            selft.startRecording()
        elif camera == 'notrecord':
            pass

        ## display stimulus/start main loop
        while ((time.time() - self.startT) < self.tLength):

            pygame.display.flip()
    	    self.screen.blit(self.image, (250,100)) # location of stimulus

            ## control feeder delay
            try:
                if (time.time() - self.startT) >  self.feedDelay:
                    if fed:
                        pass
                    elif GPIO.event_detected(self.feederin):
		                time.sleep(1.0)
		                GPIO.output(self.feederout,True)
                        fed = True
   		    else:
                       GPIO.output(self.feederout, False)

            except KeyboardInterrupt:
                self.safeQuit()

if __name__ == '__main__':

    ## load in command line argumenents
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

    ## parse trial details and pass it to the Trial class
    if args.["feed"]:
        T = Trial(args["presentedStim"], args["startTime"], 'feed')
    else:
        T = Trial(args["presentedStim"], args["startTime"], 'notfeed'))

    T.checkPiIP()
    T.whatStimulus()
    T.videoFileName(args["species"], args["round"], args["fishstandardlength"],
                    args["sex"], args["fish"], args["day"], args["session"], args["fedSide"])

    ## initialize camera IF attached to Pi
    if args["camera"]:
        T.cameraInit()
    else:
        pass

    ## start camera recording IF attached to Pi and begin mainloop of Trial
    if args["camera"]:
        T.mainLoop('record')
    else:
        T.mainLoop('notrecord')

    ## stop camera recording IF attached to Pi
    if args["camera"]:
        T.stopRecording()
    else:
        pass

    ## cleanup camera IF attached to Pi
    if args["camera"]:
	       T.cameraQuit()

    ## cleanup remaining processes and exit
    T.safeQuit()
