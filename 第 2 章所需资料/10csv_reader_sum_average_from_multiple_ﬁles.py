import csv
import glob
import os
import sys
input_path = sys.argv[1]
output_file = sys.argv[2]
output_header_list = ['file_name','total_sales','average_sales']
csv_out_file = open(output_file,'a',newline='')
filewriter = csv.writerow(csv_out_file)
filewriter.writerow(output_header_list)
for input_file in glob.glob(os.path.join(input_path, 'sales_*')):
	with open(input_file,'r',newline='') as csv_in_file:
		filereader = csv.reader(csv_in_file)
		output_list = []
		output_list.append(os.path.basename(input_file))
		