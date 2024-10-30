#!/usr/bin/python
#/*************************************************************************************
#                PURPOSE:  Script to:
#														1) Count rows in csvs and output to csv (filepath + filename in column 1, rows in that file in column 2, total rowcount)
#														2) Overwrite (certain) Column names values
#														3) Drop Column by column name
#														4) Populate PreProcessed files into separate folder
#														5) Consolidate all pre processed CSVs into one CSV
#														
#               DATABASE:  File System (S:)
#                 AUTHOR:  Simeon Meerson
#
#                CREATED:  09-20-2023
#          LAST MODIFIED:  10-30-2024
#  					
#********************************************************************************************************************************************************************************************/
# General libraries used
import re
import os
import csv
import glob
import time
import pandas as pd

# Sorting through and moving files in directories
import os.path
import shutil
import fnmatch


# rawpath variables: rawpath is where raw (downloaded) files are located, preprocessedpath is preprocessedpathination of output file(s)
rawpath = r'C:\Users\...\Raw Downloads\FY2025\2024_07\20240729'
preprocessedpath = r'C:\Users\...\Pre Processed\2024_07\20240729'
finaldestination = r'C:\Users\...\Deliverables\...\FY2025\2024_07\20240729'

# sort files
files = os.listdir(rawpath)
files.sort()


#######################################
#		Consolidate csv files     				#
#######################################

# Get date of files being processed
def getfilenamedate(filedate):
  for file in files:
    filenames = ''
    filenames += '' + file
    filedate = file[:8]
    return filedate

filedate = getfilenamedate(rawpath)

# data structure to store and map row counts in each file
counts = []

# output file containing results
writer = csv.writer(open(filedate + '_RowCounts.csv', "w", newline=''))
writer.writerow(["Filename", "RowCount"])

# function to count rows in files
def rowCounter(fname):
  with open(fname, "r", errors ="ignore") as f:
    reader = csv.reader(f, delimiter=",")
    if any(reader):
    	data = list(reader)
    	row_count = len(data)
    	writer.writerow([fname, row_count]) 
    	counts.append(row_count)

# function performing rowcounter on each file parsed
def totals(fs):
    for i in fs: 
        rowCounter(rawpath + '\\' + i)

#Execute counter functions
totals(files)
sum(counts)

# Writing rows to file counts file
writer.writerow([" "])
writer.writerow(["Total Count: ", sum(counts)])

# Club File Column Name Clean up:
filecount = 0;
for f in files:
	if f.endswith('csv'): 
		fp = os.path.join(rawpath, f)
		df = pd.read_csv(fp, encoding='cp1252')
		filecount += 1
		cols = df.columns
		new_cols = {}
		for c in cols:
			new_col = re.sub('Column Text To Remove .*? - ', '', c)
			new_cols[c] = new_col
		print('Overwriting column values in: ' + f)
		df2 = df.rename(columns=new_cols)
		df2 = df2.drop('Column To Drop', axis = 1)
				# to write a new file
		df2.to_csv(os.path.join(preprocessedpath, f), index=False)

# Data Frame to Read CSV files in path directory location
dfs = [pd.read_csv(os.path.join(preprocessedpath, f), low_memory=False, encoding='latin-1') for f in files]

# Club Files are Data Frames for Data Frame
dfs = [df for df in dfs]

# Concactenate Data Frames into one Data Frame
df = pd.concat(dfs, sort=False)

# Write Concactenated Data Frame to CSV
#df.to_csv(time.strftime("AprilClubRegistrations") + '.csv')
df.to_csv(os.path.join(finaldestination, filedate + "_CSV_Consolidations.csv"), index=False)

# console output 
print(filedate + ' CSVs are being consolidated...')
print(filedate + ' Files have been processed!')