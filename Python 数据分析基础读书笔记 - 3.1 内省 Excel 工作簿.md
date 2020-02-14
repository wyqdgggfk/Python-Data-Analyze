# 第 3 章 Excel 文件

Python 自带了 csv 文件的处理库，但是没有自带 Excel 文件的处理库，要完成本章的学习，需要自行下载 xlrd 和 xlwt，书中提到如果读者已经安装了 Anaconda Python，那么就有了这两个扩展包，当然如果没有，也不是什么难事，两个 pip3 命令就可以搞定的事情，我在这里不浪费笔墨了。

书中提到要开始本章内容的学习，需要先创建一个 Excel 工作簿，包含三个工作表，即 january_2013、february_2013 和 march_2013，并分别在里面添加数据，然后命名为 sales_2013.xlsx，好在我已经将这个 excel 文件下载下来，并放在[链接](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/sales_2013.xlsx)中，各位看官可以直接打开进行学习。

## 3.1 内省 Excel 工作簿

当我们拿到一个 Excel 工作簿时，我们可能知道它的大致内容，比如销售经理拿到的 Excel 文件中，应该会有货物，金额，进价，库存，销售量等等信息，但我们无法知道这个工作簿中包含了多少条数据，如果数据少还好办，直接打开看就可以了，但如果数据比较大，可能我们打开这个 Excel 文件的时间都够喝一杯咖啡了。

书中先是用 [sales_2013.xlsx](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/sales_2013.xlsx) 给了我们一个示例，保存为 [1excel_introspect_workbook.py](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第%203%20章所需资料/1excel_introspect_workbook.py) ，代码如下：

```python
import sys
from xlrd import open_workbook
input_file = sys.argv[1]
workbook = open_workbook(input_file)
print("Number of worksheets:",workbook.nsheets)
for worksheet in workbook.sheets():
	print("Worksheet name:",worksheet.name,"\tRows:",worksheet.nrows,"\tColumns:",worksheet.ncols)
```

实际上这个文件可以说是一个通用代码，如果您的 Excel 文件只有原始数据，没有一些图表之类的特殊数据，那么这个文件应该都是可以打开您的 Excel 文件来查看有多少行列的。

