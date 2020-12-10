# Consistency imports
import pyaudio
import numpy as np
import time
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
# importing whole tkinter module
import tkinter as tk
# Import Frequency detector
import PyTunner as Tunner
# Import Pnadas for reading tone frequencies
import pandas as pd

MusicalPitches = pd.read_csv('MusicalPitches.txt',sep='\t')

def Freq2Note(f):
    prefilter = MusicalPitches[MusicalPitches.Frequency <= f]
    try:
        return prefilter.iloc[-1]['Note']
    except IndexError:
        return '---'

class TunnerGUI:

    '''
    Class for showing pitch and freq
    in a window for tunning
    '''

    def __init__(self,capture_noise = False):
        '''
        Function for instatiating Tunner GUI
        '''
        # Elements of raw GUI
        self.window = tk.Tk()
        self.window.title('PyTunner')
        self.Label = tk.Label(self.window,
                              text = 'Main Freq. = 0.0')
        # Element for measuring main frequency
        self.FrecDetector = Tunner.DataProcessor()
        # Frequency key
        self.x = np.linspace(0,self.FrecDetector.SAMP_RATE/2,\
                            num=self.FrecDetector.CHUNK_SIZE//2)
        # Capture ambient noise
        if capture_noise:
            self.FrecDetector.CaptureNoise()

    def UpdateLabel(self):
        '''
        Update frequancy label
        '''
        # Determine maximum frequency
        freq = self.x[self.FrecDetector.MainFreqsAudio()]
        # Determine Note
        note = Freq2Note(freq)
        # Update label text
        self.Label.config(\
            text = 'Main Freq. = ' + '{:6.2f}'.format(freq) + ' Hz' + \
            ' (' + note + ')')
        # Pack label
        self.Label.after(100,self.UpdateLabel)

    def RunTunner(self):
        '''
        Display and update window with
        measured frequency
        '''
        self.Label.pack(anchor = 'center')
        self.UpdateLabel()
        self.window.mainloop()

if __name__ == '__main__':

    PitchApp = TunnerGUI()
    PitchApp.RunTunner()
