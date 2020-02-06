## 3.2 处理单个工作表

我们首先需要做的，是处理单个 Excel 工作表，然后推广至整个工作簿。

### 3.2.1 读写 Excel 文件

#### 基础 Python 和 xlrd、xlwt 模块

如果用基础的 Python 和 xlrd、xlwt 模块来读写一个 Excel 文件，可以参考 [2excel_parsing_and_write.py](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/2excel_parsing_and_write.py) 这个代码：

```python
import sys
from xlrd import open_workbook
from xlwt import Workbook
input_file = sys.argv[1] # 此处为 sales_2013.xlsx
output_file = sys.argv[2] # 此处为 2output.xls
output_workbook = Workbook() # 初始化一个 output_workbook 对象
output_worksheet = output_workbook.add_sheet('jan_2013_output') # 给 output_workbook 加入一个 sheet，取名 jan_2013_output
with open_workbook(input_file) as workbook:
	worksheet = workbook.sheet_by_name('january_2013')
	"""按照行列将原工作表 sales_2013.xlsx 中的每个数据输入到新工作表 2output.xls 中"""
	for row_index in range(worksheet.nrows):
		for column_index in range(worksheet.ncols):
			output_worksheet.write(row_index,column_index,worksheet.cell_value(row_index,column_index))
output_workbook.save(output_file)
```

