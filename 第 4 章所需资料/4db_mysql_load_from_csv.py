import MySQLdb
import csv
import sys
from datetime import datetime,date 

# CSV 输入文件的路径和文件名
input_file = sys.argv[1]
con = MySQLdb.connect(host='localhost',port=3306,db='my_suppliers',user='root',passwd='JKWing1990')
c = con.cursor()
# 向 Suppliers 表中插入数据
file_reader = csv.reader(open(input_file,'r',newline=''))
header = next(file_reader)
for row in file_reader:
	data = []
	for column_index in range(len(header)):
		if column_index < 4:
			data.append(str(row[column_index]).lstrip('$').replace(',','').strip())
		else:
			a_date = datetime.date(datetime.strftime(str(row[column_index]), '%m/%d/%Y'))
			# %Y: year is 2015;  %y:year is 15
			a_date = a_date.strftime('%Y-%m-%d')
			data.append(a_date)
	print(data)
	c.execute("""INSERT INTO Suppliers VALUES (%S,%S,%S,%S,%S);""",data)
con.commit()
print("")
# 查询 Suppliers 表
c.execute("SELECT * FROM Suppliers")
rows = c.fetchall()	
for row in rows:
	row_list_output = []
	for column_index in range(len(row)):
		row_list_output.append(str(row[column_index]))
	print(row_list_output)