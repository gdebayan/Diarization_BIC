# README #

#directory structure

HEAD
    
    
    
    
    
    
    --diarization
    --DIAR_4comit
	--DIAR_MAIN.py
		#RUN THIS FILE TO PERFORM DIARIZATION
		#First Argument : Input Wav FIle Directory(wav file)
		#Second Argument: Wav FIle FEATURE Directory(csv file) : i/p SHape:( Dimension X Samples). eg Mfcc=(13, Samples)
		#Third Argument : Penalty Factor, usually between (2-12)
		#Fourth Argument: Penalty Factor for Linear CLustering, usually set to 3.5;(3 to 4 usually)
		#Fifth Argument : NAME TAG , I.E the desired 'file name' attribute in the o/p RTTM file
		#Sixth argument:numfrwin, I.E. the window size during segmentation. 100=1s; 250=2.5s and so on.Keep at 100 usually.

		#returns 'dat' with timestamps and cluster name
		#also creates a file with filename "'tag'+'pfo'+'.txt'" which is RTTM form of output; in the folder of running
	--seg_main.py
		#To check segmentation performance
		#Second Argument: Wav FIle FEATURE Directory(csv file) : i/p SHape:( Dimension X Samples). eg Mfcc=(13, Samples)
		#Third Argument : AMplitude threhold; usually set to : 1
		#Fourth Argument: dist_1 threhold; usually set to 4.2
		#Fifth argument:numfrwin, I.E. the window size during segmentation. 100=1s; 250=2.5s and so on.Keep at 100 usually.

		#returns timeStamps,FrameStamps and the features(which is inputted by user;used to pass onto cluster function )
	--seg1.py
		#performs segmentation
	--clus1.py
		#performs Linear and Agglomerative CLustering
	--peakdetect.py
		#finds peaks for segmentation purpose
	--bic2.py
		#BIC Function (this is used in linear clustering)
	--bic_single_gaus.py
		#BIC Function (used in Hierarchical clustering)
	--readcsv.py


		
 
	

