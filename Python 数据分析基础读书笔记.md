# 第 1 章 Python 基础

略

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

有了上述的代码，我们可以稍微修改一下，在 Kaggle 官网上找到 YouTube 的一些[视频观看数据](https://www.kaggle.com/datasnaek/youtube-new)来进行简单的筛选，具体代码如下：

```python
import csv
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

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

































































































































































































































































































































































































