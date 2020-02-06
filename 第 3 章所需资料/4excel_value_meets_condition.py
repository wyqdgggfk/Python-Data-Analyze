import sys
from datetime import date
from xlrd import open_workbook,xldate_as_tuple
from xlwt import Workbook
input_file = sys.argv[1]
output_file = sys.argv[2]
output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('jan_2013_output')
sale_amount_column_index = 3
with open_workbook(input_file) as workbook:
	worksheet = workbook.sheet_by_name('january_2013')
	data = []
	header = worksheet.row_values(0) # 获取标题行
	data.append(header)
	for row_index in range(1,worksheet.norows):
		row_list = []
		sale_amount = worksheet.cell_value(row_index, sale_amount_column_index)
		if sale_amount > 1400.0:
			for column_index in range(worksheet.ncols):
				cell_value = worksheet.cell_value(row_index, column_index)
				cell_type = worksheet._cell_type(row_index,column_index)
				if cell_type == 3:
					date_cell = xldate_as_tuple(cell_value, workbook.datemode)
					date_cell = date(*date_cell[0:3]).strftime('%m/%d/%Y')