# PyTunner

The objective of this repo is to illustrate the use of DFT in a simple tuning application. By computing the first peak in the harmonic series of a musical sound in real time, and using a customizable series of musical pitches, the applications allows pitch determination in a rudimentary GUI. It works reasonably well with a recorder and human voice. Nevertheless, it needs a more sophisticated algorithm for pitch detection in order to have universal validity. I implemented a calculation of *cepstrum*, but obtained no improvement.

## Requirements

* Python 3.x
* [PortAudio](http://www.portaudio.com)
* [PyAudio](https://people.csail.mit.edu/hubert/pyaudio/)
* [Pandas](https://pandas.pydata.org)
* Tkinter

## Instructions for use

Clone this repo in a local directory. Make sure that all files are located on the same folder. On a terminal window, execute

```
python GUIprogram.py
```

To produce a GUI that shows the main frequency of the sound, and its corresponding musical note. If you want to work with a non standard temperament, change the entries on ```MusicalPitches.txt```, separating columns using **TAB** character.

To see live FFT of signal, execute command

```
python TunnerTest.py
```

To stop execution, force ```KeyboardInterrupt``` on your system.
