import random
import sys
import os
import numpy as np
import math
import soundfile as sf
#from python_speech_features import mfcc
from numpy.linalg import inv
from peakdetect import peakdet
from bic_single_gaus import bicdist_single


from readcsv import getcsvfeat




#Inputs
#speech_seg[i]--->ith speech segment
#1-->Amplitude Threshold for Peak Detection ( See documentation of peakdetect.py for more information)
#4.2-->Distance Threshold for Peak Detection ( See documentation of peakdetect.py for more information)
#numfrwin--> Segmentation Window Size. eg. numfrwin=100;nsh=0.010 ;Segmentation Window= 100*0.010=1s
#nsh--> frame shift (0.010 default)
#pflin--> Penalty Factor For Linear CLustering.(in BIC formula)
#fs-->sampling frequency

#Returns
#time_stamp-->Time Stamp of change points followed by ONLY Segmentation
#frame_stamp-->Frame Stamp of change points followed by ONLY Seg,Segmentation
#ts_lin-->Time Stamp of change points followed by Segmentation AND Linear Clustering
#fs_lin-->Frame Stamp of change points followed by Segmentation AND Linear Clustering
#clus-->Speech Clusters followed by ONLY Segmentation
#cluslin-->Speech Clusters followed by Segmentation AND Linear Clustering



def segmentvad(feat,amplitude,dist_1,numfrwin,nsh,pflin,fs):

    #Performing Segmentation

    win_ind_1=0
    win_ind_2=win_ind_1+numfrwin

    
    dim=len(feat[:,1])#to find the dimensions of the FEATURE
   
    dist=0
    count=0
    
    w1=np.zeros((dim,numfrwin))
    w2=np.zeros((dim,numfrwin))

    d=[]
    frame_no=[]

    num_frame=len(feat[1,:])
    Nw=math.floor(fs*0.03)
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
         cov1=np.diag(cov1)
         
         
         cov2=np.var(w2,1)
         cov2=np.diag(cov2)

         mean1.shape=(1,dim)
         mean2.shape=(1,dim)

         dist1=(np.trace(np.dot(inv(cov2),cov1)))
         dist2=np.dot((mean2-mean1),inv(cov2))
         mean1.shape=(dim,1)
         mean2.shape=(dim,1)
         dist2=np.dot(dist2,(mean2-mean1))
         k=dim
         dist3=(np.linalg.det(cov2)/np.linalg.det(cov1))
         dist3=np.log(dist3)
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
    b=[]
    max1,min2=peakdet(d1,dist_1) #max1 gives maxima peaks;min2 gives minima peaks
    temp=[]
    temp.append(feat)
    siz=max1.size
    if(siz==0): #If no change point found, return the entire feat file as it is
        return b,b,b,b,temp,temp
        


    
    time_stamp=[]

    for i in range(0,len(max1[:,0])):
       if(max1[i,1]<amplitude):
          max1[i,1]=0
       else:
          time_stamp.append(max1[i,0]*(Nsh)/fs)

    frame_stamp=max1[:,0]
    frame_stamp=frame_stamp.tolist()

    clus=[]
    i=0

    lasfram=len(feat[1,:])


   #segmenting the features depending on change points
    Nen=int(frame_stamp[0])
    Nst=0
    clus.append(feat[:,Nst:Nen])

 
    while(i<len(time_stamp)-1):
        
        
          Nst=int(frame_stamp[i])
          Nen=int(frame_stamp[i+1])
          clus.append(feat[:,Nst:Nen])
                            
          i=i+1

    Nst=int(frame_stamp[len(frame_stamp)-1])
    Nen=lasfram
    clus.append(feat[:,Nst:Nen])
    
     
    counlin=1
    cluslin=[]
    cov_lin=[]
    mfcc_lin=[]
    clus2=clus
    ts_lin=[]
    fs_lin=[]

    #performing linear clustering
    while(counlin<len(clus2)):

        if(counlin<=1):
            bicdist=bicdist_single(clus2[counlin],clus2[counlin-1],pflin)
            if(bicdist<0):
                clus3=np.concatenate((clus2[counlin],clus2[counlin-1]),axis=1)
                
                cluslin.append(clus3)
                
            else:
                cluslin.append(clus2[counlin-1])
                cluslin.append(clus2[counlin])
                ts_lin.append(time_stamp[counlin-1])
                fs_lin.append(frame_stamp[counlin-1])
        else:
             bicdist=bicdist_single(clus2[counlin],cluslin[len(cluslin)-1],pflin)
             if(bicdist<0):

                 
                clus3=np.concatenate((cluslin[len(cluslin)-1],clus2[counlin]),axis=1)
                cluslin[len(cluslin)-1]=clus3
             
                
                
             else:
                
                cluslin.append(clus2[counlin])
                ts_lin.append(time_stamp[counlin-1])
                fs_lin.append(frame_stamp[counlin-1])
        counlin=counlin+1    
            
    
    return time_stamp,frame_stamp,ts_lin,fs_lin,clus,cluslin
