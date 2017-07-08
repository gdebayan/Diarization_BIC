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
import peakutils
from peakutils.plot import plot as pplot
from matplotlib import pyplot
from sklearn import mixture
from peakdetect import peakdet
from readcsv import getcsvfeat
from seg1 import segment
from clus1 import clusterDIAR

#First Argument : Input Wav FIle Directory(wav file)
#Second Argument: Wav FIle FEATURE Directory(csv file) : i/p SHape:( Dimension X Samples). eg Mfcc=(13, Samples)
#Third Argument : Penalty Factor, usually between (2-12)
#Fourth Argument: Penalty Factor for Linear CLustering, usually set to 3.5
#Fifth Argument : NAME TAG , I.E the desired 'file name' attribute in the o/p RTTM file
#Sixth argument:numfrwin, I.E. the window size during segmentation. 100=1s; 250=2.5s and so on.Keep at 100 usually.

#returns 'dat' with timestamps and cluster name
#also creates a file with filename "'tag'+'pfo'+'.txt'" which is RTTM form of output; in the folder of running

#EG.:
##wav_file='/home/deb/pythonproj/ARCTic/wav/CMU_20050912-0900_hsum_NONE.wav'
##feat_file='/home/deb/DIAR_FINAL/CMU_90012.csv'
##pfo=4
##pflin=3.5
##tag='CMU_20050912-0900_hsum_NONE'
##numfrwin=100


parser = argparse.ArgumentParser(description='I/p arguments for Diarization')

parser.add_argument('-wav', '--wavfile',help='Directory of the wav file', default='wavnotprovided',required='True')
parser.add_argument('-feat', '--features',help='Feature Vectors of the wav file',default='NoneProvided')

parser.add_argument('-pfo', '--pfo',help='Penalty Factor for hierichal clustering',default='4')

parser.add_argument('-pflin', '--pflin',
                        help='Penalty Factor for linear clustering',default='3.5')
parser.add_argument('-tag', '--tag',help='Tag for output to RTTM File',default='DIAR_TEST')
parser.add_argument('-numfrwin', '--numfrwindow',help='length of window during segmentation(100 default)',default='100')
parser.add_argument('-res', '--resolution',help='The Shift of window in secs (eg: 0.010). PLEASE MENTION Window SHift', default='1')

results = parser.parse_args()
wav_file=results.wavfile
feat_file=results.features
pfo=results.pfo
pflin=results.pflin
tag=results.tag
numfrwin=results.numfrwindow



##if(feat_file=='NoneProvided'):
##    
##    parser.add_argument('-res', '--resolution',help='The Shift of window in secs (eg: 0.010)', default='0.010')
##else:
##    parser.add_argument('-res', '--resolution',help='The Shift of window in secs (eg: 0.010). FEATURES PROVIDED, PLEASE MENTION Window SHift', default='0.010',required='True')
##
nsh=results.resolution
dat=clusterDIAR(wav_file,feat_file,float(pfo),float(pflin),(tag),int(numfrwin),float(nsh))




