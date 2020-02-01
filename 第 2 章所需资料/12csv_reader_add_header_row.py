import sys
import csv

"""
开始之前，请打开 supplier_data.csv 文件，把标题行删了，然后将此文件另存为supplier_data_no_header_row.csv
"""

input_file = sys.argv[1] # 此处为 supplier_data_no_header_row.csv
output_file = sys.argv[2] # 此处为 12output.csv

with open(input_file,'r',newline='') as csv_in_file:
	with open(output_file,'w',newline='') as csv_out_file:
		filereader = csv.reader(csv_in_file)
		filewriter = csv.writer(csv_out_file)
		header_list = ['Supplier Name','Invoice Number','Part Number','Cost','Purchase Date']
		filewriter.writerow(header_list)
		for row in filereader:
			filewriter.writerow(row)		