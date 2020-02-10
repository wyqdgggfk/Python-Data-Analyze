import pandas as pd
import sys
input_file = sys.argv[1]
output_file = sys.argv[2]
data_frame = pd.read_excel(input_file,sheet_name=None,index_col=None)
row_output=[]
for worksheet_name,data in data_frame.items():
	row_output.append(data[data['Sale Amount'].astype(float) > 2000.0])
filtered_rows = pd.concat(row_output,axis=0,ignore_index=True)
writer = pd.ExcelWriter(output_file)