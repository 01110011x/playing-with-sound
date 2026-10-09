# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 22:37:17 2026

@author: solace

I am going to create a booth check simulation game!
"""
from shared_imports import np, sd

def main():
    print("Let's do a booth listening check!")
    wait = input("Press enter to continue...")
    
    #Define available choices
    available_freqs = [250, 500, 1000, 2000, 3000, 4000, 6000, 8000]
    
    #Ask user for starting frequency
    frequency_str = input(
        '''Which frequency should we start with?
    250 Hz, 500 Hz, 1000 Hz, 2000 Hz, 
    3000 Hz, 4000 Hz, 6000 Hz, or 8000 Hz?
    Type Here: ''')  
    
    #Convert string answer into Hz int
    process_answer = "".join(char for char in frequency_str if char.isdigit())
    frequency = int(process_answer)
    
    #Check that answer is in available freq list. If so, play sound.
    if frequency in available_freqs:
        available_freqs.remove(frequency) #removes selection from list
        print("Here we go...push 'enter' to check this frequency!")
        input(wait)
        sound_check = pure_tone(frequency) #play selected freq
        sd.play(sound_check)
        sd.wait()
        
    #If not, give user another chance.
    else:
        frequency_str = input(f'''\nPlease select a clinically tested frequency
                        {available_freqs}
                        Type selection here: ''')
        #Convert string answer into Hz int
        process_answer = "".join(char for char in frequency_str if char.isdigit())
        frequency = int(process_answer)
        available_freqs.remove(frequency) #remove selection from list
        print(f'''\nYou picked {frequency}!
        Press 'enter' to test. ''')
        input(wait)
        sound_check = pure_tone(frequency) #play selected freq
        sd.play(sound_check)
        sd.wait()
    
    print("Great job! Let's continue.")
    input(wait)
    
    #Start a loop that runs as long as there are frequencies to test
    while available_freqs:
        print(f"\nWhich frequency should we test next? {available_freqs}")
        frequency_str = input("Type selection here: ")
        #Turn input into an integer and play sound
        process_answer = "".join(char for char in frequency_str if char.isdigit())
        frequency = int(process_answer)
        sound_check = pure_tone(frequency)
        
        #Once again, verify ththat the user's choice is valid
        if frequency in available_freqs:
            available_freqs.remove(frequency)
            input(f"\nYou picked {frequency}! Press 'enter' to test. ")
            sound_check = pure_tone(frequency)
            sd.play(sound_check)
            sd.wait()
            input(wait)
            
        #If not, prompt them to select from the list.
        else:
            #todo this prints weird w/ the n slash
            frequency_str = input(f'''n\Please select a clinically tested frequency.
                  Recall, options are {available_freqs} 
                  Type selection here: ''')
            process_answer = "".join(char for char in frequency_str if char.isdigit())
            frequency = int(process_answer)
            available_freqs.remove(frequency)
            #todo as does this line with the n slash
            input(f"n\You picked {frequency}! Press 'enter' to test. ")
            sound_check = pure_tone(frequency)
            sd.play(sound_check)
            sd.wait()
            input(wait)
             

    print("Booth check done! Happy testing!")
    input(wait)
    input("Press enter to end. ")
    
    #Old code that checks the rest of the frequencies x number of times
    '''
    This loops thorugh 8 choices. Above, we see a loop that removes choices as 
    they are picked.
    for i in range(7):
        frequency_str = input(
        "Which frequency should we check next?
        Type Here: ")
        process_answer = "".join(char for char in frequency_str if char.isdigit())
        frequency = int(process_answer)
        sound_check = pure_tone(frequency)
        sd.play(sound_check)
        sd.wait()
        input(wait)
        print("Great job!")
        input(wait)
        
    print("Booth check done! Happy testing!")
    input("Press enter to end. ") 
    '''

#Create a pure tone of any selected frequency
def pure_tone(
        frequency,
        duration: float = 2.0,
        sample_rate: int = 48000,
        amplitude: float = 0.5,
        ) -> np.ndarray:
    
        #Calculate total number of samples
        total_samples = int(duration * sample_rate)
    
        #Create an array of time points
        time_points = np.linspace(0, duration, total_samples, False)
        sine = np.sin(2 * np.pi * frequency * time_points)
    
        #Scale by amplitude
        sine *= amplitude
        return sine
    
    
if __name__ == "__main__":
    main()
