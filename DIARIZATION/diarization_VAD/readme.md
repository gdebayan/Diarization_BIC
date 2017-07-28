- Install Dependencies :
	
	-PythonSPeechFeatures : https://github.com/jameslyons/python_speech_features
	
	-webrtcvad : https://github.com/wiseman/py-webrtcvad
	
	-soundfile : https://github.com/bastibe/PySoundFile

- Versions of Library Used:
	
	-numpy==1.11.1
	
	-python-speech-features==0.5
	
	-webrtcvad==2.0.10
	
	-soundfile==0.9.0


-FOLDER 1: diarization_VAD

	-Features: 
	
		-Performes VAD, Segmentation and Hierarchical Clustering.
	
		-Output File format <rttm or standard> format
	
		-Text File will be present in ./results
	
		-Results from Perform_eval.py, which varies pflin/npskrs and give DER.present in ./eval_res
	



	
    - Arguments in DIARIZATION_MAIN.py and Perform_eval.py:
	
	-wav: The Location of the wav file
		
		- Eg. : -wav /home/deb/RT06/CMU_20050914-0900_D02_NONE.wav
	
	-feat: The location of the CSV File with Feature Vectors
		
		-Eg. : -feat /home/deb/RT06/feat.csv
			-CSV FILE FORMAT:Each row is a sample , ie shape = (Nsample X Dimension)
		
		-Default : 'NoneProvided'---> System Does Feature Extraction
		
		-(If calling diar_vad() from another script and want to pass numpy matrix: Make feattype variable as 'numpy')
			-Numpy Matrix Dimension:(Dimension X Nsample)
	
	-feattype : Type of argument for feat_file(feat) ,i.e. CSV file or numpy matrix
		
		-If want to pass Numpy Matrix (Perhaps calling function from another script) , pass 'numpy' as argument
		
		-eg.: -feattype numpy 
		
		'csv'-->If passing CSV File to feat_file OR Making system EXTRACT FEATURE (DEFAULT-->CSV)
		
		'numpy'---->If passing a numpy Feature Matrix to feat_file(feat). Shape=(Dimension, Nsamples)
	
	-pfo : Penalty Factor for BIC in Hierarchical Clustering. 
		
		- Set to 1 for best performance. Vary numspkrs(Number of speakers) preferably as a stopping criteria.
		
		- Rich gets richer problem arises when pfo is increased
		
		- By default stopping criteria is with BIC, if numspkrs not specified
	
	-pflin : Penalty Factor for BIC in Linear Clustering
		
		- Usual Values : 2.1/2.6/3.1 ; Usual Range=(1-4); THIS ESTIMATE IS FOR 13-d MFCCS. For different features,vary and set appropiate threshold
	
	-tag :The output file will be named: 'tag'+'_'+'numspk'+'_'+'pflin'+'_'+'pfo'+'_'+'.txt'
		
		-OUTPUT TEXT FILE WILL BE PRESENT in : ./results directory
	
	-numfrwin: Segmentation Window Size
		
		- eg. numfrwin=100;nsh=0.010 ;Segmentation Window= 100*0.010=1s
	
	-res : frame overlap while calculating MFCC features (nshift).
		
		- eg. 0.010 .****MUST Mention if providing features(from a CSV File)
	
	-mdt : Used for smoothing out the VAD output.
		
		-if Silence Time<MDT----> Treat as Voice
		
		-EG. MDT=30; Nshift=0.01 ,Minimum duration time=30*0.01=0.3secs
	
	-spkrs: Number of speakers in the wav file. Will  get clustered to these many clusters 		

	-filetype : type of output file rttm/standard.(for the text file which will be created) 
		-filetype rttm for RTTM format, or else standard by default
		
		default: <SPID> <START FRAME> <END FRAME>
		
		rttm: SPEAKER <tag> 1 <Start Time> <Duration Time> <NA> <NA> <SpkID> <NA> <NA>
	
	-verbose : 
		
		-1:Show Step by Step output
		
		-0:Show Only Required Output
		
		-1 by default
	-amplitude

		-Amplitude Threshold For Peak Detection during Segmentation

		-See documentation in peakdetect.py for more information

	-dist_1

		-Distance Threshold for Peak Detection during Segmentation
		
		-See documentation in peakdetect.py for more information
	-vadtxt	
		-Text File Containing Frame by Frame VAD O.P
	

	-groundtruth ( Present only in Perform_eval.py)

		-Compulsary Argument. Directory of the Groundtruth File
		
		


		
	-To see how to call diar_vad() from a script, see documentation at DIARIZATION_MAIN.py		

