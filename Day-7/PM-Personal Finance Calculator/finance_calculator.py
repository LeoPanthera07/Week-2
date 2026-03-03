"""Personal Finance Calculator for employee benefits portal."""

LINE_EQ = "=" * 44
LINE_DASH = "-" * 44


def format_indian_number(value):
    """Format a number using Indian comma grouping with 2 decimal places."""
    is_negative = value < 0
    value = abs(value)

    number_str = f"{value:.2f}"
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
    return f"{prefix}{grouped}.{decimal_part}"


def format_inr(amount):
    """Format a float as INR currency with Indian number grouping."""
    return f"Rs.{format_indian_number(amount)}"


def get_valid_string(prompt):
    """Prompt until user enters a non-empty string."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("  Error: value cannot be empty. Try again.")


def get_valid_float(prompt, min_value=None, max_value=None):
    """Prompt until user enters a float within the optional [min_value, max_value] range."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            print("  Error: please enter a valid number (e.g. 1200000).")
            continue

        if min_value is not None and value < min_value:
            print(f"  Error: value must be >= {min_value}. Try again.")
            continue
        if max_value is not None and value > max_value:
            print(f"  Error: value must be <= {max_value}. Try again.")
            continue

        return value


def calc_monthly_salary(annual_salary):
    """Return monthly gross salary from annual salary."""
    return annual_salary / 12.0


def calc_tax(gross_monthly, tax_percent):
    """Return monthly tax deduction."""
    return gross_monthly * (tax_percent / 100.0)


def calc_net_salary(gross_monthly, monthly_tax):
    """Return net monthly salary after tax."""
    return gross_monthly - monthly_tax


def calc_savings(net_monthly, savings_percent):
    """Return monthly savings amount."""
    return net_monthly * (savings_percent / 100.0)


def calc_disposable(net_monthly, monthly_rent, monthly_savings):
    """Return disposable income after rent and savings."""
    return net_monthly - monthly_rent - monthly_savings


def calc_rent_ratio(monthly_rent, net_monthly):
    """Return rent as a percentage of net salary."""
    if net_monthly == 0:
        return 0.0
    return (monthly_rent / net_monthly) * 100.0


def print_report(name, annual_salary, tax_percent, monthly_rent, savings_percent):
    """Compute all values and print the formatted financial summary report."""
    gross_monthly = calc_monthly_salary(annual_salary)
    monthly_tax = calc_tax(gross_monthly, tax_percent)
    net_monthly = calc_net_salary(gross_monthly, monthly_tax)
    rent_ratio = calc_rent_ratio(monthly_rent, net_monthly)
    monthly_savings = calc_savings(net_monthly, savings_percent)
    disposable = calc_disposable(net_monthly, monthly_rent, monthly_savings)

    annual_tax = monthly_tax * 12.0
    annual_savings = monthly_savings * 12.0
    annual_rent = monthly_rent * 12.0

    print(LINE_EQ)
    print("       EMPLOYEE FINANCIAL SUMMARY")
    print(LINE_EQ)
    print(f"{'Employee':<16}: {name}")
    print(f"{'Annual Salary':<16}: {format_inr(annual_salary)}")
    print(LINE_DASH)
    print("Monthly Breakdown:")
    print(f"  {'Gross Salary':<14}: {format_inr(gross_monthly)}")
    print(f"  {'Tax (' + str(tax_percent) + '%)':<14}: {format_inr(monthly_tax)}")
    print(f"  {'Net Salary':<14}: {format_inr(net_monthly)}")
    print(f"  {'Rent':<14}: {format_inr(monthly_rent)}  ({rent_ratio:.1f}% of net)")
    print(f"  {'Savings (' + str(savings_percent) + '%)':<14}: {format_inr(monthly_savings)}")
    print(f"  {'Disposable':<14}: {format_inr(disposable)}")
    print(LINE_DASH)
    print("Annual Projection:")
    print(f"  {'Total Tax':<14}: {format_inr(annual_tax)}")
    print(f"  {'Total Savings':<14}: {format_inr(annual_savings)}")
    print(f"  {'Total Rent':<14}: {format_inr(annual_rent)}")
    print(LINE_EQ)

def calc_health_score(rent_ratio, savings_percent, disposable, net_monthly):
    """Calculate a financial health score out of 100 based on rent ratio, savings, and disposable income."""
    score = 0

    # Rent ratio score (40 pts)
    if rent_ratio < 30:
        score += 40
    elif rent_ratio <= 40:
        score += 20
    else:
        score += 0

    # Savings rate score (30 pts)
    if savings_percent >= 20:
        score += 30
    elif savings_percent >= 10:
        score += 15
    else:
        score += 0

    # Disposable income score (30 pts)
    disposable_ratio = calc_rent_ratio(disposable, net_monthly)
    if disposable_ratio >= 30:
        score += 30
    elif disposable_ratio >= 15:
        score += 15
    else:
        score += 0

    return score


