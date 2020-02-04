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

同样的功能，我们来稍微做个小练习，找到一个名为 DEvideos.csv 的文件，此文件是从 [Kaggle](https://www.kaggle.com/datasnaek/youtube-new) 网站下载的 YouTube 观看数据之一，打开检查一下这个 csv 文件，第一排有 video_id,trending_date,title,channel_title,category_id 等等信息，现在的任务是，要抓取比较多的数据，具体要求如下：

1. 抓取的数据应该包括除了 description 以外的所有数据；
2. 对于 publish_time，仅保留日期，不用保留具体时间；
3. 每抓取一条信息，都在终端打印下来。

为了处理这个问题，我们依次来看要求，首先是抓取的数据要除开 description，这个比较好办，一共有 16 列的数据，而且 description 刚好在最后，只要一个 range 函数就可以了；其次是 publish_time，仅保留日期，不需要时间，这个稍微麻烦一点点，需要用到正则匹配；最后是打印下来，这个没什么难度了，就是直接打印，只是在实际打印的过程中，我发现如果不打印，那么程度处理得会很快，如果打印，CodeRunner 出现了转彩球的状况，为了演示，我们加入一个简单的延时 time.sleep(0.001)，在实际操作时可以根据自己的情况酌情考虑是否延时，请看下面的代码：

```python
import csv
import re
import time

pattern = re.compile('T[\d]+:[\d]+:[\S]+') # 正则表达式，用来筛选 publish_time 中的日期

"""实在不想在写好代码后，跑去终端运行，就直接把路径写下来吧"""
input_file = '/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/Trending_YouTube_Video_Statistics/DEvideos.csv'
output_file = '/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/DEvideo_write_column_by_index.csv'
with open(input_file,'r',newline='') as csv_in_file:
	with open(output_file,'w',newline='') as csv_out_file:
		filereader = csv.reader(csv_in_file)
		filewriter = csv.writer(csv_out_file)
		for row_list in filereader:
			row_list_output = []
			for i in range(15):
				if i==5:
					row_list[i] = re.sub(pattern, '', row_list[i]) #将 publish_time 中日期后面的部分用替换的方式删除掉
				row_list_output.append(row_list[i])
			filewriter.writerow(row_list_output)
			print(row_list_output)
			time.sleep(0.001)
```

书中还给出了利用 pandas 挑选指定列的方法，比使用 csv 会更加简单，如下所示：

```python
import pandas as pd
import sys
input_file = sys.argv[1]
output_file = sys.argv[2]
data_frame = pd.read_csv(input_file)
data_frame_column_by_index = data_frame.iloc[:,[0,3]]
data_frame_column_by_index.to_csv(output_file,index=False) 
```

很明显，用 pandas 会比用 csv 更加简单，代码量也更少。

### 2.3.2 列标题

除了用索引选取特定列以外，还可以在 csv 文件中使用列标题来选取特定的列，可参考如下代码：

```python
import csv
import sys

input_file = sys.argv[1]
output_file = sys.argv[2]

my_columns = ['Invoice Number','Purchase Date']
my_columns_index = []

with open(input_file,'r',newline='') as csv_in_file:
	with open(output_file,'w',newline='') as csv_out_file:
		filereader = csv.reader(csv_in_file)
		filewriter = csv.writer(csv_out_file)
		header = next(filereader,None)
		for index_value in range(len(header)):
			if header[index_value] in my_columns:
				my_columns_index.append(index_value)
		filewriter.writerow(my_columns)
		for row_list in filereader:
			row_list_output =[]
			for index_value in my_columns_index:
				row_list_output.append(row_list[index_value])
			filewriter.writerow(row_list_output)
```

原书的代码有一处错误，倒数第二排的  row_list_output.append(row_list[index_value]) 没有缩进。另外，最后一排代码，filewriter.writerow(row_list_output)，我不清楚是我机器的问题还是书中代码的问题，这一段代码也需要缩进到第二个 for 循环下，而不是第一个 for 循环下，如果不缩进，那么在我的 Mac 上运行时，只读取到了 supplier_data.csv 中最后一排的发票和价格。

## 2.4 选取连续的行

书中提到有时我们可能会遇到工作表的头部和尾部都是不想处理的信息，此时需要选择那些我们需要处理的数据，可参考以下代码：

```python
import csv
import sys
input_file = sys.argv[1] # 此处是 supplier_data_unnecessary_header_footer.csv
output_file = sys.argv[2] # 此处是 11output.csv
row_counter = 0	

with open(input_file,'r',newline='') as csv_in_file:
	with open(output_file,'w',newline='') as csv_out_file:
		filereader = csv.reader(csv_in_file)
		filewriter = csv.writer(csv_out_file)
		for row in filereader:
			if row_counter >= 3 and row_counter <= 15:
				filewriter.writerow([value.strip() for value in row])
			row_counter += 1
```

以上代码可以在 [supplier_data_unnecessary_header_footer.csv](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第2章所需资料/supplier_data_unnecessary_header_footer.csv) 这个文件中跳过行开头的数据，过滤行结尾的数据，只选择我们需要的部分。

另外，在实际操作过程中，我将 supplier_data.csv 另存为一个新的 csv 文件，添加三行 “I don't care this line” 到表头，又添加三行“I don't care this line either” 到表尾，并保存成 supplier_data_unnecessary_header_footer.csv 时，运行上述代码遇到一个问题，错误提示是“UnicodeDecodeError: 'utf-8' codec can't decode byte 0xd5 in position 5: invalid continuation byte”，网上查了一下这应该是 utf-8 的解码问题，如果您也遇到了类似问题，不妨试试我的方法：把所有单元格的内容整体复制下来，新建一个 csv 文件粘贴进去，我是这样解决的。

刚刚是用 Python 自带的 csv 库完成了筛选特定行的操作，如果用 Pandas 的话，其实会更加简单，如下所示：

```python
import pandas as pd
import sys
input_file = sys.argv[1] # 此处为 supplier_data_unnecessary_header_footer.csv
output_file = sys.argv[2] # 此处为 pandas_output_select_contiguous_rows.csv

data_frame = pd.read_csv(input_file,header=None)
data_frame = data_frame.drop([0,1,2,16,17,18])
data_frame.columns = data_frame.iloc[0]
indexInfo = data_frame.index.drop(3)
data_frame = data_frame.reindex(data_frame.index.drop(3)) # 为了弄懂这一行代码的含义，我在 csv 文件中加了一列 indextest 索引，从 1 到 12
data_frame.to_csv(output_file,index=False)
```

当然，一开始我是没有弄懂这段代码的，比如这一句

```python
data_frame = data_frame.reindex(data_frame.index.drop(3))
```

到底能达到什么目的？在网上查了一下，drop() 函数的功能是把 data_frame 中对应的行或列的值抛掉，那么 `data_frame.index.drop(3)` 是什么鬼，打开已经操作好的 [pandas_output_select_contiguous_rows.csv](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第2章所需资料/pandas_output_select_contiguous_rows.csv) 文件，它是长这个样子的：

| Supplier Name | Invoice Number | Part Number | Cost         | Purchase Date | indextest |
| ------------- | -------------- | ----------- | ------------ | ------------- | --------- |
| Supplier X    | 001-1001       | 2341        | $500.00      | 1/20/14       | 1         |
| Supplier X    | 001-1001       | 2341        | $500.00      | 1/20/14       | 2         |
| Supplier X    | 001-1001       | 5467        | $750.00      | 1/20/14       | 3         |
| Supplier X    | 001-1001       | 5467        | $750.00      | 1/20/14       | 4         |
| Supplier Y    | 50-9501        | 7009        | $250.00      | 1/30/14       | 5         |
| Supplier Y    | 50-9501        | 7009        | $250.00      | 1/30/14       | 6         |
| Supplier Y    | 50-9505        | 6650        | $125.00      | 2002/3/14     | 7         |
| Supplier Y    | 50-9505        | 6650        | $125.00      | 2002/3/14     | 8         |
| Supplier Z    | 920-4803       | 3321        | $615.00      | 2002/3/14     | 9         |
| Supplier Z    | 920-4803       | 3321        | $615.00      | 2002/10/14    | 10        |
| Supplier Z    | 920-4803       | 3321        | $60,15.00    | 2/17/14       | 11        |
| Supplier Z    | 920-4803       | 3321        | $10,06015.00 | 2/24/14       | 12        |

换句话讲，书中的 pandas 代码的确达到了我们想要的结果，即筛选特定行的数据，我们试试看逐个测试这段代码，并将结果打印下来，看看是怎样。

首先把 `input_file` 和 `output_file` 都直接表示为路径，即

```python
input_file = '/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/supplier_data_unnecessary_header_footer.csv' # 请注意此处需要替换为您自己电脑上对应文件的路径
output_file = '/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/pandas_output_select_contiguous_rows.csv' # 请注意此处需要替换为您自己电脑上对应文件的路径
```

这一步操作是为了可以直接在 CodeRunner 中运行出结果，省掉了终端命令的过程。

接下来，分别在每一行代码的下方加一句 `print()`，查看当前状态下的各种信息是怎样的：

```python
# 第一次 print
import pandas as pd
import sys
input_file = '/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/supplier_data_unnecessary_header_footer.csv' # 请注意此处需要替换为您自己电脑上对应文件的路径
output_file = '/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/pandas_output_select_contiguous_rows.csv' # 请注意此处需要替换为您自己电脑上对应文件的路径

data_frame = pd.read_csv(input_file,header=None)
print(data_frame)
```

此时的输出是长这样：

|      | 0                             | 1              | ...  | 4             | 5         |
| ---- | ----------------------------- | -------------- | ---- | ------------- | --------- |
| 0    | I don't care this line        | NaN            | ...  | NaN           | NaN       |
| 1    | I don't care this line        | NaN            | ...  | NaN           | NaN       |
| 2    | I don't care this line        | NaN            | ...  | NaN           | NaN       |
| 3    | Supplier Name                 | Invoice Number | ...  | Purchase Date | indextest |
| 4    | Supplier X                    | 001-1001       | ...  | 1/20/14       | 1         |
| 5    | Supplier X                    | 001-1001       | ...  | 1/20/14       | 2         |
| 6    | Supplier X                    | 001-1001       | ...  | 1/20/14       | 3         |
| 7    | Supplier X                    | 001-1001       | ...  | 1/20/14       | 4         |
| 8    | Supplier Y                    | 50-9501        | ...  | 1/30/14       | 5         |
| 9    | Supplier Y                    | 50-9501        | ...  | 1/30/14       | 6         |
| 10   | Supplier Y                    | 50-9505        | ...  | 2002/3/14     | 7         |
| 11   | Supplier Y                    | 50-9505        | ...  | 2002/3/14     | 8         |
| 12   | Supplier Z                    | 920-4803       | ...  | 2002/3/14     | 9         |
| 13   | Supplier Z                    | 920-4804       | ...  | 2002/10/14    | 10        |
| 14   | Supplier Z                    | 920-4805       | ...  | 2/17/14       | 11        |
| 15   | Supplier Z                    | 920-4806       | ...  | 2/24/14       | 12        |
| 16   | I don't care this line either | NaN            | ...  | NaN           | NaN       |
| 17   | I don't care this line either | NaN            | ...  | NaN           | NaN       |
| 18   | I don't care this line either | NaN            | ...  | NaN           | NaN       |

利用 `data_frame = pd.read_csv(input_file,header=None) ` 这一句代码，将 supplier_data_unnecessary_header_footer.csv 文件中的所有信息赋值给了 data_frame，不得不说真心方便。

```python
# 第二次 print
import pandas as pd
import sys
input_file = '/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/supplier_data_unnecessary_header_footer.csv' # 请注意此处需要替换为您自己电脑上对应文件的路径
output_file = '/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/pandas_output_select_contiguous_rows.csv' # 请注意此处需要替换为您自己电脑上对应文件的路径

data_frame = pd.read_csv(input_file,header=None)

data_frame = data_frame.drop([0,1,2,16,17,18])
print(data_frame)
```

此时的输出已经没有了开头的 `I don't care this line` 和结尾的 `I don't care this line either`，其输出为：

|      | 0             | 1              | 2           | 3            | 4             | 5         |
| ---- | ------------- | -------------- | ----------- | ------------ | ------------- | --------- |
| 3    | Supplier Name | Invoice Number | Part Number | Cost         | Purchase Date | indextest |
| 4    | Supplier X    | 001-1001       | 2341        | $500.00      | 1/20/14       | 1         |
| 5    | Supplier X    | 001-1001       | 2341        | $500.00      | 1/20/14       | 2         |
| 6    | Supplier X    | 001-1001       | 5467        | $750.00      | 1/20/14       | 3         |
| 7    | Supplier X    | 001-1001       | 5467        | $750.00      | 1/20/14       | 4         |
| 8    | Supplier Y    | 50-9501        | 7009        | $250.00      | 1/30/14       | 5         |
| 9    | Supplier Y    | 50-9501        | 7009        | $250.00      | 1/30/14       | 6         |
| 10   | Supplier Y    | 50-9505        | 6650        | $125.00      | 2002/3/14     | 7         |
| 11   | Supplier Y    | 50-9505        | 6650        | $125.00      | 2002/3/14     | 8         |
| 12   | Supplier Z    | 920-4803       | 3321        | $615.00      | 2002/3/14     | 9         |
| 13   | Supplier Z    | 920-4804       | 3321        | $615.00      | 2002/10/14    | 10        |
| 14   | Supplier Z    | 920-4805       | 3321        | $60,15.00    | 2/17/14       | 11        |
| 15   | Supplier Z    | 920-4806       | 3321        | $10,06015.00 | 2/24/14       | 12        |

上面的代码用了一段 drop 函数 `data_frame = data_frame.drop([0,1,2,16,17,18])`将第 0，1，2，16，17，18 行数据删除掉。

然后我们再来看看 `data_frame.iloc[0]` 能干什么，书上是说可以使用 iloc 这个函数根据行索引选取一个单独行作为列索引，那么使用 iloc[0] 应该就是把第 0 行的各个单元格的值作为索引，从实际代码来看，也确实如此：

```python
# 第三次 print
import pandas as pd
import sys
input_file = '/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/supplier_data_unnecessary_header_footer.csv' # 请注意此处需要替换为您自己电脑上对应文件的路径
output_file = '/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/pandas_output_select_contiguous_rows.csv' # 请注意此处需要替换为您自己电脑上对应文件的路径

data_frame = pd.read_csv(input_file,header=None)
data_frame = data_frame.drop([0,1,2,16,17,18])
data_frame.columns = data_frame.iloc[0]
print(data_frame)
```

这一次 `print` 把上一次打印的第一排的 0 1 2 3 4 5 换成了列标题，如下所示：

| 3    | Supplier Name | Invoice Number | Part Number | Cost         | Purchase Date | indextest |
| ---- | ------------- | -------------- | ----------- | ------------ | ------------- | --------- |
| 3    | Supplier Name | Invoice Number | Part Number | Cost         | Purchase Date | indextest |
| 4    | Supplier X    | 001-1001       | 2341        | $500.00      | 1/20/14       | 1         |
| 5    | Supplier X    | 001-1001       | 2341        | $500.00      | 1/20/14       | 2         |
| 6    | Supplier X    | 001-1001       | 5467        | $750.00      | 1/20/14       | 3         |
| 7    | Supplier X    | 001-1001       | 5467        | $750.00      | 1/20/14       | 4         |
| 8    | Supplier Y    | 50-9501        | 7009        | $250.00      | 1/30/14       | 5         |
| 9    | Supplier Y    | 50-9501        | 7009        | $250.00      | 1/30/14       | 6         |
| 10   | Supplier Y    | 50-9505        | 6650        | $125.00      | 2002/3/14     | 7         |
| 11   | Supplier Y    | 50-9505        | 6650        | $125.00      | 2002/3/14     | 8         |
| 12   | Supplier Z    | 920-4803       | 3321        | $615.00      | 2002/3/14     | 9         |
| 13   | Supplier Z    | 920-4804       | 3321        | $615.00      | 2002/10/14    | 10        |
| 14   | Supplier Z    | 920-4805       | 3321        | $60,15.00    | 2/17/14       | 11        |
| 15   | Supplier Z    | 920-4806       | 3321        | $10,06015.00 | 2/24/14       | 12        |

我试过把代码中的 `iloc[0]` 换成 `iloc[1]`，此时上面的列标题也会随之更换，意味着我们通过 `iloc[]`这个函数实现了重新根据行索引选取一个单独行来作为列索引，可是明明在`data_frame = data_frame.drop([0,1,2,16,17,18])` 中不是已经把第 0 行丢掉了么？是的，丢掉了，`iloc[0]`在这段代码里面指的也不是最初的第 0 行，请看表格最左的数字，`iloc[0]`指代的是数字 3 那一行。

再做一个小测试，在上一次打印时我们可以看到索引为 3 的那一行重复了，那么如果在`data_frame.columns = data_frame.iloc[0]`的下面加一行，把表格重复的内容去掉，应该如何操作？我试过 `data_frame = data_frame.drop(3)`是可行的，下面是具体代码和打印下来的表格：

```python
# 第四次 print
import pandas as pd
import sys
input_file = '/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/supplier_data_unnecessary_header_footer.csv' # 请注意此处需要替换为您自己电脑上对应文件的路径
output_file = '/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/pandas_output_select_contiguous_rows.csv' # 请注意此处需要替换为您自己电脑上对应文件的路径

data_frame = pd.read_csv(input_file,header=None)
data_frame = data_frame.drop([0,1,2,16,17,18])
data_frame.columns = data_frame.iloc[0]
data_frame = data_frame.drop(3)
print(data_frame)
```

| 3    | Supplier Name | Invoice Number | Part Number | Cost         | Purchase Date | indextest |
| ---- | ------------- | -------------- | ----------- | ------------ | ------------- | --------- |
| 4    | Supplier X    | 001-1001       | 2341        | $500.00      | 1/20/14       | 1         |
| 5    | Supplier X    | 001-1001       | 2341        | $500.00      | 1/20/14       | 2         |
| 6    | Supplier X    | 001-1001       | 5467        | $750.00      | 1/20/14       | 3         |
| 7    | Supplier X    | 001-1001       | 5467        | $750.00      | 1/20/14       | 4         |
| 8    | Supplier Y    | 50-9501        | 7009        | $250.00      | 1/30/14       | 5         |
| 9    | Supplier Y    | 50-9501        | 7009        | $250.00      | 1/30/14       | 6         |
| 10   | Supplier Y    | 50-9505        | 6650        | $125.00      | 2002/3/14     | 7         |
| 11   | Supplier Y    | 50-9505        | 6650        | $125.00      | 2002/3/14     | 8         |
| 12   | Supplier Z    | 920-4803       | 3321        | $615.00      | 2002/3/14     | 9         |
| 13   | Supplier Z    | 920-4804       | 3321        | $615.00      | 2002/10/14    | 10        |
| 14   | Supplier Z    | 920-4805       | 3321        | $60,15.00    | 2/17/14       | 11        |
| 15   | Supplier Z    | 920-4806       | 3321        | $10,06015.00 | 2/24/14       | 12        |

这证明 `data_frame.drop(3)` 这段命令的确把多余的 Supplier Name 那一行去掉了，注意去掉的是第二个 Supplier Name 那一行，并不是第一个。

好了，测试完成，让我们回到书中代码本身，并再来一个打印，看看究竟有什么变化：

```python
# 第五次 print
import pandas as pd
import sys
input_file = '/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/supplier_data_unnecessary_header_footer.csv' # 请注意此处需要替换为您自己电脑上对应文件的路径
output_file = '/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/pandas_output_select_contiguous_rows.csv' # 请注意此处需要替换为您自己电脑上对应文件的路径

data_frame = pd.read_csv(input_file,header=None)
data_frame = data_frame.drop([0,1,2,16,17,18])
data_frame.columns = data_frame.iloc[0]
data_frame = data_frame.reindex(data_frame.index.drop(3)) # 为了弄懂这一行代码的含义，我在 csv 文件中加了一列 indextest 索引，从 1 到 12
print(data_frame)
```

第五次 `print `中，主要就是解释`data_frame = data_frame.reindex(data_frame.index.drop(3))`这一段的含义，按照刚刚小测试的结果，`data_frame.index.drop(3)`丢掉了第二个 Supplier Name 那一行，而 `data_frame.reindex()`的含义就是重新创建索引，合起来就是，先删掉多余的 Supplier Name，再重建索引，其打印结果与上面的那个表格一致，最后再写入到新的 csv 文件即可。

## 2.5 添加标题行

这一节的意思是，有时我们会收到没有标题行的 csv 数据，需要自己添加标题行，其实有时候也会遇到需要修改标题行的情况，可参考以下代码添加标题行：

```python
import sys
import csv

"""
开始之前，请打开 supplier_data.csv 文件，把标题行删了，然后将此文件另存为supplier_data_no_header_row.csv
"""

input_file = sys.argv[1] # 此处为 supplier_data_no_header_row.csv
output_file = sys.argv[2] # 此处为 12output.csv

with open(input_file,'r',newline='') as csv_in_file:
	with open(output_file,'w',newline='') as csv_out_file:
		filereader = csv.reader(csv_in_file)
		filewriter = csv.writer(csv_out_file)
		header_list = ['Supplier Name','Invoice Number','Part Number','Cost','Purchase Date']
		filewriter.writerow(header_list)
		for row in filereader:
			filewriter.writerow(row)		
```

同样的功能，如果用 pandas 会更简单一些，毕竟书中的原话是“pandas 中的 read_csv 可以直接指定输入文件不包含标题行，并可以提供一个列标题列表”，可参考以下代码：

```python
import pandas as pd
import sys

input_file = sys.argv[1] # 此处为 supplier_data_no_header_row.csv
output_file = sys.argv[2] # 此处为 pandas_add_header_row_output.csv

header_list = ['Supplier Name','Invoice Number','Part Number','Cost','Purchase Date']
data_frame = pd.read_csv(input_file,header=None,names=header_list)
data_frame.to_csv(output_file,index=False)
```

## 2.6 读取多个 CSV 文件

书中需要让读者自行创建三个 csv 文件，分别是 sales_january_2014.csv，sales_february_2014.csv，sales_march_2014.csv，所创建的 csv 文件内容是 Customer ID，Customer Name，Invoice Number，Sale Amount，Purchase Date 这种信息，那么我们不妨结合一下之前所学过的内容，试试看统计一下我自己从[国家统计局](http://www.stats.gov.cn)获取的[房地产开发投资情况](https://github.com/wyqdgggfk/Python-Data-Analyze/tree/master/房地产开发投资情况)，这里面我已经准备好了 excel 文件和 csv 文件，稍后我们会先从 csv 文件入手。

### 文件计数与文件中的行列计数

开始之前先看看两个要用到的东西，一个是 glob 库，一个是 os.path.join() 函数。

首先看一个 Python 自带的库 glob，参考了一下网上的资料，这个库的功能就是获取当前文件夹下的子文件和子文件夹，用 * 作通配符匹配，比如下面的代码：

```python
import glob

testpath = '/*' #获取根目录下的所有文件夹

for name in glob.glob(testpath):
	print(name)
```

这段代码会获取我电脑上根目录文件夹的所有子文件夹，并将其打印下来。再比如下面的代码会获取我电脑上所有安装的软件名称，不过是以路径形式：

```python
import glob
testpath = '/Applications/*' #获取应用程序目录下的所有软件
for name in glob.glob(testpath):
	print(name)
```

接着看看 os.path.join() 函数的功能，实际上它和字符串的拼接有点像，但它主要是针对路径的，如果路径中没有 \，它可以自动补全，举个例子:

```python
import os
path1 = 'home'
path2 = 'admin'
path3 = 'document'
path_final = os.path.join(path1, path2,path3)
print(path_final) # 此时输出的 path_final 就是 home/admin/document
```

明白了这些之后，如果我们想要看懂书上的 8csv_reader_counts_for_multiple_ﬁles.py 源代码，还有一个需要了解，试想一下，如果我们要找某个文件夹中所有[以 pandas 开头的文件](https://github.com/wyqdgggfk/Python-Data-Analyze/tree/master/第2章所需资料)，应该怎样处理？我们试试看找一下之前我们保存过的以 pandas 开头的文件：

```python
import os
import glob

test_file = '/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料' # 注意此处要换成您自己电脑上对应的路径
for pandasfile in glob.glob(os.path.join(test_file, 'pandas_*')):
	print(pandasfile)
```

这里用到了 `glob.glob(os.path.join(test_file, 'pandas_*'))`，实际上这就是我们要找的当前文件夹下所有以 pandas_ 开头的文件，用 * 表示通配查找，打印下来的结果如下：

```python
"""
/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/pandas_output_select_contiguous_rows.csv
/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/pandas_select_contiguous_rows.py
/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/pandas_value_in_set.py
/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/pandas_value_meets_condition.py
/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/pandas_add_header_row_output.csv
/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/pandas_value_meets_condition.csv
/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/pandas_value_matches_pattern.py
/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/pandas_column_by_index.py
/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/pandas_parsing_and_write.gif
/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/pandas_add_header_row.py
/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/pandas_value_matches_pattern_5output.csv
/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/pandas_output_column_by_index.csv
/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/pandas_output.csv
/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/pandas_ parsing_and_write.py
"""
```

好了，我们可以开始学习书中第 73 页的代码了，源代码如下：

```python
import csv
import glob
import os
import sys
input_path = sys.argv[1]
file_counter = 0
for input_file in glob.glob(os.path.join(input_path, 'sales_*')):
	row_counter = 1
	with open(input_file,'r',newline='') as csv_in_file:
		filereader = csv.reader(csv_in_file)
		header = next(filereader,None)
		for row in filereader:
			row_counter += 1
	print('{0!s}:\t{1:d} rows \t{2:d} columns'.format(os.path.basename(input_file), row_counter,len(header)))
	file_counter += 1
print('Number of files:{0:d}'.format(file_counter))
```

原书中说运行上面的代码需要在终端执行下面这段代码：

```shell
python 8csv_reader_counts_for_multiple_files.py "C:\Users\Clinton\Desktop"
```

由于我并没有去创建 sales 文件，且自己找到了[一些资料](https://github.com/wyqdgggfk/Python-Data-Analyze/tree/master/房地产开发投资情况)，所以我将上面的代码稍微进行了一点修改，请看如下：

```python
import csv
import glob
import os
import sys
input_path = sys.argv[1]
file_counter = 0
for input_file in glob.glob(os.path.join(input_path, '*csv')): # 此处把 sales_* 修改为 *csv
	row_counter = 1
	with open(input_file,'r',newline='') as csv_in_file:
		filereader = csv.reader(csv_in_file)
		header = next(filereader,None)
		for row in filereader:
			row_counter += 1
	print('{0!s}:\t{1:d} rows \t{2:d} columns'.format(os.path.basename(input_file), row_counter,len(header)))
	file_counter += 1
print('Number of files:{0:d}'.format(file_counter))
```

然后打开终端，导航至 8csv_reader_counts_for_multiple_ﬁles.py 所在的文件夹，并输入如下命令：

```shell
python3 8csv_reader_counts_for_multiple_ﬁles.py /Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/房地产开发投资情况/csvFile
```

此时终端就会输出每个 csv 文件有多少行多少列，最后会输出一共有多少文件。

## 2.7 从多个文件中连接数据

实际处理数据时，可能会有多个文件，这些文件的内容格式一致，需要放在一起进行数据统计工作，比如全国各地提交给统计局的房地产数据，它们可能是“北京.csv”，“上海.csv”，“广东.csv”这样的命名方式。

在原书中是将三个 sales 文件的数据合并到一起，我会在这里贴上[原代码](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第2章所需资料/9csv_reader_concat_rows_from_multiple_ﬁles.py)，同时附上我们自己修改后的代码。

### 基础 Python

先附上原代码：

```python
import csv
import glob
import os
import sys
input_path = sys.argv[1]
output_file = sys.argv[2]
first_file = True
for input_file in glob.glob(os.path.join(input_path, 'sales_*')):
	print(os.path.basename(input_file)) # 打印当前处理文件的名称
	with open(input_file,'r',newline='') as csv_in_file:
		with open(output_file,'a',newline='') as csv_out_file:
			filereader = csv.reader(csv_in_file)
			filewriter = csv.writer(csv_out_file)
			if first_file:
				for row in filereader:
					filewriter.writerow(row)
				first_file = False
			else:
				header = next(filereader,None)
				for row in filereader:
					filewriter.writerow(row)
```

根据上面的代码，我们试试把[房地产开发投资情况](https://github.com/wyqdgggfk/Python-Data-Analyze/tree/master/房地产开发投资情况)中的各个 csv 文件进行一下整合，要求如下：

1. 所有的 csv 文件中的数据需要整合到一张 csv 表里面；
2. 整合后的数据需要能够看得出来是哪个省份在哪个时间的房地产数据；
3. 对于单独的每个 csv 文件开头几行的数据库地区时间这些，要剔除掉，最后一排的数据来源，每个表里面都有，为了统计的需要，也不用每个都保留下来。

那么我们先打开其中任意一个 csv 文件来看看，它都有些什么数据，打开的方式并不是直接双击这个 csv 文件，因为我们要考虑到在实际工作中，我们可能要打开十几个以 GB 为单位的 csv 文件，同时也为了练习一下刚才的代码，我们试试用 Python 来打开并输出其中一个文件，此处就挑选[内蒙古.csv](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/房地产开发投资情况/csvFile/内蒙古.csv) 这个文件，那么代码可以这样写：

```python
import csv
import sys
input_file = sys.argv[1]
with open(input_file) as csv_in_file:
	filereader = csv.reader(csv_in_file)
	for row in filereader:
		for cell in row:
			if cell:
				print(cell,end='\t')
		print('')
```

打印下来的数据大概长这个样子：

| 数据库：分省月度数据       |            |            |            |      |           |
| -------------------------- | ---------- | ---------- | ---------- | ---- | --------- |
| 地区：内蒙古自治区         |            |            |            |      |           |
| 时间：最近36个月           |            |            |            |      |           |
| 指标                       | 2019年12月 | 2019年11月 | 2019年10月 | ...  | 2017年1月 |
| 房地产投资累计值(亿元)     | 1041.95    | 1026.08    | 957.6      | ...  |           |
| 房地产投资累计增长(%)      | 18         | 17.2       | 15.8       | ...  |           |
| 房地产住宅投资累计值(亿元) | 782.13     | 769.18     | 702.77     | ...  |           |
| 房地产住宅投资累计增长(%   | 21.8       | 20.7       | 16.9       | ...  |           |
| 数据来源：国家统计局       |            |            |            |      |           |

在原始数据中，内蒙古刚好没有 2917 年 1 月的相关房地产数据，这里也给我们提了个醒，对于数据的整理工作，务必要注意，并不是每个单元格都是有数据的，也并不是每个单元格的数据都是正确的。

好了，开始正式的代码：

```python
import csv
import glob
import os
import sys
import re

input_path = sys.argv[1]
output_file = sys.argv[2]
first_file = True

for input_file in glob.glob(os.path.join(input_path, '*csv')):
	message = "Dealing with file " + str(os.path.basename(input_file))
#	print(message)
	with open(input_file,'r',newline='') as csv_in_file:
		with open(output_file,'a',newline='') as csv_out_file:
			filereader = csv.reader(csv_in_file)
			filewriter = csv.writer(csv_out_file)
			row_counter = 1
			if first_file:
				for row in filereader:
					if row_counter > 3 and row_counter < 9: # 对于第一个处理的文件，前 3 行和第 9 行数据是不需要的，只保留从第 4 行开始的数据
						if row_counter == 4:
							row.insert(0,"地区") # 在第 4 行的开头插入一个地区列，用来区分这些数据是哪个省市的
						else:
							pattern = re.compile("\.csv") # 用正则表达式把文件名的 .csv 去掉，把文件名加入到地区那一列
							location_name = re.sub(pattern, '', os.path.basename(input_file))
							row.insert(0,location_name)
						filewriter.writerow(row)
					row_counter += 1
				first_file = False
			else:
				for row in filereader:
					if row_counter > 4 and row_counter < 9:
						pattern = re.compile("\.csv")
						location_name = re.sub(pattern, '', os.path.basename(input_file))
						row.insert(0,location_name)
						filewriter.writerow(row)
					row_counter += 1
```

### pandas 连接多个文件

首先我还是贴出书中的原代码：

```python
import pandas as pd
import glob
import os
import sys
input_path = sys.argv[1]
output_file = sys.argv[2]
all_files = glob.glob(os.path.join(input_path, 'sales_*'))
all_data_frames = []
for file in all_files:
	data_frame = pd.read_csv(file,index_col=None)
	all_data_frames.append(data_frame)
data_frame_concat = pd.concat(all_data_frames,axis=0,ignore_index = True)
data_frame_concat.to_csv(output_file,index=False)
```

书中第 78 页提到，这段代码是垂直堆叠数据框，如果需要平行连接数据，那么就在 concat 函数中设置 axis=1。我想到了一个平行连接数据的实际需求，试想一下，如果要追踪一群人每年的某些数据，比如 NBA 球星在每年的三分球，场均得分，助攻等等数据，而他们每年的数据是按年列的 csv 表格，就可能需要按平行连接数据，各位看官可以自己试试看。

贴出了原代码，我仍然不会按照这段代码去运行，而是用 pandas 来整合房地产的数据，下面请看我自己修改过后的代码：

```python
import pandas as pd
import glob
import os
import sys
import re

finishwriting = "Finish writing data to file"

input_path = sys.argv[1]
output_file = sys.argv[2]
all_house_price_files = glob.glob(os.path.join(input_path,'*csv'))
all_data_frames = []
first_file = True

for house_price_file in all_house_price_files:
	if first_file:
		"""以下代码是用来获取当前处理 csv 文件的文件名"""
		district_names = []
		file_name = os.path.basename(house_price_file)
		pattern = re.compile('\.csv')
		district_name = re.sub(pattern, '', file_name)		
		
		"""还记得之前的 drop 函数和 iloc 函数么，又用到他们来挑选指定行了"""
		data_frame = pd.read_csv(house_price_file,header=None)
		data_frame = data_frame.drop([0,1,2,8])
		data_frame.columns = data_frame.iloc[0]
		data_frame = data_frame.reindex(data_frame.index.drop(3))
		
		"""为了知道汇总后的数据都是哪个省市的房地产数据，需要提前插入一列地区"""
		for row in range(data_frame.shape[0]):
			district_names.append(district_name)
		data_frame.insert(0,'地区',district_names)
		data_frame.to_csv(output_file,mode='a',index=None,encoding='utf-8-sig') # 需要注意，可能由于一些兼容性问题，我的电脑上编码居然是 utf-8-sig，不然可能出现写入文件乱码
		print(data_frame)
		first_file = False
	else:
		district_names = []
		file_name = os.path.basename(house_price_file)
		pattern = re.compile('\.csv')
		district_name = re.sub(pattern,'',file_name)
		
		data_frame = pd.read_csv(house_price_file,header=None)
		data_frame = data_frame.drop([0,1,2,3,8])
		
		for row in range(data_frame.shape[0]):
			district_names.append(district_name)
		
		data_frame.insert(0,'地区',district_names)
		data_frame.to_csv(output_file,mode='a',index=None,header=None,encoding='utf-8-sig') # mode='a' 意思就是向文件中以附加的方式写入数据，而不是覆盖写入
print(finishwriting)
```

原始代码放在这里，您也可以查找对应写入好的 [pandas_concat_rows_from_multiple_ﬁles_in_房地产开发投资情况.csv](https://github.com/wyqdgggfk/Python-Data-Analyze/blob/master/第2章所需资料/pandas_concat_rows_from_multiple_ﬁles_in_房地产开发投资情况.csv) 文件，简单说一下我在写这段代码时遇到的问题，仅供各位参考：

1. 每个省份或直辖市的数据是单独存放在不同的 csv 文件中的，如果我把它们整合到一起，那么会不知道哪个数据属于哪个省份，此时需要在对应数据的前面加一列代表省份或直辖市；
2. 把所有数据合并到一起时，可能会出现有多个标题列，这并不是我们想看到的，可以设定一个 first_file = True 的旗标，当输入为第一个文件时，我们保存这个标题列，当输入不是第一个文件时，我们用 header=None 来忽略掉标题列，只保留相应数据；
3. 选择合并的方法并不唯一，可以把所有数据都先整合到一个 all_data_frames 中再统一写入文件，也可以分别写入数据，注意分别写入时，data_frame.to_csv 的限定条件有一个 mode='a'，代表附加写入，而不是覆盖写入；
4. 乱码问题，解决这个问题的最好办法其实是在 csv 文件中不要包含中文，因为 python 本身对中文的支持并不是很好，当然我们都知道，这在实际应用中是不可能的，你无法要求录入数据的人一个汉字都不写，所以要在处理数据时注意解码问题。

## 2.8 计算每个文件中值的总和与均值

有时候我们会收到很多文件格式一致的数据，要求计算出里面某个列的总和，对于单个文件来讲，我们可以直接使用一些内置的 Excel 函数，但是如果有多个文件则会更复杂，比如某公司某年所有销售点的营业额总和，所有销售点营业额的均值，进一步可以计算每个销售点的盈利能力等等，下面看看用 python 具体如何处理。

#### 基础 Python

```python
import csv
import glob
import os
import sys
input_path = sys.argv[1]
output_file = sys.argv[2]
output_header_list = ['file_name','total_sales','average_sales'] # 创建一个输出文件的列标题列表
csv_out_file = open(output_file,'a',newline='')
filewriter = csv.writerow(csv_out_file)
filewriter.writerow(output_header_list) # 将标题行写入输出文件
for input_file in glob.glob(os.path.join(input_path, 'sales_*')):
	with open(input_file,'r',newline='') as csv_in_file:
		filereader = csv.reader(csv_in_file)
		output_list = [] # 用来保存要写入输出文件中的每行输出
		output_list.append(os.path.basename(input_file))
		header = next(filereader) # next() 函数去除每个输入文件的标题行
		total_sales = 0.0
		number_of_sales = 0.0
		for row in filereader:
			sale_amount = row[3]
			total_sales += float(str(sale_amount).strip('$').replace(',',''))
			number_of_sales += 1
		average_sales = '{0:.2f}'.format(total_sales/number_of_sales)
		output_list.append(total_sales)
		output_list.append(average_sales)
		filewriter.writerow(output_list)
csv_out_file.close()
```

#### pandas 实现



















