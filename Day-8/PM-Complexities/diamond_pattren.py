"""
Day 8 PM Part C: Diamond Pattern using nested loops only.

AI prompt used:
'Write a Python program that prints a diamond pattern of asterisks.
The user inputs the number of rows for the upper half.
Include proper spacing and use nested loops only (no string multiplication tricks).'
"""


def print_diamond(n):
    """Print a diamond pattern of height (2n - 1) using nested loops."""
    if n <= 0:
        print("  Error: n must be >= 1.")
        return

    # Upper half (including middle row)
    for i in range(1, n + 1):
        # Print leading spaces
        for _ in range(n - i):
            print(" ", end="")
        # Print stars
        for _ in range(2 * i - 1):
            print("*", end="")
        print()

    # Lower half (mirror, excluding middle row)
    for i in range(n - 1, 0, -1):
        # Print leading spaces
        for _ in range(n - i):
            print(" ", end="")
        # Print stars
        for _ in range(2 * i - 1):
            print("*", end="")
        print()


def main():
    """Prompt for n and print diamond."""
    print("\n--- Diamond Pattern Generator ---\n")
    while True:
        raw = input("Enter number of rows for upper half: ").strip()
        try:
            n = int(raw)
            if n <= 0:
                print("  Error: enter a positive integer.")
                continue
            break
        except ValueError:
            print("  Error: enter a whole number.")

    print()
    print_diamond(n)


if __name__ == "__main__":
    main()
