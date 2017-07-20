import random
import sys
import os
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


def vadfn(x,nsh,fs,feat):
    #Making a webrtcvad Object. For more information , Visit: https://github.com/wiseman/py-webrtcvad
    #Setting Mode 0 of 'Aggresiveness'. Visit: https://github.com/wiseman/py-webrtcvad
    vad = webrtcvad.Vad()
    vad.set_mode(0)


    lenx=len(x)
    i=0
    count=0
    ind=0
    Nsh=fs*nsh #frame window shift in samples
    Nw=fs*0.030#frame window size in samples


    
    numfram1=int(math.ceil(((lenx-Nw)/(Nsh)))) #number of frames with Size Nw and overlapp Nsh
    numfram=min(numfram1,len(feat[1,:]))#taking min(len(features),numfram) to avoid mismatch. Usually will be same.
    
    
    frame=np.zeros((int(Nw),numfram)) #frame shape

    

    #dividing audio signal into overlapping frames, with parameters :(Nsh,Nw)    

    while(i<lenx-Nw):
        j=0
        while(j<Nw):
            frame[j,ind]=x[count]
            j=j+1
            count=count+1
        ind=ind+1

        i=i+Nsh
        count=i


   
    feat_1=feat[:,0:numfram]
    vad_flag=np.zeros((numfram,))
    #checking each frame if Voiced or Unvoiced.Using webrtcvad library
    for k in range(0,numfram):
        fr = np.int16(frame[:,k] * 32768).tobytes()
        #webrtcvad requires input to be in Byte format, not in 'decimal', hence converting
        a=(vad.is_speech(fr, fs))
        vad_flag[k]=int(a)
        

    return vad_flag,feat_1,numfram
    #vad_flag--> Frame by Frame VAD info for each overlapping frame.Eg. vad_flag= array[1 0 0 0 1 1 1 0 1 0 1 1 1 0 0.......]
    #numfram-->Number of samples(feature samples) taken into account. numfram= min(number of VAD samples, Number of Feature Samples). Done to avoid Mismatch
    #feat_1-->Returns features with 'numfram' samples . len(feat_1)=numfram
                                        
    
   
