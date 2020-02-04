import csv
import glob
import os
import sys
input_path = sys.argv[1]
output_file = sys.argv[2]
output_header_list = ['file_name','total_sales','average_sales'] # 创建一个输出文件的列标题列表
csv_out_file = open(output_file,'a',newline='')
filewriter = csv.writer(csv_out_file)
filewriter.writerow(output_header_list) # 将标题行写入输出文件
for input_file in glob.glob(os.path.join(input_path, 'sales_*')):
	with open(input_file,'r',newline='') as csv_in_file:
		filereader = csv.reader(csv_in_file)
		output_list = [] # 用来保存要写入输出文件中的每行输出
		output_list.append(os.path.basename(input_file)) # 您可以试试看，这个地方保留的 input_file 是有后缀 .csv 的，那么写入到输出文件时怎么去除后续呢
		header = next(filereader) # next() 函数去除每个输入文件的标题行
		total_sales = 0.0
		number_of_sales = 0.0
		for row in filereader:
			sale_amount = row[3]
			total_sales += float(str(sale_amount).strip('$').replace(',',''))
			number_of_sales += 1
		average_sales = '{0:.2f}'.format(total_sales/number_of_sales)
		output_list.append(total_sales)
		output_list.append(average_sales)
		filewriter.writerow(output_list)
csv_out_file.close()