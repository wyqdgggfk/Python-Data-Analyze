import glob
import os
import sys
from datetime import date 
from xlrd import open_workbook,xldate_as_tuple
from xlwt import Workbook
input_folder = sys.argv[1]
output_file = sys.argv[2]
output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('all_data_all_workbooks')
data = []
first_worksheet = True
for input_file in glob.glob(os.path.join(input_folder, '*.xls')) # 原书中此处匹配的是 '*.xls*'