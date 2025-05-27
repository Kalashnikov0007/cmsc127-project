import datetime
from db import connect
import mysql.connector

def add_organization():
    print("")

    while True:
        name = input("Organization name to add: ").strip()
        if not name:
            print("Error: Organization name cannot be empty.\n")
        elif len(name) > 100:
            print("Error: Organization name is too long (max 100 characters).\n")
        else:
            break

    while True:
        description = input("Description to add: ").strip()
        if len(description) > 500:
            print("Error: Description is too long (max 500 characters).\n")
        else:
            break

    conn = connect()
    cursor = conn.cursor()

    try:
        sql = "INSERT INTO organization (name, description) VALUES (%s, %s)"
        cursor.execute(sql, (name, description))
        conn.commit()
        print("\nOrganization added successfully!")
    except mysql.connector.Error as err:
        print(f"\nError: {err}")
    finally:
        conn.close()


def add_member():
    print("")

    while True:
        student_number = input("Enter student number to add: ").strip()
        if len(student_number) != 10 or not (student_number[:4].isdigit() and student_number[4] == '-' and student_number[5:].isdigit()):
            print("Error: Student number must be in the format XXXX-XXXXX.\n")
        else:
            break

    while True:
        name = input("Enter member name to add: ").strip()
        if not name:
            print("Error: Name cannot be empty.\n")
        elif len(name) > 35:
            print("Error: Name is too long (max 35 characters).\n")
        else:
            break

    valid_genders = ['Male', 'Female', 'Non-binary', 'Other', 'Prefer not to say']

    while True:
        gender = input("Enter gender to add (Male/Female/Non-binary/Other/Prefer not to say): ").strip()
        if gender not in valid_genders:
            print("Error: Invalid gender.\n")
        else:
            break

    while True:
        degree_program = input("Enter degree program to add: ").strip()
        if not degree_program:
            print("Error: Degree program cannot be empty.\n")
        elif len(degree_program) > 100:
            print("Error: Degree program is too long (max of 500).\n")
        else:
            break

    while True:
        academic_batch = input("Enter academic batch year to add: ").strip()
        if not academic_batch.isdigit() or len(academic_batch) != 4:
            print("Error: Academic batch must be a 4-digit year.\n")
        else:
            break

    while True:
        graduation_date = input("Enter graduation date to add (YYYY-MM-DD or leave blank): ").strip()
        if graduation_date == "":
            graduation_date = None
            break
        try:
            datetime.datetime.strptime(graduation_date, "%Y-%m-%d")
            break
        except ValueError:
            print("Error: Invalid date format.\n")

    valid_semesters = ['First', 'Second']

    while True:
        graduation_semester = input("Enter graduation semester to add (First/Second or leave blank): ").strip()
        if graduation_semester == "":
            graduation_semester = None
            break
        elif graduation_semester not in valid_semesters:
            print("Error: Invalid semester.\n")
        else:
            break

    while True:
        graduation_year = input("Enter graduation year to add (YYYY or leave blank): ").strip()
        if graduation_year == "":
            graduation_year = None
            break
        elif not graduation_year.isdigit() or len(graduation_year) != 4:
            print("Error: Graduation year must be a 4-digit year.\n")
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
        print("\nMember added successfully!")
    except mysql.connector.Error as err:
        print(f"\nError: {err}")
    finally:
        conn.close()


