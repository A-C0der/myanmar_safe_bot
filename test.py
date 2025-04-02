import sqlite3 as sql
conn = sql.connect("earthdb.db")
cursor = conn.cursor()
# Create table
# cursor.execute('''
#     CREATE TABLE IF NOT EXISTS mdysafe (
#         id INTEGER PRIMARY KEY AUTOINCREMENT,
#         name TEXT NOT NULL,
#         phone CHAR,
#         location CHAR,
#         date CHAR
        
#     )
# ''')

data = ( "Test1", '088484', "mdy",'18.05.2024-2025')

# Insert query
cursor.execute('''
    INSERT INTO mdysafe(name, phone, location,date) 
    VALUES (?, ?, ?, ?)
''', data)

# Commit and close the connection
conn.commit()
conn.close()
print("Table created successfully!")