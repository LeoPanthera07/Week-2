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


def main():
    """Entry point: collect inputs, validate, and print report."""
    print("\n--- Personal Finance Calculator ---\n")

    name = get_valid_string("Employee name: ")
    annual_salary = get_valid_float("Annual salary (INR): ", min_value=0.01)
    tax_percent = get_valid_float("Tax bracket % (0-50): ", min_value=0.0, max_value=50.0)
    monthly_rent = get_valid_float("Monthly rent (INR): ", min_value=0.01)
    savings_percent = get_valid_float("Savings goal % (0-100): ", min_value=0.0, max_value=100.0)

    print()
    print_report(name, annual_salary, tax_percent, monthly_rent, savings_percent)


if __name__ == "__main__":
    main()