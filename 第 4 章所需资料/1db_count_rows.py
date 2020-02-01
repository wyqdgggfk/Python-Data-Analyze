import sqlite3

# 创建 SQLite3 内存数据库
# 创建带有 4 个属性的 sales 表
con = sqlite3.connect('you_database_path') # 书中原代码此处是 :memory:，我把它换成了 my_test_database.db 的路径
query = """CREATE TABLE sales
			(customer VARCHAR(20),# 此处表示 customer 属性是一个变长字符型字段，最大字符数为 20
			product VARCHAR(40), # 此处表示 product 属性也是一个变长字符型字段，最大字符数为 40
			amount FLOAT, #此处表示 amount 属性是一个浮点数型字段
			date DATE);""" # 此处表示 date 属性是一个日期字段
con.execute(query) # 使用连接对象的 execute() 方法执行包含在变量 query 中的 SQL 命令，创建 sales 表
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