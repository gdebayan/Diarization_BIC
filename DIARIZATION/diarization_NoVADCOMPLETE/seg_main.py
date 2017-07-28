import random
import sys
import argparse
import os
import numpy as np
sys.path.insert(0,'./..')

import math
import soundfile as sf
from python_speech_features import mfcc
from numpy.linalg import inv




from peakdetect import peakdet
from readcsv import getcsvfeat
from seg1 import segment
from clus1 import clusterDIAR

sys.path.insert(0,'./..')

#Install PythonSPeechFeatures : https://github.com/jameslyons/python_speech_features
parser = argparse.ArgumentParser(description='I/p arguments for Segmentation')

parser.add_argument('-wav', '--wavfile',help='Directory of the wav file', default='wavnotprovided',required='True')
#The Location of the wav file .  Eg. : /home/deb/RT06/CMU_20050914-0900_D02_NONE.wav
parser.add_argument('-feat', '--features',help='Feature Vectors of the wav file',default='NoneProvided')
#The location of the CSV File with Feature Vectors.  Eg, : /home/deb/RT06/feat.csv
parser.add_argument('-amp', '--amp',help='Amplitude Threshold for Peak Detection',default='1')
#See documentation in peakdetect.py for more information
parser.add_argument('-dist', '--dist',
                        help='Distance Threshold for Peak Detection',default='4.2')
#See documentation in peakdetect.py for more information
parser.add_argument('-numfrwin', '--numfrwindow',help='length of window during segmentation(100 default)',default='100')
#numfrwin--> Segmentation Window Size. eg. numfrwin=100;nsh=0.010 ;Segmentation Window= 100*0.010=1s
parser.add_argument('-res', '--resolution',help='The Shift of window in secs (eg: 0.010). PLEASE MENTION Window SHift', default='1')
#res-->frame overlap while calculating MFCC features. eg.: 0.010 .MUST Mention if providing features
parser.add_argument('-tag', '--tag',help='Name of the o/p file', default='DIAR_TEST')
#The output file will be named: 'tag'+'_'+'numspk'+'_'+'pflin'+'_'+'pfo'+'_'+'.txt'
#OUTPUT TEXT FILE WILL BE PRESENT in : ./segmentation_op
results = parser.parse_args()
wav_file=results.wavfile
feat_file=results.features
amp=results.amp
dist=results.dist
numfrwin=results.numfrwindow
nsh=results.resolution
tag=results.tag
ts,fs,feat=segment(wav_file,feat_file,float(amp),float(dist),int(numfrwin),float(nsh))


str12='./segmentation_op/'+tag+'_'+str(amp)+'_'+str(dist)+'_'+'.txt'

text_file = open(str12, "w")
for i in range(0,len(ts)):
    text_file.write(str(ts[i])+"\n")

text_file.close()
    
     

