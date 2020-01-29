import csv
import glob
import os
import sys

input_path = sys.argv[1]
file_counter = 0
for input_file in glob.glob(os.path.join(input_file, 'sales_*')):
	row_counter = 1
	with open(input_file,'r',newline='') as csv_in_file:
		filereader = csv.reader(csv_in_file)
		header = next(filereader,None)
		for row in filereader:
			row_counter += 1
	