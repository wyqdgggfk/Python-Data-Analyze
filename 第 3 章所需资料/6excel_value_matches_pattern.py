import re
import sys
from datetime import date
from xlrd import open_workbook,xldate_as_tuple
from xlwt import Workbook
input_file = sys.argv[1] # 此处为 sales_2013.xlsx
output_file = sys.argv[2] # 此处为 6output.xls
output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('jan_2013_output')
pattern = re.compile(r'(?P<my_pattern>^J.*)') # 这段文字中 ^J.* 是最重要的,意为从开头进行匹配,J后面可跟任意多个字符
customer_name_column_index = 1
"""
以下代码的逻辑与之前很类似,一样是打开文件,逐个单元格查看,如果满足要求,就将此行数据提出
"""
with open_workbook(input_file) as workbook:
	worksheet = workbook.sheet_by_name('january_2013')
	data = []
	header = worksheet.row_values(0)
	data.append(header)
	for row_index in range(1,worksheet.nrows):
		row_list = []
		if pattern.search(worksheet.cell_value(row_index, customer_name_column_index)):
			for column_index in range(worksheet.ncols):
				cell_value = worksheet.cell_value(row_index, column_index)
				cell_type = worksheet.cell_type(row_index, column_index)
				if cell_type == 3:
					date_cell = xldate_as_tuple(cell_value, workbook.datemode)
					date_cell = date(*date_cell[0:3]).strftime('%m/%d/%Y')
					row_list.append(date_cell)
				else:
					row_list.append(cell_value)
		if row_list:
			data.append(row_list)
	for list_index,output_list in enumerate(data):
		for element_index,element in enumerate(output_list):
			output_worksheet.write(list_index,element_index,element)
output_workbook.save(output_file)