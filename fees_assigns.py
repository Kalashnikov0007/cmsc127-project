from db import connect

def add_assigns():
    student_number = input("Student Number: ")
    organization_id = int(input("Organization ID: "))
    academic_year = input("Academic Year (e.g., 2024-2025): ")
    semester = input("Semester (First/Second): ")
    membership_status = input("Membership Status (Active/Inactive/Alumni): ")
    committee = input("Committee: ")
    role = input("Role (President/Executive/Member): ")

    conn = connect()
    cursor = conn.cursor()
    sql = """
    INSERT INTO assigns
    (student_number, organization_id, academic_year, semester, membership_status, committee, role)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(sql, (student_number, organization_id, academic_year, semester, membership_status, committee, role))
        conn.commit()
        print("Assigns record added successfully.")
    except Exception as e:
        print("Error adding assigns record:", e)
    finally:
        cursor.close()
        conn.close()


def add_fee():
    amount = float(input("Amount: "))
    description = input("Description: ")
    date_issued = input("Date Issued (YYYY-MM-DD): ")
    due_date = input("Due Date (YYYY-MM-DD): ")
    date_settled = input("Date Settled (YYYY-MM-DD or leave blank): ")
    if date_settled.strip() == "":
        date_settled = None
    payment_status = input("Payment Status (Not Paid/Paid): ")
    academic_year = input("Academic Year (e.g., 2024-2025): ")
    semester = input("Semester (First/Second): ")
    organization_id = int(input("Organization ID: "))
    student_number = input("Student Number: ")

    conn = connect()
    cursor = conn.cursor()
    sql = """
    INSERT INTO fee
    (amount, description, date_issued, due_date, date_settled, payment_status, academic_year, semester, organization_id, student_number)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(sql, (amount, description, date_issued, due_date, date_settled, payment_status, academic_year, semester, organization_id, student_number))
        conn.commit()
        print("Fee record added successfully.")
    except Exception as e:
        print("Error adding fee record:", e)
    finally:
        cursor.close()
        conn.close()


def show_assigns():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM assigns")
    rows = cursor.fetchall()
    print("Assigns records:")
    for row in rows:
        print(row)
    cursor.close()
    conn.close()


def show_fees():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fee")
    rows = cursor.fetchall()
    print("Fee records:")
    for row in rows:
        print(row)
    cursor.close()
    conn.close()


def add_has():
    student_number = input("Student Number: ")
    organization_id = int(input("Organization ID: "))
    academic_year_joined = input("Academic Year Joined (e.g., 2024-2025): ")
    semester_joined = input("Semester Joined (First/Second): ")
    organization_batch = input("Organization Batch (e.g., Batch 10): ")

    conn = connect()
    cursor = conn.cursor()
    sql = """
    INSERT INTO has
    (student_number, organization_id, academic_year_joined, semester_joined, organization_batch)
    VALUES (%s, %s, %s, %s, %s)
    """
    try:
        cursor.execute(sql, (student_number, organization_id, academic_year_joined, semester_joined, organization_batch))
        conn.commit()
        print("Has record added successfully.")
    except Exception as e:
        print("Error adding has record:", e)
    finally:
        cursor.close()
        conn.close()


def show_has():
    conn = connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM has")
    rows = cursor.fetchall()
    print("Has records:")
    for row in rows:
        print(row)
    cursor.close()
    conn.close()