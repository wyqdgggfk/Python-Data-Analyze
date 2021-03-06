import pandas as pd
import sys
input_file = sys.argv[1] # 此处为 sales_2013.xlsx
output_file = sys.argv[2] # 此处为 pandas_value_matches_pattern_output
data_frame = pd.read_excel(input_file,'january_2013',index_col=None)
data_frame_value_matchs_pattern = data_frame[data_frame['Customer Name'].str.startswith("J")]
writer = pd.ExcelWriter(output_file)
data_frame_value_matchs_pattern.to_excel(writer,sheet_name='jan_13_output',index=False)
writer.save()