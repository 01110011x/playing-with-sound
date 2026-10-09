# -*- coding: utf-8 -*-
"""
Created on Sat Sep 12 14:16:29 2026

@author: foofi

Put all your common imports into a centralized module.
Call this at the top of your main function by using 
    from shared_imports import *
"""

import numpy as np #makes functions on large number sets easier
import sounddevice as sd #allows us to play sound i/o
import soundfile as sf #allows us to read and write soundfiles
import wave #built-in module that reads and writes uncompressed audio files
import time #low-level platform-dependent functions for handling time access
import pyaudio #record, play, and manipulate audio streams
import matplotlib.pyplot as plt #spectrogram
import pandas as pd

#Define exactly what gets sent out when called via "import *"
__all__ = ['np', 'sd', 'sf', 'wave', 'time', 'pyaudio', 'plt', 'pd']