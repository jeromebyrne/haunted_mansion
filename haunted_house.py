# -*- coding: utf-8 -*-
from picamera import PiCamera
import datetime
import io
import os
import time
from PIL import Image
from time import sleep
from subprocess import call
import pygame
import random

def compare():
   camera.resolution = (streamWidth, streamHeight)
   stream = io.BytesIO()
   camera.capture(stream, format = 'bmp')
   stream.seek(0)
   im = Image.open(stream)
   buffer = im.load()
   stream.close()
   return im, buffer

def triggerSurprise():
    randomSoundFile = "sfx/chainsaw.wav"
    
    if soundTheme == entranceSounds:
        randomSoundFile = random.choice(entranceSounds)
    elif soundTheme == jumpScareSounds:
        randomSoundFile = random.choice(jumpScareSounds)
    elif soundTheme == randomSounds:
        randomSoundFile = random.choice(randomSounds)
    elif soundTheme == mixSounds:
    	randomSoundFile = random.choice(mixSounds)
    
    sound = pygame.mixer.Sound(randomSoundFile)
    sound.play()
    sleep(sound.get_length() + postSurpriseDelay)

#sound effect lists
entranceSounds = ["sfx/haunted_mansion_2.wav", "sfx/not_a_game.wav", "sfx/prepare.wav", "sfx/stay_out.wav"]
jumpScareSounds = ["sfx/chainsaw.wav", "sfx/witch.wav", "sfx/incoherent.wav"]
randomSounds = ["sfx/hounds.wav", "sfx/dont_lose_your_head.wav", "sfx/rosie.wav", "sfx/don_julio.wav", "sfx/incoherent_2.wav", "sfx/leave_here.wav"]
mixSounds = ["sfx/hounds.wav", "sfx/dont_lose_your_head.wav", "sfx/rosie.wav","sfx/haunted_mansion_2.wav", "sfx/not_a_game.wav", "sfx/prepare.wav", "sfx/stay_out.wav","sfx/chainsaw.wav", "sfx/witch.wav","sfx/don_julio.wav", "sfx/incoherent_2.wav", "sfx/leave_here.wav"]

#set the soundTheme appropriate to the placement of the camera
#soundTheme = entranceSounds
#soundTheme = jumpScareSounds
#soundTheme = randomSounds
soundTheme = mixSounds

#motion vars
streamWidth = 320
streamHeight = 180
streamTotalPixels = streamWidth * streamHeight
difference = 15
pixelThreshold = streamTotalPixels * 0.05
sleepBetweenFrames = 0.1
postSurpriseDelay = 3

#camera setup
camera = PiCamera()
camera.rotation = 180
camera.resolution = (1920,1080)
#camera.start_preview(alpha=200)

#brief startup delay to move out of the way etc...
startupDelay=3
sleep(startupDelay)

#create the first image
image1, buffer1 = compare()

#init audio
pygame.mixer.init()

while (True):

    sleep(sleepBetweenFrames)
    image2, buffer2 = compare()

    changedpixels = 0
    for x in range(0, streamWidth):
        for y in range(0, streamHeight):
            pixdiff = abs(buffer1[x,y][1] - buffer2[x,y][1])
            if pixdiff > difference:
                changedpixels += 1

    if changedpixels > pixelThreshold:
        triggerSurprise()
        image1, buffer1 = compare()
        image2, buffer2 = compare()
    else:
        image1 = image2
        buffer1 = buffer2 
