from collections import defaultdict
from typing import Any


def create_student(name: str, roll: str, **marks: int) -> dict:
    """Create a student record.

    Args:
        name: Student name.
        roll: Student roll number.
        **marks: Subject marks as keyword arguments. You may also pass
            attendance as a keyword argument.

    Returns:
        A student dictionary with name, roll, marks, and attendance.

    Raises:
        ValueError: If name or roll is empty, or marks/attendance are invalid.
    """
    if not isinstance(name, str) or not name.strip():
        raise ValueError("name must be a non-empty string")
    if not isinstance(roll, str) or not roll.strip():
        raise ValueError("roll must be a non-empty string")

    attendance = marks.pop("attendance", 0.0)

    try:
        attendance = float(attendance)
    except (TypeError, ValueError):
        raise ValueError("attendance must be a number")

    if attendance < 0 or attendance > 100:
        raise ValueError("attendance must be between 0 and 100")

    clean_marks = {}
    for subject, score in marks.items():
        if not isinstance(subject, str) or not subject.strip():
            raise ValueError("subject names must be non-empty strings")
        if not isinstance(score, (int, float)):
            raise ValueError("marks must be numeric")
        if score < 0 or score > 100:
            raise ValueError("marks must be between 0 and 100")
        clean_marks[subject] = int(score)

    return {
        "name": name.strip(),
        "roll": roll.strip(),
        "marks": clean_marks,
        "attendance": attendance,
    }


def calculate_gpa(*marks: float, scale: float = 10.0) -> float:
    """Calculate GPA from any number of marks.

    Args:
        *marks: Variable number of numeric marks.
        scale: GPA scale. Defaults to 10.0.

    Returns:
        GPA rounded to 2 decimals.

    Raises:
        ValueError: If scale is invalid or any mark is invalid.
    """
    if scale <= 0:
        raise ValueError("scale must be greater than 0")
    if not marks:
        return 0.0

    clean_marks = []
    for mark in marks:
        if not isinstance(mark, (int, float)):
            raise ValueError("all marks must be numeric")
        if mark < 0 or mark > 100:
            raise ValueError("marks must be between 0 and 100")
        clean_marks.append(float(mark))

    avg = sum(clean_marks) / len(clean_marks)
    return round((avg / 100) * scale, 2)


def get_top_performers(
    students: list[dict],
    n: int = 5,
    subject: str | None = None,
) -> list[dict]:
    """Return top n students.

    Args:
        students: List of student dictionaries.
        n: Number of students to return.
        subject: Optional subject name for subject-wise ranking.

    Returns:
        A list of top-performing student dictionaries.
    """
    if not students or n <= 0:
        return []

    def score(student: dict) -> float:
        marks = student.get("marks", {})
        if not isinstance(marks, dict) or not marks:
            return 0.0
        if subject:
            return float(marks.get(subject, -1))
        return sum(marks.values()) / len(marks)

    ranked = sorted(students, key=score, reverse=True)
    return ranked[:n]


def generate_report(student: dict, **options: Any) -> str:
    """Generate a formatted report string.

    Args:
        student: Student dictionary.
        **options: Formatting options:
            include_rank: Whether to include rank. Defaults to True.
            include_grade: Whether to include grade. Defaults to True.
            verbose: Whether to include marks and attendance. Defaults to False.
            rank: Optional rank value to include.

    Returns:
        A formatted report string.
    """
    if not isinstance(student, dict) or not student:
        return "Invalid student record."

    include_rank = options.get("include_rank", True)
    include_grade = options.get("include_grade", True)
    verbose = options.get("verbose", False)
    rank = options.get("rank")

    name = student.get("name", "Unknown")
    roll = student.get("roll", "Unknown")
    marks = student.get("marks", {})
    attendance = student.get("attendance", 0.0)

    values = list(marks.values()) if isinstance(marks, dict) else []
    gpa = calculate_gpa(*values) if values else 0.0

    if gpa >= 9:
        grade = "A"
    elif gpa >= 8:
        grade = "B"
    elif gpa >= 6:
        grade = "C"
    else:
        grade = "D"

    parts = [f"Student: {name} ({roll})", f"GPA: {gpa}"]

    if include_grade:
        parts.append(f"Grade: {grade}")
    if include_rank and rank is not None:
        parts.append(f"Rank: {rank}")
    if verbose:
        parts.append(f"Attendance: {attendance}%")
        parts.append(f"Marks: {marks}")

    return " | ".join(parts)


def classify_students(students: list[dict]) -> dict:
    """Classify students into grade buckets.

    Args:
        students: List of student dictionaries.

    Returns:
        A dictionary with keys A, B, C, D and student lists as values.
    """
    grouped = defaultdict(list)

    for student in students:
        marks = student.get("marks", {})
        values = list(marks.values()) if isinstance(marks, dict) else []
        gpa = calculate_gpa(*values) if values else 0.0

        if gpa >= 9:
            grouped["A"].append(student)
        elif gpa >= 8:
            grouped["B"].append(student)
        elif gpa >= 6:
            grouped["C"].append(student)
        else:
            grouped["D"].append(student)

    for grade in ("A", "B", "C", "D"):
        grouped[grade]

    return dict(grouped)