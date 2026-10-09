# -*- coding: utf-8 -*-
"""
Created on Fri Sep 04 17:31:15 2026

Based on videoseries by garrea01 on YouTube: Using Psychopy and Python for
Sound Experiments (video 3): Non blocking sound presentation

@author: solace
"""


import wave
import pyaudio
from datetime import datetime
import time

n = 1024 #number of samples per chunk. consider limitations on stream rate

#Step 1 - Open the wave file
sound_stim = wave.open('whitenoise_1000msec.wav', 'rb')
num_samples = sound_stim.getnframes()
print("Num Samples (s): " + str(num_samples))
sample_rate = sound_stim.getframerate()
print("Sample Rate (s/sec): " + str(sample_rate))
duration = round(num_samples/sample_rate, 4)
print("Duration (sec): " + str(duration))

#Step 2 - Initiate pyAudio
p = pyaudio.PyAudio()

def callback(in_data, frame_count, time_info, status):
    data = sound_stim.readframes(frame_count)
    return(data, pyaudio.paContinue)

stream = p.open(format=p.get_format_from_width(sound_stim.getsampwidth()),
   channels=sound_stim.getnchannels(),
   rate = sample_rate,
   output = True,
   stream_callback = callback
   )

before = datetime.now()
stream.start_stream()
after = datetime.now()
delta = round((after.microsecond / 1000) - (before.microsecond / 1000), 3)
print("Time difference: %6.3f" % (delta))

while stream.is_active():
    time.sleep(0.1)

#Stop while loop and close stream
stream.stop_stream()
stream.close()

#Terminate pyAudio
p.terminate() 
