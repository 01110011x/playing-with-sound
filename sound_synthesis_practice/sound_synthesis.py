# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 12:50:30 2026

@author: solace

This was created based on the tutorial by Code Mewostro on YouTube: 
    Introduction to sound synthesis with Python: The Basics of Digital 
    Audio Programming
Honestly, this video was far too brief and presented a lot of information into 
11 minutes. There was so much brought up that I had to spend time picking apart
to understand thoroughly. I prefer garrea01's tutorial far more. Although he
uses PyAudio, which is now outdated.
"""
from shared_imports import np, sd 
#import numpy as np #makes functions on large number sets easier
#import sounddevice as sd #allows us to play sound i/o

#sd.default.device = [None, 22]
#print(sd.query_devices())

def main():
    #Generate white noise
    broadband = white_noise()
    #Play sound
    sd.play(broadband) #this plays back a NumPy array through audio output device
    sd.wait() #wait until audio is done before executing more code
    
    #Generate concert A
    pure_tone = sine_wave()
    #Play sound
    sd.play(pure_tone)
    sd.wait()
    

def white_noise(
        duration: float = 1.0,
        amplitude: float = 0.5,
        sample_rate: int = 48000 #standard sample rate
        ) -> np.ndarray: #saves newly created samples as a NumPy array


    #Calculate the number of samples needed
    n_samples = int(duration * sample_rate) #casted to interger for whole #
    
    #Generate white noise with values -1 < x < 1, using random generator
    noise = np.random.uniform(-1, 1, n_samples)
    
    #Scale by amplitude
    noise *= amplitude #adjusts volume of entire sample
    return noise

def sine_wave(
        frequency: int = 440,
        duration: float = 1.0,
        amplitude: float = 0.5,
        sample_rate: int = 48000
        ) -> np.ndarray:
        
    #Calculate number of samples needed
    total_samples = int(duration * sample_rate)
    
    #Create an array of time points corresponding to a sample on the sinewave
    time_points = np.linspace(0, duration, total_samples, False)
    '''
    Linspace creates an array of evenly spaced points
    that starts at 0, ends just before duration, and with 
    length = total_samples. False excludes the endpoint, ensuring
    we end just before the full duration.
    '''
    
    #Calculate a sine value for each time point by converting Hz to rad/sec
    #Then multiply that by time_points to get phase at each time point
    sine = np.sin(2 * np.pi * frequency * time_points)
    #This results in an array that contains values -1<x<1 that represent
    #The smooth movement of the sine wave
    
    #Scale by amplitude 
    sine *= amplitude
    return sine

#Execute the main function. Defining a function stores it, but you must exe.
#Add standard entry point logic to end of script
if __name__ == "__main__":
    main()