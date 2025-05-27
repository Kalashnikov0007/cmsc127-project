import mysql.connector

def connect():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Tyler123",
        database="orgdb"  
    )

if __name__ == "__main__":
    try:
        conn = connect()
        print("Connection successful.")
        conn.close()
    except mysql.connector.Error as err:
        print("Connection failed:")
        print(err)