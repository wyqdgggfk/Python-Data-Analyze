import glob
import os
import sys
from xlrd import open_workbook
input_directory = sys.argv[1]
workbook_counter = 0
for input_file in glob.glob(os.path.join(input_directory, '*.xls')): # 原书中的匹配是 '*.xls*',但这会匹配 xlsx 的文件
	workbook = open_workbook(input_file)
	"""
	需要注意下面的这种 print 方式,适用于单次 print
	如果您的代码在编写的过程中有多次修改,或者本身就有多次 print
	我一般会建议您创建一个 message 变量,把要 print 的内容赋值给 message 变量
	然后 print(message)
	"""
	print('Workbook: %s' % os.path.basename(input_file))
	print('Number of worksheets:%d' % workbook.nsheets)
	for worksheet in workbook.sheets():
		print('Worksheet name:',worksheet.name,'\tRows:',worksheet.nrows,'\tColumns:',worksheet.ncols)
	workbook_counter += 1	
	print('=====================================================') # 原书没有这一段,我加上作为分割线
print('Number of Excel workbooks:%d' %(workbook_counter))
