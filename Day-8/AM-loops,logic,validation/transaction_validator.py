"""Day 8 Bonus: Smart Transaction Validator — rule-based fraud detection."""

CATEGORY_LIMITS = {
    "food": 5000,
    "electronics": 30000,
    "travel": float("inf"),
    "other": float("inf"),
}

SINGLE_LIMIT = 50000
DAILY_LIMIT = 100000


def get_limits(is_vip):
    """Return (single_limit, daily_limit, category_limits) adjusted for VIP."""
    multiplier = 2 if is_vip else 1
    adjusted_categories = {k: v * multiplier for k, v in CATEGORY_LIMITS.items()}
    return SINGLE_LIMIT * multiplier, DAILY_LIMIT * multiplier, adjusted_categories


def validate_transaction(amount, category, hour, daily_spent, is_vip=False):
    """Evaluate a transaction and return a result string."""
    single_limit, daily_limit, cat_limits = get_limits(is_vip)

    # BLOCK rules — override everything
    if amount > single_limit:
        return f"BLOCKED: exceeds single transaction limit of Rs.{single_limit:,.0f}"

    if daily_spent + amount > daily_limit:
        return (
            f"BLOCKED: daily limit of Rs.{daily_limit:,.0f} would be exceeded "
            f"(Rs.{daily_spent:,.0f} already spent + Rs.{amount:,.0f} = "
            f"Rs.{daily_spent + amount:,.0f})"
        )

    # FLAG rules
    if hour < 6 or hour > 23:
        return f"FLAGGED: unusual transaction hour ({hour:02d}:00 — outside 06:00–23:00)"

    cat_limit = cat_limits.get(category, float("inf"))
    if amount > cat_limit:
        return (
            f"FLAGGED: {category} transaction of Rs.{amount:,.0f} "
            f"exceeds category limit of Rs.{cat_limit:,.0f}"
        )

    return "APPROVED"


def main():
    """Collect transaction details and print validation result."""
    print("\n--- Smart Transaction Validator ---\n")

    while True:
        raw = input("Transaction amount (Rs): ").strip()
        try:
            amount = float(raw)
            if amount <= 0:
                print("  Error: amount must be positive.")
                continue
            break
        except ValueError:
            print("  Error: enter a valid number.")

    valid_categories = list(CATEGORY_LIMITS.keys())
    while True:
        category = input(f"Category ({'/'.join(valid_categories)}): ").strip().lower()
        if category in valid_categories:
            break
        print(f"  Error: choose from {valid_categories}.")

    while True:
        raw = input("Hour of transaction (0-23): ").strip()
        try:
            hour = int(raw)
            if 0 <= hour <= 23:
                break
            print("  Error: hour must be between 0 and 23.")
        except ValueError:
            print("  Error: enter a whole number.")

    while True:
        raw = input("Amount already spent today (Rs): ").strip()
        try:
            daily_spent = float(raw)
            if daily_spent < 0:
                print("  Error: cannot be negative.")
                continue
            break
        except ValueError:
            print("  Error: enter a valid number.")

    vip_input = input("VIP customer? (yes/no): ").strip().lower()
    is_vip = vip_input == "yes"

    result = validate_transaction(amount, category, hour, daily_spent, is_vip)
    vip_tag = " [VIP — limits doubled]" if is_vip else ""
    print(f"\nTransaction: Rs.{amount:,.0f} | {category} | {hour:02d}:00{vip_tag}")
    print(f"Decision: {result}")


if __name__ == "__main__":
    main()