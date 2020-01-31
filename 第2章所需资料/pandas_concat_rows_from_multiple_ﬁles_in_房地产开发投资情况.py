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