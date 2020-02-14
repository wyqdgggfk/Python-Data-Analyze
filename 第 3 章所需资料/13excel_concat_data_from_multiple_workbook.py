import glob
import os
import sys
from datetime import date 
from xlrd import open_workbook,xldate_as_tuple
from xlwt import Workbook
input_folder = sys.argv[1]
output_file = sys.argv[2]
output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('all_data_all_workbooks')
data = []
first_worksheet = True
for input_file in glob.glob(os.path.join(input_folder, '*.xls')): # 原书中此处匹配的是 '*.xls*'
	print(os.path.basename(input_file)) # 原书此处 print 没有加括号
	with open_workbook(input_file) as workbook: # 开始打开具体工作簿
		for worksheet in workbook.sheets(): # 打开工作簿中的工作表
			if first_worksheet:
				header_row = worksheet.row_values(0)
				data.append(header_row)
				first_worksheet = False
			for row_index in range(1,worksheet.nrows):
				row_list = []
				for column_index in range(worksheet.ncols):
					cell_value = worksheet.cell_value(row_index,column_index)
					cell_type = worksheet
		