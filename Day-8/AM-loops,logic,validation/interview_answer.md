# Day 8 — Interview Ready

## Q1: elif vs multiple if statements

### Key difference
`elif` is part of a chain — once one condition is True, all remaining
branches are skipped. Multiple `if` statements are independent — every
single one is evaluated regardless of what happened before.

### Example where they produce different output

**Input:** score = 85

**Using multiple if:**
```python
if score >= 60:
    grade = 'D'
if score >= 70:
    grade = 'C'
if score >= 80:
    grade = 'B'
if score >= 90:
    grade = 'A'
print(grade)   # Output: B
```
All four conditions are checked. score=85 satisfies the first three,
so grade is overwritten to 'D', then 'C', then 'B'. The final value is 'B'.

**Using elif:**
```python
if score >= 90:
    grade = 'A'
elif score >= 80:
    grade = 'B'
elif score >= 70:
    grade = 'C'
elif score >= 60:
    grade = 'D'
print(grade)   # Output: B
```
Once score >= 80 is True, all elif branches are skipped. grade = 'B'.

**Why the difference happens:**
Multiple `if` statements keep overwriting the variable. The last matching
condition wins. With `elif`, the first matching condition wins and the
chain stops — which is the correct behavior for mutually exclusive grades.

Note: for score=85, both produce 'B' coincidentally. The difference becomes
clear at score=95 — multiple if gives 'A' (correct), but only because >=90
happens to be last. If slabs were in ascending order with multiple if,
score=95 would incorrectly give 'D' since >=60 fires first and gets
overwritten — but wait, it still gets overwritten to 'A' since all run.
The real danger: score=85 with multiple if in ASCENDING order (as written
in Q3) gives 'B' — the last condition that fires. With elif in DESCENDING
order it gives 'B' correctly for the right reason.


## Q2: classify_triangle function

```python
def classify_triangle(a, b, c):
    """Classify a triangle given three sides."""
    # Edge case: zero or negative values
    if a <= 0 or b <= 0 or c <= 0:
        return "Not a triangle: sides must be positive"

    # Triangle inequality theorem
    if a >= b + c or b >= a + c or c >= a + b:
        return "Not a triangle: violates triangle inequality"

    if a == b == c:
        return "Equilateral"
    if a == b or b == c or a == c:
        return "Isosceles"
    return "Scalene"
```


## Q3: Debug the grading code

**Bug:** All four conditions use `if` instead of `elif`.

**Why it gives wrong output:**
score = 85 satisfies `score >= 60`, `score >= 70`, and `score >= 80` —
all three conditions are True and each one overwrites `grade`. The final
assignment wins, so grade = 'B'. For score = 95, all four fire and grade
ends up as 'A' — accidentally correct. But for score = 65, grade = 'C'
(wrong — should be 'D') because >= 60 fires first, then >= 70... wait,
65 < 70 so it stops at 'D'. Actually the real subtle bug: the conditions
are in ascending order so every condition that the score meets will
overwrite, and the LAST one to fire wins instead of the FIRST, which is
logically wrong.

**Correct fix:**
```python
if score >= 90:
    grade = 'A'
elif score >= 80:
    grade = 'B'
elif score >= 70:
    grade = 'C'
elif score >= 60:
    grade = 'D'
else:
    grade = 'F'
print(grade)
```
Use `elif` in descending order so the first matching condition wins and
the chain stops immediately.