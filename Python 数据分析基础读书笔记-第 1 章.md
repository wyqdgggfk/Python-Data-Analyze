# 第 2 章 CSV 文件

## 2.1  基础 Python 与 pandas

### 2.1.1 读写 CSV 文件(第 1 部分)

#### 基础 Python，不使用 CSV 模块

如果不使用 python 的 csv 模块，那么如何读写 csv 文件？可参考以下代码：

```python
import sys

input_file = sys.argv[1] #获取输入的文件
output_file = sys.argv[2] #获取输出的文件

with open(input_file,'r',newline='') as filereader:
	with open(output_file,'w',newline='') as filewriter:
		header = filereader.readline()
		header = header.strip()
		header_list = header.split(',')
		print(header_list)
		filewriter.write(','.join(map(str, header_list))+'\n')
		for row in filereader:
			row = row.strip()
			row_list = row.split(',')
			print(row_list)
			filewriter.write(','.join(map(str, row_list))+'\n')
```

对于以上代码中的 `sys.argv[]`，可参考 [覆手为云的介绍](https://www.cnblogs.com/aland-1415/p/6613449.html)，弄明白什么是 argv[] 后，再参考书中 ${P}_{53}-{P}_{54}$ 的操作方法，Mac 上的具体实现步骤如下：

1. 打开终端；
2. cd 命令到本文件所保存的文件路径：`cd /Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料 `;
3. 在终端输入此命令：`python3  1csv_read_with_simple_parsing_and_write.py supplier_data.csv 1output.csv`，其中 `python3` 指的是让终端执行 python3 的命令，而 `1csv_read_with_simple_parsing_and_write.py` 就是要执行的 python 命令，也就是书中的代码，`supplier_data.csv` 是向这个命令提交的第一个参数，也就是代码中指代的 `sys.argv[1]`，同理可得 `1output.csv` 是向代码提交的第二个参数，即 `sys.argv[2]`
4. 最后呈上终端运行时的 gif 图：![image](https://github.com/wyqdgggfk/Python-/blob/master/第2章所需资料/chapter2readwriteCSVviaTerminal.gif)

利用 Pandas 也可以处理 CSV 文件，具体参考如下代码：

```python
import sys
import pandas as pd

input_file = sys.argv[1]
output_file = sys.argv[2]

data_frame = pd.read_csv(input_file)
print(data_frame)
data_frame.to_csv(output_file,index=False)
```

在实际运行时，我的终端总是提示我找不到 pandas_，发现是无法正确找到 pandas 这个库，所以我稍微修改了一下源代码，如下：

```python
import sys
import pandas as pd
input_file = '/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/supplier_data.csv'
output_file = '/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/1output.csv'
data_frame = pd.read_csv(input_file)
print(data_frame)
data_frame.to_csv(output_file,index=False)
```

请注意，以上代码的 input_file 和 output_file 要置换为你自己电脑上相应文件的路径，否则无法运行。

再来看看上面的代码在 CodeRunner 中的运行结果：

![image](https://github.com/wyqdgggfk/Python-/blob/master/第2章所需资料/pandas_parsing_and_write.gif)

### 2.1.2  基本字符串分析是如何失败的

对于 1csv_read_with_simple_parsing_and_write.py 中的代码，要考虑一种情况，就是如果数据中有逗号怎么办，代码是以逗号分隔每行数据中的每个数据，如果数据本身有逗号，就会形成干扰。

### 2.1.3 读写 CSV 文件(第 2 部分)

#### 基础 Python，使用 CSV 模块

使用 CSV 模块的一个好处就是：不需要仅仅为了正确处理数据而花费时间来设计正则表达式和条件逻辑。

将 supplier_data.csv 中 cost 一列的最下方两个数据更改为 6,015.00 和 1,006,015.00，然后新建一个 .py 文件，命名为 2csv_reader_parsing_and_write.py，存储在对应的文件夹下，代码如下：

```python
import csv
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file,'r',newline='') as csv_in_file:
	with open(output_file,'w',newline='') as csv_out_file:
		filereader = csv.reader(csv_in_file,delimiter=',')
		filewriter = csv.writer(csv_out_file,delimiter=',')
		for row_list in filereader:
			print(row_list)
			filewriter.writerow(row_list)
```

运行结果如下：

![image](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第2章所需资料/2csv_reader_parsing_and_write.png)

## 2.2 筛选特定的行

**注意以下伪代码的结构**：

```python
for row in filereader:
  ***if value in row meets some business rule or set of rules:***
    		do something
	else:
  		do something else      
```

### 2.2.1 行中的值满足某个条件

#### 基础 Python

以下代码可检验行值是否满足两个具体条件，并将满足条件的行的子集写入一个输出文件：

```python
import csv
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

with open(input_file,'r',newline='') as csv_in_file:
	with open(output_file,'w',newline='') as csv_out_file:
		filereader = csv.reader(csv_in_file)
		filewriter = csv.writer(csv_out_file)
		header = next(filereader) #使用 csv 模块的 next 函数读出输入文件的第一行，赋名 header 列表
		filewriter.writerow(header)
		for row_list in filereader: #按行读取数据
			supplier  = str(row_list[0]).strip()
			cost = str(row_list[3]).strip('$').replace(',','')
			if supplier == 'Supplier Z' or float(cost) > 600.0:
				filewriter.writerow(row_list)
```

有了上述的代码，我们可以稍微修改一下，在 Kaggle 官网上找到 YouTube 的一些[视频观看数据](https://www.kaggle.com/datasnaek/youtube-new)来进行简单的筛选，我已经将要读取的名为 [YouTubeReadFile.csv](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第2章所需资料/YouTubeReadFile.csv) 的文件放在仓库中，具体代码如下：

```python
import csv
import sys

input_file = sys.argv[1] #要读取的 csv 文件名为 YouTubeReadFile.csv
output_file = sys.argv[2] #要写入的 csv 文件名为 YouTubeWriteFile.csv

with open(input_file,'r',newline='') as csv_in_file:
	with open(output_file,'w',newline='') as csv_out_file:
		filereader = csv.reader(csv_in_file)
		filewriter = csv.writer(csv_out_file)
		header = next(filereader)
		filewriter.writerow(header)
		for row_list in filereader:
			views = int(str(row_list[7]).strip()) # 观看人数
			likes = int(str(row_list[8]).strip()) # 点赞人数
			if views >= 1147000 and likes >= 39000: # 筛选观看人数和点赞人数均大于平均数的数据，共 5994 个
				filewriter.writerow(row_list)
```

#### 利用 pandas 选择符合特定条件值的行

loc 函数：pandas 提供的可以同时选择特定行与列的函数。在逗号前面设定行筛选条件，在逗号后面设定列筛选条件。

如果我想在 supplier_data.csv 中筛选供应商名称包含字母'Z'，或者 cost 大于 600.0 的数据应该如何做呢？且看具体示例代码 pandas_value_meets_condition.py：

```python
import pandas as pd
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

data_frame = pd.read_csv(input_file) #读取输入的表格
data_frame['Cost'] = data_frame['Cost'].str.strip('$') # 试试看，如果某个 Cost 的值有逗号会怎样，比如 6,015.00
data_frame['Cost'] = data_frame['Cost'].str.replace(',','').astype(float)

data_frame_value_meets_condition = data_frame.loc[(data_frame['Supplier Name'].str.contains('Z'))|(data_frame['Cost']>600.0),:]
data_frame_value_meets_condition.to_csv(output_file,index=False)
```

原书的代码与本代码有些不一样，原书没有考虑到 Cost 数值中有逗号的情形，这在转换为 float 时会报错。

同样参考以上代码，如果我想筛选出 YouTubeFile.csv 中 views 大于 114700，likes 大于 39000 且 comment_count 大于 5043 的电视节目，应该怎样做呢？可以参考下面的这段代码：

```python
import sys
import pandas as pd

input_file = sys.argv[1]
output_file = sys.argv[2]

data_frame = pd.read_csv(input_file) #读取输入的 csv 文件，此处为 YouTubeReadFile.csv
data_frame['views'] = data_frame['views'].astype(float)
data_frame['likes'] = data_frame['likes'].astype(float)
data_frame['comment_count'] = data_frame['comment_count'].astype(float)

data_frame_value_meets_condition = data_frame.loc[(data_frame['views']>=1147000)&(data_frame['likes']>=39000)&(data_frame['comment_count']>=5043),:]
data_frame_value_meets_condition.to_csv(output_file,index=False)
```

这里会将 YouTubeReadFile.csv 文件中符合条件的值筛选出来，并存储到 YouTube_pandas_value_meets_condition.py 中。

### 2.2.2 行中的值属于某个集合

如果行中的某个值属于某个范围，也可以筛选出来，比如特定的某几个日期，再比如特定的某几种属性，可参考以下代码：

```python
import csv
import sys

input_file = sys.argv[1] #此处获取的是 supplier_data.csv
output_file = sys.argv[2] #此处输出的是 4output.csv

important_dates = ['1/20/14','1/30/14']

with open(input_file,'r',newline='') as csv_in_file:
	with open(output_file,'w',newline='') as csv_out_file:
		
		filereader = csv.reader(csv_in_file)
		filewriter = csv.writer(csv_out_file)
		header = next(filereader)
		filewriter.writerow(header)
		for row_list in filereader:
			a_date = row_list[4]
			if a_date in important_dates:
				filewriter.writerow(row_list)
```

以上代码是通过 csv 库实现的效果，如果用 pandas 会更加简单，如下所示：

```python
import pandas as pd
import sys
input_file = sys.argv[1]
output_file = sys.argv[2]
data_frame = pd.read_csv(input_file)
important_dates = ['1/20/14','1/30/14']
data_frame_value_in_set = data_frame.loc[data_frame['Purchase Date'].isin(important_dates),:] #isin 这个命令很简单实用
data_frame_value_in_set.to_csv(output_file,index=False)
```

### 2.2.3 行中的值匹配于某个模式/正则表达式

正则表达式一般用于查找某种通用规律的数据，例如：

1. 身份证号开头是 110102 的人，这代表某人的籍贯是北京；
2. 学号第二位到第五位是 2018 的学生，通常这可能意味着他是 20 年入学，而 18 代表学院编号；
3. 在某个城市，车牌尾号的数字是 1，3，5 的汽车在周一，周三，周五限行。

同样的例子还有很多，可以通过给出的数据进行筛选，下面看一段书中用 csv 和 re 两个库实现的代码：

```python
import csv
import re
import sys

input_file = sys.argv[1] #此处为 supplier_data.csv
output_file = sys.argv[2]] #此处为 5csv_reader_value_matches_pattern.csv

pattern = re.compile(r'(?P<my_pattern_group>^001-.*)',re.I)
with open(input_file,'r',newline='') as csv_in_file:
	with open(output_file,'w',newline='') as csv_out_file:
		filereader = csv.reader(csv_in_file)
		filewriter = csv.writer(csv_out_file)
		header = next(filereader)
		filewriter.writerow(header)
		for row_list in filereader:
			invoice_number = row_list[1]
			if pattern.search(invoice_number):
				filewriter.writerow(row_list)
```

如何运行？此处只是补充说明，实际上在之前的笔记中有过讲解，只要在终端用 cd 命令先导航到此 .py 文件的路径下，比如在我的 Mac 上就是

```
cd /Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料
```

然后运行此命令

```
python3 5csv_reader_value_matches_pattern.py supplier_data.csv 5csv_reader_value_matches_pattern.csv
```

即可将 supplier_data.csv 中符合要求的数据写入 5csv_reader_value_matches_pattern.csv 中。

在以上代码中，我们要搜索的是以 “001-”开头的的字符串(注意 001 后面的那一根短横线，也是要匹配的对象)，实心句号代表匹配除了换行符的任意字符，而星号则是匹配多个前面的字符，那么 “*” 连起来的意思就是“匹配除换行符以外的多个字符”，re.I 的意思是进行大小写敏感的匹配，当然在这段代码中并不重要。

同样的功能，如果用 pandas 来实现，代码量会更少，可参考如下：

```python
import pandas as pd
import sys

input_file = sys.argv[1] #此处的文件还是 supplier_data.csv
output_file = sys.argv[2] #此处的文件是 pandas_value_matches_pattern_5output.csv

data_frame = pd.read_csv(input_file)
data_frame_value_matches_pattern = data_frame.loc[data_frame['Invoice Number'].str.startswith("001-"),:]
data_frame_value_matches_pattern.to_csv(output_file,index=False)
```

需要注意的是，我在用 CodeRunner 写 pandas 时，总是不能自动补全，导致一些细节错误无法正常运行代码，不过，这也正好可以练习一下写代码的基本功，毕竟一些常用的功能模块是需要记住的，不能都靠代码补全功能。

## 2.3 选取特定的列

### 2.3.1 列索引值

在 CSV 文件中选取特定的列的一种办法就是使用对应列的索引值，当然，这有一些限定条件，比如：

1. 想保留的列的索引值非常容易识别到；
2. 处理多个输入文件时，各个输入文件中列的位置一致。

对于 supplier_data.csv 文件中，如果我们想只保留供应商名称和成本这两列，我们就可以使用索引值来选取这两列，书中将以下代码保存为 6csv_reader_column_by_index.py：

```python
import csv
import sys
input_file = sys.argv[1] #此处为 supplier_data.csv
output_file = sys.argv[2] #此处为 6output.csv
my_columns = [0,3]
with open(input_file,'r',newline='') as csv_in_file:
	with open(output_file,'w',newline='') as csv_out_file:
		filereader = csv.reader(csv_in_file)
		filewriter = csv.writer(csv_out_file)
		for row_list in filereader:
			row_list_output = []
			for index_value in my_columns:
				row_list_output.append(row_list[index_value])
			filewriter.writerow(row_list_output)
```

完成以上代码后，在资料文件夹中创建一个空白的 6output.csv 文件，然后终端运行如下命令：

1. 先导航到 .py 文件所在路径下 `cd /Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料`
2. 运行此命令：`python3 6csv_reader_column_by_index.py supplier_data.csv 6output.csv`

终端不会有任何输出，但是此时打开 6output.csv 文件，就能看到供应商名称和对应的价格了。

























第 2 章的家庭作业，在学习完第 2 章后，把各个省份的房地产数据做个简单整合













































































































































































































































































































































































