# -*- coding: utf-8 -*-
"""
Created on Sat Oct  3 18:40:23 2026

This is based off of video series by garrea01 on YouTube:
    Auditory psychophysics using Python and Psychopy

@author: solace
"""
from shared_imports import np, sd, wave, sf
from datetime import datetime
sample_rate: int = 48000

def main():
    #Create puretone and save value sent back by return function (i.e., faded_soundwave)
    freq = 1000
    my_sound = pure_tone(freq)
    file_name = save_wave(my_sound, str(freq))
    open_play(file_name)   
     
def pure_tone(
        frequency: int,
        duration: float = 0.25,
        fade_duration: float = 0.01,
        amplitude: float = 0.5,
        sample_rate: int = 48000
        ) -> np.ndarray: #saves newly created samples as a numpy array
    
    #Calculate number of samples needed in total and for fade in/out
    total_samples = int(duration * sample_rate)
    fade_samples = int(fade_duration * sample_rate)
    
    #Create an array of time points corresponding to sample on array
    time_points = np.linspace(0, duration, total_samples, False)
    
    '''Returns evenly spaced numbers over a specified interval.
    Start = starting value of sequence
    Stop = end value of the sequence, unless endpoint set to False
    Num = int, optional; number of samples to generate
    Endpoint = bool, optional; T stop is last sample, F last sample excluded'''
    
    #Calculate a sine value for each time point by converting Hz to rad/sec
    #Then multiply that by time_points to get phase at each time point
    sinewave = np.sin(2 * np.pi * frequency * time_points)
    
    #Scale by amplitude
    sinewave *= amplitude
    
    #Create the fade in/out curves
    fade_in = np.linspace(0, fade_duration, fade_samples)
    fade_out = np.linspace((duration - fade_duration), duration, fade_samples)
    
    #Create a master envelope matching full length of audio
    #Starts at 0, ramps up, stays at 1, ramps down to 0
    envelope = np.ones(total_samples)
    envelope[:fade_samples] = fade_in
    envelope[-fade_samples:] = fade_out
    
    #Multiply the sinewave by the envelope
    faded_sinewave = sinewave * envelope
    return faded_sinewave

def save_wave(my_sound, freq):
    #Convert float array (-0.5 to 0.5) to 16-bit integers (-32768 to 32767)
    audio_int16 = (my_sound * 32767).astype(np.int16)
    
    #Get current datetime and store in variable to be printed
    now = datetime.now()
    
    file_name = now.strftime(freq + "Hz_%H%M%S.wav")
    
    #Save using standard wave library
    with wave.open(file_name, "wb") as wav_file: # This saves correctly, but doesn't play correctly
        wav_file.setnchannels(1) # 1 = Mono, 2 = Stereo
        wav_file.setsampwidth(2) # 2 bytes = 16-bit audio
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_int16.tobytes())
    
    print("File Saved!")
    return file_name
    
def open_play(file_name):
    file_name = file_name
    data, fs = sf.read(file_name)
    sd.play(data, fs)
    
    
    

if __name__ == "__main__": 
    main()