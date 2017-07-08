import random
import sys
import argparse
import os
import numpy as np
import wave
import scipy.io.wavfile as wavfile
import math
import soundfile as sf
from python_speech_features import mfcc
from numpy.linalg import inv
from scipy.stats import norm

from matplotlib import pyplot
from sklearn import mixture
from peakdetect import peakdet
from readcsv import getcsvfeat
from seg1 import segment
from clus1 import clusterDIAR

#First Argument : Input Wav FIle Directory(wav file)
#Second Argument: Wav FIle FEATURE Directory(csv file) : i/p SHape:( Dimension X Samples). eg Mfcc=(13, Samples)
#Third Argument : AMplitude threhold; usually set to : 1
#Fourth Argument: dist_1 threhold; usually set to 4.2

#Fifth argument:numfrwin, I.E. the window size during segmentation. 100=1s; 250=2.5s and so on.Keep at 100 usually.

#returns timeStamps,FrameStamps and the features(which is inputted by user;usedto pass onto cluster function)




#x1=sys.argv

#segment(wav_file,feat_file,amplitude,dist_1,numfrwin):


parser = argparse.ArgumentParser(description='I/p arguments for Segmentation')

parser.add_argument('-wav', '--wavfile',help='Directory of the wav file', default='wavnotprovided',required='True')
parser.add_argument('-feat', '--features',help='Feature Vectors of the wav file',default='NoneProvided')

parser.add_argument('-amp', '--amp',help='Amplitude Threshold for Peak Detection',default='1')

parser.add_argument('-dist', '--dist',
                        help='Distance Threshold for Peak Detection',default='4.2')
parser.add_argument('-numfrwin', '--numfrwindow',help='length of window during segmentation(100 default)',default='100')
parser.add_argument('-res', '--resolution',help='The Shift of window in secs (eg: 0.010). PLEASE MENTION Window SHift', default='1')
results = parser.parse_args()
wav_file=results.wavfile
feat_file=results.features
amp=results.amp
dist=results.dist
numfrwin=results.numfrwindow
nsh=results.resolution
ts,fs,feat=segment(wav_file,feat_file,float(amp),float(dist),int(numfrwin),float(nsh))
