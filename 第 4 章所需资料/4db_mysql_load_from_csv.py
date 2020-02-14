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
