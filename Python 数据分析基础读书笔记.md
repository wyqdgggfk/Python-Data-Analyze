# 第 1 章 Python 基础

略

# 第 2 章 CSV 文件

### 基础 Python，不使用 CSV 模块

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

![image](

