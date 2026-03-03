"""Day 8 PM: Password Strength Analyzer and Generator."""

import random
import string

SPECIAL_CHARS = "!@#$%^&*"


def analyze_password(password):
    """
    Analyze password strength and return (score, missing_list).

    Scoring:
      Length >= 8  → +1, >= 12 → +2, >= 16 → +3
      Has uppercase → +1
      Has lowercase → +1
      Has digit     → +1
      Has special   → +1
      No char repeated > 2 in a row → +1
    """
    score = 0
    missing = []

    # Length scoring
    if len(password) >= 16:
        score += 3
    elif len(password) >= 12:
        score += 2
    elif len(password) >= 8:
        score += 1
    else:
        missing.append("too short (need >= 8 chars)")

    # Character type checks using for loop
    has_upper = False
    has_lower = False
    has_digit = False
    has_special = False

    for char in password:
        if char.isupper():
            has_upper = True
        if char.islower():
            has_lower = True
        if char.isdigit():
            has_digit = True
        if char in SPECIAL_CHARS:
            has_special = True

    if has_upper:
        score += 1
    else:
        missing.append("uppercase")

    if has_lower:
        score += 1
    else:
        missing.append("lowercase")

    if has_digit:
        score += 1
    else:
        missing.append("digit")

    if has_special:
        score += 1
    else:
        missing.append("special char (!@#$%^&*)")

    # No more than 2 repeated characters in a row
    no_repeat = True
    for i in range(len(password) - 2):
        if password[i] == password[i + 1] == password[i + 2]:
            no_repeat = False
            break

    if no_repeat:
        score += 1
    else:
        missing.append("3+ repeated chars in a row")

    return score, missing


def get_rating(score):
    """Return strength rating label for a given score."""
    if score >= 7:
        return "Very Strong"
    if score >= 5:
        return "Strong"
    if score >= 3:
        return "Medium"
    return "Weak"


def generate_password(length):
    """Generate a random password of given length using all character types."""
    char_pool = string.ascii_letters + string.digits + string.punctuation
    password = ""
    for _ in range(length):
        password += random.choice(char_pool)
    return password


def print_analysis(password):
    """Print full strength analysis for a given password."""
    score, missing = analyze_password(password)
    rating = get_rating(score)
    print(f">> Strength: {score}/7 ({rating})")
    if missing:
        print(f">> Missing: {', '.join(missing)}")
    return score


def run_analyzer():
    """Use a while loop to keep asking for input until strength >= 5."""
    print("\n--- Password Strength Analyzer ---\n")
    while True:
        password = input("Enter password: ").strip()
        score = print_analysis(password)
        if score >= 5:
            print(">> Password accepted!\n")
            break
        print(">> Try again...\n")


def run_generator():
    """Generate a random password and display its strength analysis."""
    print("\n--- Password Generator ---\n")
    while True:
        raw = input("Enter desired password length: ").strip()
        try:
            length = int(raw)
            if length < 1:
                print("  Error: length must be at least 1.")
                continue
            break
        except ValueError:
            print("  Error: enter a whole number.")

    password = generate_password(length)
    print(f"\nGenerated password: {password}")
    print_analysis(password)


def main():
    """Main entry point — choose analyzer or generator."""
    print("\n=== Password Tool ===")
    print("1. Analyze a password")
    print("2. Generate a password")
    choice = input("Choose (1 or 2): ").strip()

    if choice == "2":
        run_generator()
    else:
        run_analyzer()


if __name__ == "__main__":
    main()