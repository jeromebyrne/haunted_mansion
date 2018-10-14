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

def compare():
   camera.resolution = (streamWidth, streamHeight)
   stream = io.BytesIO()
   camera.capture(stream, format = 'bmp')
   stream.seek(0)
   im = Image.open(stream)
   buffer = im.load()
   stream.close()
   return im, buffer


streamWidth = 320
streamHeight = 180
streamTotalPixels = streamWidth * streamHeight

difference = 20
pixelThreshold = streamTotalPixels * 0.01

sleepBetweenFrames = 0.4
startupDelay=3

camera = PiCamera()
camera.rotation = 180
camera.resolution = (1920,1080)
camera.start_preview(alpha=128)

sleep(startupDelay)

timestamp = time.time()

image1, buffer1 = compare()

pygame.mixer.init()

while (True):

    sleep(sleepBetweenFrames)
    image2, buffer2 = compare()
    timestamp = time.time()

    changedpixels = 0
    for x in range(0, streamWidth):
        for y in range(0, streamHeight):
            pixdiff = abs(buffer1[x,y][1] - buffer2[x,y][1])
            if pixdiff > difference:
                changedpixels += 1

    if changedpixels > pixelThreshold:
        pygame.mixer.music.load("sfx/haunted_mansion_2.wav")
        pygame.mixer.music.play()
        sleep(30)
    image1 = image2
    buffer1 = buffer2 
