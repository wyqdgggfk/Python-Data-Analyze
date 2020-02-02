import sys
from xlrd import open_workbook
input_file = sys.argv[1]
workbook = open_workbook(input_file)
print("Number of worksheets:",workbook.nsheets)