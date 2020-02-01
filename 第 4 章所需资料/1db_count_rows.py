import sqlite3

# 创建 SQLite3 内存数据库
# 创建带有 4 个属性的 sales 表
con = sqlite3.connect('you_database_path') # 书中原代码此处是 :memory:，我把它换成了 my_test_database.db 的路径
query = """CREATE TABLE sales
			(customer VARCHAR(20),
			product VARCHAR(40),
			amount FLOAT,
			date DATE);"""
con.execute(query)
con.commit()

# 在表中插入几行数据
data = [('Richard Lucas','Notepad',2.50,'2014-01-02'),
		('Jenny Kim','Binder',4.15,'2014-01-15'),
		('Svetlana Crow','Printer',155.75,'2014-02-03'),
		('Stephen Randolph','Computer',679.40,'2014-02-20')]	
statement = "INSERT INTO sales VALUES(?,?,?,?)"
con.executemany(statement,data)
con.commit()

# 查询 sales 表
cursor = con.execute("SELECT * FROM sales")
rows = cursor.fetchall()

# 计算查询结果中行的数量
row_counter = 0
for row in rows:
	print(row)
	row_counter += 1
print("Number of rows:%d" % (row_counter))