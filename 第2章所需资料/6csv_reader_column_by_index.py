import csv
import sys
input_file = sys.argv[1]
output_file = sys.argv[2]
my_column = [0,3]
with open(input_file,'r',newline='') as csv_in_file:
	with open(output_file,'w',newline='') as csv_out_file:
		filereader = csv.reader(csv_in_file)
		filewriter = csv.writer(csv_out_file)