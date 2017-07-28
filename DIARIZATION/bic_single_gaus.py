import random
import sys
import os
import numpy as np
import math
import soundfile as sf
#from python_speech_features import mfcc
from numpy.linalg import inv
from matplotlib import pyplot
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
    #print(covx)
    #covx=np.diag(covx)
    det1=0#log(dex) performing
    for i in range(0,len(covx)):
        det1=det1+math.log(covx[i])

    det2=0      
    covy=np.var(y,1)
    for j in range(0,len(covy)):
        det2=det2+math.log(covy[j])
    
    #covy=np.diag(covy)

    covz=np.var(z,1)
    det3=0
    for k in range(0,len(covz)):
        det3=det3+math.log(covz[k])
    
    d,n1=x.shape
    d,n2=y.shape
    d,n3=z.shape
 
    p=0.5*(d+0.5*d*(d+1))*(math.log(n3))
    bic=n3*det3-n1*det1-n2*det2-p*pf

    return bic    



    

    
    

    
