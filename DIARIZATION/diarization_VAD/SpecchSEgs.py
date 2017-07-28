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
from funcVAD import vadfn


def getSpeechSEgments(vad_flag,MDT,feat_1,numfram):

    

    #MDT-->Minimum Duration Time. Used for smoothing out the VAD output. if (Silence Time<MDT)----> Treat as Voice
    vad_op=[]
    fram_stmp_st=[]
    fram_stmp_end=[]




    countzer=0

    fram_st=[]
    fram_end=[]
    frame_stamp=[]
    #fram_st.append(vad_flag[0])

    #finding the transition from Voice->Unvoice or Unvoice->Voice
    for i in range(1,len(vad_flag)):
        if(vad_flag[i]!=vad_flag[i-1]):
            frame_stamp.append(i)

    i=0
    clus=[]#clus-->divide features into ALTERNATE Voiced/Unvoiced segments
    vadflag=[]#--> VAD flag of each clus[] segment. It is '1 0 1 0 1 0' format (as alternate voiced/unvoiced)

    
    while(i<len(frame_stamp)-1):
            if(i==0):
              Nen=int(frame_stamp[i])
              Nst=0
              clus.append(feat_1[:,Nst:Nen])
              vadflag.append(vad_flag[Nst])
              Nst=int(frame_stamp[i])
              Nen=int(frame_stamp[i+1])
              clus.append(feat_1[:,Nst:Nen])
              vadflag.append(vad_flag[Nst])
                      
            else:
              Nst=int(frame_stamp[i])
              Nen=int(frame_stamp[i+1])
              clus.append(feat_1[:,Nst:Nen])
              vadflag.append(vad_flag[Nst])
            
            i=i+1

    Nst=frame_stamp[len(frame_stamp)-1]
    Nen=numfram
    clus.append(feat_1[:,Nst:Nen])
    vadflag.append(vad_flag[Nst])
            
                
    counlin=1
    cluslin=[]
    mfcc_lin=[]
    clus2=clus
    ts_lin=[]
    fram_stamp_final=[]
    Nstrt=[]
    Nend=[]

    for g in range(0,len(clus)):
        x,y=clus[g].shape #Smoothing out the VAD output
        if((vadflag[g]==0)and(y<MDT)):
            vadflag[g]=1


            

    counlin=1
    cluslin=[]
    vadfl_fin=[]
    #Join subsequent 'Voiced' segments
    while(counlin<len(clus2)):

        if(counlin==1):
             if((vadflag[counlin]==1)and(vadflag[counlin-1]==1)):

                 clus3=np.concatenate((clus2[counlin],clus2[counlin-1]),axis=1)
                    
                 cluslin.append(clus3)
                
             else:
                 cluslin.append(clus2[counlin-1])
                 cluslin.append(clus2[counlin])
                 fram_stamp_final.append(frame_stamp[counlin-1])
             
                 
            
        else:
        
             if((vadflag[counlin]==1)and(vadflag[counlin-1]==1)):
                 clus3=np.concatenate((cluslin[len(cluslin)-1],clus2[counlin]),axis=1)
                        
                 cluslin[len(cluslin)-1]=clus3
                 
             else:
                 cluslin.append(clus2[counlin])
                 fram_stamp_final.append(frame_stamp[counlin-1])

        counlin=counlin+1
            
        
    ts_final=[]
    
    if(vadflag[0]==1):
        start=1
    else:
        start=0
    for k in range(0,len(fram_stamp_final)):
        ts_final.append(fram_stamp_final[k]*0.01)
        if((k%2)==0):
            if(start==1):
                vadfl_fin.append(1)
            else:
                vadfl_fin.append(0)
        else:
            if(start==1):
                vadfl_fin.append(0)
            else:
                vadfl_fin.append(1)
            
    if(vadfl_fin[len(vadfl_fin)-1]==1):
        vadfl_fin.append(0)
    else:
        vadfl_fin.append(1)
        
                
        
    speech_seg=[]
    speech_seg_start=[]
    speech_seg_end=[]
    for n in range(0,len(cluslin)-1):
        if(n==0):
            Nst=0
            Nen=fram_stamp_final[n]

        else:
            Nst=fram_stamp_final[n-1]
            Nen=fram_stamp_final[n]


        if(vadfl_fin[n]==1):
            speech_seg.append(cluslin[n])
            speech_seg_start.append(Nst)
            speech_seg_end.append(Nen)




    return speech_seg,speech_seg_start,speech_seg_end
    #speech_seg--> Returns Speech Segment windows.
    #speech_seg_start-->Start Time of Each Speech Segment
    #speech_seg_end-->End Time of Each Speech Segment

    
