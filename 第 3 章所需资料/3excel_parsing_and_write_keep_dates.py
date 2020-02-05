import sys
from datetime import date
from xlrd import open_workbook,xldate_as_tuple
from xlwt import Workbook
input_file = sys.argv[1] # 此处为 sales_2013.xlsx
output_file = sys.argv[2] # 此处为 3output.xls
output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('jan_2013_output')
with open_workbook(input_file) as workbook:
	worksheet = workbook.sheet_by_name('january_2013')
	for row_index in range(worksheet.nrows):
		row_list_output = [] # 实际上这个 row_list_output 根本不影响输出文件
		for col_index in range(worksheet.ncols):
			"""如果这个单元格是时间"""
			if worksheet.cell_type(row_index, col_index) == 3: # 可查看 xlrd 的文档，检验单元格类型是否为数字 3，类型为 3 表示包含日期数据
				date_cell = xldate_as_tuple(worksheet.cell_value(row_index, col_index), workbook.datemode) # 参数 workbook.datemode 是必需的，可以确定日期是基于 1900 年还是 1904 年
				date_cell = date(*date_cell[0:3]).strftime('%m/%d/%Y')
				row_list_output.append(date_cell) # 实际上这个 row_list_output 根本不影响输出文件
				output_worksheet.write(row_index,col_index,date_cell)
			"""如果这个单元格不是时间"""
			else:
				non_date_cell = worksheet.cell_value(row_index, col_index)
				row_list_output.append(non_date_cell) # 实际上这个 row_list_output 根本不影响输出文件
				output_worksheet.write(row_index,col_index,non_date_cell)
output_workbook.save(output_file)