### 1. Exact Prompt Used

> Write a Python function that takes two dictionaries representing student grades from two different semesters and produces a merged report showing: combined GPA, grade trend (improving/declining/stable), and subjects common to both semesters. Use defaultdict and dict comprehension.

---

### 2. AI-Generated Output

#### 2.1 AI Code

```python
from collections import defaultdict

def merge_student_grades(semester1, semester2):
    """
    Merge two semesters' grades into a report.
    """
    all_subjects = defaultdict(list)
    
    # Collect all grades
    for subject, grade in semester1.items():
        all_subjects[subject].append(('sem1', grade))
    
    for subject, grade in semester2.items():
        all_subjects[subject].append(('sem2', grade))
    
    # Calculate combined GPA
    total_grades = []
    common_subjects = []
    
    for subject, grades in all_subjects.items():
        if len(grades) == 2:
            common_subjects.append(subject)
        
        for _, grade in grades:
            total_grades.append(grade)
    
    combined_gpa = sum(total_grades) / len(total_grades) if total_grades else 0
    
    # Grade trend
    if common_subjects:
        sem1_avg = sum(semester1[s] for s in common_subjects) / len(common_subjects)
        sem2_avg = sum(semester2[s] for s in common_subjects) / len(common_subjects)
        
        if sem2_avg > sem1_avg:
            trend = "improving"
        elif sem2_avg < sem1_avg:
            trend = "declining"
        else:
            trend = "stable"
    else:
        trend = "no common subjects"
    
    return {
        "combined_gpa": combined_gpa,
        "grade_trend": trend,
        "common_subjects": common_subjects
    }
```