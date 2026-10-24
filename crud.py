

import sqlite3

DB_NAME = "students.db"


# DATABASE CONNECTION
def connect_db():
    return sqlite3.connect(DB_NAME)


# CREATE TABLE
def create_table():
    with connect_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL DEFAULT '',
                gender TEXT NOT NULL DEFAULT '',
                age INTEGER NOT NULL DEFAULT 18,
                year INTEGER NOT NULL DEFAULT 1,
                department TEXT NOT NULL DEFAULT ''
            )
        """)

        # Add missing columns to an existing database
        columns = {
            row[1]
            for row in conn.execute(
                "PRAGMA table_info(students)"
            ).fetchall()
        }

        missing_columns = {
            "name": "TEXT NOT NULL DEFAULT ''",
            "gender": "TEXT NOT NULL DEFAULT ''",
            "age": "INTEGER NOT NULL DEFAULT 18",
            "year": "INTEGER NOT NULL DEFAULT 1",
            "department": "TEXT NOT NULL DEFAULT ''"
        }

        for column, definition in missing_columns.items():
            if column not in columns:
                conn.execute(
                    f"ALTER TABLE students ADD COLUMN "
                    f"{column} {definition}"
                )

    print("Database is ready!")


# DISPLAY ONE STUDENT
def display_student(student):
    print("\n--- STUDENT INFORMATION ---")
    print(f"Student ID : {student[0]}")
    print(f"Name       : {student[1]}")
    print(f"Gender     : {student[2]}")
    print(f"Age        : {student[3]}")
    print(f"Year       : {student[4]}")
    print(f"Department : {student[5]}")


# CREATE: ADD STUDENT
def add_student():
    try:
        student_id = int(input("Enter Student ID: "))
        if student_id <= 0:
            print("Student ID must be positive.")
            return
    except ValueError:
        print("Student ID must be a number.")
        return

    name = input("Enter name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    gender = input("Enter gender (Male/Female/Other): ").strip().title()
    if gender not in ("Male", "Female", "Other"):
        print("Enter Male, Female, or Other.")
        return

    try:
        age = int(input("Enter age: "))
        if not 1 <= age <= 120:
            print("Age must be between 1 and 120.")
            return

        year = int(input("Enter academic year (1-6): "))
        if not 1 <= year <= 6:
            print("Year must be between 1 and 6.")
            return
    except ValueError:
        print("Age and year must be numbers.")
        return

    department = input("Enter department: ").strip()
    if not department:
        print("Department cannot be empty.")
        return

    try:
        with connect_db() as conn:
            conn.execute("""
                INSERT INTO students
                    (id, name, gender, age, year, department)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                student_id, name, gender, age, year, department
            ))
        print("Student added successfully!")
    except sqlite3.IntegrityError:
        print("This Student ID already exists. Use another ID.")


# READ: VIEW ALL STUDENTS
def view_students():
    with connect_db() as conn:
        students = conn.execute("""
            SELECT id, name, gender, age, year, department
            FROM students ORDER BY id
        """).fetchall()

    if not students:
        print("No student records found.")
        return

    print("\n--- ALL STUDENTS ---")
    for student in students:
        display_student(student)


# SEARCH: FIND STUDENT BY ID
def search_student_by_id():
    try:
        student_id = int(input("Enter Student ID to search: "))
    except ValueError:
        print("Student ID must be a number.")
        return

    with connect_db() as conn:
        student = conn.execute("""
            SELECT id, name, gender, age, year, department
            FROM students WHERE id = ?
        """, (student_id,)).fetchone()

    if student:
        display_student(student)
    else:
        print("Student not found.")


# SELECT: DISPLAY STUDENT BY ID
def select_student():
    try:
        student_id = int(input("Enter Student ID to select: "))
    except ValueError:
        print("Student ID must be a number.")
        return

    with connect_db() as conn:
        student = conn.execute("""
            SELECT id, name, gender, age, year, department
            FROM students WHERE id = ?
        """, (student_id,)).fetchone()

    if student:
        display_student(student)
    else:
        print("Student not found.")


# UPDATE: EDIT STUDENT
def update_student():
    try:
        student_id = int(input("Enter Student ID to update: "))
    except ValueError:
        print("Student ID must be a number.")
        return

    with connect_db() as conn:
        student = conn.execute("""
            SELECT id, name, gender, age, year, department
            FROM students WHERE id = ?
        """, (student_id,)).fetchone()

        if student is None:
            print("Student not found.")
            return

        print("Press Enter to keep the current value.")

        name = input(f"Name [{student[1]}]: ").strip() or student[1]
        gender = input(
            f"Gender [{student[2]}]: "
        ).strip().title() or student[2]

        if gender not in ("Male", "Female", "Other"):
            print("Enter Male, Female, or Other.")
            return

        age_text = input(f"Age [{student[3]}]: ").strip()
        year_text = input(f"Year [{student[4]}]: ").strip()
        department = (
            input(f"Department [{student[5]}]: ").strip()
            or student[5]
        )

        try:
            age = int(age_text) if age_text else student[3]
            year = int(year_text) if year_text else student[4]

            if not 1 <= age <= 120:
                print("Age must be between 1 and 120.")
                return
            if not 1 <= year <= 6:
                print("Year must be between 1 and 6.")
                return
        except ValueError:
            print("Age and year must be numbers.")
            return

        conn.execute("""
            UPDATE students
            SET name = ?, gender = ?, age = ?, year = ?,
                department = ?
            WHERE id = ?
        """, (name, gender, age, year, department, student_id))

    print("Student updated successfully!")


# DELETE: REMOVE STUDENT
def delete_student():
    try:
        student_id = int(input("Enter Student ID to delete: "))
    except ValueError:
        print("Student ID must be a number.")
        return

    with connect_db() as conn:
        student = conn.execute(
            "SELECT name FROM students WHERE id = ?",
            (student_id,)
        ).fetchone()

        if student is None:
            print("Student not found.")
            return

        confirm = input(
            f"Delete {student[0]}? Type yes to confirm: "
        ).strip().lower()

        if confirm != "yes":
            print("Deletion cancelled.")
            return

        conn.execute(
            "DELETE FROM students WHERE id = ?",
            (student_id,)
        )

    print("Student deleted successfully!")


# MAIN MENU
def main():
    create_table()

    while True:
        print("\n===== STUDENT MANAGEMENT SYSTEM =====")
        print("1. Add Student")
        print("2. View All Students")
        print("3. Search Student by ID")
        print("4. Select Student by ID")
        print("5. Update Student")
        print("6. Delete Student")
        print("7. Exit")

        choice = input("Choose option (1-7): ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            view_students()
        elif choice == "3":
            search_student_by_id()
        elif choice == "4":
            select_student()
        elif choice == "5":
            update_student()
        elif choice == "6":
            delete_student()
        elif choice == "7":
            print("Thank you for using the system!")
            break
        else:
            print("Invalid choice. Enter 1-7.")


if __name__ == "__main__":
    main()
