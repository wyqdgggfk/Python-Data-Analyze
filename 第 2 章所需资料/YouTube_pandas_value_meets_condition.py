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