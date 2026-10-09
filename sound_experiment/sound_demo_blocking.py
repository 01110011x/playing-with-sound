# -*- coding: utf-8 -*-
"""
Created on Mon Aug 31 21:07:58 2026

Based on videoseries by garrea01 on YouTube: Using Psychopy and Python for
Sound Experiments (video 2): Using pyaudio to play sound files

@author: solace
"""


import wave
import pyaudio

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

#Step 3 - Create a stream object using p.open function 
    #arguments required for p.open(format, channels, rate, output)
        #format is bit rate, we will use .wav file to define it:
            #use sound_stim as defined. recall, we used our gen'd file
        #channels obtained from selected sound stimulus. think mono v. stereo
            #let wav file determine appropriate channels
        #rate from what was alread calculated above
        #output, is it an output? y/n
stream = p.open(format=p.get_format_from_width(sound_stim.getsampwidth()),
   channels=sound_stim.getnchannels(),
   rate = sample_rate,
   output = True)

#Step 4 - Read Data from wave, readframes(n)
    #So now we've got .wav, got stream, now we need to add info from .wav into stream
    #Let's use a blocking routine where we pass chunks of samples to stream 
        #Until we reach end of .wav
data = sound_stim.readframes(n)

#Step 5 - Pass data to stream.write and continually update position in .wav
    #While we have data, we need to write that data to the stream. Update our
        #place in the .wav
while data:
    stream.write(data) #blocks the next data read until finished sec=(n/samplerate)
    data = sound_stim.readframes(n)
    print("Current Position: " + str(sound_stim.tell())) #tell position on .wav

#Step 6 - Stop while loop and close stream
stream.stop_stream()
stream.close()

#Step 7 - Terminate pyAudio
p.terminate() 
