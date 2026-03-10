from student_analytics import (
    create_student,
    calculate_gpa,
    get_top_performers,
    generate_report,
    classify_students,
)


students = [
    create_student("Amit", "R001", math=85, python=92, ml=78, attendance=90),
    create_student("Priya", "R002", math=95, python=88, ml=91, attendance=96),
    create_student("Rohan", "R003", math=72, python=75, ml=70, attendance=82),
    create_student("Neha", "R004", math=55, python=60, ml=58, attendance=76),
]


# create_student: minimum 3 tests
s = create_student("Isha", "R010", math=80, python=90)
assert s["name"] == "Isha"
assert s["roll"] == "R010"
assert s["marks"]["math"] == 80
assert s["attendance"] == 0.0

s2 = create_student("Kabir", "R011", ml=88, attendance=85)
assert s2["marks"]["ml"] == 88
assert s2["attendance"] == 85.0

try:
    create_student("", "R012", math=90)
    assert False
except ValueError:
    assert True


# calculate_gpa: minimum 3 tests
assert calculate_gpa(85, 92, 78) == 8.5
assert calculate_gpa(100, 100, scale=4.0) == 4.0
assert calculate_gpa() == 0.0

try:
    calculate_gpa(90, -1)
    assert False
except ValueError:
    assert True


# get_top_performers: minimum 3 tests
top_one = get_top_performers(students, n=1)
assert len(top_one) == 1
assert top_one[0]["name"] == "Priya"

top_python = get_top_performers(students, n=2, subject="python")
assert len(top_python) == 2
assert top_python[0]["name"] == "Amit"

assert get_top_performers([], n=3) == []


# generate_report: minimum 3 tests
report = generate_report(students[0])
assert "Student: Amit (R001)" in report
assert "GPA:" in report
assert "Grade:" in report

report_with_rank = generate_report(students[1], rank=1)
assert "Rank: 1" in report_with_rank

verbose_report = generate_report(students[2], verbose=True, include_rank=False)
assert "Attendance:" in verbose_report
assert "Marks:" in verbose_report


# classify_students: minimum 3 tests
classified = classify_students(students)
assert set(classified.keys()) == {"A", "B", "C", "D"}
assert any(s["name"] == "Priya" for s in classified["A"])
assert any(s["name"] == "Amit" for s in classified["B"])
assert any(s["name"] == "Rohan" for s in classified["C"])
assert any(s["name"] == "Neha" for s in classified["D"])