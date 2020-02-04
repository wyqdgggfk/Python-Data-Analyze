import pandas as pd
import glob
import os
import sys
input_path = sys.argv[1]
output_file = sys.argv[2]
all_files = glob.glob(os.path.join(input_path, 'sales_*'))
all_data_frames = []
for input_file in all_files:
	data_frame = pd.read_csv(input_file,index_col=None)
	total_cost = pd.DataFrame([float(str(value).strip('$').replace(',','')) for value in data_frame.loc[:,'Sale Amount']]).sum()
	average_cost = pd.DataFrame([float(str(value).strip('$').replace(',','')) for value in data_frame.loc[:,'Sale Amount']]).mean()