"""
Day 8: PAN Card Validator — improved version.

PAN format: 5 uppercase letters + 4 digits + 1 uppercase letter
4th character indicates taxpayer type:
  P = Individual, C = Company, H = HUF, F = Firm,
  A = AOP, B = BOI, G = Government, J = Artificial Juridical Person,
  L = Local Authority, T = Trust
"""

TAXPAYER_TYPES = {
    "P": "Individual",
    "C": "Company",
    "H": "Hindu Undivided Family (HUF)",
    "F": "Firm",
    "A": "Association of Persons (AOP)",
    "B": "Body of Individuals (BOI)",
    "G": "Government",
    "J": "Artificial Juridical Person",
    "L": "Local Authority",
    "T": "Trust",
}


def validate_pan(pan):
    """
    Validate a PAN card number and return (is_valid, message).

    Format: AAAAA9999A — 5 uppercase letters, 4 digits, 1 uppercase letter.
    """
    pan = pan.strip().upper()

    if len(pan) != 10:
        return False, f"Invalid length: expected 10 characters, got {len(pan)}."

    for i in range(5):
        if not pan[i].isalpha():
            return False, f"Position {i+1} must be a letter, got '{pan[i]}'."

    for i in range(5, 9):
        if not pan[i].isdigit():
            return False, f"Position {i+1} must be a digit, got '{pan[i]}'."

    if not pan[9].isalpha():
        return False, f"Position 10 must be a letter, got '{pan[9]}'."

    taxpayer_char = pan[3]
    taxpayer_type = TAXPAYER_TYPES.get(taxpayer_char, "Unknown")

    return True, f"Valid PAN. Taxpayer type (4th char '{taxpayer_char}'): {taxpayer_type}."


def main():
    """Prompt for PAN and print validation result."""
    print("\n--- PAN Card Validator ---\n")
    pan = input("Enter PAN number: ").strip()
    is_valid, message = validate_pan(pan)
    status = "VALID" if is_valid else "INVALID"
    print(f"\nResult: {status}")
    print(f"Details: {message}")


if __name__ == "__main__":
    main()