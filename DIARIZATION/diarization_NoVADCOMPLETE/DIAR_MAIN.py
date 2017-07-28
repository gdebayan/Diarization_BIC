import random
import sys
import argparse
sys.path.insert(0,'./..')
import os
import numpy as np
import math
import soundfile as sf
from python_speech_features import mfcc
from numpy.linalg import inv
import peakutils
from peakdetect import peakdet
from readcsv import getcsvfeat
from seg1 import segment
from clus1 import clusterDIAR


#Install PythonSPeechFeatures : https://github.com/jameslyons/python_speech_features
#SEE seg_main.py FOR SEGMENTATION OUTPUT
#SEE PerformEval.py for getting DER by varying pflin and nspkrs

parser = argparse.ArgumentParser(description='I/p arguments for Diarization')

parser.add_argument('-wav', '--wavfile',help='Directory of the wav file', default='wavnotprovided',required='True')
#The Location of the wav file .  Eg. : /home/deb/RT06/CMU_20050914-0900_D02_NONE.wav
parser.add_argument('-feat', '--features',help='Feature Vectors of the wav file',default='NoneProvided')
#The location of the CSV File with Feature Vectors.  Eg, : /home/deb/RT06/feat.csv

parser.add_argument('-pfo', '--pfo',help='Penalty Factor for hierichal clustering',default='1')
#Penalty Factor for BIC in Hierarchical Clustering. Set to 1 for best performance. Vary numspkrs(Number of speakers) preferably as a stopping criteria.
#Rich gets richer problem arises when pfo is increased
#By default stopping criteria is with BIC, if numspkrs not specified
parser.add_argument('-pflin', '--pflin',
                        help='Penalty Factor for linear clustering',default='2')
#Penalty Factor for BIC in Linear Clustering. Usual Values : 2.1/2.6/3.1 ; Usual Range=(1-4); THIS ESTIMATE IS FOR 13-d MFCCS. For different features,vary and set appropiate threshold(START WITH pflin=1!)
parser.add_argument('-tag', '--tag',help='Tag for output to RTTM File',default='DIAR_TEST')
#The output file will be named: 'tag'+'_'+'numspk'+'_'+'pflin'+'_'+'pfo'+'_'+'.txt'
#OUTPUT TEXT FILE WILL BE PRESENT in : ./results
parser.add_argument('-numfrwin', '--numfrwindow',help='length of window during segmentation(100 default)',default='100')
#numfrwin--> Segmentation Window Size. eg. numfrwin=100;nsh=0.010 ;Segmentation Window= 100*0.010=1s
parser.add_argument('-res', '--resolution',help='The Shift of window in secs (eg: 0.010). PLEASE MENTION Window SHift', default='1')
#res-->frame overlap while calculating MFCC features. eg.: 0.010 .MUST Mention if providing features
parser.add_argument('-spkrs','--spkrs',help='Number of Speakers to get clustered to',default='None')
#Number of speakers in the wav file. Wil  get clustered to these many clusters
parser.add_argument('-amplitude','--amplitude',help='Amplitude Threshold For Peak Detection during Segmentation',default='1')
#See documentation in peakdetect.py for more information
parser.add_argument('-dist_1','--dist_1',help='Distance Threshold for Peak Detection during Segmentation ',default='4.2')
#See documentation in peakdetect.py for more information
parser.add_argument('-verbose','--verbose',help='1:Show Step by Step output ; 0:Show Only Required Output; 1 by default ',default='1')


results = parser.parse_args()
wav_file=results.wavfile
feat_file=results.features
pfo=results.pfo
pflin=results.pflin
tag=results.tag
numfrwin=results.numfrwindow
spkrs=results.spkrs
amplitude=results.amplitude
dist_1=results.dist_1
verbose=results.verbose

nsh=results.resolution
dat=clusterDIAR(wav_file,feat_file,float(pfo),float(pflin),(tag),int(numfrwin),float(nsh),spkrs,float(amplitude),float(dist_1),int(verbose))

#dat--> [SPKID,End time of SPK]
#EG [11.76,2]
#   [12.7,3]---> SPEAKER 2 : 0 TO 11.76s ; SPEAKER 3 :11.77 to 12.7 s 


