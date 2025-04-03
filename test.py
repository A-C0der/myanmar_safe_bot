import sqlite3 as sql
conn = sql.connect("earthdb.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS donation (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        phone CHAR,
        location CHAR,
        township CHAR,
        type  CHAR,
        link  CHAR,
        division CHAR,
        remark CHAR,
        date CHAR
       
    )
''')

data = ( "arkar", '0833232', "no 3 stree,mdy road",'haling','အစားအစာအလျှူ','my.com','yangon','လှူနှစ်ရာစာ','05-04-2025 -> 06-05-2025')

# Insert query
cursor.execute('''
    INSERT INTO donation(name,phone,location,township,type,link,division,remark,date) 
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
''', data)

# Commit and close the connection
conn.commit()
conn.close()
print("Table created successfully!")