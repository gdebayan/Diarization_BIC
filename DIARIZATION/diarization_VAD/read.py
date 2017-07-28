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



def readVADFile(vadtxt,feat):
    #File should be in format : [frame number, VAD value(0/1)]
    print('Using Provided VAD File')
    f = open(vadtxt, "r")
    words = f.read().split()

    ind=[]
    vad_op=[]
    k=0
    for w in words:
        if(k%2==0):
            ind.append(int(float((w)))) #each index
        else:
            vad_op.append(int(float((w))))#VAD value
        
        k=k+1



    numfram=min(len(vad_op),len(feat[1,:]))
    #taking min(len(vad_op),len(feat[1,:])) to avoid mismatch. Usually will be same.
    
    feat_1=feat[:,0:numfram]
  
    
    return vad_op,feat_1,numfram