def edit_organization():
    print("")

    while True:
        try:
            org_id = int(input("Enter Organization ID to edit: ").strip())
            if 1 <= org_id <= 99999:
                break
            else:
                print("Error: Invalid Organization ID (must be from 1 to 99999).\n")
        except ValueError:
            print("Error: Please enter a valid integer.\n")

    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM organization WHERE organization_id = %s", (org_id,))
        org = cursor.fetchone()

        if not org:
            print(f"\nNo organization found with ID {org_id}!")
            return

        print(f"\nCurrent Organization Info:")
        print(f"\n{'ID'.ljust(6)} {'Organization Name'.ljust(101)}")
        print("-" * 107)
        print(f"{str(org[0]).ljust(6)} {org[1].ljust(101)}")

        confirm = input("\nAre you sure you want to edit this organization? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("\nEdit cancelled!")
            return

        while True:
            new_name = input("\nEnter new name (leave blank to keep current): ").strip()
            if new_name == "":
                new_name = org[1]
                break
            elif len(new_name) > 100:
                print("Error: Organization name is too long (max 100 characters).\n")
            else:
                break

        new_description = input("Enter new description (leave blank to keep current or type 'BLANK' to remove it): ").strip()

        if new_description == "":
            new_description = org[2]
        if new_description.upper() == "BLANK":
            new_description = ""
        
        print(f"\nNew Organization Info:")
        print(f"\n{'ID'.ljust(6)} {'Organization Name'.ljust(101)}")
        print("-" * 107)
        print(f"{str(org[0]).ljust(6)} {new_name.ljust(101)}")

        confirm = input("\nAre you really sure you want to edit this organization? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("\nEdit cancelled!")
            return

        sql = "UPDATE organization SET name = %s, description = %s WHERE organization_id = %s"
        cursor.execute(sql, (new_name, new_description, org_id))
        conn.commit()

        print(f"\nOrganization with ID {org_id} updated successfully!")

    except mysql.connector.Error as err:
        print(f"\nError: {err}")
    finally:
        conn.close()


def edit_member():
    print("")

    while True:
        student_number = input("Enter Student Number to edit: ").strip()

        if len(student_number) != 10 or not (student_number[:4].isdigit() and student_number[4] == '-' and student_number[5:].isdigit()):
            print("Error: Student number must be in the format XXXX-XXXXX.\n")
        else:
            break

    conn = connect()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM member WHERE student_number = %s", (student_number,))
        member = cursor.fetchone()

        if not member:
            print(f"\nNo member found with student number {student_number}!")
            return

        print(f"\nCurrent Member Info:")
        print(f"{'Student Number'.ljust(15)} {'Name'.ljust(31)} {'Gender'.ljust(18)} {'Degree Program'.ljust(31)} {'Academic Batch'.ljust(16)}")
        print("-" * 116)
        print(f"{member[0].ljust(15)} {member[1].ljust(31)} {member[2].ljust(18)} {member[3].ljust(31)} {str(member[4]).ljust(16)}")

        confirm = input("\nAre you sure you want to edit this member? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("\nEdit cancelled!")
            return
        
        while True:
            new_name = input("\nEnter new name (leave blank to keep current): ").strip()
            if new_name == "":
                new_name = member[1]
                break
            elif len(new_name) > 35:
                print("Error: Name is too long (max 35 characters).\n")
            else:
                break

        valid_genders = ['Male', 'Female', 'Non-binary', 'Other', 'Prefer not to say']

        while True:
            new_gender = input("Enter new gender (Male/Female/Non-binary/Other/Prefer not to say) (leave blank to keep current): ").strip()
            if new_gender == "":
                new_gender = member[2]
                break
            elif new_gender not in valid_genders:
                print("Error: Invalid gender.\n")
            else:
                break

        while True:
            new_degree_program = input("Enter new degree program (leave blank to keep current): ").strip()
            if new_degree_program == "":
                new_degree_program = member[3]
                break
            elif len(new_degree_program) > 100:
                print("Error: Degree program is too long (max of 500).\n")
            else:
                break
        
        while True:
            new_graduation_date = input("Enter new graduation date(YYYY-MM-DD) (leave blank to keep current or type 'BLANK' to remove it): ").strip()
            if new_graduation_date == "":
                new_graduation_date = member[5]
                break
            if new_graduation_date.upper() == "BLANK":
                new_graduation_date = ""
            try:
                datetime.datetime.strptime(new_graduation_date, "%Y-%m-%d")
                break
            except ValueError:
                print("Error: Invalid date format.\n")

        valid_semesters = ['First', 'Second']

        while True:
            new_graduation_semester = input("Enter new graduation semester to add (First/Second) (leave blank to keep current or type 'BLANK' to remove it): ").strip()
            if new_graduation_semester == "":
                new_graduation_semester = member[6]
                break
            elif new_graduation_semester.upper() == "BLANK":
                new_graduation_semester = ""
                break
            elif new_graduation_semester not in valid_semesters:
                print("Error: Invalid semester.\n")
            else:
                break

        while True:
            new_graduation_year = input("Enter new graduation year to add (YYYY) (leave blank to keep current or type 'BLANK' to remove it): ").strip()
            if new_graduation_year == "":
                new_graduation_year = member[7]
                break
            elif not new_graduation_year.isdigit() or len(new_graduation_year) != 4:
                print("Error: Graduation year must be a 4-digit year.\n")
            else:
                break

        print(f"\nNew Member Info:")
        print(f"{'Student Number'.ljust(15)} {'Name'.ljust(31)} {'Gender'.ljust(18)} {'Degree Program'.ljust(31)} {'Academic Batch'.ljust(16)}")
        print("-" * 116)
        print(f"{member[0].ljust(15)} {new_name.ljust(31)} {new_gender.ljust(18)} {new_degree_program.ljust(31)} {str(member[4]).ljust(16)}")

        confirm = input("\nAre you really sure you want to edit this member? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("\nEdit cancelled!")
            return
        
        sql = "UPDATE member SET name = %s, gender = %s, degree_program = %s, graduation_date = %s, graduation_semester = %s, graduation_year = %s WHERE student_number = %s"
        cursor.execute(sql, (new_name, new_gender, new_degree_program, new_graduation_date, new_graduation_semester, new_graduation_year, student_number))
        conn.commit()

        print(f"\nMember with student number {student_number} updated successfully!")

    except mysql.connector.Error as err:
        print(f"\nError: {err}")
    finally:
        conn.close()


def delete_organization():
    print("")

    while True:
        try:
            org_id = int(input("Enter Organization ID to delete: ").strip())
            if 1 <= org_id <= 99999:
                break
            else:
                print("Error: Invalid Organization ID (must be from 1 to 99999).\n")
        except ValueError:
            print("Error: Please enter a valid integer.\n")

    conn = connect()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT * FROM organization WHERE organization_id = %s", (org_id,))
        org = cursor.fetchone()

        if not org:
            print(f"\nNo organization found with ID {org_id}!")
            return

        print(f"\nFound Organization:")
        print(f"\n{'ID'.ljust(6)} {'Organization Name'.ljust(101)}")
        print("-" * 107)
        print(f"{str(org[0]).ljust(6)} {org[1].ljust(101)}")
        
        confirm = input("\nAre you sure you want to delete this organization? (y/n): ").strip().lower()
        
        if confirm != 'y':
            print("\nDeletion cancelled!")
            return

        sql = "DELETE FROM organization WHERE organization_id = %s"
        cursor.execute(sql, (org_id,))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"\nOrganization with ID {org_id} deleted successfully!")
        else:
            print("\nError: Deletion failed!")

    except mysql.connector.Error as err:
        print(f"\nError: {err}")
    finally:
        conn.close()


def delete_member():
    print("")

    while True:
        student_number = input("Enter Student Number to delete: ").strip()

        if len(student_number) != 10 or not (student_number[:4].isdigit() and student_number[4] == '-' and student_number[5:].isdigit()):
            print("Error: Student number must be in the format XXXX-XXXXX.\n")
        else:
            break

    conn = connect()
    cursor = conn.cursor()
    
    try:
        cursor.execute("SELECT * FROM member WHERE student_number = %s", (student_number,))
        member = cursor.fetchone()

        if not member:
            print(f"\nNo member found with student number {student_number}!")
            return

        print(f"\nFound Member:")
        print(f"{'Student Number'.ljust(15)} {'Name'.ljust(31)} {'Gender'.ljust(18)} {'Degree Program'.ljust(31)} {'Academic Batch'.ljust(16)}")
        print("-" * 116)
        print(f"{member[0].ljust(15)} {member[1].ljust(31)} {member[2].ljust(18)} {member[3].ljust(31)} {member[4].ljust(16)}")

        confirm = input("\nAre you sure you want to delete this member? (y/n): ").strip().lower()
        if confirm != 'y':
            print("\nDeletion cancelled!")
            return

        cursor.execute("DELETE FROM member WHERE student_number = %s", (student_number,))
        conn.commit()

        if cursor.rowcount > 0:
            print(f"\nMember with student number {student_number} deleted successfully!")
        else:
            print("\nError: Deletion failed!")

    except mysql.connector.Error as err:
        print(f"\nError: {err}")
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
        print(f"\nError: {err}")
    finally:
        conn.close()


def show_members():
    conn = connect()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT * FROM member")
        members = cursor.fetchall()
        print(f"\n{'Student Number'.ljust(15)} {'Name'.ljust(31)} {'Gender'.ljust(18)} {'Degree Program'.ljust(31)} {'Academic Batch'.ljust(16)}")
        print("-" * 116)

        for member in members:
            student_number = str(member[0]).ljust(15)
            name = str(member[1]).ljust(31)
            gender = str(member[2]).ljust(18)
            degree = str(member[3]).ljust(31)
            batch = str(member[4]).ljust(16)
            print(f"{student_number} {name} {gender} {degree} {batch}")
    except mysql.connector.Error as err:
        print(f"\nError: {err}")
    finally:
        conn.close()
        