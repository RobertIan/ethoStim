__author__ = 'ian'


# imports
import sys
import time
import csv
from psychopy import visual, core, event
import os
import subprocess


# housekeeping
clock = core.Clock()
date = time.strftime('%m%d%Y')
now = time.strftime('%X')
nowfolder = time.strftime('%H%M%S')


# open output csv file for writing or appending

f = os.path.join(os.getcwd() + date + '_ethotrials.csv')
print f
try:
    fsize = os.stat(f).st_size
except OSError:
    w = csv.writer(open(f, "w+b"))
    w.writerow(
        ['date', 'trial time start', 'stimulus ID', 'trial type', 'fish group', 'stimulus1 name', 'stimulus1 screen',
         'stimulus2 name',
         'stimulus2 screen'])
else:
    if fsize > 0:
        w = csv.writer(open(f, 'a'), delimiter=',')
# fish specification

try:
    pesces = sys.argv[3]
except IndexError:
    print "you forgot to say which fish these are (e.g.; 'm1_f3' -[lftf_rghtf]"
    pesces = 'lf?_rf?'

try:
    lftpez, rgtpez = pesces.split("_")
except NameError:
    pass


# presentation windows
win1 = visual.Window(screen=0, size=(1024, 768), pos=(0, 0))
win2 = visual.Window(screen=1, size=(1024, 768), pos=(0, 0))

# stimulus picking tree, adjust trial TypeIDs/stimulus combinations here
try:
    stimID = sys.argv[1]
    if stimID == '5_10':
        trialstim1 = visual.ImageStim(win1, image='5.png', pos=(0, 0.75), colorSpace='rgb', name='5.png')
        trialstim2 = visual.ImageStim(win2, image='10.png', pos=(0, 0.75), colorSpace='rgb', name='10.png')
    if stimID == '6_12':
        trialstim1 = visual.ImageStim(win1, image='6.png', pos=(0, 0.75), colorSpace='rgb', name='6.png')
        trialstim2 = visual.ImageStim(win2, image='12.png', pos=(0, 0.75), colorSpace='rgb', name='12.png')
    if stimID == '7_14':
        trialstim1 = visual.ImageStim(win1, image='7.png', pos=(0, 0.75), colorSpace='rgb', name='7.png')
        trialstim2 = visual.ImageStim(win2, image='14.png', pos=(0, 0.75), colorSpace='rgb', name='14.png')
    if stimID == '8_12':
        trialstim1 = visual.ImageStim(win1, image='8.png', pos=(0, 0.75), colorSpace='rgb', name='8.png')
        trialstim2 = visual.ImageStim(win2, image='12.png', pos=(0, 0.75), colorSpace='rgb', name='12.png')
    if stimID == '9_12':
        trialstim1 = visual.ImageStim(win1, image='9.png', pos=(0, 0.75), colorSpace='rgb', name='9.png')
        trialstim2 = visual.ImageStim(win2, image='12.png', pos=(0, 0.75), colorSpace='rgb', name='12.png')
    if stimID == 'acclim_acclim':
        trialstim1 = visual.ImageStim(win1, image='0.png', pos=(0, 0.75), colorSpace='rgb', name='0.png')
        trialstim2 = visual.ImageStim(win2, image='0.png', pos=(0, 0.75), colorSpace='rgb', name='0.png')
    if stimID == '10_5':
        trialstim1 = visual.ImageStim(win2, image='5.png', pos=(0, 0.75), colorSpace='rgb', name='5.png')
        trialstim2 = visual.ImageStim(win1, image='10.png', pos=(0, 0.75), colorSpace='rgb', name='10.png')
    if stimID == '12_6':
        trialstim1 = visual.ImageStim(win2, image='6.png', pos=(0, 0.75), colorSpace='rgb', name='6.png')
        trialstim2 = visual.ImageStim(win1, image='12.png', pos=(0, 0.75), colorSpace='rgb', name='12.png')
    if stimID == '14_7':
        trialstim1 = visual.ImageStim(win2, image='7.png', pos=(0, 0.75), colorSpace='rgb', name='7.png')
        trialstim2 = visual.ImageStim(win1, image='14.png', pos=(0, 0.75), colorSpace='rgb', name='14.png')
    if stimID == '12_8':
        trialstim1 = visual.ImageStim(win2, image='8.png', pos=(0, 0.75), colorSpace='rgb', name='8.png')
        trialstim2 = visual.ImageStim(win1, image='12.png', pos=(0, 0.75), colorSpace='rgb', name='12.png')
    if stimID == '12_9':
        trialstim1 = visual.ImageStim(win2, image='9.png', pos=(0, 0.75), colorSpace='rgb', name='9.png')
        trialstim2 = visual.ImageStim(win1, image='12.png', pos=(0, 0.75), colorSpace='rgb', name='12.png')

