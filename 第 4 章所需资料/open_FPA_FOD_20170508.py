import sqlite3

con = sqlite3.connect('/Users/jason/Desktop/FPA_FOD_20170508.sqlite')

cursor = con.execute("SELECT * FROM spatial_ref_sys")