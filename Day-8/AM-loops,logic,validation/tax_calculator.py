"""Day 8: Indian Income Tax Calculator — New Regime FY 2024-25."""

STANDARD_DEDUCTION = 75000

TAX_SLABS = [
    (300000, 0.00),
    (700000, 0.05),
    (1000000, 0.10),
    (1200000, 0.15),
    (1500000, 0.20),
    (float("inf"), 0.30),
]


def format_inr(amount):
    """Format amount with Indian number grouping."""
    is_negative = amount < 0
    amount = abs(amount)
    number_str = f"{amount:.2f}"
    integer_part, decimal_part = number_str.split(".")

    if len(integer_part) <= 3:
        grouped = integer_part
    else:
        last3 = integer_part[-3:]
        rest = integer_part[:-3]
        parts = []
        while rest:
            parts.append(rest[-2:])
            rest = rest[:-2]
        grouped = ",".join(reversed(parts)) + "," + last3

    prefix = "-" if is_negative else ""
    return f"Rs.{prefix}{grouped}.{decimal_part}"


def calc_progressive_tax(taxable_income):
    """Calculate slab-wise tax and return (total_tax, slab_breakdown list)."""
    breakdown = []
    total_tax = 0.0
    previous_limit = 0

    slab_labels = [
        "0 – 3L      (0%)",
        "3L – 7L     (5%)",
        "7L – 10L   (10%)",
        "10L – 12L  (15%)",
        "12L – 15L  (20%)",
        "Above 15L  (30%)",
    ]

    for i, (slab_limit, rate) in enumerate(TAX_SLABS):
        if taxable_income <= previous_limit:
            break

        income_in_slab = min(taxable_income, slab_limit) - previous_limit
        tax_in_slab = income_in_slab * rate
        total_tax += tax_in_slab

        breakdown.append({
            "label": slab_labels[i],
            "income": income_in_slab,
            "rate": rate,
            "tax": tax_in_slab,
        })

        previous_limit = slab_limit

    return total_tax, breakdown


def print_tax_report(annual_income):
    """Print full tax breakdown for given annual income."""
    taxable_income = max(0, annual_income - STANDARD_DEDUCTION)
    total_tax, breakdown = calc_progressive_tax(taxable_income)
    effective_rate = (total_tax / annual_income * 100) if annual_income > 0 else 0

    print("\n" + "=" * 52)
    print("       INCOME TAX BREAKDOWN (New Regime FY 2024-25)")
    print("=" * 52)
    print(f"  {'Gross Annual Income':<24}: {format_inr(annual_income)}")
    print(f"  {'Standard Deduction':<24}: {format_inr(STANDARD_DEDUCTION)}")
    print(f"  {'Taxable Income':<24}: {format_inr(taxable_income)}")
    print("-" * 52)
    print(f"  {'Slab':<22} {'Income in Slab':>14} {'Tax':>12}")
    print("-" * 52)

    for slab in breakdown:
        print(f"  {slab['label']:<22} {format_inr(slab['income']):>14} {format_inr(slab['tax']):>12}")

    print("-" * 52)
    print(f"  {'Total Tax':<22} {'':>14} {format_inr(total_tax):>12}")
    print(f"  {'Effective Tax Rate':<22} {'':>14} {effective_rate:>11.2f}%")
    print("=" * 52)


def main():
    """Collect income input and print tax report."""
    print("\n--- Indian Income Tax Calculator (New Regime FY 2024-25) ---\n")
    while True:
        raw = input("Annual Income (Rs): ").strip()
        try:
            income = float(raw)
            if income < 0:
                print("  Error: income cannot be negative.")
                continue
            break
        except ValueError:
            print("  Error: enter a valid number.")

    print_tax_report(income)


if __name__ == "__main__":
    main()
