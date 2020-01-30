import csv
import glob
import os
import sys
import re

input_path = sys.argv[1]
output_file = sys.argv[2]
first_file = True

for input_file in glob.glob(os.path.join(input_path, '*csv')):
	message = "Dealing with file " + str(os.path.basename(input_file))
#	print(message)
	with open(input_file,'r',newline='') as csv_in_file:
		with open(output_file,'a',newline='') as csv_out_file:
			filereader = csv.reader(csv_in_file)
			filewriter = csv.writer(csv_out_file)
			row_counter = 1
			if first_file:
				for row in filereader:
					if row_counter > 3 and row_counter < 9:
						if row_counter == 4:
							row.insert(0,"地区")
						else:
							pattern = re.compile("\.csv")
							location_name = re.sub(pattern, '', os.path.basename(input_file))
							row.insert(0,os.path.basename(input_file))
						print(row)
					row_counter += 1
				first_file = False
			else:
				for row in filereader:
					if row_counter > 4 and row_counter < 9:
						print(row)
					row_counter += 1
