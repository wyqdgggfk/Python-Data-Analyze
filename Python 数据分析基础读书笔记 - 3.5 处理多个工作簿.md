# 3.5 处理多个工作簿

首先引用一下原书中的话:

> 本章前面的几小节演示了如何为单个工作表,工作簿中所有的工作表和工作簿中的一组工作表筛选出特定的行与特定的列.这些处理工作簿的技术是非常有用的.但是,有时你需要处理多个工作簿.在这种情况下,Python 会给你惊喜,因为它可以让你自动化和规模化地进行数据处理,远远超过手工处理能够达到的限度.

没错,这就是作用,实际工作时,我们可能收到多个来自不同部门的数据,比如新疆销售数据,河南销售数据,又比如腕达影院电影票房数据,保立影院电影票房数据等等.综合咱们之前学习过的筛选行,筛选列,读取工作簿中的多个工作表,现在我们要看看怎样读取多个工作簿.

书中会用到 [sales_2014.xlsx](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/sales_2014.xlsx) 和 [sales_2015.xlsx](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/sales_2015.xlsx) 这两个 Excel 表格进行讲解,我已经将此表格放到了我的仓库,欢迎 star.

## 3.5.1 工作表计数以及每个工作表中的行列计数

我知道一个工作簿中有多少工作表,每个工作表有多少行列,有什么作用呢?实际上,当我们拿到一些数据的时候,这些数据可能很大,也可能很多,每个工作表有多少行多少列,都有些什么内容,我们都不一定清楚,如果工作表较少或者文件不是很大,我们可以直接打开来看看,但如果有很多工作表,光是打开它们就很费劲了,所以可以利用 Python 先对这些工作表进行一下集中的处理,知道个大概的数据量.下面就看看怎么操作:

文件名称:12excel_introspect_all_workbooks.py

所需文件:

输出文件:None

```python
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

```