需要注意，xls 与 xlsx 是有区别的，xlrd 和 xlwt 这两个库对 xls 文件的操作没有问题，但如果您需要对 xlsx 文件进行更好的读写，推荐您看看我的[另一篇文章](https://www.jianshu.com/p/5c1ac33b355f)，另外，如果您自己通过上面的代码运行一次后，可能会发现，Purchase Date 那一列的数据并不是**日期**，而是**数值**，这和 Excel 的工作方式有关，具体原因可以自行查阅，下面主要讲一下如何把数值转换为日期。

首先还是看一下书上的原代码，稍后我会进行一些解释：

```python
import sys
from datetime import date
from xlrd import open_workbook,xldate_as_tuple
from xlwt import Workbook
input_file = sys.argv[1] # 此处为 sales_2013.xlsx
output_file = sys.argv[2] # 此处为 3output.xls
output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('jan_2013_output')
with open_workbook(input_file) as workbook:
	worksheet = workbook.sheet_by_name('january_2013')
	for row_index in range(worksheet.nrows):
		row_list_output = [] # 实际上这个 row_list_output 根本不影响输出文件
		for col_index in range(worksheet.ncols):
			"""如果这个单元格是时间"""
			if worksheet.cell_type(row_index, col_index) == 3: # 可查看 xlrd 的文档，检验单元格类型是否为数字 3，类型为 3 表示包含日期数据
				date_cell = xldate_as_tuple(worksheet.cell_value(row_index, col_index), workbook.datemode) # 参数 workbook.datemode 是必需的，可以确定日期是基于 1900 年还是 1904 年
				date_cell = date(*date_cell[0:3]).strftime('%m/%d/%Y')
				row_list_output.append(date_cell) # 实际上这个 row_list_output 根本不影响输出文件
				output_worksheet.write(row_index,col_index,date_cell)
			"""如果这个单元格不是时间"""
			else:
				non_date_cell = worksheet.cell_value(row_index, col_index)
				row_list_output.append(non_date_cell) # 实际上这个 row_list_output 根本不影响输出文件
				output_worksheet.write(row_index,col_index,non_date_cell)
output_workbook.save(output_file)
```

相对来说上面的这段代码比较简单，主要是理解它的运行逻辑，我在必要的地方加入了备注。

### Pandas 读写 Excel 文件

对比一下用 xlrd 和 xlwt 来处理 Excel，你可能会觉得 Pandas 代码量很少，下面是书中 [pandas_read_and_write_excel.py](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/pandas_read_and_write_excel.py) 的代码：

```python
import pandas as pd
import sys
input_file = sys.argv[1]
output_file = sys.argv[2]
data_frame = pd.read_excel(input_file,sheetname='january_2013')
writer = pd.ExcelWriter(output_file)
data_frame.to_excel(writer,sheet_name='jan_13_output',index=False)
writer.save()
```

如果您运行一遍这段代码,或者您本身对 Pandas 比较了解,应该会发现代码中有一处错误会导致无法运行,下面是修改过后的代码,试试看能不能找出哪里有问题:

```python
import pandas as pd
import sys
input_file = sys.argv[1]
output_file = sys.argv[2]
data_frame = pd.read_excel(input_file,sheet_name='january_2013')
writer = pd.ExcelWriter(output_file)
data_frame.to_excel(writer,sheet_name='jan_13_output',index=False)
writer.save()
```

如果打开 [pandas_output.xls](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/pandas_output.xls) 这个文件,我们会发现 purchase date 也是正确的,并不是以数字方式显示.

### 3.2.2 筛选特定行

接下来我们将讨论如何按照以下方式筛选行:

1. 行中的值满足特定条件;
2. 行中的值属于某个集合;
3. 行中的值匹配于特定的正则表达式.

不知道各位看官在读这些技术类书籍的时候是否曾有过这样的一些疑问:

1. 这个技能我知道了,然后呢,它有什么作用?
2. 这个算法我了解了,那么能干什么呢?

稍后所有章节中的代码,我都会尽可能帮大家举一些实际应用的例子,方便理论结合实际.接下来就看具体的代码了.

#### 1.行中的值满足某个条件

此功能主要用于查找,比如我们想从上万条销售数据里面找到某个业务员的销售数据,再比如找到销售额大于某个值的数据,进阶一点,找到某个销售员在某个时间范围内销售额大于某个值的全部数据,接下来请看代码演示.

##### 基础 Python 处理筛选选中满足某个条件的值

文件名称:[4excel_value_meets_condition.py](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/4excel_value_meets_condition.py)

所需文件:[sales_2013.xlsx](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/sales_2013.xlsx)

输出文件:[4output.xls](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/4output.xls)

```python
import sys
from datetime import date
from xlrd import open_workbook,xldate_as_tuple
from xlwt import Workbook
input_file = sys.argv[1] # 此处为 sales_2013.xlsx
output_file = sys.argv[2] # 此处为 4output.xls
output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('jan_2013_output')
sale_amount_column_index = 3
with open_workbook(input_file) as workbook:
	worksheet = workbook.sheet_by_name('january_2013')
	data = []
	header = worksheet.row_values(0) # 获取标题行
	data.append(header)
	for row_index in range(1,worksheet.nrows):
		row_list = []
		sale_amount = worksheet.cell_value(row_index, sale_amount_column_index)
		if sale_amount > 1400.0:
			for column_index in range(worksheet.ncols):
				cell_value = worksheet.cell_value(row_index, column_index)
				cell_type = worksheet.cell_type(row_index,column_index)
				if cell_type == 3:
					date_cell = xldate_as_tuple(cell_value, workbook.datemode)
					date_cell = date(*date_cell[0:3]).strftime('%m/%d/%Y')
					row_list.append(date_cell)
				else:
					row_list.append(cell_value)
		if row_list:
			data.append(row_list)
"""list_index 为行,element_index 为列"""
	for list_index,output_list in enumerate(data):
		for element_index,element in enumerate(output_list):
			output_worksheet.write(list_index,element_index,element)
output_workbook.save(output_file)
```

##### Pandas 处理筛选行中满足某个条件的值

文件名称:[pandas_value_meets_condition.py](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/pandas_value_meets_condition.py)

所需文件:[sales_2013.xlsx](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/sales_2013.xlsx)

输出文件:[pandas_value_meets_condition_output.xls](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/pandas_value_meets_condition_output.xls)

```python
import pandas as pd
import sys
input_file = sys.argv[1] # 此处为 sales_2013.xlsx
output_file = sys.argv[2] # 此处为 pandas_value_meets_condition_output.xls
data_frame = pd.read_excel(input_file,'january_2013',index_col=None)
data_frame_value_meets_condition = data_frame[data_frame['Sale Amount'].astype(float) > 1400.0]
writer = pd.ExcelWriter(output_file)
data_frame_value_meets_condition.to_excel(writer,sheet_name='jan_13_output',index=False)
writer.save()
```

在原书中有这样一句话:

> 如果你需要设定多个条件,那么可以将这些条件放在圆括号中,根据需要的逻辑顺序用"&"或"|"连接起来.

然而很多抱歉,我并没有看到哪个地方适合这样做.

























