import pandas as pd
import sys
input_file = sys.argv[1]
output_file = sys.argv[2]
data_frame = pd.read_excel(input_file,sheet_name=None,index_col=None) # 原书中此处是 sheetname 不是 sheet_name
column_output = []
for worksheet_name,data in data_frame.items():
	column_output.append(data.loc[:,['Customer Name','Sale Amount']])
selected_columns = pd.concat(column_output,axis=0,ignore_index=True)
writer = pd.ExcelWriter(output_file)
selected_columns.to_excel(writer,sheet_name='selected_columns_all_worksheets',index=False)
writer.save()