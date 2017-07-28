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
from SpecchSEgs import getSpeechSEgments
from read import readVADFile
from clus_vad_spk import clus_vad1_spk


def diar_vad(wav_file,feat_file,pfo,pflin,tag,numfrwin,nsh,MDT,vadtxt,spkrs,filetype,verbose,feattype,amplitude,dist_1):


    #Making a webrtcvad Object. For more information , Visit: https://github.com/wiseman/py-webrtcvad
    vad = webrtcvad.Vad()
    vad.set_mode(0) #Setting Mode 0 of 'Aggresiveness'. Visit: https://github.com/wiseman/py-webrtcvad

    x, fs = sf.read(wav_file)
    #Reading The wav File. x=array of samples of the wav file(decimal). fs= sampling frequency


    #Feature Extraction




    if(feattype=='csv'):
        
        if(feat_file=='NoneProvided'):

            #If no external Features Provided by the User, System will extract the feature using python_speech_features Library.
            #More information on the Library : https://github.com/jameslyons/python_speech_features
            #x=wav file(array of decimals)
            #fs=sampling Frequency
            #0.03=Window Size in seconds ; AKA 30mS
            #0.01=Window Shift in seconds ; AKA 10ms
            #13= Dimension of MFCC Feature
            
            feat = mfcc(x,fs,0.03,0.010,13)
            feat= feat.transpose()#feat-->FEATURE VARIABLE. Shape=(dimension, samples)
            
            nsh=0.010 #nsh Variable--> Indiactes window shift interval
            print('using Inbuilt MFFCs as features')
        else:
            feat=getcsvfeat(feat_file) #Gets the features from the CSV File path which is provided
            #feat-->FEATURE VARIABLE. Shape=(dimension, samples)                            

            #When CSV File is provided, but the Window SHift AKA nsh is not provided (nsh==1 by default(see DIAR_MAIN.py)), throw an ERROR
            
            if(nsh==1):
                 print('ERROR, please enter -res (Window Shift) as Features are provided')
                 sys.exit()
            print('Using provided Features')
    
    elif(feattype=='numpy'):
        feat=feat_file
    else:
        print('ERROR, please ENTER Feature options correctly . (feattype)-->indicate numpy or csv')
        sys.exit()
        
        
    
        

    #get the Frame By Frame VAD Output(For each overlapping frame, do VAD and get '1==speech' or '0==no Speech' For each overlapping frame

    if(vadtxt=='1'):
        vad_flag,feat_1,numfram=vadfn(x,nsh,fs,feat)
        print('Performing VAD')
    #vadtxt-->Filename containing VAD Information.If no File Name provided, vadtxt=1 by default. If no file given, perform VAD.
    #feat---> feature file  (Dim,sample)
    #vadfn --> performs VAD using the webrtcvad Library
    #vad_flag--> Frame by Frame VAD info for each overlapping frame.Eg. vad_flag= array[1 0 0 0 1 1 1 0 1 0 1 1 1 0 0.......]
    #numfram-->Number of samples(feature samples) taken into account. numfram= min(number of VAD samples, Number of Feature Samples). Done to avoid Mismatch
    #feat_1-->Returns features with 'numfram' samples . len(feat_1)=numfram
                                        
                                                        
        
    else:
        vad_flag,feat_1,numfram=readVADFile(vadtxt,feat)
    #vadtxt-->Filename containing VAD Information.
    #vad_flag--> Frame by Frame VAD info for each overlapping frame.Eg. vad_flag= array[1 0 0 0 1 1 1 0 1 0 1 1 1 0 0.......]
    #numfram-->Number of samples(feature samples) taken into account. numfram= min(number of VAD samples, Number of Feature Samples). Done to avoid Mismatch
    #feat_1-->Returns features with 'numfram' samples .len(feat_1)=numfram
    print('Number of VAD Samples : '+str(len(vad_flag)))
    print('Number of Extracted Feature Samples : '+str(len(feat[1,:])))
    print('Number of Samples Considered : '+str(numfram))                                    

    speech_seg,speech_seg_start,speech_seg_end=getSpeechSEgments(vad_flag,MDT,feat_1,numfram)
    #getSpeechSEgments--> Analyses the VAD information and gets only the SPEECH Segments.
    #MDT-->Minimum Duration Time. Used for smoothing out the VAD output. if Silence Time<MDT----> Treat as Voice

    #speech_seg--> Returns Speech Segment windows.
        #Each Segment --> Features of the 'Voiced Part'.
        #eg. ---> speech_seg[0].shape=(13,4562) ; speech_seg[1].shape=(13,2341). speech_seg[i]-->returns 'ith' Speech Segment
    #speech_seg_start-->Start Time of Each Speech Segment
    #speech_seg_end-->End Time of Each Speech Segment


    clus_final=[]#Will contain the various speech segments AFTER Segmentation+Linear Clustering
    frms_start=[]#Start Frame of each speech segment after Segmentation+Linear Clustering
    frms_end=[]#End Frame of each speech segment after Segmentation+Linear Clustering

    #Performing Segmentation + Linear Clustering in Each of the Speech Segments
    for u in range(0,len(speech_seg)):
        
        x,y=speech_seg[u].shape
        #y--->Number of Samples in 'speech_seg[u]'
        
        if(y<(numfrwin+30)):#If Number of samples<numfrwin+30, DONT do segmentation+Linear CLustering. Add the entire speech segment. eg., if numfram=100,and nsh=0.010; 130*0.010=1.3s. If segment size less than 1.3s, add entire segment as it is
            
            clus_final.append(speech_seg[u])
            frms_start.append(speech_seg_start[u])
            frms_end.append(speech_seg_end[u])
        else:
            time_stamp,frame_stamp,ts_lin,fs_lin,clus,cluslin=segmentvad( speech_seg[u],amplitude,dist_1,numfrwin,nsh,pflin,fs)
            #segmentvad-->Does Segmeatation followed by linear clustering on the speech segments.

            #Outputs
            #time_stamp-->Time Stamp of change points followed by ONLY Segmentation
            #frame_stamp-->Frame Stamp of change points followed by ONLY Seg,Segmentation
            #ts_lin-->Time Stamp of change points followed by Segmentation AND Linear Clustering
            #fs_lin-->Frame Stamp of change points followed by Segmentation AND Linear Clustering
            #clus-->Speech Clusters followed by ONLY Segmentation
            #cluslin-->Speech Clusters followed by Segmentation AND Linear Clustering

            #Inputs
            #speech_seg[i]--->ith speech segment
            #amplitude-->Amplitude Threshold for Peak Detection ( See documentation of peakdetect.py for more information)
            #dist_1-->Distance Threshold for Peak Detection ( See documentation of peakdetect.py for more information)
            #numfrwin--> Segmentation Window Size. eg. numfrwin=100;nsh=0.010 ;Segmentation Window= 100*0.010=1s
            #nsh--> frame shift (0.010 default)
            #pflin--> Penalty Factor For Linear CLustering.(in BIC formula)
            #fs-->sampling frequency
            
            
            
            for t in range(0,len(cluslin)):
                clus_final.append(cluslin[t])

            #calculating Frame Start and Frame End for each 'segmented+Linear clustered' speech segment
            if(len(cluslin)==1):
                frms_start.append(speech_seg_start[u])
                frms_end.append(speech_seg_end[u])
                
            else:
                
            
                nst=0
                nen=fs_lin[0]
                frms_start.append(nst+speech_seg_start[u])
                frms_end.append(nen+speech_seg_start[u])
                

                if(len(fs_lin)==1):
                    nst=fs_lin[0]
                    nen=speech_seg_end[u]-speech_seg_start[u]
                    frms_start.append(nst+speech_seg_start[u])
                    frms_end.append(nen+speech_seg_start[u])
                else:
                    for y in range(1,len(fs_lin)):
                        nst=fs_lin[y-1]
                        nen=fs_lin[y]
                        frms_start.append(nst+speech_seg_start[u])
                        frms_end.append(nen+speech_seg_start[u])
                    nst=fs_lin[len(fs_lin)-1]
                    nen=speech_seg_end[u]-speech_seg_start[u]
                    frms_start.append(nst+speech_seg_start[u])
                    frms_end.append(nen+speech_seg_start[u])
                    
                
  

      #Performing Hierarchical Clustering on the Speech Signals
      #Two ways of terminating Clustering
    if(spkrs=='None'):
        clusters_spkrs=clus_vad1(clus_final,pfo,tag,verbose) #End Point of Clustering is based on BIC Value; If delta(BIC)>0; Stop Merging.
        #clusters_spkrs----> The Final CLusters of the speakers AFTER Hierarchical CLustering
    else:
        clusters_spkrs=clus_vad1_spk(clus_final,pfo,tag,int(float(spkrs)),verbose)#End Point of Clustering ---> Number of clusters= Number of speakers
        #clusters_spkrs----> The Final CLusters of the speakers AFTER Hierarchical CLustering
            
    for k in range(len(clusters_spkrs)):
        print(clusters_spkrs[k].shape)

        
    flag_pt=[]
    #Doing Speaker Matching; comparing each speech segment with the speaker clusters and assign speaker ID
    for i in range(0,len(clus_final)):
        kld=[]
        for j in range(0,len(clusters_spkrs)): #all the spkr clusters
       
            kld.append(bicdist_single(clus_final[i],clusters_spkrs[j],pfo))
   
        klin=min(kld)
        index=kld.index(klin)
        flag_pt.append(index)#flag_pt contains speaker ID
       


    #Write to File
    pf1=pfo
    str12='./results/'+tag+'_'+str(spkrs)+'_'+str(pfo)+'_'+str(pflin)+'.txt'
    text_file = open(str12, "w")

    data_time=np.zeros((len(clus_final),3))
    data_frame=np.zeros((len(clus_final),3))
    
    for i in range(0,len(clus_final)):
        
        start=frms_start[i]*nsh
        end=frms_end[i]*nsh
        dur=end-start
        
        spkid=flag_pt[i]
        data_time[i,0]=spkid
        data_time[i,1]=start
        data_time[i,2]=end-nsh

        data_frame[i,0]=spkid
        data_frame[i,1]=frms_start[i]
        data_frame[i,2]=frms_end[i]-1
        if(filetype=='rttm'):
            str1='SPEAKER '+ tag+' 1 '+str(start)+' '+str(dur)+' <NA> <NA> '+str(spkid)+' <NA> <NA>'
            text_file.write(str1+"\n")
