import sqlite3 as sql
conn = sql.connect("earthdb.db")
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS dontmiss (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location CHAR,
        status  CHAR,
        donation  CHAR,
        required CHAR
       
    )
''')

data = ( "test villege2", 'naer mandaly', "အသေအပျောက်များ",'လှူမဲ့သူများရောက်မလာသေး','ဆေးများများလို')

# Insert query
cursor.execute('''
    INSERT INTO dontmiss(name, location, status, donation,required) 
    VALUES (?, ?, ?, ?, ?)
''', data)

# Commit and close the connection
conn.commit()
conn.close()
print("Table created successfully!")