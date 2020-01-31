import pandas as pd
import glob
import sys

input_path = sys.argv[1]
output_file = sys.argv[2]
all_house_price_files = glob.glob(os.path.join(input_path,'*csv'))
all_data_frames = []
first_file = True

for house_price_file in all_house_price_files:
	if first_file:
		data_frame = pd.read_csv(house_price_file,index_col=None)
		data_frame = data_frame.drop([0,1,2])
		print(data_frame)
	