##        else:
##            str1='SP'+str(spkid)+' '+str(frms_start[i])+' '+str(frms_end[i])
##            text_file.write(str1+"\n")

    
    #print(str(len(feat[1,:]))+'   feat_1 '+str(len(feat_1[1,:])))
    data_perfrm=[]
    if(data_frame[0,1]!=0):
        for j in range(0,data_frame[0,1]):
                      data_perfrm.append('SIL')
          
        


    datafrm_sil=[]
    datatim_sil=[]
    for i in range(0,len(data_frame[:,1])):

          size=data_frame[i,2]-data_frame[i,1]+1
          datafrm_sil.append(data_frame[i])
          datatim_sil.append(data_time[i])

          for k in range(0,int(size)):
              data_perfrm.append(data_frame[i,0])
              

          if(i<len(data_frame[:,1])-1):
              
              size2=data_frame[i+1,1]-data_frame[i,2]
              
              if(size2>1):
                  tmp=np.array(['SIL',data_frame[i,2]+1,data_frame[i+1,1]-1])
                  datafrm_sil.append(tmp)    
                  tmp2=np.array(['SIL',(data_frame[i,2]+1)*nsh,(data_frame[i+1,1]-1)*nsh])
                  datatim_sil.append(tmp2)
                  for j in range(0,int(size2)-1):
                      data_perfrm.append('SIL')
          
                  
              
              
        
    datafrm_sil=np.array(datafrm_sil)
    datatim_sil=np.array(datatim_sil)

    for n in range(0,len(datafrm_sil)):
        if(filetype!='rttm'):
            if(datafrm_sil[n,0]!='SIL'):
                str1='SP'+str(int(float(datafrm_sil[n,0])))+' '+str((datafrm_sil[n,1]))+' '+str((datafrm_sil[n,2]))
                text_file.write(str1+"\n")
            else:
                str1=str((datafrm_sil[n,0]))+' '+str((datafrm_sil[n,1]))+' '+str((datafrm_sil[n,2]))
                text_file.write(str1+"\n")
                
            
        
    text_file.close()
    return data_time,data_frame,data_perfrm,datafrm_sil,datatim_sil




