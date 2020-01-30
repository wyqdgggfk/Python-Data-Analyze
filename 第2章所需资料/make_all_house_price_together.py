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
					if row_counter > 3 and row_counter < 9: # 对于第一个处理的文件，前 3 行和第 9 行数据是不需要的，只保留从第 4 行开始的数据
						if row_counter == 4:
							row.insert(0,"地区") # 在第 4 行的开头插入一个地区列，用来区分这些数据是哪个省市的
						else:
							pattern = re.compile("\.csv") # 用正则表达式把文件名的 .csv 去掉，把文件名加入到地区那一列
							location_name = re.sub(pattern, '', os.path.basename(input_file))
							row.insert(0,location_name)
						filewriter.writerow(row)
					row_counter += 1
				first_file = False
			else:
				for row in filereader:
					if row_counter > 4 and row_counter < 9:
						pattern = re.compile("\.csv")
						location_name = re.sub(pattern, '', os.path.basename(input_file))
						row.insert(0,location_name)
						filewriter.writerow(row)
					row_counter += 1
