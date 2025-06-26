import mysql.connector
import re
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="Mitali@1234",
        database="college"
    )

def register_student(cursor):
    cursor.execute("SELECT COUNT(*) FROM student")
    count = cursor.fetchone()[0] + 1
    student_id = f"STU2025{count:03d}"

    print("\n--- Student Registration ---")
    Name = input("Enter name (CAPITAL LETTERS): ")

    while True:
        Dob_input = input("Enter Date of Birth (YYYY-MM-DD): ")
        try:
            Dob = datetime.strptime(Dob_input, "%Y-%m-%d").date()
            break
        except ValueError:
            print("Invalid format. Use YYYY-MM-DD.")

    Gmail = input("Enter Gmail ID: ")
    pattern = r'^\S+@\S+\.\S+$'
    if not re.match(pattern, Gmail):
        print(" Invalid Gmail ID.")

    while True:
        Phone_input = input("Enter 10-digit phone number: ")
        if Phone_input.isdigit() and len(Phone_input) == 10:
            Phone = int(Phone_input)
            break
        else:
            print(" Invalid phone number.")

    City = input("Enter city: ")
    State = input("Enter state: ")

    Subject1 = int(input("Enter marks for Subject 1: "))
    Subject2 = int(input("Enter marks for Subject 2: "))
    Subject3 = int(input("Enter marks for Subject 3: "))
    Subject4 = int(input("Enter marks for Subject 4: "))
    Subject5 = int(input("Enter marks for Subject 5: "))

    Average = (Subject1 + Subject2 + Subject3 + Subject4 + Subject5) / 5
    
    if Average >= 90:
        Grade = 'A'
    elif Average >= 75:
        Grade = 'B'
    elif Average >= 60:
        Grade = 'C'
    else:
        Grade = 'D'

    query = """
INSERT INTO student (student_id, Name, Dob, Gmail, Phone, City, State,
                     Subject1, Subject2, Subject3, Subject4, Subject5, Average, Grade)
VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
"""

    data = (student_id, Name, Dob, Gmail, Phone, City, State,
            Subject1, Subject2, Subject3, Subject4, Subject5, Average, Grade)

    cursor.execute(query, data)
    print("\n Student registered successfully!")

def view_all_students(cursor):
    cursor.execute("SELECT * FROM student")
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print("\n Student:", row)
    else:
        print("No student records found.")

def search_student(cursor):
    name = input("Enter student name to search: ")
    cursor.execute("SELECT * FROM student WHERE Name = %s", (name,))
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print("\n Student Details:")
            print(f"ID       : {row[0]}")
            print(f"Name     : {row[1]}")
            print(f"DOB      : {row[2]}")
            print(f"Gmail    : {row[3]}")
            print(f"Phone    : {row[4]}")
            print(f"City     : {row[5]}")
            print(f"State    : {row[6]}")
            print(f"Marks    : {row[7]}, {row[8]}, {row[9]}, {row[10]}, {row[11]}")
            print(f"Average  : {row[12]}")
            print(f"Grade    : {row[13]}")
    else:
        print(" No student found with that name.")

def main():
    conn = connect_db()
    cursor = conn.cursor()

    while True:
        print("\n===== STUDENT MANAGEMENT MENU =====")
        print("1. Register Student")
        print("2. View All Students")
        print("3. Search Student by Name")
        print("4. Exit")

        choice = input("Enter your choice (1-4): ")

        if choice == '1':
            register_student(cursor)
            conn.commit()
        elif choice == '2':
            view_all_students(cursor)
        elif choice == '3':
            search_student(cursor)
        elif choice == '4':
            print("\n Exiting. Goodbye!")
            break
        else:
            print(" Invalid choice. Please try again.")

    cursor.close()
    conn.close()

if __name__ == "__main__":
    main()
