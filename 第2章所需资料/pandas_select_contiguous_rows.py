import pandas as pd
import sys
input_file = sys.argv[1]
output_file = sys.argv[2]

data_frame = pd.read_csv(input_file,header=None)
data_frame = data_frame.drop([0,1,2,16,17,18])
data_frame.columns = data_frame.iloc[0]
indexInfo = data_frame.index.drop(3)
data_frame = data_frame.reindex(data_frame.index.drop(3)) # 为了弄懂这一行代码的含义，我在 csv 文件中加了一列 indextest 索引，从 1 到 12
data_frame.to_csv(output_file,index=False)
