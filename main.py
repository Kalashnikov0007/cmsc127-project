import os


# --- Utility Functions ---

def get_terminal_width():
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80  # default fallback


def center_text(text, width):
    return text.center(width)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def pause():
    input("\nPress Enter to continue...")


def print_logo():
    logo_lines = [
        "▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄               ▄▄▄▄▄▄▄▄▄▄   ▄▄▄▄▄▄▄▄▄▄    ",
        "▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌▐░░░░░░░░░░░▌             ▐░░░░░░░░░░▌ ▐░░░░░░░░░░▌   ",
        "▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀▀▀              ▐░█▀▀▀▀▀▀▀█░▌▐░█▀▀▀▀▀▀▀█░▌  ",
        "▐░▌       ▐░▌▐░▌       ▐░▌▐░▌                       ▐░▌       ▐░▌▐░▌       ▐░▌  ",
        "▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌▐░▌ ▄▄▄▄▄▄▄▄  ▄▄▄▄▄▄▄▄▄▄▄ ▐░▌       ▐░▌▐░█▄▄▄▄▄▄▄█░▌  ",
        "▐░▌       ▐░▌▐░░░░░░░░░░░▌▐░▌▐░░░░░░░░▌▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░▌   ",
        "▐░▌       ▐░▌▐░█▀▀▀▀█░█▀▀ ▐░▌ ▀▀▀▀▀▀█░▌ ▀▀▀▀▀▀▀▀▀▀▀ ▐░▌       ▐░▌▐░█▀▀▀▀▀▀▀█░▌  ",
        "▐░▌       ▐░▌▐░▌     ▐░▌  ▐░▌       ▐░▌             ▐░▌       ▐░▌▐░▌       ▐░▌  ",
        "▐░█▄▄▄▄▄▄▄█░▌▐░▌      ▐░▌ ▐░█▄▄▄▄▄▄▄█░▌             ▐░█▄▄▄▄▄▄▄█░▌▐░█▄▄▄▄▄▄▄█░▌▄ ",
        "▐░░░░░░░░░░░▌▐░▌       ▐░▌▐░░░░░░░░░░░▌             ▐░░░░░░░░░░▌ ▐░░░░░░░░░░▌▐░▌",
        " ▀▀▀▀▀▀▀▀▀▀▀  ▀         ▀  ▀▀▀▀▀▀▀▀▀▀▀               ▀▀▀▀▀▀▀▀▀▀   ▀▀▀▀▀▀▀▀▀▀  ▀ "
    ]
    width = get_terminal_width()
    print("\n".join(center_text(line, width) for line in logo_lines))


def print_menu_border(title, options):
    width = get_terminal_width()
    clear_screen()
    print_logo()
    
    horizontal_border = "╔" + "═" * (width - 2) + "╗"
    horizontal_separator = "╠" + "═" * (width - 2) + "╣"
    horizontal_bottom = "╚" + "═" * (width - 2) + "╝"

    print(horizontal_border)
    print("║" + title.center(width - 2) + "║")
    print(horizontal_separator)

    for option in options:
        print("║" + option.center(width - 2) + "║")
        
    print(horizontal_bottom)


# --- Module Imports ---

from core import (
    add_organization, add_member,
    edit_organization, edit_member,
    delete_organization, delete_member,
    show_organizations, show_members,
    show_tables
)

from report_generation import (
    view_members_by_org_details,
    view_unpaid_dues_by_org_semester,
    view_unpaid_dues_by_member,
    view_executive_committee_members,
    view_presidents_reverse_chrono,
    view_late_payments,
    view_active_vs_inactive_percentage,
    view_alumni_as_of_date,
    view_highest_debt_members,
    view_dues_summary_as_of_date,
    print_report
)

from fees_assigns import (
    add_assigns, add_fee,
    show_assigns, show_fees,
    add_has, show_has
)


# --- Authentication Data and Function ---

users = {
    "admin": {"password": "admin123", "role": "admin"},
    "user": {"password": "user123", "role": "user"},
}

def login():
    clear_screen()
    print_logo()
    print("\nPlease login to continue.")
    username = input("Username: ").strip()
    password = input("Password: ").strip()

    user = users.get(username)
    if user and user["password"] == password:
        print(f"\nWelcome, {username}! You are logged in as '{user['role']}'.")
        pause()
        return user["role"]
    else:
        print("\nInvalid username or password.")
        pause()
        return None


# --- Menus ---

