import sqlite3

con = sqlite3.connect(database='filestore.sqlite')

cur = con.cursor()

cur.execute('select * from login')

print(cur.fetchall())

con.close()
