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

然而很抱歉,我并没有看到哪个地方适合这样做.

#### 2.行中的值属于某个集合

这个功能也与查找相关,而且和上一个功能很类似,但比较上一个功能而言,此功能查找的通常是多个独立的条件,比如某几个日期相关的数据,或者某些人的数据,可参考这个伪代码:

```python
condition_set = ['name_one','name_two']
for column_index in range(worksheet.ncols):
  if cell_value in condition_set:
    do something
  else:
    do other thing
```

下面请看具体的代码演示:

##### 基础 Python 查找行中属于某个集合的值

文件名称:[5excel_value_in_set.py](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/5excel_value_in_set.py)

所需文件:[sales_2013.xlsx](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/sales_2013.xlsx)

输出文件:[5output.xls](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/5output.xls)

```python
import sys
from datetime import date
from xlrd import open_workbook,xldate_as_tuple
from xlwt import Workbook
input_file = sys.argv[1] # 此处为 sales_2013.xlsx
output_file = sys.argv[2] # 此处为 5output.xls
output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('jan_2013_output')
important_dates = ['01/24/2013','01/31/2013']
purchase_date_column_index = 4
with open_workbook(input_file) as workbook:
	worksheet = workbook.sheet_by_name('january_2013')
	data = []
	header = worksheet.row_values(0)
	data.append(header)
	for row_index in range(1,worksheet.nrows):
		purchase_datetime = xldate_as_tuple(worksheet.cell_value(row_index, purchase_date_column_index), workbook.datemode)
		purchase_date = date(*purchase_datetime[0:3]).strftime('%m/%d/%Y')
		row_list = []
		if purchase_date in important_dates:
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

这段演示代码与上一功能的演示代码非常类似,大致逻辑都是打开文件,按条件找到符合的数据,然后写入到新文件.

##### Pandas 查找行中属于某个集合的值

文件名称:[pandas_value_in_set.py](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/pandas_value_in_set.py)

所需文件:[sales_2013.xlsx](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/sales_2013.xlsx)

输出文件:[pandas_5output.xls](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/pandas_5output.xls)

```python
import pandas as pd
import sys
input_file = sys.argv[1]
output_file = sys.argv[2]
data_frame = pd.read_excel(input_file,'january_2013',index_col=None)
important_dates = ['01/24/2013','01/31/2013']
data_frame_value_in_set = data_frame[data_frame['Purchase Date'].isin(important_dates)]
writer = pd.ExcelWriter(output_file)
data_frame_value_in_set.to_excel(writer,sheet_name='jan_13_output',index=False)
writer.save()
```

#### 3.行中的值匹配于特定模式

原书中对于这个功能有一个应用举例:

> 要使用基础 Python 筛选出客户姓名包含一个特定模式(例如:以大写字母 J 开头)的行.

简单来说,如果落脚到中国的情况,那就有可能是：

1. 筛选所有姓李的学生;
2. 在以 xxxx-xx-xx 格式时间单位的表格中，筛选所有 2013 年的数据;
3. 对于一份某地注册公司的名单,筛选公司名字包含"集团"的个数.

进一步的,我们可以根据上面的筛选执行统计总数,计算平均数,或依据具体需要计算其它数据.下面让我们看看书中匹配字符串开头是大写 **J** 的名字,具体的代码示例如下:

##### 基础 Python查找行中匹配特定模式的值

文件名称:[6excel_value_matches_pattern.py](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/6excel_value_matches_pattern.py)

所需文件:[sales_2013.xlsx](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/sales_2013.xlsx)

输出文件:[6output.xls](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/6output.xls)

```python
import re
import sys
from datetime import date
from xlrd import open_workbook,xldate_as_tuple
from xlwt import Workbook
input_file = sys.argv[1] # 此处为 sales_2013.xlsx
output_file = sys.argv[2] # 此处为 6output.xls
output_workbook = Workbook()
output_worksheet = output_workbook.add_sheet('jan_2013_output')
pattern = re.compile(r'(?P<my_pattern>^J.*)') # 这段文字中 ^J.* 是最重要的,意为从开头进行匹配,J后面可跟任意多个字符
customer_name_column_index = 1
"""
以下代码的逻辑与之前很类似,一样是打开文件,逐个单元格查看,如果满足要求,就将此行数据提出
"""
with open_workbook(input_file) as workbook:
	worksheet = workbook.sheet_by_name('january_2013')
	data = []
	header = worksheet.row_values(0)
	data.append(header)
	for row_index in range(1,worksheet.nrows):
		row_list = []
		if pattern.search(worksheet.cell_value(row_index, customer_name_column_index)):
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

