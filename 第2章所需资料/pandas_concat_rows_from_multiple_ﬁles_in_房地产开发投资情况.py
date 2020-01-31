import pandas as pd
import glob
import os
import sys
import re

input_path = sys.argv[1]
output_file = sys.argv[2]
all_house_price_files = glob.glob(os.path.join(input_path,'*csv'))
all_data_frames = []
first_file = True

for house_price_file in all_house_price_files:
	if first_file:
		"""为了知道汇总后的数据都是哪个省市的房地产数据，需要提前插入一列地区"""
		file_name = os.path.basename(house_price_file)
		pattern = re.compile('\.csv')
		dictrict_name = re.sub(pattern, '', file_name)

		data_frame = pd.read_csv(house_price_file,header=None)
		data_frame = data_frame.drop([0,1,2,8])
		row_counter = len(data_frame)
		
		print(row_counter)
		first_file = False
#	else:
		