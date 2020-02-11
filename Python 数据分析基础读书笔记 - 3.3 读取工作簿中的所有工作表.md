# 3.3 读取工作簿中的所有工作表

其实有了之前的铺垫,下面的内容并不会太难,只是在一个工作表的基础上增加到多个工作表,但道理都是相通的,简单来讲,就是在原有基础上,加入一个列表或循环遍历整个工作簿.

至于读取工作簿中所有工作表的作用,已经不言而喻了,我们很多时候需要整合数据,筛选满足条件的数据,下面来看看具体的实例.

## 3.3.1 在所有工作表中筛选特定行

这里筛选的就是满足特定条件的行,比如销售额大于某个值的行,学生总分大于某个分数的行,只是需要在整个工作簿中进行筛选,会涉及到多个工作表,比如一月的销售数据是一个工作表,二月的销售数据是另一个工作表.

###  1.基础 Python 在所有工作表中筛选特定行

在所有工作表中筛选出销售额大于 $2000.0 的所有行.

文件名称:[9excel_value_meets_condition_all_worksheets.py](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/9excel_value_meets_condition_all_worksheets.py)

所需文件:[sales_2013.xlsx](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/sales_2013.xlsx)

输出文件:[9output.xls](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/9output.xls)

```python
import sys
from datetime import date
from xlrd import open_workbook,xldate_as_tuple
from xlwt import Workbook
input_file = sys.argv[1]
output_file = sys.argv[2]	
output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('filetered_rows_all_worksheets')
sales_column_index = 3
threshold = 2000.0
first_worksheet = True # 用一个 tag 判断处理的是否第一个工作表
with open_workbook(input_file) as workbook:
	data = []
	for worksheet in workbook.sheets():
		"""如果此处是第一个工作表,则需要保留其表头作为标题列"""
		if first_worksheet:
			header_row = worksheet.row_values(0)
			data.append(header_row)
			first_worksheet = False # 表头保留完成,将 first_worksheet 设置为 False
		for row_index in range(1,worksheet.nrows):
			row_list = []
			sale_amount = worksheet.cell_value(row_index,sales_column_index)
			if sale_amount > threshold:
				for column_index in range(worksheet.ncols):
					cell_value = worksheet.cell_value(row_index,column_index)
					cell_type = worksheet.cell_type(row_index,column_index)
					
					"""如果表格中的数据是日期,需要对其进行格式转换"""
					if cell_type == 3:
						date_cell = xldate_as_tuple(cell_value, workbook.datemode)
						date_cell = date(*date_cell[0:3]).strftime('%m/%d/%Y')
						row_list.append(date_cell)
					else:
						row_list.append(cell_value)
			
			if row_list:
				data.append(row_list)
	for list_index,output_list in enumerate(data):
		for element_index,element in enumerate(output_list):
			output_worksheet.write(list_index,element_index,element)
output_workbook.save(output_file)
```

### 2.Pandas 在所有工作表中筛选特定行

借用原书中的话进行说明:

> 在 Pandas 中,通过在 read_excel 函数中设置 `sheetname=None`,可以一次性读取工作簿中的所有工作表.Pandas 将这些工作表读入一个数据框字典,字典中的键就是工作表的名称,值就是包含工作表中数据的数据框.

需要声明一下,在写这篇笔记时,已经不再是 `sheetname=None`,而是`sheet_name=None`,多了一个下划线.

文件名称:[pandas_value_meets_condition_all_worksheets.py](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/pandas_value_meets_condition_all_worksheets.py)

所需文件:[sales_2013.xlsx](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/sales_2013.xlsx)

输出文件:[9output_pandas.xls](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/9output_pandas.xls)

```python
import pandas as pd
import sys
input_file = sys.argv[1]
output_file = sys.argv[2]
data_frame = pd.read_excel(input_file,sheet_name=None,index_col=None) # 原书中是 sheetname,无法运行的,要加下划线
row_output=[]
for worksheet_name,data in data_frame.items():
	row_output.append(data[data['Sale Amount'].astype(float) > 2000.0])
filtered_rows = pd.concat(row_output,axis=0,ignore_index=True)
writer = pd.ExcelWriter(output_file)
filtered_rows.to_excel(writer,sheet_name='sale_amount_gt2000',index=False)
writer.save()
```

## 3.3.2 在所有工作表中选取特定列

此处的应用场景与 3.3.1 类似,只不过一个是选取特定行,一个是选取特定列.下面的代码将会演示如何在所有工作表中选取 Customer Name 和 Sale Amount 列.

### 1.基础 Python

文件名称:[10excel_column_by_name_all_worksheet.py](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/10excel_column_by_name_all_worksheet.py)

所需文件:[sales_2013.xlsx](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/sales_2013.xlsx)

输出文件:[10output.xls](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/10output.xls)

```python
import sys
from datetime import date 
from xlrd import open_workbook,xldate_as_tuple
from xlwt import Workbook
input_file = sys.argv[1]
output_file = sys.argv[2]
output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('selected_columns_all_worksheets')
my_columns = ['Customer Name','Sale Amount']
first_worksheet = True
with open_workbook(input_file) as workbook:
	data = [my_columns]
	index_of_cols_to_keep = []
	for worksheet in workbook.sheets():
		if first_worksheet:
			header = worksheet.row_values(0)
			for column_index in range(len(header)):
				if header[column_index] in my_columns:
					index_of_cols_to_keep.append(column_index)
			first_worksheet = False
		for row_index in range(1,worksheet.nrows):
			row_list = []
			for column_index in index_of_cols_to_keep:
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

### 2.Pandas

文件名称:[pandas_column_by_name_all_worksheets.py](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/pandas_column_by_name_all_worksheets.py)

所需文件:[sales_2013.xlsx](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/sales_2013.xlsx)

输出文件:[10output_pandas.xls](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/10output_pandas.xls)

```python
import pandas as pd
import sys
input_file = sys.argv[1]
output_file = sys.argv[2]
data_frame = pd.read_excel(input_file,sheet_name=None,index_col=None) # 原书中此处是 sheetname 不是 sheet_name
column_output = []
for worksheet_name,data in data_frame.items():
	column_output.append(data.loc[:,['Customer Name','Sale Amount']])
selected_columns = pd.concat(column_output,axis=0,ignore_index=True)
writer = pd.ExcelWriter(output_file)
selected_columns.to_excel(writer,sheet_name='selected_columns_all_worksheets',index=False)
writer.save()
```

