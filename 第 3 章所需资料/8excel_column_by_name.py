import sys
from datetime import date
from xlrd import open_workbook,xldate_as_tuple
from xlwt import Workbook
input_file = sys.argv[1] # 此处为 sales_2013.xlsx 
output_file = sys.argv[2] # 此处为 8output.xls
output_workboos = Workbook()