def core_menu():
    while True:
        clear_screen()
        options = [
            "1. Add Organization   ",
            "2. Add Member         ",
            "3. Edit Organization  ",
            "4. Edit Member        ",
            "5. Delete Organization",
            "6. Delete Member      ",
            "7. Show Organizations ",
            "8. Show Members       ",
            "9. Show Tables        ",
            "0. Back to Main Menu  "
        ]
        print_menu_border("Core Functionality Menu", options)
        choice = input("Enter choice: ")

        if choice == "1":
            add_organization()
            pause()
        elif choice == "2":
            add_member()
            pause()
        elif choice == "3":
            edit_organization()
            pause()
        elif choice == "4":
            edit_member()
            pause()
        elif choice == "5":
            delete_organization()
            pause()
        elif choice == "6":
            delete_member()
            pause()
        elif choice == "7":
            show_organizations()
            pause()
        elif choice == "8":
            show_members()
            pause()
        elif choice == "9":
            show_tables()
            pause()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")
            pause()


def report_menu():
    while True:
        clear_screen()
        options = [
            "1. View Members by Organization Details                   ",
            "2. View Unpaid Dues by Org & Semester                     ",
            "3. View Unpaid Dues by Member                             ",
            "4. View Executive Committee Members                       ",
            "5. View Presidents (Chronological)                        ",
            "6. View Late Payments                                     ",
            "7. View % of Active vs Inactive Members (Last N Semesters)",
            "8. View Alumni Members as of a Given Date                 ",
            "9. View Total Paid and Unpaid Dues as of a Given Date     ",
            "10. View Member(s) with Highest Debt by Semester          ",
            "0. Back to Main Menu                                      "
        ]
        print_menu_border("Report Generation Menu", options)
        choice = input("Enter choice: ")

        if choice == "1":
            org_id = int(input("Enter Organization ID: "))
            view_members_by_org_details(org_id)
            pause()
        elif choice == "2":
            org_id = int(input("Enter Organization ID: "))
            semester = input("Enter Semester (First/Second): ")
            academic_year = input("Enter Academic Year (e.g., 2024-2025): ")
            view_unpaid_dues_by_org_semester(org_id, semester, academic_year)
            pause()
        elif choice == "3":
            member_name = input("Enter Full Name of the Member: ")
            view_unpaid_dues_by_member(member_name)
            pause()
        elif choice == "4":
            result = view_executive_committee_members()
            if result:
                columns, rows = result
                print("\nExecutive Committee Members:")
                print_report(columns, rows)
            pause()
        elif choice == "5":
            result = view_presidents_reverse_chrono()
            if result:
                columns, rows = result
                print("\nPresidents (Reverse Chronological):")
                print_report(columns, rows)
            pause()
        elif choice == "6":
            result = view_late_payments()
            if result:
                columns, rows = result
                print("\nLate Payments:")
                print_report(columns, rows)
            pause()
        elif choice == "7":
            view_active_vs_inactive_percentage()
            pause()
        elif choice == "8":
            view_alumni_as_of_date()
            pause()
        elif choice == "9":
            view_dues_summary_as_of_date()
            pause()
        elif choice == "10":
            view_highest_debt_members()
            pause()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")
            pause()


def fees_assigns_menu():
    while True:
        clear_screen()
        options = [
            "1. Add Assigns Record  ",
            "2. Add Fee Record      ",
            "3. Add Has Record      ",
            "4. Show Assigns Records",
            "5. Show Fee Records    ",
            "6. Show Has Records    ",
            "0. Back to Main Menu   "
        ]
        print_menu_border("Fees, Assigns, Has Menu", options)
        choice = input("Enter choice: ")

        if choice == "1":
            add_assigns()
            pause()
        elif choice == "2":
            add_fee()
            pause()
        elif choice == "3":
            add_has()
            pause()
        elif choice == "4":
            show_assigns()
            pause()
        elif choice == "5":
            show_fees()
            pause()
        elif choice == "6":
            show_has()
            pause()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Try again.")
            pause()


# --- Main Loop ---

def main():
    while True:
        role = None
        while role is None:
            role = login()

        while True:
            clear_screen()
            options = ["1. Report Generation   "]
            if role == "admin":
                options.extend([
                    "2. Core Functionalities",
                    "3. Fees and Assigns    "
                ])
            options.append("0. Logout / Exit       ")

            print_menu_border("Main Menu", options)
            choice = input("Enter choice: ")

            if choice == "1":
                report_menu()
            elif choice == "2" and role == "admin":
                core_menu()
            elif choice == "3" and role == "admin":
                fees_assigns_menu()
            elif choice == "0":
                print("Logging out...")
                pause()
                break
            else:
                print("Invalid choice or insufficient permissions.")
                pause()
            
if __name__ == "__main__":
    main()
