import glob
import os
import sys
from xlrd import open_workbook
input_directory = sys.argv[1]
workbook_counter = 0
for input_file in glob.glob(os.path.join(input_directory, '*.xls')): # 原书中的匹配是 '*.xls*',但这会匹配 xlsx 的文件
	workbook = open_workbook(input_file)
	print('Workbook: %s' % os.path.basename(input_file))
	print('Number of worksheets:%d' % workbook.nsheets)
	for worksheet in workbook.sheets():
		print('Worksheet name:',worksheet.name,'\tRows:',worksheet.nrows,'\tColumns:',worksheet.ncols)
	workbook_counter += 1	
	print('=====================================================') # 原书没有这一段,我加上作为分割线
print('Number of Excel workbooks:%d' %(workbook_counter))
