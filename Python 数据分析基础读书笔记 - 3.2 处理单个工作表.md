## 3.2 处理单个工作表

我们首先需要做的，是处理单个 Excel 工作表，然后推广至整个工作簿。

### 3.2.1 读写 Excel 文件

#### 基础 Python 和 xlrd、xlwt 模块

如果用基础的 Python 和 xlrd、xlwt 模块来读写一个 Excel 文件，可以参考 2excel_parsing_and_write.py 这个代码：

```python
import sys
from xlrd import open_workbook
from xlwt import Workbook
input_file = sys.argv[1]
output_file = sys.argv[2]
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

需要注意，xls 与 xlsx 是有区别的，xlrd 和 xlwt 这两个库对 xls 文件的操作没有问题，但如果您需要对 xlsx 文件进行更好的读写，推荐您看看我的[另一篇文章](https://www.jianshu.com/p/5c1ac33b355f)，另外，如果您自己通过上面的代码运行一次后，可能会发现，Purchase Date 那一列的数据并不是**日期**，而是**数值**，这和 Excel 的工作方式有关，具体原因可以自行查阅，下面主要讲一下如何把数值转换为日期，