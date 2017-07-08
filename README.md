# README #

#directory structure
#INSTALL MFCC EXTRACTION LIBRARY : https://github.com/jameslyons/python_speech_features
#Uses 13-D MFCC Features as Features if No features are provided
HEAD
    --diarization
    
	--DIAR_MAIN.py
		#RUN THIS FILE TO PERFORM DIARIZATION
		#First Argument : Input Wav FIle Directory(wav file) [REQUIRED]
			-wav filename
		#Second Argument: Wav FIle FEATURE Directory(csv file) : i/p SHape:( Sample X Dimension). eg Mfcc=(Samples, 13)
			-feat filename	
		#Third Argument : Penalty Factor, usually between (2-12)
			-pfo value
		#Fourth Argument: Penalty Factor for Linear CLustering, usually set to 3.5;(3 to 4 usually)
			-pflin value
		#Fifth Argument : NAME TAG , I.E the desired 'file name' attribute in the o/p RTTM file
			-tag value	
		#Sixth argument:numfrwin, I.E. the window size during segmentation. 100=1s; 250=2.5s and so on.Keep at 100 usually.
			-numfrwin value	
		#Seventh argument:resolution, i.e the window shift in seconds , eg. -res 0.010 = (10mS shift)[REQUIRED if FEATURES PROVIDED]
			-res value
	
		#returns 'dat' with timestamps and cluster name
		#also creates a file with filename "'tag'+'pfo'+'.txt'" which is RTTM form of output; in the folder of running
	--seg_main.py
		#To check segmentation performance
		#First Argument: Input Wav FIle  Directory(wav file)[REQUIRED]
			-wav filename
		#Second Argument: Wav FIle FEATURE Directory(csv file) : i/p SHape:( Samples X Dimensions). eg Mfcc=(Samples, 13)
			-feat filename
		#Third Argument : AMplitude threhold; usually set to : 1
			-amp value
		#Fourth Argument: dist_1 threhold; usually set to 4.2
			-dist value		
		#Fifth argument:numfrwin, I.E. the window size during segmentation. 100=1s; 250=2.5s and so on.Keep at 100 usually
			-numfrwin value	
		#Sixth argument:resolution, i.e the window shift in seconds , eg. -res 0.010 = (10mS shift)[REQUIRED if FEATURES PROVIDED]
			-res value
	

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


		
 
	

