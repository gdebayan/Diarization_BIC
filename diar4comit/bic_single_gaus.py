import random
import sys
import os
import numpy as np
import wave
import scipy.io.wavfile as wavfile
import math
import soundfile as sf
#from python_speech_features import mfcc
from numpy.linalg import inv
from scipy.stats import norm
from matplotlib import pyplot
from sklearn import mixture
from peakdetect import peakdet


def bicdist_single(x,y,pf):
            
   
    covx=[]
    covy=[]
    covz=[]
    meanx=[]
    meany=[]
    meanz=[]
    
    
    z=np.concatenate((x,y),axis=1)
    meanx=np.mean(x,1)
    meany=np.mean(y,1)
    meanz=np.mean(z,1)

    covx=np.var(x,1)
    covx=np.diag(covx)

    covy=np.var(y,1)
    covy=np.diag(covy)

    covz=np.var(z,1)
    covz=np.diag(covz)

    det1=np.linalg.det(covx)
    det1=math.log(det1)
    det2=np.linalg.det(covy)
    det2=math.log(det2)
    det3=np.linalg.det(covz)
    det3=math.log(det3)
    d,n1=x.shape
    d,n2=y.shape
    d,n3=z.shape
    
    p=0.5*(d+0.5*d*(d+1))*(math.log(n3))
    bic=n3*det3-n1*det1-n2*det2-p*pf

    return bic    



    

    
    

    