-Run DIARIZATION_MAIN.py , and specify the arguments. DIARIZATION_MAIN.py just makes the textfile in ./results folder
	
	-wav is a compulsary argument
	
	-res is a compulsary argument if directory of CSV file provided under -feat

-Run Perform_eval.py , and specify the arguments. Will vary pflin and spkrs and calculate DER.It will make a csv file of the format [DER ,pflin, SPKRS]. Will be present in ./eval_res

	-groundtruth ( Present only in Perform_eval.py)

		-Compulsary Argument. Directory of the Groundtruth File
	
	-wav is a compulsary argument
	
	-res is a compulsary argument if directory of CSV file provided under -feat

	
-FOLDER 2: diarization_NoVADCOMPLETE

	- Features
		
		-Performs Segmentation and Hierarchical Clustering

		-Output file will be in <rttm> format Only.

		-Text File will be in ./results

		-Results from Perform_eval.py, which varies pflin/npskrs and give DER.present in ./eval_res		

      - Arguments in DIAR_MAIN.py and PerformEval.py:

	-wav: The Location of the wav file
		
		- Eg. : -wav /home/deb/RT06/CMU_20050914-0900_D02_NONE.wav
	
	-feat: The location of the CSV File with Feature Vectors
		
		-Eg. : -feat /home/deb/RT06/feat.csv
			-CSV FILE FORMAT:Each row is a sample , ie shape = (Nsample X Dimension)
		
		-Default : 'NoneProvided'---> System Does Feature Extraction
		
		-(If calling diar_vad() from another script and want to pass numpy matrix: Make feattype variable as 'numpy')
			-Numpy Matrix Dimension:(Dimension X Nsample)

		-pfo : Penalty Factor for BIC in Hierarchical Clustering. 
		
		- Set to 1 for best performance. Vary numspkrs(Number of speakers) preferably as a stopping criteria.
		
		- Rich gets richer problem arises when pfo is increased
		
		- By default stopping criteria is with BIC, if numspkrs not specified
	
	-pflin : Penalty Factor for BIC in Linear Clustering
		
		- Usual Values : 2.1/2.6/3.1 ; Usual Range=(1-4); THIS ESTIMATE IS FOR 13-d MFCCS. For different features,vary and set appropiate threshold
	
	-tag :The output file will be named: 'tag'+'_'+'numspk'+'_'+'pflin'+'_'+'pfo'+'_'+'.txt'
		
		-OUTPUT TEXT FILE WILL BE PRESENT in : ./results directory
	
	-numfrwin: Segmentation Window Size
		
		- eg. numfrwin=100;nsh=0.010 ;Segmentation Window= 100*0.010=1s
	
	-res : frame overlap while calculating MFCC features (nshift).
		
		- eg. 0.010 .****MUST Mention if providing features(from a CSV File)

	-spkrs: Number of speakers in the wav file. Will  get clustered to these many clusters 		
	
	-verbose : 
		
		-1:Show Step by Step output
		
		-0:Show Only Required Output
		
		-1 by default
	-amplitude

		-Amplitude Threshold For Peak Detection during Segmentation

		-See documentation in peakdetect.py for more information

	-dist_1

		-Distance Threshold for Peak Detection during Segmentation
		
		-See documentation in peakdetect.py for more information

	
	-groundtruth ( Present only in PerformEval.py)

		-Compulsary Argument. Directory of the Groundtruth File

-Run DIAR_MAIN.py , and specify the arguments. DIAR_MAIN.py just makes the textfile in ./results folder
	
	-wav is a compulsary argument
	
	-res is a compulsary argument if directory of CSV file provided under -feat

-Run PerformEval.py , and specify the arguments. Will vary pflin and spkrs and calculate DER.It will make a csv file of the format [DER ,pflin, SPKRS]. Will be present in ./eval_res

	-groundtruth ( Present only in PerformEval.py)

		-Compulsary Argument. Directory of the Groundtruth File
	
	-wav is a compulsary argument
	
	-res is a compulsary argument if directory of CSV file provided under -feat

-Run seg_main.py and specify the given arguments. Segmentation o/p will be in ./segmentation_op


-FOLDER 3 : diarization_NoVad

	Features:
		
		-Performs Segmentation and Linear Clustering

		-Requires No wav file as input

		-feat_file input is a numpy matrix . shape :(Ndimensions X Nsamples

		-File made just so that cluster_DIAR can be called from any script,without having to give wav file as input

		-Functionality same as diarization_NoVADCOMPLETE, READ DOCUMENTATION IN DIAR_MAIN.py for more information

	


	













