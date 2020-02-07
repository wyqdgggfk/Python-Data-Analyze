import sys
from datetime import date
from xlrd import open_workbook,xldate_as_tuple
from xlwt import Workbook
input_file = sys.argv[1]
output_file = sys.argv[2]
output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('jan_2013_output')
important_dates = ['01/24/2013','01/31/2013']
purchase_date_column_index = 4
with open_workbook(input_file) as workbook:
	worksheet = workbook.sheet_by_name('january_2013')
	data = []
	header = worksheet.row_values(0)
	data.append(header)
	for row_index in range(1.worksheet.nrows):
		purchase_datetime = xldate_as_tuple(worksheet.cell_value(row_index, purchase_date_column_index), workbook.datemode)