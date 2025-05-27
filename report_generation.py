from db import connect
import mysql.connector


def print_report(columns, rows, padding=4):
    if not columns or not rows:
        print("No data to display.")
        return

    col_widths = [
        max(len(str(col)), max(len(str(row[i])) for row in rows)) + padding * 2
        for i, col in enumerate(columns)
    ]

    total_width = sum(col_widths) + 3 * len(col_widths) + 1  # spaces and separators
    border = "=" * total_width
    print(border)

    header = "|"
    for i, col in enumerate(columns):
        header += " " * padding + str(col).center(col_widths[i] - padding * 2) + " " * padding + "|"

    print(header)
    print("-" * total_width)

    for row in rows:
        row_str = "|"
        for i in range(len(columns)):
            cell = str(row[i])
            row_str += " " * padding + cell.ljust(col_widths[i] - padding * 2) + " " * padding + "|"
        print(row_str)
    print(border)


def view_members_by_org_details(organization_id):
    conn = connect()
    cursor = conn.cursor()
    try:
        query = """
        SELECT org.name AS `Organization Name`, mem.name AS `Name`, a.role AS `Role`, 
            a.membership_status AS `Status`, mem.gender AS `Gender`, 
            mem.degree_program AS `Degree Program`, 
            CASE 
                WHEN h.semester_joined = 'First' THEN SUBSTRING(h.academic_year_joined, 1, 4)
                WHEN h.semester_joined = 'Second' THEN SUBSTRING(h.academic_year_joined, 6, 4)
            END AS `Organization Batch Year`, 
            a.committee AS `Committee`
        FROM organization org
        JOIN assigns a ON org.organization_id = a.organization_id
        JOIN has h ON org.organization_id = h.organization_id AND a.student_number = h.student_number
        JOIN member mem ON mem.student_number = a.student_number
        WHERE org.organization_id = %s
        ORDER BY a.role, a.membership_status, mem.gender, mem.degree_program, 
            CASE 
                WHEN h.semester_joined = 'First' THEN SUBSTRING(h.academic_year_joined, 1, 4)
                WHEN h.semester_joined = 'Second' THEN SUBSTRING(h.academic_year_joined, 6, 4)
            END, a.committee
        """
        cursor.execute(query, (organization_id,))
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        print("\nMember Report by Organization Details:")
        print(" | ".join(columns))
        for row in results:
            print(" | ".join(str(col) for col in row))

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()

def view_unpaid_dues_by_org_semester(organization_id, semester, academic_year):
    conn = connect()
    cursor = conn.cursor()
    try:
        query = """
        SELECT org.name AS `Organization Name`, mem.name AS `Name`, f.amount AS `Amount`, 
            f.payment_status AS `Payment Status`, f.date_issued AS `Date Issued`, f.due_date AS `Due Date`
        FROM organization org
        JOIN fee f ON org.organization_id = f.organization_id
        JOIN member mem ON mem.student_number = f.student_number
        WHERE f.payment_status = 'Not Paid' 
            AND f.semester = %s 
            AND f.academic_year = %s 
            AND org.organization_id = %s
        """
        cursor.execute(query, (semester, academic_year, organization_id))
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        print("\nUnpaid Dues by Organization and Semester:")
        print(" | ".join(columns))
        for row in results:
            print(" | ".join(str(col) for col in row))

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()

def view_unpaid_dues_by_member(member_name):
    conn = connect()
    cursor = conn.cursor()
    try:
        query = """
        SELECT org.name AS `Organization Name`, mem.name AS `Name`, f.amount AS `Amount`, 
            f.payment_status AS `Payment Status`, f.date_issued AS `Date Issued`, f.due_date AS `Due Date`
        FROM member mem
        JOIN fee f ON mem.student_number = f.student_number
        JOIN organization org ON org.organization_id = f.organization_id
        WHERE f.payment_status = 'Not Paid' 
            AND mem.name = %s
        """
        cursor.execute(query, (member_name,))
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        print("\nUnpaid Dues by Member:")
        print(" | ".join(columns))
        for row in results:
            print(" | ".join(str(col) for col in row))

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()


def view_executive_committee_members():
    org_id = input("Enter Organization ID to view: ").strip()
    academic_year = input("Enter Academic Year (e.g. 2024-2025): ").strip()

    conn = connect()
    cursor = conn.cursor()
    try:
        sql = """
        SELECT org.name AS `Organization Name`, mem.name AS `Name`, a.role AS `Role`, a.semester AS `Semester`, a.academic_year AS `Academic Year`
        FROM organization org, member mem, assigns a
        WHERE org.organization_id = a.organization_id AND mem.student_number = a.student_number 
            AND a.organization_id = %s AND a.role != 'Member' AND a.academic_year = %s;
        """
        cursor.execute(sql, (org_id, academic_year))
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        print("\nExecutive Committee Members:")
        print(" | ".join(columns))
        for row in results:
            print(" | ".join(str(col) for col in row))

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()


def view_presidents_reverse_chrono():
    org_id = input("Enter Organization ID to view: ").strip()

    conn = connect()
    cursor = conn.cursor()
    try:
        sql = """
        SELECT org.name AS `Organization Name`, mem.name AS `Name`, a.semester AS `Semester`, a.academic_year AS `Academic Year`
        FROM organization org, member mem, assigns a
        WHERE org.organization_id = a.organization_id AND mem.student_number = a.student_number 
            AND a.role = 'President' AND org.organization_id = %s
        ORDER BY a.academic_year DESC, a.semester DESC;
        """
        cursor.execute(sql, (org_id,))
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        print("\nPresidents (Reverse Chronological):")
        print(" | ".join(columns))
        for row in results:
            print(" | ".join(str(col) for col in row))

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()


