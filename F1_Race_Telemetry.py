#https://www.formula1.com/en/f1-live.html

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

import csv

import pytesseract as tess

import os
import cv2
import re
import time

import tkinter as tk
from tkinter import filedialog


def OCR_RACE_TELEMETRICS_IPAD(path, FPS, filename):
	## Creation of DF


	Headers1=['Frame','Driver','Speed', 'Sector', 'Lap']
	CSV1 = pd.DataFrame(columns=Headers1)

	CSV2 = pd.DataFrame(columns=Headers1)


	root = tk.Tk()
	root.withdraw()

	#path = filedialog.askopenfilename()


	img = cv2.VideoCapture(path) 
	success, image = img.read()

	Digit_Config = r'--oem 3 --psm 6 outputbase digits'
	Lap_Config = r'--oem 3 tessedit_char_whitelist=0123456789/ --psm 13'



	BG = np.sum(np.array([64, 55, 57]))
	a=time.time()

	length = int(img.get(cv2.CAP_PROP_FRAME_COUNT))

	frame=1
	Stopper1 = False
	Stopper2 = False  
	S1_1_test = False
	S3_1_test = False
	S1_2_test = False
	S3_2_test = False

	while success:

		#Get Frame
		#a=time.time()

		img.set(1, frame)
		success, image = img.read()
		ret, currentFrame = img.read()
		print(' Processing frame: ', frame,' of ',length,' (',round(100*frame/length,1),'%)')

		#print('a->b',str(time.time()-a))
		
		#b=time.time()

		

		try:

		#Driver 1
			roi_track = currentFrame[21:42, 16:76]

			roi_name1 = currentFrame[130:157, 259:480]
			
			roi_speed1 = currentFrame[343:367, 404:469] 

			roi_sec1_1 =currentFrame[555:560, 300:370]
			roi_sec2_1 =currentFrame[555:560, 400:470]
			roi_sec3_1 =currentFrame[555:560, 500:570]

			

			roi_lap1 = currentFrame[1257:1295, 1274:1381]

		#Driver 2
			roi_name2 = currentFrame[772:809, 258:440]
			
			roi_speed2 = currentFrame[993:1019, 409:465] 

			roi_sec1_2 =currentFrame[1206:1212, 312:356]
			roi_sec2_2 =currentFrame[1208:1212, 407:448]
			roi_sec3_2 =currentFrame[1207:1213, 507:539]

		except:
			break

		## 1st Frame Selection (Names, Track)

		if (frame==1):

			## Driver 1 Name
			roi_name1 = cv2.cvtColor(roi_name1, cv2.COLOR_BGR2GRAY)
			#(thresh, roi_name1) = cv2.threshold(roi_name1, 127, 255, cv2.THRESH_BINARY)

			Name1 = tess.image_to_string(roi_name1, lang='eng', config='--psm 6')
			Name1 = re.sub('',"", Name1)
			Name1 = re.sub('\n',"", Name1)


			## Driver 2 Name
			roi_name2 = cv2.cvtColor(roi_name2, cv2.COLOR_BGR2GRAY)
			#(thresh, roi_name2) = cv2.threshold(roi_name2, 127, 255, cv2.THRESH_BINARY)

			Name2 = tess.image_to_string(roi_name2, lang='eng', config='--psm 6')
			Name2 = re.sub('',"", Name2)
			Name2 = re.sub('\n',"", Name2)

					
			roi_track = cv2.cvtColor(roi_track, cv2.COLOR_BGR2GRAY)
			(thresh, roi_track) = cv2.threshold(roi_track, 127, 255, cv2.THRESH_BINARY)

			Track = tess.image_to_string(roi_track, config='--psm 6')
			Track = re.sub('',"", Track)
			Track = re.sub('\n',"", Track)


		##Sectors Driver 1

		sec1col_1= np.around(np.mean(roi_sec1_1, axis=(0,1)),decimals=0)
		sec2col_1= np.around(np.mean(roi_sec2_1, axis=(0,1)),decimals=0)
		sec3col_1= np.around(np.mean(roi_sec3_1, axis=(0,1)),decimals=0)
		
		#print(type(np.sum(sec3col)),type(BG))
		
		if ((BG*1.10>np.sum(sec3col_1)) and (BG*1.10<np.sum(sec2col_1)) and (BG*1.10<np.sum(sec1col_1))):
			#print("\nSector 3")
			Sector_1 = "Sector 3"

		if ((BG*1.10<np.sum(sec3col_1)) and (BG*1.10<np.sum(sec2col_1)) and (BG*1.10<np.sum(sec1col_1))):
			#print("\nSector 1")
			Sector_1 = "Sector 1"

		if ((BG*1.10>np.sum(sec3col_1)) and (BG*1.10>np.sum(sec2col_1)) and (BG*1.10<np.sum(sec1col_1))):
			#print("\nSector 2")
			Sector_1 = "Sector 2"

		##Sectors Driver 2

		sec1col_2= np.around(np.mean(roi_sec1_2, axis=(0,1)),decimals=0)
		sec2col_2= np.around(np.mean(roi_sec2_2, axis=(0,1)),decimals=0)
		sec3col_2= np.around(np.mean(roi_sec3_2, axis=(0,1)),decimals=0)
		
		#print(type(np.sum(sec3col)),type(BG))
		
		if ((BG*1.10>np.sum(sec3col_2)) and (BG*1.10<np.sum(sec2col_2)) and (BG*1.10<np.sum(sec1col_2))):
			#print("\nSector 3")
			Sector_2 = "Sector 3"

		if ((BG*1.10<np.sum(sec3col_2)) and (BG*1.10<np.sum(sec2col_2)) and (BG*1.10<np.sum(sec1col_2))):
			#print("\nSector 1")
			Sector_2 = "Sector 1"

		if ((BG*1.10>np.sum(sec3col_2)) and (BG*1.10>np.sum(sec2col_2)) and (BG*1.10<np.sum(sec1col_2))):
			#print("\nSector 2")
			Sector_2 = "Sector 2"


		### Sector Test for Sequence Driver 1

		if (Sector_1 == "Sector 1" and Stopper1 == False) :
			S1_1_test=True
			S3_1_test=False
			


		if Sector_1 == 'Sector 3' and S1_1_test == True:
			S1_1_test = False
			S3_1_test = True
			Stopper1 = True

		if Sector_1 == 'Sector 1' and S3_1_test == True:
			S1_1_test = False
			S3_1_test = False


		### Sector Test for Sequence Driver 2

		if (Sector_2 == "Sector 1" and Stopper2 == False) :
			S1_2_test=True
			S3_2_test=False


		if Sector_2 == 'Sector 3' and S1_2_test == True:
			S1_2_test = False
			S3_2_test = True
			Stopper2 = True

		if Sector_2 == 'Sector 1' and S3_2_test == True:
			S1_2_test = False
			S3_2_test = False


		### Lap
		roi_lap1 = cv2.cvtColor(roi_lap1, cv2.COLOR_BGR2GRAY)
		(thresh, roi_speed2) = cv2.threshold(roi_speed2, 127, 255, cv2.THRESH_BINARY)
		

		Lap1 = tess.image_to_string(roi_lap1,lang='lapTime', config=Lap_Config)  #Time Creep, train data


		Lap1 = re.sub('',"", Lap1)
		Lap1 = re.sub('\n',"", Lap1)
		Lap1 = re.sub('\.',"", Lap1)		
		Lap1 = re.sub(' ',"", Lap1)
		Lap1 = re.sub('/'," of ", Lap1)


		### DF log & speed for driver 1
		if S1_1_test == True or S3_1_test == True:

			## Speed Driver 1
			try:
				roi_speed1 = cv2.cvtColor(roi_speed1, cv2.COLOR_BGR2GRAY)
				(thresh, roi_speed1) = cv2.threshold(roi_speed1, 127, 255, cv2.THRESH_BINARY)

				Speed1 = tess.image_to_string(roi_speed1, lang ='F1r', config=Digit_Config)
				Speed1 = int(re.sub("[^0-9]", "", Speed1))
				
			except:
				break

		 
			### Print result
			print('\n'+Track+': '+Name1+' at '+str(Speed1)+' kph on frame: '+str(frame)+' for '+Sector_1+' '+Lap1+'\n')



			### Log in DFs
			CSV1_While = pd.DataFrame([{'Frame':frame,'Driver':Name1, 'Speed':Speed1, 'Sector':Sector_1, 'Lap': Lap1}], columns=Headers1)

			CSV1 = CSV1.append(CSV1_While)


