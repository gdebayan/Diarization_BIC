import random
import sys
import os
sys.path.insert(0,'./..')
import numpy as np
import math
import soundfile as sf
from python_speech_features import mfcc
from numpy.linalg import inv
from peakdetect import peakdet
from readcsv import getcsvfeat
import webrtcvad
from seg_vad import segmentvad
from clus_vad import clus_vad1
from bic_single_gaus import bicdist_single
import argparse
from diarization_vad import diar_vad

#Install PythonSPeechFeatures : https://github.com/jameslyons/python_speech_features
#Install webrtcvad : https://github.com/wiseman/py-webrtcvad

parser = argparse.ArgumentParser(description='I/p arguments for Diarization')

parser.add_argument('-wav', '--wavfile',help='Directory of the wav file', default='wavnotprovided',required='True')
#The Location of the wav file .  Eg. : /home/deb/RT06/CMU_20050914-0900_D02_NONE.wav


parser.add_argument('-feat', '--features',help='Feature Vectors of the wav file',default='NoneProvided')
#The location of the CSV File with Feature Vectors.  Eg, : /home/deb/RT06/feat.csv
#CSV FILE FORMAT:Each row is a sample , ie shape = (Nsample X Dimension)

parser.add_argument('-pfo', '--pfo',help='Penalty Factor for hierichal clustering',default='1')
#Penalty Factor for BIC in Hierarchical Clustering. Set to 1 for best performance. Vary numspkrs(Number of speakers) preferably as a stopping criteria.
#Rich gets richer problem arises when pfo is increased
#By default stopping criteria is with BIC, if numspkrs not specified

parser.add_argument('-pflin', '--pflin',help='Penalty Factor for linear clustering',default='2.1')
#Penalty Factor for BIC in Linear Clustering. Usual Values : 2.1/2.6/3.1 ; Usual Range=(1-4); THIS ESTIMATE IS FOR 13-d MFCCS. For different features,vary and set appropiate threshold(START WITH pflin=1!)

parser.add_argument('-tag', '--tag',help='Tag for output of the text File',default='DIAR_TEST')
#The output file will be named: 'tag'+'_'+'numspk'+'_'+'pflin'+'_'+'pfo'+'_'+'.txt'
#OUTPUT TEXT FILE WILL BE PRESENT in : ./results

parser.add_argument('-numfrwin', '--numfrwindow',help='length of window during segmentation(100 default)',default='100')
#numfrwin--> Segmentation Window Size. eg. numfrwin=100;nsh=0.010 ;Segmentation Window= 100*0.010=1s

parser.add_argument('-res', '--resolution',help='The Shift of window in secs (eg: 0.010). PLEASE MENTION Window SHift', default='1')
#res-->frame overlap while calculating MFCC features. eg.: 0.010 .MUST Mention if providing features
parser.add_argument('-mdt', '--mdt',help='Minimum Duration Time of silence in VAD', default='30')
#Minimum Duration time. : Used for smoothing out the VAD output. if Silence Time<MDT----> Treat as Voice
#EG. MDT=30; Nshift=0.01 ,Minimum duration time=30*0.01=0.3secs
parser.add_argument('-vadtxt', '--vadtxt',help='Text File Containing Frame by Frame VAD O.P', default='1')

parser.add_argument('-feattype','--feattype',help='csv/numpy',default='csv')
#If want to pass Numpy Matrix (Perhaps calling function from another script) , pass 'numpy' as argument
#eg.: -feattype numpy .
#It is 'csv' by default, in which case Feature Extraction is based on the '-feat' argument


#Location of the text file with VAD Output. Text file should be of format'[frame no,VAD Output]
#eg.
#61285 1.0
#61286 1.0
#61287 1.0
#61288 1.0
#61289 0.0
#61290 0.0
#61291 1.0
#61292 1.0

parser.add_argument('-spkrs','--spkrs',help='Number of Speakers to get clustered to',default='None')
#Number of speakers in the wav file. Wil  get clustered to these many clusters
parser.add_argument('-filetype','--filetype',help='type of output file" rttm/standard. Type -filetype rttm for RTTM format, or else standard',default='rttm')
#if rttm format specified, O/P : SPEAKER <tag> 1 <Start Time> <Duration Time> <NA> <NA> <SpkID> <NA> <NA>
#default: <SPID> <START FRAME> <END FRAME>
#To activate rttm output mode: -filetype rttm

parser.add_argument('-verbose','--verbose',help='1:Show Step by Step output ; 0:Show Only Required Output; 1 by default ',default='1')

parser.add_argument('-amplitude','--amplitude',help='Amplitude Threshold For Peak Detection during Segmentation',default='1')
#See documentation in peakdetect.py for more information
parser.add_argument('-dist_1','--dist_1',help='Distance Threshold for Peak Detection during Segmentation ',default='4.2')
#See documentation in peakdetect.py for more information

#OUTPUT TEXT FILE WILL BE PRESENT in : ./results
results = parser.parse_args()
wav_file=results.wavfile
feat_file=results.features
pfo=results.pfo
pflin=results.pflin
tag=results.tag
numfrwin=results.numfrwindow
MDT=results.mdt
vad=results.vadtxt
spkrs=results.spkrs
filetype=results.filetype
nsh=results.resolution
verbose=results.verbose
feattype=results.feattype
amplitude=results.amplitude
dist_1=results.dist_1

data_time,data_frame,data_perfrm,datafrm_sil,datatim_sil=diar_vad(wav_file,feat_file,float(pfo),float(pflin),(tag),int(numfrwin),float(nsh),int(MDT),vad,spkrs,filetype,int(verbose),feattype,float(amplitude),float(dist_1))




#data_time=[<spkid> , <SPEAKER start time> , <SPEAKER end time> ]; NO SIL INCLUDED
#data_frame=[<spkid> , <SPEAKER start frame> , <SPEAKER end frame>] ; NO SIL INCLUDED
#data_perfrm=[<SPKID>] #Per Frame SPKID; 'SIL' for silence
#datafrm_sil=[<spkid> , <SPEAKER start frame> , <SPEAKER end frame>] ; SIL INCLUDED
#datatim_sil=[<spkid> , <SPEAKER start time> , <SPEAKER end time> ]; SIL INCLUDED

#Instructions on using diar_vad() from another script
#wav_file:str:Location of the wav file

#feat_file:str: Location of the feat .csv file . Pass 'NoneProvided' to make the system extract features

#NOTE: If want to pass a Numpy Matrix , in the 'feattype' argument pass :str:'numpy'; 
#If Numpy Matrix Being Passed, Shape:(Dimension x Samples)

#feattype :str: 'csv'-->If passing CSV File to feat_file OR Making system EXTRACT FEATURE
#         :str: 'numpy'---->If passing a numpy Feature Matrix to feat_file. Shape=(dimension, samples)

#pfo:float:Penalty Factor for Hierarchical CLustering. Set to '1' Usually

#pflin:float: Penalty Factor for Linear Clustering. Set to '2.1' Usually

#tag:String

#numfrwin: int:100 usually

#nsh:float: 0.010 Window Shift during feature extraction

#MDT:int: 30 usually

#vad:str: location of VAD File.

#spkrs:str:'None'--->If Thresholding based on BIC
#     :str: eg.: '4'----> Give the number of speakers in String format (If thresholding based on number of speakers)

#filetype:str. 'rttm' for rttm format output textfile
#              'standard' for default format output textfile

#verbose:int:1-->SHOW ALL O/P. 0---->Show Minimum O/P 