def collect_employee_data(label):
    """Prompt and collect all inputs for one employee."""
    print(f"\n--- Enter details for {label} ---")
    name = get_valid_string("Employee name: ")
    annual_salary = get_valid_float("Annual salary (INR): ", min_value=0.01)
    tax_percent = get_valid_float("Tax bracket % (0-50): ", min_value=0.0, max_value=50.0)
    monthly_rent = get_valid_float("Monthly rent (INR): ", min_value=0.01)
    savings_percent = get_valid_float("Savings goal % (0-100): ", min_value=0.0, max_value=100.0)
    return name, annual_salary, tax_percent, monthly_rent, savings_percent


def compute_summary(annual_salary, tax_percent, monthly_rent, savings_percent):
    """Return a dict of all computed financial values for one employee."""
    gross_monthly = calc_monthly_salary(annual_salary)
    monthly_tax = calc_tax(gross_monthly, tax_percent)
    net_monthly = calc_net_salary(gross_monthly, monthly_tax)
    rent_ratio = calc_rent_ratio(monthly_rent, net_monthly)
    monthly_savings = calc_savings(net_monthly, savings_percent)
    disposable = calc_disposable(net_monthly, monthly_rent, monthly_savings)
    health_score = calc_health_score(rent_ratio, savings_percent, disposable, net_monthly)

    return {
        "gross_monthly": gross_monthly,
        "monthly_tax": monthly_tax,
        "net_monthly": net_monthly,
        "rent_ratio": rent_ratio,
        "monthly_savings": monthly_savings,
        "disposable": disposable,
        "annual_tax": monthly_tax * 12,
        "annual_savings": monthly_savings * 12,
        "annual_rent": monthly_rent * 12,
        "health_score": health_score,
    }


def print_comparison(name1, data1, rent1, savings_pct1, name2, data2, rent2, savings_pct2):
    """Print a side-by-side comparison table of two employees."""
    col = 20
    print("\n" + "=" * 64)
    print("          EMPLOYEE COMPARISON TABLE")
    print("=" * 64)
    print(f"{'Metric':<22} {name1:>{col}} {name2:>{col}}")
    print("-" * 64)

    rows = [
        ("Gross Monthly",   format_inr(data1["gross_monthly"]),    format_inr(data2["gross_monthly"])),
        ("Monthly Tax",     format_inr(data1["monthly_tax"]),      format_inr(data2["monthly_tax"])),
        ("Net Salary",      format_inr(data1["net_monthly"]),      format_inr(data2["net_monthly"])),
        ("Rent",            format_inr(rent1),                     format_inr(rent2)),
        ("Rent Ratio",      f"{data1['rent_ratio']:.1f}%",         f"{data2['rent_ratio']:.1f}%"),
        ("Savings %",       f"{savings_pct1:.1f}%",                f"{savings_pct2:.1f}%"),
        ("Monthly Savings", format_inr(data1["monthly_savings"]),  format_inr(data2["monthly_savings"])),
        ("Disposable",      format_inr(data1["disposable"]),       format_inr(data2["disposable"])),
        ("Annual Tax",      format_inr(data1["annual_tax"]),       format_inr(data2["annual_tax"])),
        ("Annual Savings",  format_inr(data1["annual_savings"]),   format_inr(data2["annual_savings"])),
        ("Health Score",    f"{data1['health_score']}/100",        f"{data2['health_score']}/100"),
    ]

    for label, val1, val2 in rows:
        print(f"  {label:<20} {val1:>{col}} {val2:>{col}}")

    print("=" * 64)


def main_comparison():
    """Entry point for 2-employee comparison mode."""
    print("\n=== Two-Employee Financial Comparison ===")

    name1, sal1, tax1, rent1, sav1 = collect_employee_data("Employee 1")
    name2, sal2, tax2, rent2, sav2 = collect_employee_data("Employee 2")

    data1 = compute_summary(sal1, tax1, rent1, sav1)
    data2 = compute_summary(sal2, tax2, rent2, sav2)

    print_report(name1, sal1, tax1, rent1, sav1)
    print_report(name2, sal2, tax2, rent2, sav2)
    print_comparison(name1, data1, rent1, sav1, name2, data2, rent2, sav2)


def main():
    """Entry point: choose single employee report or two-employee comparison."""
    print("\n--- Personal Finance Calculator ---")
    print("1. Single employee report")
    print("2. Two-employee comparison")
    choice = input("Choose (1 or 2): ").strip()

    if choice == "2":
        main_comparison()
    else:
        print("\n--- Single Employee Mode ---\n")
        name = get_valid_string("Employee name: ")
        annual_salary = get_valid_float("Annual salary (INR): ", min_value=0.01)
        tax_percent = get_valid_float("Tax bracket % (0-50): ", min_value=0.0, max_value=50.0)
        monthly_rent = get_valid_float("Monthly rent (INR): ", min_value=0.01)
        savings_percent = get_valid_float("Savings goal % (0-100): ", min_value=0.0, max_value=100.0)
        print()
        print_report(name, annual_salary, tax_percent, monthly_rent, savings_percent)

if __name__ == "__main__":
    main()