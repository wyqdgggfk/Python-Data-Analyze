import sys
from datetime import date 
from xlrd import open_workbook,xldate_as_tuple
from xlwt import Workbook
input_file = sys.argv[1]
output_file = sys.argv[2]
output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('set_of_worksheets')
my_sheets = [0,1]
threshold = 1900.0
sales_column_index = 3
first_worksheet = True
with open_workbook(input_file) as workbook:
	data = []
	for sheet_index in range(workbook.nsheets):
		if sheet_index in my_sheets:
			worksheet = workbook.sheet_by_index(sheet_index)
			if first_worksheet:
				header_row = worksheet.row_values(0)
				data.append(header_row)
				first_worksheet = False
			for row_index in range(1,worksheet.nrows):
				row_list = []
				sales_amount = worksheet.cell_value(row_index, sales_column_index)
				if sales_amount > threshold:
					for column_index in range(worksheet.ncols):
						cell_value = worksheet.cell_value(row_index, column_index)