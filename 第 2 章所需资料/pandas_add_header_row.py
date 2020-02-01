import pandas as pd
import sys

input_file = sys.argv[1] # 此处为 supplier_data_no_header_row.csv
output_file = sys.argv[2] # 此处为 pandas_add_header_row_output.csv

header_list = ['Supplier Name','Invoice Number','Part Number','Cost','Purchase Date']
data_frame = pd.read_csv(input_file,header=None,names=header_list)
data_frame.to_csv(output_file,index=False)