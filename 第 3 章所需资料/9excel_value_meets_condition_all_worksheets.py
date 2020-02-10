import sys
from datetime import date
from xlrd import open_workbook,xldate_as_tuple
from xlwt import Workbook
input_file = sys.argv[1]
output_file = sys.argv[2]	
output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('filetered_rows_all_worksheets')