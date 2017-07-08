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
from bic2 import bicdista
from bic_single_gaus import bicdist_single
from seg1 import segment




def clusterDIAR(wav_file,feat_file,pfo,pflin,tag,numfrwin,nsh):

    amplitude=1
    dist_1=4.2
    time_stamp,frame_stamp,feat = segment(wav_file,feat_file,amplitude,dist_1,numfrwin,nsh)
    biclin=[]
    i=0
    Nst=0
    Nen=0
    clus=[]
    cov_mat=[]
   


    while(i<len(time_stamp)-1):
        if(i==0):
          Nen=int(frame_stamp[i])
          Nst=0
          clus.append(feat[:,Nst:Nen])
          Nst=int(frame_stamp[i])
          Nen=int(frame_stamp[i+1])
          clus.append(feat[:,Nst:Nen])
                  
        else:
          Nst=int(frame_stamp[i])
          Nen=int(frame_stamp[i+1])
          clus.append(feat[:,Nst:Nen])
        
        
        i=i+1





    #Linear CLustering Done Here
    counlin=1
    cluslin=[]
    cov_lin=[]
    mfcc_lin=[]
    clus2=clus
    cov_mat2=cov_mat
    ts_lin=[]

    while(counlin<len(clus2)):

        if(counlin<=1):
            bicdist=bicdista(clus2[counlin],clus2[counlin-1],pflin)
            #bicdist=bicdist_single(clus2[counlin],clus2[counlin-1],pflin)
            biclin.append(bicdist)
            if(bicdist<0):
                clus3=np.concatenate((clus2[counlin],clus2[counlin-1]),axis=1)
                
                cluslin.append(clus3)
                
            else:
                cluslin.append(clus2[counlin-1])
                cluslin.append(clus2[counlin])
                ts_lin.append(time_stamp[counlin-1])
        else:
             bicdist=bicdista(clus2[counlin],cluslin[len(cluslin)-1],pflin)
             #bicdist=bicdist_single(clus2[counlin],cluslin[len(cluslin)-1],pflin)
             biclin.append(bicdist)
             if(bicdist<0):

                 
                clus3=np.concatenate((cluslin[len(cluslin)-1],clus2[counlin]),axis=1)
                cluslin[len(cluslin)-1]=clus3
             
                
                
             else:
                x,y=clus2[counlin].shape
                if(y>10):
                    
                    cluslin.append(clus2[counlin])
                    ts_lin.append(time_stamp[counlin-1])
                else:
                     
                    clus3=np.concatenate((cluslin[len(cluslin)-1],clus2[counlin]),axis=1)
                    cluslin[len(cluslin)-1]=clus3
                    
                                    
        counlin=counlin+1     



    count=0
    i_ind=[]
    j_ind=[]
    dist=[]
    covmat_new=[]
    bic=-0.01
    clus1=cluslin
  
   
   
    print('original cluster:')
    print(len(clus))
    print('after linear clustering')
    print(len(cluslin))
    count1=0
    bicact=[]

    tslin=[]
    dist_dict={}


    while((len(clus1)>1)&(bic<0)):
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
        print(bic)
        bicact.append(bic)
        c1=dist.index(bic)
        el1=i_ind[c1]
        el2=j_ind[c1]
        print(el1)
        print(el2)
        clusnew=[]
        gmmodelnew=[]
      
        dictnew={}
        
        clus3=np.concatenate((clus1[el1],clus1[el2]),axis=1)
      
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


    print(len(clus1))
    flag_pt=[] 
    for i in range(0,len(cluslin)):
        kld=[]
        for j in range(0,len(clus1)): #all the clusters(small no)
           
            kld.append(bicdist_single(cluslin[i],clus1[j],pfo))
       
        klin=min(kld)
        index=kld.index(klin)
        flag_pt.append(index)
       

    ts=[]

    ind=[]

    for k in range(0,len(flag_pt)-1):
        if(flag_pt[k]!=flag_pt[k+1]):
            
            ts.append(ts_lin[k])
            ind.append(flag_pt[k])

    dat=np.zeros((len(ts),2))
    dat1=np.zeros((len(flag_pt),2))
    dat[:,0]=ts
    dat[:,1]=ind
   
    pf1=pfo
    str12=tag+str(pf1)+'.txt'
    text_file = open(str12, "w")
    for i in range(0,len(ts)):
        
        if(i==0):
            start=0
            end=ts[i]
            dur=end-start
        else:
            start=ts[i-1]+0.01
            end=ts[i]
            dur=end-start
        spkid=ind[i]
        str1='SPEAKER '+ tag+' 1 '+str(start)+' '+str(dur)+' <NA> <NA> '+str(spkid)+' <NA> <NA>'
        text_file.write(str1+"\n")
        

    text_file.close()
    return dat


