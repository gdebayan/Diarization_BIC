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


def bicdista(x,y,pf):
            
   
    covx=[]
    covy=[]
    covz=[]
    meanx=[]
    meany=[]
    meanz=[]
    
    gmm1=mixture.GaussianMixture(n_components=1,covariance_type='full').fit(x.transpose())
    gmm2=mixture.GaussianMixture(n_components=1,covariance_type='full').fit(y.transpose())
    
    z=np.concatenate((x,y),axis=1)
    gmm3=mixture.GaussianMixture(n_components=1,covariance_type='full').fit(z.transpose())

    meanx=gmm1.means_
    covx=gmm1.covariances_
 
    
    meany=gmm2.means_
    covy=gmm2.covariances_
   
    meanz=gmm3.means_
    covz=gmm3.covariances_
    
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
    bic=n3*det3-n1*det1-n2*det2-pf*p

    return bic    


