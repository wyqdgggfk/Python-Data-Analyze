import csv
import glob
import os
import sys
input_path = sys.argv[1]
output_file = sys.argv[2]
first_file = True
for input_file in glob.glob(os.path.join(input_path, 'sales_*')):
	print(os.path.basename(input_file)) # 打印当前处理文件的名称
	with open(input_file,'r',newline='') as csv_in_file:
		filereader = csv.reader(csv_in_file)