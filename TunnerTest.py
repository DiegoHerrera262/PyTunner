# Consistency imports
import pyaudio
import numpy as np
import time
from matplotlib import pyplot as plt
from scipy.signal import find_peaks
# Import of PyTunner
import PyTunner as Tunner

FrecDetector = Tunner.DataProcessor()
FrecDetector.CaptureNoise()

FrecDetector.DemoLiveSpectrum()
