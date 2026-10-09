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

'''
    This imports the datetime "module" which is something that serves to create 
    a separation of attributes under a hierarchy so you don't accidentally over-
    write other code on import.
    
    "Modules" expose attributes on import. The "attribute" you are accessing is
    the datetime module's datetime attribute which is a class that happens to
    just have the same name. So when you access it, it looks like 
    datetime.datetime
    
    That "class" supports a "method" (which is also an attribute of the class, 
    not the module) named "now". So when you are accessing that method, it looks 
    like datetime.datetime.now() to call it.
    
    If you wanted to simplify the hierarchy on import, you could clarify that
    you only want the datetime class out of the datetime module, as seen above.
'''

n = 1024 #number of samples per chunk. consider limitations on stream rate

#Step 1 - Open the wave file
sound_stim = wave.open('whitenoise_1000msec.wav', 'rb') #note, rb = read wave file
num_samples = sound_stim.getnframes() #frames = samples
print("Num Samples (s): " + str(num_samples))
sample_rate = sound_stim.getframerate() #rate is samples per second
print("Sample Rate (s/sec): " + str(sample_rate))
duration = round(num_samples/sample_rate, 4) #calculate duration, round to 4dc
print("Duration (sec): " + str(duration))

#Step 2 - Initiate pyAudio
p = pyaudio.PyAudio()

#Looking for a way to play sound without waiting for it to write to the stream.
#Do so by using callback function
#This starts a second 'thread' that is devoted to playing the sound stimulus
#It doesn't block the execution of our main while loop
def callback(in_data, frame_count, time_info, status):
    #^ these will be grabbed from stream_callback
    data = sound_stim.readframes(frame_count)
    return(data, pyaudio.paContinue) #is there still data to read?

#Create a stream object using p.open(format, channels, rate, output) function 
#format = bit rate; channels = mono v. stereo; rate = samples/sec; output t/f
stream = p.open(format=p.get_format_from_width(sound_stim.getsampwidth()),
   channels=sound_stim.getnchannels(),
   rate = sample_rate,
   output = True,
   stream_callback = callback #this calls the callback above and reads frames for us
   )

#Read Data from wave, readframes(n)
#data = sound_stim.readframes(n) <- no longer needed bc it's in the callback

#Pass data to stream.write and continually update position in .wav
#while data:
   # stream.write(data)
    #data = sound_stim.readframes(n)
    #print("Current Position: " + str(sound_stim.tell())) tell position on .wav

before = datetime.now()
stream.start_stream() #this allows stream to start in second thread
#frees up space here to start things to run simultaneous to your stimulus
after = datetime.now()
delta = round((after.microsecond / 1000) - (before.microsecond / 1000), 3)
print("Time difference: %6.3f" % (delta)) #formats a floating-point number to
#use a total width of 6 characters with 3 digits after the decimal point

while stream.is_active():
    time.sleep(0.1)

#Stop while loop and close stream
stream.stop_stream()
stream.close()

#Terminate pyAudio
p.terminate() 
