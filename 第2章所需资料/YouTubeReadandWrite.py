import csv
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file,'r',newline='') as csv_in_file:
	with open(output_file,'w',newline='') as csv_out_file:
		filereader = csv.reader(csv_in_file)
		filewriter = csv.writer(csv_out_file)
		header = next(filereader)
		filewriter.writerow(header)
		for row_list in filereader:
			views = int(str(row_list[7]).strip()) # 观看人数
			likes = int(str(row_list[8]).strip()) # 点赞人数
			if views >= 1147000 and likes >= 39000: # 筛选观看人数和点赞人数均大于平均数的数据，共 5994 个
				filewriter.writerow(row_list)