##### Pandas 查找行中匹配特定模式的值

相较于基础 Python 的匹配特定模式,Pandas 提供了若干字符串和正则表达式函数,包括 startwith,endswith,match 和 search,可以直接使用这些函数在文本中识别子字符串和模式.具体如何做,请看以下示例代码:

文件名称:[pandas_value_matches_pattern.py](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/pandas_value_matches_pattern.py)

所需文件:[sales_2013.xlsx](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/sales_2013.xlsx)

输出文件:[pandas_value_matches_pattern_output](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/pandas_value_matches_pattern_output.xls)

```python
import pandas as pd
import sys
input_file = sys.argv[1] # 此处为 sales_2013.xlsx
output_file = sys.argv[2] # 此处为 pandas_value_matches_pattern_output
data_frame = pd.read_excel(input_file,'january_2013',index_col=None)
data_frame_value_matchs_pattern = data_frame[data_frame['Customer Name'].str.startswith("J")]
writer = pd.ExcelWriter(output_file)
data_frame_value_matchs_pattern.to_excel(writer,sheet_name='jan_13_output',index=False)
writer.save()
```

对比一下,使用基础 Python 需要 37 行代码的任务,用 Pandas 仅 9 行即可实现,在实际运用中,可见 Pandas 的重要性和必要性.

### 3.2.3 选取特定列

顾名思义,选取特定列就是在文件中只选择需要的列,但此功能建议慎用,因为在实际的工作中,当我们拿到一个数据表格时,并不一定每个必需的单元格里面都有我们期待的数据,比如金额可能写成 50,也可能写成 $50,对于中国的发票,也可能写成伍拾,还可能没有数据,我们到底是要哪些列数据,需要慎重考虑.

那么这个功能可以干什么,我能帮各位想到的是瘦身,如果一个财务报表大小为 1 GB,里面有地区列,时间列,团队列,人员列,经销商列,仓库列,快递列,运费列,备注列等等各种信息一应俱全,可是我们分析的时间只要商品名称和商品价格这两列,那就可以直接选取这两列新建一个表格,方便后续的处理.

书中提到有两种通用方法可以在 Excel 文件中选取特定的列,一种是使用列索引值,第二种是使用列标题.

### 1.列索引值

借用原书的话进行一下说明:

>从工作表中选取特定列的一种方法是使用要保留的列的索引值.当你想保留的列的索引值非常容易识别,或者在处理多个输入文件过程中,各个输入文件中列的位置是一致(也就是不会发生改变)的时候,这种方法非常有效.

什么意思呢?就是说如果现在有 50 份 Excel 表格,每人表格打开后,其排列形式都是一样的或者基本一样的(比如前 N 列都一样,只有少数不一样),就可以用列索引这种方式来查找需要的值.请看下面用基础 Python 和 Pandas 的代码演示.

#### 基础 Python 通过列索引值选取特定列

文件名称:[7excel_column_by_index.py](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/7excel_column_by_index.py)

所需文件:[sales_2013.xlsx](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/sales_2013.xlsx)

输出文件:[7output.xls](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/7output.xls)

```python
import sys
from datetime import date
from xlrd import open_workbook,xldate_as_tuple
from xlwt import Workbook
input_file = sys.argv[1] # 此处为 sales_2013.xlsx
output_file = sys.argv[2] # 此处为 7output.xls
output_workbook	= Workbook()
output_worksheet = output_workbook.add_sheet('jan_2013_output')
my_columns = [1,4]
with open_workbook(input_file) as workbook:
	worksheet = workbook.sheet_by_name('january_2013')
	data = []
	for row_index in range(worksheet.nrows):
		row_list = []
		for column_index in my_columns:
			cell_value = worksheet.cell_value(row_index, column_index)
			cell_type = worksheet.cell_type(row_index, column_index)
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

#### Pandas 通过列索引值选取特定列

文件名称:[pandas_column_by_index.py](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/pandas_column_by_index.py)

所需文件:[sales_2013.xlsx](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/sales_2013.xlsx)

输出文件:[pandas_column_by_index_output.xls](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/pandas_column_by_index_output.xls)

```python
import pandas as pd
import sys
input_file = sys.argv[1] # 此处为 sales_2013.xlsx
output_file = sys.argv[2] # 此处为 pandas_column_by_index_output.xls
data_frame = pd.read_excel(input_file,'january_2013',index_col=None)
data_frame_column_by_index = data_frame.iloc[:,[1,4]]
writer = pd.ExcelWriter(output_file)
data_frame_column_by_index.to_excel(writer,sheet_name='jan_13_output',index=False)
writer.save()
```

### 2.列标题















































































































































































































































