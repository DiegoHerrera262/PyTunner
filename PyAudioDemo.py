import pyaudio
import numpy as np
import time
from matplotlib import pyplot as plt

class DataProcessor:

    '''
    Class for reading, plotting and processing audio data for
    my tunner
    '''

    # Parameters for reading audio
    CHUNK_SIZE = 4*1024                 # Number of samples in one data capture
    AUDIO_FORMAT = pyaudio.paInt16      # Format of audio data
    NUM_CHANNELS = 1                    # Number of channels that read input
    SAMP_RATE = 44100                   # Sampling Rate
    PyAudioInterface = pyaudio.PyAudio()
    # Reading object from pyaudio

    # Init function of data processor (for completeness)
    def __init__(self,CHUNK_SIZE = 4*1024,\
                 AUDIO_FORMAT = pyaudio.paInt16,\
                 NUM_CHANNELS = 1,SAMP_RATE = 44100):
        '''
        Function for initialising DataProcessor
        '''
        self.CHUNK_SIZE = CHUNK_SIZE
        self.AUDIO_FORMAT = AUDIO_FORMAT
        self.NUM_CHANNELS = NUM_CHANNELS
        self.SAMP_RATE = SAMP_RATE
        self.stream = self.PyAudioInterface.open(format=self.AUDIO_FORMAT,\
                        channels=self.NUM_CHANNELS,\
                        rate=self.SAMP_RATE,\
                        input=True,
                        frames_per_buffer=self.CHUNK_SIZE)

    # Function for closing audio input
    def CloseMicrophone(self):
        '''
        Function for closing Audio input
        '''
        # Close stream
        self.stream.stop_stream()
        self.stream.close()
        self.PyAudioInterface.terminate()

    # Function for demo of waveform
    def DemoLiveAudio(self):
        '''
        Function for live demo of waveform
        '''
        # Set matplotlib for fast update
        fig, ax = plt.subplots()
        ax.set_ylim(-3,3)
        ax.set_title('Demo of Live Audio Input - Pulse Ctr + C to Exit')
        x = np.arange(0,self.CHUNK_SIZE)
        line, = ax.plot(x,np.random.rand(self.CHUNK_SIZE))
        # Set timer for live plot of waveform
        Proceed = True
        while Proceed:
            try:
                # Read data using pyaudio
                rawdata = self.stream.read(\
                self.CHUNK_SIZE,exception_on_overflow=False)
                # Convert to numpy array using numpy
                data = np.frombuffer(rawdata,dtype=np.int16)
                data = 1.0/500 * data
                # Update data on graphics and plot
                line.set_ydata(data)
                fig.canvas.draw()
                fig.canvas.flush_events()
                plt.pause(0.01)
            except KeyboardInterrupt:
                self.CloseMicrophone()
                Proceed = False
            except:
                raise Exception('Finised Demo')

DemoRecorder = DataProcessor()
DemoRecorder.DemoLiveAudio()
