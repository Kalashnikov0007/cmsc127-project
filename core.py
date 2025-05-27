from db import connect
import mysql.connector

def add_organization():
    name = input("Organization name: ")
    description = input("Description: ")
    conn = connect()
    cursor = conn.cursor()
    try:
        sql = "INSERT INTO organization (name, description) VALUES (%s, %s)"
        cursor.execute(sql, (name, description))
        conn.commit()
        print("Organization added.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()

def delete_organization(organization_id):
    conn = connect()
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM organization WHERE organization_id = %s"
        cursor.execute(sql, (organization_id,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Organization with ID {organization_id} deleted.")
        else:
            print(f"No organization found with ID {organization_id}.")
    except mysql.connector.Error as err:
        print(f"Error deleting organization: {err}")
    finally:
        conn.close()

def add_member():
    student_number = input("Enter student number: ")
    name = input("Enter member name: ")
    gender = input("Enter gender (Male/Female/Non-binary/Other/Prefer not to say): ")
    degree_program = input("Enter degree program: ")
    academic_batch = input("Enter academic batch (year): ")
    graduation_date = input("Enter graduation date (YYYY-MM-DD or leave blank): ")
    graduation_semester = input("Enter graduation semester (First/Second or leave blank): ")
    graduation_year = input("Enter graduation year (year or leave blank): ")
    conn = connect()
    cursor = conn.cursor()
    try:
        sql = """
            INSERT INTO member 
            (student_number, name, gender, degree_program, academic_batch, graduation_date, graduation_semester, graduation_year)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(sql, (student_number, name, gender, degree_program, academic_batch, graduation_date, graduation_semester, graduation_year))
        conn.commit()
        print("Member added.")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()

def delete_member(student_number):
    conn = connect()
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM member WHERE student_number = %s"
        cursor.execute(sql, (student_number,))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Member with student number {student_number} deleted.")
        else:
            print(f"No member found with student number {student_number}.")
    except mysql.connector.Error as err:
        print(f"Error deleting member: {err}")
    finally:
        conn.close()

def show_tables():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = cursor.fetchall()
    conn.close()
    print("Tables in database:")
    for table in tables:
        print(f" - {table[0]}")

def show_table(table_name):
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        print(f"\nContents of `{table_name}`:")
        print("-" * 40)
        print(" | ".join(columns))
        print("-" * 40)
        for row in rows:
            print(" | ".join(str(col) for col in row))
        print("-" * 40)
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()

def get_organizations():
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM organization")
        orgs = cursor.fetchall()
        for org in orgs:
            print(f"ID: {org[0]}, Name: {org[1]}, Description: {org[2]}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()

def get_members():
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM member")
        members = cursor.fetchall()
        for member in members:
            print(f"Student Number: {member[0]}, Name: {member[1]}, Gender: {member[2]}, Degree: {member[3]}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()
