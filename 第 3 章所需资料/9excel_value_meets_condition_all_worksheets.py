import sys
from datetime import date
from xlrd import open_workbook,xldate_as_tuple
from xlwt import Workbook
input_file = sys.argv[1]
output_file = sys.argv[2]	
output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('filetered_rows_all_worksheets')
sales_column_index = 3
threshold = 2000.0
first_worksheet = True # 用一个 tag 判断处理的是否第一个工作表
with open_workbook(input_file) as workbook:
	data = []
	for worksheet in workbook.sheets():
		"""如果此处是第一个工作表,则需要保留其表头作为标题列"""
		if first_worksheet:
			header_row = worksheet.row_values(0)
			data.append(header_row)
			first_worksheet = False # 表头保留完成,将 first_worksheet 设置为 False
		for row_index in range(1,worksheet.nrows):
			row_list = []
			sale_amount = worksheet.cell_value(row_index,sales_column_index)
			if sale_amount > threshold:
				for column_index in range(worksheet.ncols):
					cell_value = worksheet.cell_value(row_index,column_index)
					cell_type = worksheet.cell_type(row_index,column_index)
					
					"""如果表格中的数据是日期,需要对其进行格式转换"""
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