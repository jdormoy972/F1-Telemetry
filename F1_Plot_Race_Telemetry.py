import numpy as np
import pandas as pd

import re

import os 

import matplotlib
matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

import tkinter as tk
from tkinter import filedialog

def Plot_Data(File1, File2, group):

	root = tk.Tk()
	root.withdraw()

	# File1 = filedialog.askopenfilename()
	# File2 = filedialog.askopenfilename()

	# File1="Output/AUT_LEC_VET_L51.MP4_AUT_LECLERC_at3fps.csv"
	# File2="Output/AUT_LEC_VET_L51.MP4_AUT_VETTEL_at3fps.csv"


	pattern = "Output/(.*?)_"

	Track1 = str(re.search(pattern, File1).group(1))
	Track2 = str(re.search(pattern, File2).group(1))

	pattern = "_at(.*?)fps"

	FPS1 = int(re.search(pattern, File1).group(1))
	FPS2 = int(re.search(pattern, File2).group(1))


	df1 = pd.read_csv(File1)
	df2 = pd.read_csv(File2)



	df1['Distance'] = df1.apply(lambda row: 1000*row.Speed*((FPS1/33.5)/3600), axis = 1 )
	df1['cumsum'] = df1['Distance'].cumsum()
#FRA: 5842
#AUT: 4318

	if Track1 =='FRA': 
		Lap_Length =5842
	if Track1 =='AUT': 
		Lap_Length =4318

	Driver1=df1['Driver'].values[0]

	Err1 = round(100*(Lap_Length-df1['Distance'].sum())/Lap_Length, 3)
	Err1 = Driver1+\
	"\nMeasured Lenght: "+str(round(df1['Distance'].sum(), 2))+" m"+\
	"\nError: "+str(Err1)+"%"


##### D2

	for index, row in df2.iterrows():
		#print(row['Frame'], row['Sector'], index)

		if (row['Sector']=='Sector 1'):
			break
		

		df2 = df2.drop([index], axis = 0)

	df2 =df2.sort_index(ascending=False)
	
	for index, row in df2.iterrows():

		if (row['Sector']=='Sector 3'):
			break

		df2 = df2.drop([index], axis = 0)


	df2 =df2.sort_index(ascending=True)



	df2['Distance'] = df2.apply(lambda row: 1000*row.Speed*((FPS2/33.5)/3600), axis = 1 )
	df2['cumsum'] = df2['Distance'].cumsum()
#FRA: 5842
#AUT: 4318

	if Track2 =='FRA': 
		Lap_Length =5842
	if Track2 =='AUT': 
		Lap_Length =4318

	Driver2=df2['Driver'].values[0]

	Err2 = round(100*(Lap_Length-df2['Distance'].sum())/Lap_Length, 3)
	Err2 = Driver2+\
	"\nMeasured Length: "+str(round(df2['Distance'].sum(), 2))+" m"+\
	"\nError: "+str(Err2)+"%"

	# print(df2)
	# print(df2['Distance'].sum())
	# print(Err2)


	## Get Sectors 
	SectorMax = (df1.loc[df1.groupby('Sector').idxmax().iloc[:, 0]])
	print(SectorMax)
	S1=SectorMax.iloc[0,2]
	S2=SectorMax.iloc[1,2]
	S3=SectorMax.iloc[2,2]



#### Plot
	fig, ax = plt.subplots()


	ax.plot('cumsum', 'Speed', data=df1, marker = '', color='b', label=Err1)
	#ax[1].plot('cumsum', 'Sector', data=df1, marker = '', color='b')

	ax.plot('cumsum', 'Speed', data=df2, linestyle='--', color='grey', label=Err2)
	#ax[1].plot('cumsum', 'Sector', data=df2, marker = '', color='grey')

	ax.legend(loc='best', bbox_to_anchor=(0.5, 0., 0.5, 0.5), shadow=True, ncol=1)
	plt.xlim([0, S3])
	ax.set_xlabel('Distance (m)')
	ax.set_ylabel('Speed (kph)')
	
	ax.xaxis.set_major_locator(MultipleLocator(250))
	ax.yaxis.set_major_locator(MultipleLocator(25))

	#ax[0].xaxis.set_major_formatter('{x:.0f}')

	#ax[0].xaxis.set_minor_locator(MultipleLocator(50))

	ax.set_title(group, pad=30)
	ax.grid(color='m', linestyle='--', linewidth=.5)
	#ax[1].grid(color='m', linestyle='--', axis='x', linewidth=1)


	ax.axvline(S1, color='black', linestyle='-.', linewidth=.8)
	plt.text(S1,ax.get_ylim()[1]+4, "Sector 1", horizontalalignment='center', verticalalignment='center',)

	ax.axvline(S2, color='black', linestyle='-.', linewidth=.8)
	plt.text(S2,ax.get_ylim()[1]+4, "Sector 2", horizontalalignment='center', verticalalignment='center',)

	ax.axvline(S3, color='black', linestyle='-.', linewidth=.8)
	plt.text(S3,ax.get_ylim()[1]+4, "Sector 3", horizontalalignment='center', verticalalignment='center',)

	# axes1.set_xlabel("x-axis 1")
	# axes2.set_xlabel("x-axis 2")


	# fig = matplotlib.pyplot.gcf()
	fig.set_size_inches(18.5, 10.5)


	# props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)

	#ax.annotate(Err, )


	plt.show()
	# plt.savefig('Plot_Out/'+group)
	return


# directory='/Users/jeromedormoy/Desktop/Jerome/Project/Python/F1 Data Viz/Output/Quali'
# ArchiveDir='/Users/jeromedormoy/Desktop/Jerome/Project/Python/F1 Data Viz/Output/Archive'
# pattern = "Output/(.*?).MP4"

# File_list=np.array([])

# for filename in os.listdir(directory):
#     if filename.endswith(".csv") :

#     	file=str(directory+filename)
#     	file = re.search(pattern, file)
#     	try:
#     		#print(file.group(1))
#     		File_list= np.append(File_list,file.group(1))

#     	except:
#     		pass

# File_list = np.unique(File_list)
# print(File_list)
# file1=0
# file2=0

# for group in File_list:


# 		for filename in os.listdir(directory):

# 			if filename.startswith(group) :

# 				if file1 == 0:
# 					file1 = filename
# 				if file1 != 0:
# 					file2 = filename
# 		print(file1, file2)
# 		Plot_Data(directory+file1,directory+file2, group)

# 		os.rename((os.path.join(directory, file1)),(os.path.join(ArchiveDir, file1)))
# 		os.rename((os.path.join(directory, file2)),(os.path.join(ArchiveDir, file2)))

# 		file1=0
# 		file2=0
