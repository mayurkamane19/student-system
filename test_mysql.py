import mysql.connector

try:
    conn = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',  # or your password
        database='webgui'
    )
    print("Connection successful!")
    conn.close()
except mysql.connector.Error as err:
    print("Error:", err)