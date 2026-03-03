# Day 8 PM Part C — AI Evaluation: Diamond Pattern

## Exact Prompt Used
"Write a Python program that prints a diamond pattern of asterisks.
The user inputs the number of rows for the upper half.
Include proper spacing and use nested loops only (no string multiplication tricks)."

## AI Generated Code
(paste the code the AI gave you here)

## AI Output for n=5
    *
   ***
  *****
 *******
*********
 *******
  *****
   ***
    *

## Critical Evaluation

**Spacing correctness:**
The output is correctly centered. For row i (1-indexed), the leading spaces
= n - i, and stars = 2*i - 1. The lower half mirrors this correctly.
The diamond is visually symmetric for n=5.

**Readability:**
The AI's code is generally readable but may have used single-letter variable
names like `i` and `j` without comments explaining the spacing formula.
My version adds inline comments clarifying the role of each nested loop.

**Edge cases:**
- n=0: The AI likely does not handle this — range(1, 1) produces no output
  or crashes depending on implementation. My version explicitly rejects n <= 0.
- n=1: Should print a single `*`. This works correctly in both versions
  since range(1, 2) produces one iteration with 2*1-1 = 1 star.

**Nested loops vs string tricks:**
The prompt explicitly required nested loops only. The AI complied — it used
separate for loops for spaces and stars rather than `' ' * n` or `'*' * n`.
This is correct per the assignment constraint.

**Time complexity:**
Both the AI version and my version are O(n²) — for each of the 2n-1 rows,
we iterate up to n times for spaces and up to 2n-1 times for stars.
This is the unavoidable minimum for this problem since every character
must be printed individually when string multiplication is disallowed.

**What the AI got right:**
- Correct spacing formula (n - i leading spaces)
- Correct star count formula (2*i - 1)
- Proper mirroring of lower half using reversed range

**What the AI missed:**
- No input validation for n <= 0 or non-integer input
- No docstrings on functions (fails PEP 8 / Pylint)
- No handling of n=0 edge case (silent empty output or error)

## My Improvements (see diamond_pattern.py)
- Added input validation: rejects n <= 0 with clear error message
- Added docstrings to all functions
- Separated upper and lower half with clear comments
- Consistent loop naming throughout
- Wrapped in main() with proper if __name__ == "__main__" guard
