import random
import sys
import os
sys.path.insert(0,'./..')
import numpy as np
import wave
import scipy.io.wavfile as wavfile
import math
import soundfile as sf
from python_speech_features import mfcc
from numpy.linalg import inv
from scipy.stats import norm


from peakdetect import peakdet
from readcsv import getcsvfeat



#feat_file : CSV file with THE FEATURES; SHAPE=(nDimensions X Samples)
#wav_file: filename of the audio WAV FILE

#usually : amplitude=1, dist_1=4.2
#numfrwin=window size=100(1s);(each frame=10ms)
#returns TimeStamp,FrameStamp, and the Features(which is inputted by the User; passed to CLustering Function


def segment(wav_file,feat_file,amplitude,dist_1,numfrwin,nsh):

    x, fs = sf.read(wav_file)

    if(feat_file=='NoneProvided'):
        feat = mfcc(x,fs,0.025,0.010,13)
        feat= feat.transpose()
        nsh=0.010
        print('using Inbuilt MFFCs as features')
    else:
        feat=getcsvfeat(feat_file)
        if(nsh==1):
             print('ERROR, please enter -res (Window Shift) as Features are provided')
             sys.exit()
        print('using provided Features')

        

    print(nsh)
    win_ind_1=0
    win_ind_2=win_ind_1+numfrwin

    
    dim=len(feat[:,1])#to find the dimensions of the FEATURE
   
    dist=0
    count=0
    w1=np.zeros((dim,numfrwin))
    w2=np.zeros((dim,numfrwin))
    w3=np.zeros((dim,2*numfrwin))
    d=[]
    frame_no=[]
    num_frame=len(feat[1,:])
    Nw=math.floor(fs*0.025)
    Nsh=math.floor(fs*nsh)#0.010 by default

    frame_index_w1=0
    frame_index_w2=0+numfrwin*Nsh

    

    
    while(win_ind_2+numfrwin<num_frame):
       #finding the KL-DIVERGENCE between W1/W2
       
    
         w1[:,0:numfrwin]=feat[:,win_ind_1:win_ind_1+numfrwin]
         w2[:,0:numfrwin]=feat[:,win_ind_2:win_ind_2+numfrwin]
        
            
      
         cov1=[]
         cov2=[]
         mean1=[]
         mean2=[]
        
         
         mean1=np.mean(w1,1)
         mean2=np.mean(w2,1)
         cov1=np.var(w1,1)
         cov11=cov1

         det1=0
         for h in range(0,len(cov11)):
             det1=det1+math.log(cov11[h])
         
         cov1=np.diag(cov1)
         
         
         
         
         cov2=np.var(w2,1)
         cov22=cov2
         det2=0
         for g in range(0,len(cov22)):
             det2=det2+math.log(cov22[g])
             

         
         cov2=np.diag(cov2)

         mean1.shape=(1,dim)
         mean2.shape=(1,dim)

         dist1=(np.trace(np.dot(inv(cov2),cov1)))
         dist2=np.dot((mean2-mean1),inv(cov2))
         mean1.shape=(dim,1)
         mean2.shape=(dim,1)
         dist2=np.dot(dist2,(mean2-mean1))
         k=dim
         #dist3=(np.linalg.det(cov2)/np.linalg.det(cov1))
         dist3=det2-det1
         #dist3=np.log(dist3)
         dist=0.5*(dist1+dist2-k+dist3)
        
         d.append(dist)
        
         frame_no.append(frame_index_w2)
         win_ind_1=win_ind_1+1
         win_ind_2=win_ind_2+1
         frame_index_w2=win_ind_2*Nsh
         frame_index_w3=win_ind_1*Nsh
    
    

    d=np.array(d)
    d.shape= (len(d),)
    d=d.tolist()
    frame_no=np.array(frame_no)
    time_stamps=frame_no/fs
    frame_no.shape=(len(frame_no),)
    time_stamps.shape=(len(frame_no),)
    frame_no=frame_no.tolist()
    time_stamps=time_stamps.tolist()
 
    d1=np.zeros((numfrwin,))
    d1=d1.tolist()
    d1.extend(d)

    #Finding the Peaks to Identify the Change points
    max1,min2=peakdet(d1,dist_1)
    time_stamp=[]

    for i in range(0,len(max1[:,0])):
       if(max1[i,1]<amplitude):
          max1[i,1]=0
       else:
          time_stamp.append(max1[i,0]*(Nsh)/fs)

    frame_stamp=max1[:,0]
    frame_stamp=frame_stamp.tolist()
    return time_stamp,frame_stamp,feat
