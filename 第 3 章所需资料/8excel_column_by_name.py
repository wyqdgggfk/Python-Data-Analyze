import sys
from datetime import date
from xlrd import open_workbook,xldate_as_tuple
from xlwt import Workbook
input_file = sys.argv[1] # 此处为 sales_2013.xlsx 
output_file = sys.argv[2] # 此处为 8output.xls
output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('jan_2013_output')
my_columns = ['Customer ID','Purchase Date']
with open_workbook(input_file) as workbook:
	worksheet = workbook.sheet_by_name('january_2013')
	data = [my_columns]
	header_list = worksheet.row_values(0) # 此处存储的是第一排的标题
	header_index_list = []
	
	"""查找所需的索引值"""	
	for header_index in range(len(header_list)):
		if header_list[header_index] in my_columns:
			header_index_list.append(header_index)
	for row_index in range(1,worksheet.nrows):
		row_list = []