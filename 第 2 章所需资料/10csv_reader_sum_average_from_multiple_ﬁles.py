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