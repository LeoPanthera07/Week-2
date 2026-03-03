"""Type Analyzer utility — Part C Q2."""


def analyze_value(value):
    """Return a string describing a value's type, truthiness, and length."""
    type_name = type(value).__name__
    truthy = bool(value)

    try:
        length = str(len(value))
    except TypeError:
        length = "N/A"

    return f"Value: {value} | Type: {type_name} | Truthy: {truthy} | Length: {length}"


def main():
    """Run sample tests for analyze_value."""
    test_cases = [42, "", [1, 2, 3], None, 0, "False", (), {"a": 1}]
    for item in test_cases:
        print(analyze_value(item))


if __name__ == "__main__":
    main()