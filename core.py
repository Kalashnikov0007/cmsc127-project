import datetime
from db import connect
import mysql.connector

def add_organization():
    while True:
        name = input("Organization name: ").strip()
        if not name:
            print("Error: Organization name cannot be empty.")
        elif len(name) > 100:
            print("Error: Organization name is too long (max 100 characters).")
        else:
            break

    while True:
        description = input("Description: ").strip()
        if len(description) > 500:
            print("Error: Description is too long (max 500 characters).")
        else:
            break

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


def add_member():
    while True:
        student_number = input("Enter student number: ").strip()
        if len(student_number) != 10:
            print("Error: Student number must be exactly 10 characters (XXXX-XXXXX).")
        else:
            break

    while True:
        name = input("Enter member name: ").strip()
        if not name:
            print("Error: Name cannot be empty.")
        elif len(name) > 35:
            print("Error: Name is too long (max 35 characters).")
        else:
            break

    valid_genders = ['Male', 'Female', 'Non-binary', 'Other', 'Prefer not to say']
    while True:
        gender = input("Enter gender (Male/Female/Non-binary/Other/Prefer not to say): ").strip()
        if gender not in valid_genders:
            print("Error: Invalid gender.")
        else:
            break

    while True:
        degree_program = input("Enter degree program: ").strip()
        if not degree_program:
            print("Error: Degree program cannot be empty.")
        elif len(degree_program) > 100:
            print("Error: Degree program is too long (max of 500)")
        else:
            break

    while True:
        academic_batch = input("Enter academic batch year: ").strip()
        if not academic_batch.isdigit() or len(academic_batch) != 4:
            print("Error: Academic batch must be a 4-digit year.")
        else:
            break

    while True:
        graduation_date = input("Enter graduation date (YYYY-MM-DD or leave blank): ").strip()
        if graduation_date == "":
            graduation_date = None
            break
        try:
            datetime.datetime.strptime(graduation_date, "%Y-%m-%d")
            break
        except ValueError:
            print("Error: Invalid date format.")

    valid_semesters = ['First', 'Second']
    while True:
        graduation_semester = input("Enter graduation semester (First/Second or leave blank): ").strip()
        if graduation_semester == "":
            graduation_semester = None
            break
        elif graduation_semester not in valid_semesters:
            print("Error: Invalid semester.")
        else:
            break

    while True:
        graduation_year = input("Enter graduation year (YYYY or leave blank): ").strip()
        if graduation_year == "":
            graduation_year = None
            break
        elif not graduation_year.isdigit() or len(graduation_year) != 4:
            print("Error: Graduation year must be a 4-digit year.")
        else:
            break

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


def delete_organization():
    while True:
        try:
            org_id = int(input("Enter Organization ID: ").strip())
            if 1 <= org_id <= 99999:
                break
            else:
                print("Error: Invalid Organization ID (must be from 1 to 99999).")
        except ValueError:
            print("Error: Please enter a valid integer.")

    conn = connect()
    cursor = conn.cursor()
    try:
        sql = "DELETE FROM organization WHERE organization_id = %s"
        cursor.execute(sql, (org_id))
        conn.commit()
        if cursor.rowcount > 0:
            print(f"Organization with ID {org_id} deleted.")
        else:
            print(f"No organization found with ID {org_id}.")
    except mysql.connector.Error as err:
        print(f"Error deleting organization: {err}")
    finally:
        conn.close()


def delete_member():
    while True:
        student_number = input("Enter Student Number to delete: ").strip()
        if len(student_number) != 10:
            print("Error: Student number must be exactly 10 characters (XXXX-XXXXX).")
        else:
            break

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
    print("\nTables in database:")
    for table in tables:
        print(f" - {table[0]}")


def show_organizations():
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM organization")
        orgs = cursor.fetchall()
        print(f"\n{'ID'.ljust(6)} {'Organization Name'.ljust(101)}")
        print("-" * 107)

        for org in orgs:
            id_str = str(org[0]).ljust(6)
            name_str = str(org[1]).ljust(101)
            print(f"{id_str} {name_str}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()


def show_members():
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM member")
        members = cursor.fetchall()
        print(f"\n{'Student Number'.ljust(15)} {'Name'.ljust(31)} {'Gender'.ljust(18)} {'Degree Program'.ljust(31)} {'Academic Batch'.ljust(15)}")
        print("-" * 115)

        for member in members:
            student_number = str(member[0]).ljust(15)
            name = str(member[1]).ljust(31)
            gender = str(member[2]).ljust(18)
            degree = str(member[3]).ljust(31)
            batch = str(member[4]).ljust(15)
            print(f"{student_number} {name} {gender} {degree} {batch}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()


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