# 3.4 在 Excel 工作簿中读取一组工作表

借用书中的原文来讲一下这个功能的用途:

> 有些情况下,你只需要处理工作簿中的一组工作表.例如,你的工作簿可能包含很多工作表,但是你只需要处理其中的 20 个.在这种情况下,可以使用工作簿的 sheet_by_index 或 sheet_by_name 函数来处理一组工作表.

## 在一组工作表中筛选特定行

此示例中,我们将从第一个和第二个工作表筛选出销售额大于 $1900.00 的那些行.

### 1.基础 Python

文件名称:[11excel_value_meets_condition_set_of_worksheets.py](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/11excel_value_meets_condition_set_of_worksheets.py)

所需文件:[sales_2013.xlsx](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/sales_2013.xlsx)

输出文件:[11output.xls](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/11output.xls)

```python
import sys
from datetime import date 
from xlrd import open_workbook,xldate_as_tuple
from xlwt import Workbook
input_file = sys.argv[1]
output_file = sys.argv[2]
output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('set_of_worksheets')
my_sheets = [0,1] # 表示要处理的工作表的索引值
threshold = 1900.0
sales_column_index = 3
first_worksheet = True
with open_workbook(input_file) as workbook:
	data = []
	for sheet_index in range(workbook.nsheets):
		if sheet_index in my_sheets:
			worksheet = workbook.sheet_by_index(sheet_index)
			if first_worksheet:
				header_row = worksheet.row_values(0)
				data.append(header_row)
				first_worksheet = False
			for row_index in range(1,worksheet.nrows):
				row_list = []
				sales_amount = worksheet.cell_value(row_index, sales_column_index)
				if sales_amount > threshold:
					for column_index in range(worksheet.ncols):
						cell_value = worksheet.cell_value(row_index, column_index)
						cell_type = worksheet.cell_type(row_index, column_index)
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

如果您一直从第 2 章看到现在,应该可以发现规律了,又是打开表格,按行列进行读取,满足要求的取出,不满足要求的就进入到下一行列查找,这样的思路贯穿了这本书.接下来看看用 Pandas 怎么处理.

### 2.Pandas







