### DF log & speed for driver 2
		if S1_2_test == True or S3_2_test == True:
			## Speed Driver 2
			try:
				
				roi_speed2 = cv2.cvtColor(roi_speed2, cv2.COLOR_BGR2GRAY)
				(thresh, roi_speed2) = cv2.threshold(roi_speed2, 127, 255, cv2.THRESH_BINARY)


				Speed2 = tess.image_to_string(roi_speed2, lang ='F1r', config=Digit_Config)
				Speed2 = int(re.sub("[^0-9]", "", Speed2))

			except:
				break

		 
			### Print result
			print('\n'+Track+': '+Name2+' at '+str(Speed2)+' kph on frame: '+str(frame)+' for '+Sector_2+' '+Lap1+'\n')



			### Log in DFs

			CSV2_While = pd.DataFrame([{'Frame':frame,'Driver':Name2, 'Speed':Speed2, 'Sector':Sector_2, 'Lap': Lap1}], columns=Headers1)

			CSV2 = CSV2.append(CSV2_While)

		frame = frame+FPS
		### While end



	FrameLapTime = CSV1['Frame']
	FrameLapTime= FrameLapTime.max()+10

	img.set(1, FrameLapTime)
	ret, currentFrame = img.read()

	roi_lastlap_1 = currentFrame[254:274, 578:676]

	roi_lastlap_1 = cv2.cvtColor(roi_lastlap_1, cv2.COLOR_BGR2GRAY)
	(thresh, roi_lastlap_1) = cv2.threshold(roi_lastlap_1, 100, 255, cv2.THRESH_BINARY_INV)
	
	lastlap_1 = tess.image_to_string(roi_lastlap_1, lang='lapTime', config=Digit_Config)
	lastlap_1 = re.sub(" ", ":", lastlap_1)
	lastlap_1 = re.sub('',"", lastlap_1)
	lastlap_1 = re.sub('\n',"", lastlap_1)
	print(lastlap_1)
	# CSV1 = CSV1.append([{'Last lap':lastlap_1}])
	print(CSV1)


	FrameLapTime = CSV2['Frame']
	FrameLapTime = FrameLapTime.max()+10

	img.set(1, FrameLapTime)
	ret, currentFrame = img.read()

	roi_lastlap_2 = currentFrame[906:926, 581:678]

	roi_lastlap_2 = cv2.cvtColor(roi_lastlap_2, cv2.COLOR_BGR2GRAY)
	(thresh, roi_lastlap_2) = cv2.threshold(roi_lastlap_2, 100, 255, cv2.THRESH_BINARY_INV)

	lastlap_2 = tess.image_to_string(roi_lastlap_2, lang='lapTime', config=Digit_Config)
	lastlap_2 = re.sub(" ", ":", lastlap_2)
	lastlap_2 = re.sub('',"", lastlap_2)
	lastlap_2 = re.sub('\n',"", lastlap_2)
	print(lastlap_2)
	# CSV2 = CSV2.append([{'Last lap':lastlap_2}])
	print(CSV2)

	CSV1.to_csv("Output/Race/"+filename+'_'+Name1+'_at'+str(FPS)+'fps'+'.csv',index=False)

	CSV2.to_csv("Output/Race/"+filename+'_'+Name2+'_at'+str(FPS)+'fps'+'.csv',index=False)

	print('##############################################################')
	print(filename,' took ',round((time.time()-a)/60,2),' min.')
	print('##############################################################')

def File_Processing():

	directory='/Users/jeromedormoy/Desktop/Jerome/Project/Python/F1 Data Viz/Input'
	ArchiveDir ='/Users/jeromedormoy/Desktop/Jerome/Project/Python/F1 Data Viz/Input/Archive'


	for filename in os.listdir(directory):
	    if filename.endswith(".mp4") or filename.endswith(".MP4"):


	    	current_path=os.path.join(directory, filename)

	    	print(current_path)

	    	OCR_RACE_TELEMETRICS_IPAD(current_path, 3, filename)
	    	time.sleep(1)

	    	os.rename((os.path.join(directory, filename)),(os.path.join(ArchiveDir, filename)))

	  
	    else:
	    	continue






while True:
	print('Looking for Video!')
	File_Processing()
	time.sleep(3)






#OCR_RACE_TELEMETRICS_IPAD('Input/Archive/AUT_LEC_RIC_L25.MP4',10,'TEST_TIME')
