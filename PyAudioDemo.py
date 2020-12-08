import pyaudio
import numpy as np
import tkinter as tk
import time
from matplotlib import pyplot as plt
from scipy.signal import find_peaks

class DataProcessor:

    '''
    Class for reading, plotting and processing audio data for
    my tunner
    '''

################################################################################
#                            PARAMETERS OF CLASS                               #
################################################################################

    # Parameters for reading audio
    CHUNK_SIZE = 10*1024             # Number of samples in one data capture
    AUDIO_FORMAT = pyaudio.paInt16      # Format of audio data
    NUM_CHANNELS = 1                    # Number of channels that read input
    SAMP_RATE = 44100                   # Sampling Rate
    PyAudioInterface = pyaudio.PyAudio()
    # Noise audio
    NOISE = None
    Proceed = True

################################################################################
#                            FUNDAMENTAL FUNCTIONS                             #
################################################################################

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
        self.window = tk.Tk()
        self.window.title('Demo Main Freq.')
        self.message = tk.Label(self.window)

    # Function for closing audio input
    def CloseMicrophone(self):
        '''
        Function for closing Audio input
        '''
        # Close stream
        self.stream.stop_stream()
        self.stream.close()
        self.PyAudioInterface.terminate()

    # Read and report audio data
    def ReadAudio(self):
        '''
        Funtion for reading and sending
        audio data for further processing
        '''
        # Read data using pyaudio
        rawdata = self.stream.read(\
        self.CHUNK_SIZE,exception_on_overflow=False)
        # Convert to numpy array using numpy
        data = np.frombuffer(rawdata,dtype=np.int16)
        data = 1.0/500 * data
        return data

    # Function for capturing ambient noise
    def CaptureNoise(self):
        '''
        Function for capturing ambient noise
        '''
        data = self.ReadAudio()
        for i in range(59):
            data = data + self.ReadAudio()
        self.NOISE =  1/60 * (data-np.mean(data))

    # Read audio and compute power spectrum using FFT
    def PowerSpectrumAudio(self):
        '''
        Function for computing FFT of
        audio for further analysis
        '''
        # Read input data
        data = self.ReadAudio() * np.hamming(self.CHUNK_SIZE)
        data = data - np.mean(data) - self.NOISE
        # Compute FFT using numpy
        data_fft = np.fft.fft(data)
        return 2/self.CHUNK_SIZE * np.abs(data_fft[:len(data)//2])

    def AutoCorrSpecAudio(self):
        '''
        Function for computing autocorrelation
        of audio Input
        '''
        # Read input Data
        data = self.ReadAudio() * np.hamming(self.CHUNK_SIZE)
        data = data - np.mean(data) - self.NOISE
        # Compute FFT using numpy
        data_fft = np.fft.fft(data)
        return 2/self.CHUNK_SIZE * np.abs(np.fft.ifft(data_fft * data_fft))

    # Read audio and compute CEPSTRUM usinf FFT
    def CepstrumAudio(self):
        '''
        Function for cumputing cepstrum.
        This is useful in detecting notes.
        '''
        # Read Power Spectrum
        data = self.PowerSpectrumAudio()
        # It already contains abs, so only log and FT remain
        return np.abs(np.fft.ifft(np.log(data[:len(data)//2])))

    # Compute principal frequencies of audio signal from Power spectrum
    def MainFreqsAudio(self):
        '''
        Function for computing main frequencies
        of audio from power spectrum
        '''
        # Read Power Spectrum
        data = self.PowerSpectrumAudio()
        data = 1/np.max(data) * data
        # Compute peaks using scipy
        mainfreqs, _ = find_peaks(data,height=0.7)
        return self.SAMP_RATE/self.CHUNK_SIZE * mainfreqs

################################################################################
#                               DEMO FUNCTIONS                                 #
################################################################################

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
        self.Proceed = True
        while self.Proceed:
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
                self.Proceed = False
            except:
                raise Exception('Finised Demo')

    # Function for demo spectrum
    def DemoLiveSpectrum(self):
        '''
        Function for demo spectrum
        '''
        # Set matplotlib for fast update
        fig, ax = plt.subplots()
        ax.set_ylim(0,2.0)
        ax.set_xlim(0,7000)
        ax.set_title('Demo of Live Audio Spectrum - Pulse Ctr + C to Exit')
        x = np.linspace(0,self.SAMP_RATE/2,num=self.CHUNK_SIZE//2)
        line, = ax.plot(x,np.random.rand(self.CHUNK_SIZE//2))
        # Set timer for live plot of waveform
        self.Proceed = True
        while self.Proceed:
            try:
                # Compute FFT data
                data = self.PowerSpectrumAudio()
                data = 1/np.max(data) * data
                # Update data on graphics and plot
                line.set_ydata(data)
                fig.canvas.draw()
                fig.canvas.flush_events()
                plt.pause(0.015)
            except KeyboardInterrupt:
                self.CloseMicrophone()
                self.Proceed = False
            except:
                raise Exception('Finised Demo')

    # Function for demo CEPSTRUM
    def DemoLiveCepstrum(self):
        '''
        Function for demo cepstrum
        '''
        # Set matplotlib for fast update
        fig, ax = plt.subplots()
        ax.set_ylim(0,0.1)
        ax.set_xlim(0,1000)
        ax.set_title('Demo of Live Audio Cepstrum - Pulse Ctr + C to Exit')
        x = 1 / np.linspace(0,self.CHUNK_SIZE/(self.SAMP_RATE*2),\
                        num=self.CHUNK_SIZE//4)
        line, = ax.plot(x,np.random.rand(self.CHUNK_SIZE//4))
        # Set timer for live plot of waveform
        self.Proceed = True
        while self.Proceed:
            try:
                # Compute FFT data
                data = self.CepstrumAudio()
                # Update data on graphics and plot
                line.set_ydata(data)
                fig.canvas.draw()
                fig.canvas.flush_events()
                plt.pause(0.015)
            except KeyboardInterrupt:
                self.CloseMicrophone()
                self.Proceed = False
            except:
                raise Exception('Finised Demo')

    # Function for demo spectrum
    def DemoLiveAutoCorr(self):
        '''
        Function for demo autocorrelation
        '''
        # Set matplotlib for fast update
        fig, ax = plt.subplots()
        ax.set_ylim(0,3.0)
        ax.set_xlim(0,self.CHUNK_SIZE)
        ax.set_title('Demo of Live Audio Autocorrelation - Pulse Ctr + C to Exit')
        x = np.arange(0,self.CHUNK_SIZE)
        line, = ax.plot(x,np.random.rand(self.CHUNK_SIZE))
        # Set timer for live plot of waveform
        self.Proceed = True
        while self.Proceed:
            try:
                # Compute FFT data
                data = self.AutoCorrSpecAudio()
                # Update data on graphics and plot
                line.set_ydata(data)
                fig.canvas.draw()
                fig.canvas.flush_events()
                plt.pause(0.015)
            except KeyboardInterrupt:
                self.CloseMicrophone()
                self.Proceed = False
            except:
                raise Exception('Finised Demo')

    # Function for demo Main Frequency
    def DemoLiveMainFreq(self):
        '''
        Function For demonstrating computation
        of fundamental frequency
        '''
        if self.Proceed:
            try:
                freqs = self.MainFreqsAudio()
                self.message.configure(text='Main freq: '+str(freqs[0]))
                self.message.after(1000,self.DemoLiveMainFreq)
                self.window.mainloop()
            except KeyboardInterrupt:
                self.CloseMicrophone()
                self.Proceed = False
            except:
                raise Exception('Finished Demo')





if __name__ == '__main__':

    DemoRecorder = DataProcessor()
    DemoRecorder.CaptureNoise()
    print('Finised Recording Noise...')
    for i in range(5):
        print(1+i)
        time.sleep(1)
    #DemoRecorder.DemoLiveSpectrum()
    #print('Main Frequencies of signal: ',DemoRecorder.MainFreqsAudio())
    #DemoRecorder.CloseMicrophone()
    DemoRecorder.DemoLiveMainFreq()
