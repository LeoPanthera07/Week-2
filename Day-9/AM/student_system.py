import os

FILENAME = "students.txt"

# Default in-memory data: at least 10 students across 3 subjects
DEFAULT_RECORDS = [
    ["Aman", "Math", 88],
    ["Priya", "Physics", 91],
    ["Rahul", "Math", 76],
    ["Sneha", "Chemistry", 84],
    ["Karan", "Physics", 67],
    ["Anita", "Math", 93],
    ["Vijay", "Chemistry", 72],
    ["Meera", "Physics", 89],
    ["Rohit", "Math", 65],
    ["Divya", "Chemistry", 95],
]

# Global records list: list of [name, subject, marks]
records = []


def load_records(filename=FILENAME):
    """Load records from file if it exists, else use defaults."""
    global records
    if not os.path.exists(filename):
        # Use a shallow copy of default rows (demonstrates slicing)
        records = [row[:] for row in DEFAULT_RECORDS]
        return

    loaded = []
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            parts = line.split(",")
            if len(parts) != 3:
                continue
            name, subject, marks_str = parts
            try:
                marks = int(marks_str)
            except ValueError:
                continue
            loaded.append([name, subject, marks])

    if loaded:
        records = loaded
    else:
        records = [row[:] for row in DEFAULT_RECORDS]


def save_records(filename=FILENAME):
    """Save current records to file."""
    with open(filename, "w", encoding="utf-8") as f:
        for name, subject, marks in records:
            f.write(f"{name},{subject},{marks}\n")


def add_student(name, subject, marks):
    """Add a student if (name, subject) is not already present."""
    global records
    # Prevent duplicate name + subject
    exists = any(
        (r[0].lower() == name.lower() and r[1].lower() == subject.lower())
        for r in records
    )
    if exists:
        print("Student with this name and subject already exists.")
        return False

    records.append([name, subject, marks])  # uses append
    print("Student added.")
    return True


def get_toppers(subject):
    """Return top 3 students for a subject sorted by marks desc."""
    subject_lower = subject.lower()
    subject_records = [r for r in records if r[1].lower() == subject_lower]

    # sorted(..., key=..., reverse=True)
    sorted_records = sorted(subject_records, key=lambda x: x[2], reverse=True)

    # slicing to get top 3
    return sorted_records[:3]


def class_average(subject):
    """Return average marks for a subject, or None if no records."""
    subject_lower = subject.lower()
    marks_list = [r[2] for r in records if r[1].lower() == subject_lower]
    if not marks_list:
        return None
    return sum(marks_list) / len(marks_list)


def above_average_students():
    """
    Return students scoring above overall class average.
    Uses comprehensions and nested logic.
    """
    if not records:
        return []

    all_marks = [r[2] for r in records]
    overall_avg = sum(all_marks) / len(all_marks)

    # Nested logic in comprehension
    above = [r for r in records if r[2] > overall_avg]
    return above


def remove_student(name):
    """
    Remove all records for a given student name.
    Do NOT use remove() in a loop. Use filter with comprehension.
    """
    global records
    name_lower = name.lower()
    new_records = [r for r in records if r[0].lower() != name_lower]
    removed_count = len(records) - len(new_records)
    records = new_records
    return removed_count


def print_records(rec_list):
    """Helper to print a list of records nicely."""
    if not rec_list:
        print("No records found.")
        return
    for name, subject, marks in rec_list:
        print(f"{name:10s} | {subject:10s} | {marks}")


def menu():
    load_records()

    while True:
        print("\n--- Student Management System ---")
        print("1. Add student")
        print("2. Show toppers (by subject)")
        print("3. Show class average (by subject)")
        print("4. Show above-average students (overall)")
        print("5. Remove student (by name)")
        print("6. Exit")

        choice = input("Enter choice (1-6): ").strip()

        if choice == "1":
            name = input("Name: ").strip()
            subject = input("Subject: ").strip()
            marks_input = input("Marks (0-100): ").strip()
            try:
                marks = int(marks_input)
            except ValueError:
                print("Invalid marks. Must be an integer.")
                continue
            add_student(name, subject, marks)

        elif choice == "2":
            subject = input("Enter subject: ").strip()
            toppers = get_toppers(subject)
            print(f"Top students in {subject}:")
            print_records(toppers)

        elif choice == "3":
            subject = input("Enter subject: ").strip()
            avg = class_average(subject)
            if avg is None:
                print("No records for this subject.")
            else:
                print(f"Average marks in {subject}: {avg:.2f}")

        elif choice == "4":
            above = above_average_students()
            print("Students above overall class average:")
            print_records(above)

        elif choice == "5":
            name = input("Enter student name to remove: ").strip()
            removed = remove_student(name)
            if removed == 0:
                print("No records found for this student.")
            else:
                print(f"Removed {removed} record(s) for {name}.")

        elif choice == "6":
            save_records()
            print("Records saved to students.txt. Exiting...")
            break

        else:
            print("Invalid choice. Please select 1-6.")


if __name__ == "__main__":
    menu()
