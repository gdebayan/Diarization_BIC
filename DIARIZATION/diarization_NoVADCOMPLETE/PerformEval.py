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
from scipy.stats import norm
import peakutils
from peakdetect import peakdet
from readcsv import getcsvfeat
from seg1 import segment
from clus1 import clusterDIAR




parser = argparse.ArgumentParser(description='I/p arguments for Diarization')

parser.add_argument('-wav', '--wavfile',help='Directory of the wav file', default='wavnotprovided',required='True')
parser.add_argument('-feat', '--features',help='Feature Vectors of the wav file',default='NoneProvided')

parser.add_argument('-pfo', '--pfo',help='Penalty Factor for hierichal clustering',default='1')

parser.add_argument('-pflin', '--pflin',
                        help='Penalty Factor for linear clustering',default='2')
parser.add_argument('-tag', '--tag',help='Tag for output to RTTM File',default='DIAR_TEST')
parser.add_argument('-numfrwin', '--numfrwindow',help='length of window during segmentation(100 default)',default='100')
parser.add_argument('-res', '--resolution',help='The Shift of window in secs (eg: 0.010). PLEASE MENTION Window SHift', default='1')
parser.add_argument('-spkrs','--spkrs',help='Number of Speakers to get clustered to',default='None')
#Number of speakers in the wav file. Wil  get clustered to these many clusters
parser.add_argument('-amplitude','--amplitude',help='Amplitude Threshold For Peak Detection during Segmentation',default='1')
#See documentation in peakdetect.py for more information
parser.add_argument('-dist_1','--dist_1',help='Distance Threshold for Peak Detection during Segmentation ',default='4.2')
#See documentation in peakdetect.py for more information
parser.add_argument('-groundtruth','--groundtruth',help='Location of ground truth file',default='0',required='True')

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
ref=results.groundtruth
verbose=results.verbose



##if(feat_file=='NoneProvided'):
##    
##    parser.add_argument('-res', '--resolution',help='The Shift of window in secs (eg: 0.010)', default='0.010')
##else:
##    parser.add_argument('-res', '--resolution',help='The Shift of window in secs (eg: 0.010). FEATURES PROVIDED, PLEASE MENTION Window SHift', default='0.010',required='True')
##
nsh=results.resolution


pflin1=[0,0.5,1,1.5,2,2.5,3]

if(spkrs=='None'):
    spkrs1=['2','3','4','5','6','7','8','9']
else:
    spkrs1=[]
    spkrs1.append(spkrs)

dat_der=[]
#ref='/home/deb/diarnewcheck/diarization_VAD/results/NIST_20051024-0930_hsum_NONE.part1.rttm'

#data_time,data_frame,data_perfrm,datafrm_sil,datatim_sil=diar_vad(wav_file,feat_file,float(pfo),float(pflin),(tag),int(numfrwin),float(nsh),int(MDT),vad,spkrs,filetype,int(verbose),feattype)


for i in range(0,len(pflin1)):
    for j in range(0,len(spkrs1)):
        pflin=pflin1[i]
        spkrs=spkrs1[j]
        dat=clusterDIAR(wav_file,feat_file,float(pfo),float(pflin),(tag),int(numfrwin),float(nsh),spkrs,float(amplitude),float(dist_1),int(verbose))

        actual='./results/'+tag+'_'+str(spkrs)+'_'+str(float(pfo))+'_'+str(float(pflin))+'.txt'+" | grep \"OVERALL SPEAKER DIARIZATION ERROR\" | cut -d' ' -f7 > tmp_file"
        str1="perl md-eval-v21.pl -c 0.25 -r "+ref+" -s "+actual
        os.system(str1)

        f = open('tmp_file', "r")
        words = f.read().split()

        num=0
        for w in words:
              num=((float((w)))) #each index
             
        f.close()

        tmp=np.array([float(num),float(pflin),float(spkrs)])
        dat_der.append(tmp)    

dat_der=np.array(dat_der)

#a = numpy.asarray([ [1,2,3], [4,5,6], [7,8,9] ])
str2='./eval_res/'+tag+'.csv'
np.savetxt(str2, dat_der, delimiter=",")


