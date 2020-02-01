import sys
import pandas as pd
input_file = '/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/supplier_data.csv'
output_file = '/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第2章所需资料/1output.csv'
data_frame = pd.read_csv(input_file)
print(data_frame)
data_frame.to_csv(output_file,index=False)