import glob
import os
import sys
from datetime import date 
from xlrd import open_workbook,xldate_as_tuple	
from xlwt import Workbook
input_folder = sys.argv[1]
output_file = sys.argv[2]
output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('sum_and_averages')
all_data = []
sales_column_index = 3
header = ['workbook','worksheet','worksheet_total','worksheet_average','workbook_total','workbook_average']
all_data.append(header)
for input_file in glob.glob(os.path.join(input_folder, '*.xls*')):
	with open_workbook(input_file) as workbook:
		list_of_totals = []
		list_of_numbers = []
		workbook_output = []
		for worksheet in workbook.sheets():
			total_sales = 0
			number_of_sales = 0
			worksheet_list = []
			worksheet_list.append(os.path.basename(input_file))
			worksheet_list.append(worksheet.name)