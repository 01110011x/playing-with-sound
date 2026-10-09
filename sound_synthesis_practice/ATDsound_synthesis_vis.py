# -*- coding: utf-8 -*-
"""
Created on Mon Sep  7 12:50:30 2026

@author: solace

I followed a tutorial to generate this sound, but I am trying to develop my 
method: generate, save to .wav, then play it.

The other tutorial was showing me how to use a non-blocking method for playback
using PyAudio. But here, I am trying to do something similar using sounddevice.
Apparently, sounddevice is less clunky than PyAudio.
"""
from shared_imports import np, sd, sf, wave, time, plt

def main():
    #Generate sound
    sample_rate = 48000
    mysound = white_noise()
    
    #Convert float array (-0.5 to 0.5) to 16-bit integers (-32768 to 32767)
    #Multiply sound array to 32767 to scale it safely for standard audio
    audio_int16 = (mysound * 32767).astype(np.int16)
    
    #Save using standard wave library
    with wave.open("faded_white_noise.wav", "wb") as wav_file:
        wav_file.setnchannels(1) # 1 = Mono, 2 = Stereo
        wav_file.setsampwidth(2) # 2 bytes = 16-bit audio
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_int16.tobytes())
    
    print("Saved faded_white_nosise.wav successfully!")
    
    #Load saved WAV file data and sample rate
    data, fs = sf.read('faded_white_noise.wav')
    
    #Launch spectrogram visualization here
    plot_spectrogram(mysound, sample_rate, title = "White Noise Spectrogram (0.1s Fades)")
    
    #Playback a NumPy array containing audio data at specified sample rate
    sd.play(data, fs)
    
    #Program can do other tasks simultaneously
    for i in range(3):
        print(f"Doing other work...{i}")
        time.sleep(1) #Simulating active background tasks

def white_noise(
        duration: float = 1.0,#in seconds
        fade_duration: float = 0.1, #in seconds
        amplitude: float = 0.5,
        sample_rate: int = 48000 #standard sample rate
        ) -> np.ndarray: #saves newly created samples as a NumPy array


    #Calculate the number of samples needed
    total_samples = int(duration * sample_rate)
    fade_samples = int(fade_duration * sample_rate)
    
    #Generate white noise with values -1 < x < 1, using random generator
    noise = np.random.uniform(-1, 1, total_samples) #Generates random data across audio spectrum
    
    #Scale by amplitude
    noise *= amplitude #adjusts volume of entire sample
    
    #Create the fade curves
    fade_in_curve = np.linspace(0.0, 1.0, fade_samples)# creates smooth ramp of multipliers from 0.000 up to 1.000
    fade_out_curve = np.linspace(1.0, 0.0, fade_samples)
        
    #Create a master envelope matching full length of audio
    #Starts at 0, ramps up, stays at 1, ramps down to 0
    envelope = np.ones(total_samples) #fills middle section of audio envelope with 1.0 so noise plays at full volume after fade-in
    envelope[:fade_samples] = fade_in_curve #apply fade-in to the start
    envelope[-fade_samples:] = fade_out_curve #apply fade-out to the end
    
    #Multiply the noise by the envelope
    faded_noise = noise*envelope
    return faded_noise #sends data back for saving/future use; stops the fcn

def plot_spectrogram(data, sample_rate, title="Spectrogram Visualization"):
    plt.figure(figsize=(10,5))
    
    #NFFT controls frequency resolution window higher=sharper
    #cmap = 'magma' black, purple, orange, yellow heatmap
    spectrum, freqs, t, im = plt.specgram(data, NFFT=1024, 
         Fs=sample_rate,cmap = 'magma')
    
    #Add labels and formatting
    plt.title(title, fontsize=14, fontweight = 'bold')
    plt.xlabel("Time (Seconds)", fontsize = 11)
    plt.ylabel("Frequency (Hertz)", fontsize = 11)
    
    #Limit frequency view up to the Nyquist freq
    plt.ylim(0, sample_rate / 2)
    
    #Add a visual color bar intensity legend to track volume level (dB scale)
    cbar = plt.colorbar(im)
    cbar.set_label("Intensity (dB)", fontsize = 11)
    
    plt.tight_layout()
    plt.show()

#Execute the main function. Defining a function stores it, but you must exe.
#Add standard entry point logic to end of script
if __name__ == "__main__":
    main()