def view_late_payments():
    org_id = input("Enter Organization ID to view: ").strip()
    semester = input("Enter Semester (First/Second): ").strip()
    academic_year = input("Enter Academic Year (e.g. 2024-2025): ").strip()

    conn = connect()
    cursor = conn.cursor()
    try:
        sql = """
        SELECT org.name AS `Organization Name`, mem.name AS `Name`, f.fee_id AS `Fee ID`, f.payment_status AS `Payment Status`, 
            f.due_date AS `Due Date`, f.date_settled AS `Date Settled`, f.semester AS `Semester`, f.academic_year AS `Academic Year`
        FROM organization org, member mem, fee f
        WHERE org.organization_id = f.organization_id AND mem.student_number = f.student_number 
            AND org.organization_id = %s AND f.semester = %s AND f.academic_year = %s
            AND ((f.date_settled IS NOT NULL AND DATEDIFF(f.date_settled, f.due_date) > 0) OR f.date_settled IS NULL)
        ORDER BY f.date_settled IS NULL ASC, f.date_settled ASC;
        """
        cursor.execute(sql, (org_id, semester, academic_year))
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        print("\nLate Payments:")
        print(" | ".join(columns))
        for row in results:
            print(" | ".join(str(col) for col in row))

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()

def view_active_vs_inactive_percentage():
    conn = connect()
    cursor = conn.cursor()
    try:
        org_id = input("Enter Organization ID: ").strip()
        num_semesters = int(input("Enter number of recent semesters to analyze: ").strip())

        subquery = f"""
        SELECT membership_status
        FROM assigns
        WHERE organization_id = %s
        ORDER BY academic_year DESC, 
            FIELD(semester, 'Second', 'First') DESC
        LIMIT {num_semesters}
        """

        cursor.execute(f"""
        SELECT membership_status, COUNT(*) AS count
        FROM ({subquery}) AS recent
        GROUP BY membership_status
        """, (org_id,) * 2)

        results = cursor.fetchall()
        total = sum([row[1] for row in results])

        print(f"\nActive vs Inactive Members in Org ID {org_id} (Last {num_semesters} semesters):")
        for status, count in results:
            percent = (count / total) * 100 if total > 0 else 0
            print(f"{status}: {count} members ({percent:.2f}%)")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()


def view_alumni_as_of_date():
    conn = connect()
    cursor = conn.cursor()
    try:
        org_id = input("Enter Organization ID: ").strip()
        date_as_of = input("Enter cutoff date (YYYY-MM-DD): ").strip()

        query = """
        SELECT org.name AS `Organization Name`, mem.name AS `Name`, a.membership_status AS `Status`
        FROM organization org
        JOIN assigns a ON org.organization_id = a.organization_id
        JOIN member mem ON mem.student_number = a.student_number
        WHERE a.membership_status = 'Alumni'
            AND org.organization_id = %s
            AND mem.graduation_date <= %s
        """
        cursor.execute(query, (org_id, date_as_of))
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        print(f"\nAlumni Members of Organization ID {org_id} as of {date_as_of}:")
        print_report(columns, results)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()


def view_dues_summary_as_of_date():
    conn = connect()
    cursor = conn.cursor()
    try:
        org_id = input("Enter Organization ID: ").strip()
        date_as_of = input("Enter cutoff date (YYYY-MM-DD): ").strip()

        query = """
        SELECT org.name AS `Organization Name`, f.payment_status AS `Payment Status`, SUM(f.amount) AS `Total Amount`
        FROM organization org
        JOIN fee f ON org.organization_id = f.organization_id
        WHERE org.organization_id = %s AND f.date_issued <= %s
        GROUP BY f.payment_status
        """
        cursor.execute(query, (org_id, date_as_of))
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        print(f"\nDues Summary for Organization ID {org_id} as of {date_as_of}:")
        print_report(columns, results)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()


def view_highest_debt_members():
    conn = connect()
    cursor = conn.cursor()
    try:
        org_id = input("Enter Organization ID: ").strip()
        semester = input("Enter semester (First or Second): ").strip()
        acad_year = input("Enter academic year (e.g. 2023-2024): ").strip()

        query = """
        SELECT org.name AS `Organization Name`, mem.name AS `Name`, SUM(f.amount) AS `Total Debt`
        FROM organization org
        JOIN fee f ON org.organization_id = f.organization_id
        JOIN member mem ON mem.student_number = f.student_number
        WHERE org.organization_id = %s AND f.semester = %s AND f.academic_year = %s AND f.payment_status = 'Not Paid'
        GROUP BY mem.student_number
        HAVING `Total Debt` = (
            SELECT MAX(total_debt)
            FROM (
                SELECT SUM(f2.amount) AS total_debt
                FROM fee f2
                WHERE f2.organization_id = %s AND f2.semester = %s AND f2.academic_year = %s AND f2.payment_status = 'Not Paid'
                GROUP BY f2.student_number
            ) AS sub
        )
        """
        cursor.execute(query, (org_id, semester, acad_year, org_id, semester, acad_year))
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        print(f"\nMember(s) with Highest Debt in Org ID {org_id}, {semester} Semester, AY {acad_year}:")
        print_report(columns, results)

    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        conn.close()