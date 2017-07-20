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
from bic_single_gaus import bicdist_single

def clus_vad1_spk(cluslin,pfo,tag,spkrs,verbose):


    
    count=0
    i_ind=[]
    j_ind=[]
    dist=[]
    covmat_new=[]
    bic=-0.01
    clus1=cluslin
  
   
   
   
    print('After VAD+Segmentation+Linear Clustering')
    print(str(len(cluslin))+' Clusters ')
    count1=0
    bicact=[]

    tslin=[]
    dist_dict={}

    #Performing Agglomerative Clustering
    #Using Dictionaries to store Values of BIC Values calculated in the previous iteration, so that dont need to recompute same values.
    


    while((len(clus1)>spkrs)):
        i_ind=[]
        j_ind=[]
        dist=[]
        
        if(count1==0):
            clus1=cluslin

        else:
            clus1=clusnew
            dist_dict=dictnew


        for i in range(0,len(clus1)-1):
            for j in range(i+1,len(clus1)):
                
                indexa=str(i)+'_'+str(j)
                if indexa in dist_dict:
                    dist.append(dist_dict[indexa])
                else:
                   
                    jsdist=bicdist_single(clus1[i],clus1[j],pfo)
                    
                    dist_dict.update({indexa:jsdist})
                    dist.append(dist_dict[indexa])

                i_ind.append(i)
                j_ind.append(j)
                
            count=count+1     
        if(len(dist)==0):
            break

        bic=min(dist)
        if(verbose==1):
            print('BIC SCORE: '+str(bic))
        bicact.append(bic)
        c1=dist.index(bic)
        el1=i_ind[c1]
        el2=j_ind[c1]#Merge segments :el1 and el2
        #print(el1)
        #print(el2)
        if(verbose==1):
            print('ELEMENTS MERGED ARE :'+str(el1)+' and '+str(el2))
        clusnew=[]
        
      
        dictnew={}
        
        clus3=np.concatenate((clus1[el1],clus1[el2]),axis=1)
        if(verbose==1):
            print('Shape Of Merged Elements '+str(clus3.shape))
      
        for k in range(0,len(clus1)):
          if((k!=el1)&(k!=el2)):
              clusnew.append(clus1[k])
 
        clusnew.append(clus3)
    
        #now finding new distance dictionary
        flagm=0
        flagn=0
        for m in range(0,len(clus1)-1):
            for n in range(m+1,len(clus1)):
                indexa=str(m)+'_'+str(n)
                con=not ((m==el1)or(m==el2)or(n==el1)or(n==el2))
                if( con):
                   
                    if((m<el1)and(n<el1)):
                        str1=str(m)+'_'+str(n)
                        dictnew.update({str1:dist_dict[indexa]})
                    elif((m<el1)and(n>el1)and(n<el2)):
                        str1=str(m)+'_'+str(n-1)
                        dictnew.update({str1:dist_dict[indexa]})
                    elif((m<el1)and(n>el2)):
                        str1=str(m)+'_'+str(n-2)
                        dictnew.update({str1:dist_dict[indexa]})
                    elif((m>el1)and(n<el2)):
                        str1=str(m-1)+'_'+str(n-1)
                        dictnew.update({str1:dist_dict[indexa]})
                    elif((m>el1)and(n>el2)and(m<el2)):
                        str1=str(m-1)+'_'+str(n-2)
                        dictnew.update({str1:dist_dict[indexa]})
                    elif((m>el2)and(n>el2)):
                        str1=str(m-2)+'_'+str(n-2)
                        dictnew.update({str1:dist_dict[indexa]})
                    else:
                        print('error in indexing ')
                        print(str(el1)+' '+str(el2)+' m/n=> '+str(m)+' '+str(n))
                        print(con)
                
                   
        
                        


        count1=count1+1
        if(verbose==1):
            print('Number of Clusters Remaining '+str(len(clus1)))
        
    return clus1
