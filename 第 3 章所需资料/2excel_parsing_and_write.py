import sys
from xlrd import open_workbook
from xlwt import Workbook
input_file = sys.argv[1] # 此处为 sales_2013.xlsx
output_file = sys.argv[2] 
output_workbook = Workbook() # 初始化一个 output_workbook 对象
output_worksheet = output_workbook.add_sheet('jan_2013_output') # 给 output_workbook 加入一个 sheet，取名 jan_2013_output
with open_workbook(input_file) as workbook:
	worksheet = workbook.sheet_by_name('january_2013')
	"""按照行列将原工作表 sales_2013.xlsx 中的每个数据输入到新工作表 2output.xls 中"""
	for row_index in range(worksheet.nrows):
		for column_index in range(worksheet.ncols):
			output_worksheet.write(row_index,column_index,worksheet.cell_value(row_index,column_index))
output_workbook.save(output_file)