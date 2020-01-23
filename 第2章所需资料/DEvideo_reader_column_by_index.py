import csv
import re
import time

pattern = re.compile('T[\d]+:[\d]+:[\S]+') # 正则表达式，用来筛选 publish_time 中的日期

"""实在不行再写好代码后，跑去终端运行，就直接把路径写下来吧"""
input_file = '/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/Trending_YouTube_Video_Statistics/DEvideos.csv'
output_file = '/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/DEvideo_write_column_by_index.csv'
with open(input_file,'r',newline='') as csv_in_file:
	with open(output_file,'w',newline='') as csv_out_file:
		filereader = csv.reader(csv_in_file)
		filewriter = csv.writer(csv_out_file)
		for row_list in filereader:
			row_list_output = []
			for i in range(15):
				if i==5:
					row_list[i] = re.sub(pattern, '', row_list[i]) #将 publish_time 中日期后面的部分用替换的方式删除掉
				row_list_output.append(row_list[i])
			filewriter.writerow(row_list_output)
			print(row_list_output)
			time.sleep(0.001)