# 3.5 处理多个工作簿

首先引用一下原书中的话:

> 本章前面的几小节演示了如何为单个工作表,工作簿中所有的工作表和工作簿中的一组工作表筛选出特定的行与特定的列.这些处理工作簿的技术是非常有用的.但是,有时你需要处理多个工作簿.在这种情况下,Python 会给你惊喜,因为它可以让你自动化和规模化地进行数据处理,远远超过手工处理能够达到的限度.

没错,这就是作用,实际工作时,我们可能收到多个来自不同部门的数据,比如新疆销售数据,河南销售数据,又比如腕达影院电影票房数据,保立影院电影票房数据等等.综合咱们之前学习过的筛选行,筛选列,读取工作簿中的多个工作表,现在我们要看看怎样读取多个工作簿.

书中会用到 [sales_2014.xlsx](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/sales_2014.xlsx) 和 [sales_2015.xlsx](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/sales_2015.xlsx) 这两个 Excel 表格进行讲解,我已经将此表格放到了我的仓库,欢迎 star.

## 3.5.1 工作表计数以及每个工作表中的行列计数

我知道一个工作簿中有多少工作表,每个工作表有多少行列,有什么作用呢?实际上,当我们拿到一些数据的时候,这些数据可能很大,也可能很多,每个工作表有多少行多少列,都有些什么内容,我们都不一定清楚,如果工作表较少或者文件不是很大,我们可以直接打开来看看,但如果有很多工作表,光是打开它们就很费劲了,所以可以利用 Python 先对这些工作表进行一下集中的处理,知道个大概的数据量.下面就看看怎么操作:

文件名称:[12excel_introspect_all_workbooks.py](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/12excel_introspect_all_workbooks.py)

所需文件:[第 3 章所需文件](https://github.com/wyqdgggfk/Python-Data-Analyze/tree/master/第%203%20章所需资料)

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
```

我在跟着书练习这段代码时,遇到了两个错误,提出来仅供参考:

其一是如果在终端直接 cd 到 12excel_introspect_all_workbooks.py 所在的文件夹,然后运行命令`python3 12excel_introspect_all_workbooks.py myFilePath`,那么我只会得到一个输出,就是 `Number of Excel workbooks:0`,但如果我不 cd 到对应文件夹,而是直接在终端下运行 `python3 12excel_introspect_all_workbooks.py myFilePath`,那么我就会得到我想要的输出;

其二是如果我的文件夹中有 .xlsx 文件,那么原书的匹配就会出错,因为在代码的第 7 行,原书的代码是 `for input_file in glob.glob(os.path.join(input_directory, '*.xls*')):`,比我的代码最后多了一个 * 星号,这样会直接匹配到 .xlsx 的文件,但 xlrd 这个库在面对 .xlsx 文件时,你懂的...

正在看这篇文章的你,不妨试试看,是否会出现我遇到的错误.

## 3.5.2 从多个工作簿中连接数据

接下来要展示从多个工作簿中的多个工作表读取数据,并将这些数据垂直连接成一个输出文件.如果您还有印象,我们在第 2 章也学过类似的内容,只不过那时是 csv 文件,现在换成了 xls 文件.

### 1. 基础 Python

文件名称:[13excel_concat_data_from_multiple_workbook.py](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/13excel_concat_data_from_multiple_workbook.py)

所需文件:[sales_data](https://github.com/wyqdgggfk/Python-Data-Analyze/tree/master/第%203%20章所需资料/sales_data)

输出文件:[13output.xls](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/13output.xls)

```python
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
for input_file in glob.glob(os.path.join(input_folder, '*.xls*')): 
	print(os.path.basename(input_file)) # 原书此处 print 没有加括号
	with open_workbook(input_file) as workbook: # 开始打开具体工作簿
		for worksheet in workbook.sheets(): # 打开工作簿中的工作表
			if first_worksheet:
				header_row = worksheet.row_values(0)
				data.append(header_row)
				first_worksheet = False
			for row_index in range(1,worksheet.nrows):
				row_list = []
				for column_index in range(worksheet.ncols):
					cell_value = worksheet.cell_value(row_index,column_index)
					cell_type = worksheet.cell_type(row_index,column_index)
					if cell_type == 3:
						date_cell = xldate_as_tuple(cell_value, workbook.datemode)
						date_cell = date(*date_cell[0:3]).strftime('%m/%d/%Y')
						row_list.append(date_cell)
					else:
						row_list.append(cell_value)
				data.append(row_list)
for list_index,output_list in enumerate(data):
	for element_index,element in enumerate(output_list):
		output_worksheet.write(list_index,element_index,element)
output_workbook.save(output_file)		
```

这个文件的运行逻辑也不复杂,和第 2 章的第 2.6 小节很相似,但看完上面的代码,不知道大家有没有想过这样一个问题,如果我得到的 100 个工作簿中,有 20 个工作簿,里面的工作表,每个都包含不同的参数,那上面的代码还管用么?答案是否定的,基于篇幅限制,此处不过多修改,如果有兴趣了解,可以关注我的公众号,私信给我.

![匠人案牍](https://tva1.sinaimg.cn/large/0082zybpgy1gbvv8r5jf9j3076076t96.jpg)

### 2. Pandas

借用原书的说明:

> pandas 提供了 concat 函数来连接数据框.如果你想把数据框一个一个地垂直堆叠起来,那么就要设置参数 axis=0.如果你想把数据框一个一个地平行连接起来,那么就要设置参数 axis=1.此外,如果你需要基于某个关键字列连接数据框,pandas 中的 merge 函数可以提供类似 SQL join 的操作.

文件名称:[pandas_concat_data_from_multiple_workbooks.py](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/pandas_concat_data_from_multiple_workbooks.py)

所需文件:[sales_data](https://github.com/wyqdgggfk/Python-Data-Analyze/tree/master/第%203%20章所需资料/sales_data)

输出文件:[13otuput_pandas.xls](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/13otuput_pandas.xls)

```python
import pandas as pd
import glob
import os
import sys
input_path = sys.argv[1]
output_file = sys.argv[2]
all_workbooks = glob.glob(os.path.join(input_path,'*.xls*'))
data_frames = []
for workbook in all_workbooks:
	all_worksheets = pd.read_excel(workbook,sheet_name = None,index_col=None)
	for worksheet_name,data in all_worksheets.items():
		data_frames.append(data)
all_data_concatenated = pd.concat(data_frames,axis=0,ignore_index=True)
writer = pd.ExcelWriter(output_file)
all_data_concatenated.to_excel(writer,sheet_name='all_data_all_workbooks',index=False)
writer.save()
```

## 3.5.3 为每个工作簿和工作表计算总数和均值

### 1.基础 Python

文件名称:14excel_sum_average_multiple_workbook.py

所需文件:

输出文件:

```python

```



































