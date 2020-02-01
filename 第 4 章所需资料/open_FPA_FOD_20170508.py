import sqlite3

con = sqlite3.connect('/Users/jason/Documents/GitHub/NoteforPythonDataAnalyze/第 4 章所需资料/FPA_FOD_20170508.sqlite')

cursor = con.execute("SELECT * FROM spatial_ref_sys")