import sqlite3

# 创建 SQLite3 内存数据库
# 创建带有 4 个属性的 sales 表

con = sqlite3.connect(':memory')
query = """CREATE TABLE sales
			(customer VARCHAR(20),
			product VARCHAR(40),
			amount FLOAT,
			date DATE);"""
con.execute(query)
con.commit()