except IndexError:
    print "you forgot to say what trial type. defaulting to 'acclim'"
    trialstim1 = visual.ImageStim(win2, image='0.png', pos=(0, 0.75), colorSpace='rgb', name='0.png')
    trialstim2 = visual.ImageStim(win1, image='0.png', pos=(0, 0.75), colorSpace='rgb', name='0.png')

try:
    lftstim, rgtstim = stimID.split("_")
except NameError:
    pass

# training or probe trial/length
try:
    ttID = sys.argv[2]
    if ttID == 'train':
        tLength = 4 * 60
    if ttID == 'probe':
        tLength = 4 * 60
except IndexError:
    print "you forgot to say if this is a 'train' or 'probe' trial"
    tLength = 1 * 60

try:
    w.writerow([date, now, stimID, ttID, pesces, trialstim1.name, trialstim1.win.screen, trialstim2.name,
                trialstim2.win.screen])
except NameError:
    w.writerow([date, now, 'stimID missing', 'ttID missing', 'fishids missing', trialstim1.name, trialstim1.win.screen,
                trialstim2.name,
                trialstim2.win.screen])

prepcam1 = subprocess.Popen(['v4l2-ctl', '-d', '/dev/video0', '--set-ctrl', 'focus_auto=0'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
prepcam2 = subprocess.Popen(['v4l2-ctl', '-d', '/dev/video1', '--set-ctrl', 'focus_auto=0'],
                            stdin=subprocess.PIPE,
                            stdout=subprocess.PIPE)
'''
prepcam1b = subprocess.Popen(['v4l2-ctl', '-d', '/dev/video0', '--set-ctrl', 'white_balance_temperature_auto=0'],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
prepcam2b = subprocess.Popen(['v4l2-ctl', '-d', '/dev/video1', '--set-ctrl', 'white_balance_temperature_auto=0'],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
'''
prepcam1c = subprocess.Popen(['v4l2-ctl', '-d', '/dev/video0', '--set-ctrl', 'focus_absolute=10'],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)
prepcam2c = subprocess.Popen(['v4l2-ctl', '-d', '/dev/video1', '--set-ctrl', 'focus_absolute=10'],
                             stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE)

allKeys = event.waitKeys()


# hang here until trial is started
for thisKey in allKeys:
    if thisKey == 's':


        # adjust these commands based on OS and desired video format/codec.
        '''
        # These capture Isight cam ('0') and desktop ('1') on OSX 10.10.2
        subprocess.Popen(['ffmpeg', '-f', 'avfoundation', '-i', '0', '-t', str(tLength / 60), '../out.mpg'],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE)
        subprocess.Popen(['ffmpeg', '-f', 'avfoundation', '-i', '1', '-t', str(tLength / 60), '../out2.mpg'],
                         stdin=subprocess.PIPE,
                         stdout=subprocess.PIPE)
        '''
        # These capture cam1 ('/dev/video0') and  cam2 ('/dev/video1') on Ubuntu with v4l2
        p1 = subprocess.Popen(
            ['ffmpeg', '-f', 'v4l2', '-i', '/dev/video0', '-q', '2', '-s', '1920x1080', '-t',
             str(tLength), str(lftpez) + str(lftstim) + '.avi'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)
        p2 = subprocess.Popen(
            ['ffmpeg', '-f', 'v4l2', '-i', '/dev/video1', '-q', '2', '-s', '1920x1080', '-t',
             str(tLength), str(rgtpez) + str(rgtstim) + '.avi'],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE)

        startT = clock.getTime()
        while (clock.getTime() - startT) < tLength:
            trialstim1.draw()
            trialstim2.draw()
            win1.flip()
            win2.flip()
            if not p1.poll():
                if (clock.getTime() - startT) > tLength + 15:
                    print 'warning, p1 requires restart'
                    p1 = subprocess.Popen(['ffmpeg', '-f', 'v4l2', '-i', '/dev/video0', '-q', '2', '-s', '1920x1080',
                                           '-t', str(tLength-(clock.getTime() - startT)), str(lftpez) + str(lftstim) + str(clock.getTime()) + '.avi'],
                                          stdin=subprocess.PIPE,
                                          stdout=subprocess.PIPE)
                    startT = clock.getTime()
            if not p2.poll():
                if (clock.getTime() - startT) > tLength + 15:
                    print 'warning, p2 requires restart'
                    p2 = subprocess.Popen(['ffmpeg', '-f', 'v4l2', '-i', '/dev/video0', '-q', '2', '-s', '1920x1080',
                                           '-t', str(tLength-(clock.getTime() - startT)), str(lftpez) + str(lftstim) + str(clock.getTime()) + '.avi'],
                                          stdin=subprocess.PIPE,
                                          stdout=subprocess.PIPE)
                    startT = clock.getTime()
            else:

                continue


if prepcam1.poll():
    prepcam1.kill()
if prepcam2.poll():
    prepcam2.kill()
if prepcam1c.poll():
    prepcam1c.kill()
if prepcam2c.poll():
    prepcam2c.kill()
if p1.poll():
    p1.kill()
if p2.poll():
    p2.kill()
win1.close()
win2.close()
core.quit()
