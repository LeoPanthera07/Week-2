"""Day 8 PM Bonus: Daily Transaction Analyzer — Paytm mini dashboard."""

HIGH_VALUE_THRESHOLD = 10000
BAR_SCALE = 1000  # 1 star per Rs.1000


def print_bar(amount, tx_type, scale):
    """Print a single bar chart row scaled dynamically."""
    stars = int(amount / scale)
    if stars == 0:
        stars = 1  # show at least 1 star so bar is never empty
    bar = ""
    for _ in range(stars):
        bar += "*"
    label = "CR" if tx_type == "credit" else "DR"
    print(f"  [{label}] Rs.{amount:>10,.0f} | {bar}")



def print_summary(transactions):
    """Print full analytics summary for all transactions."""
    if not transactions:
        print("No transactions recorded.")
        return

    total_credit = 0.0
    total_debit = 0.0
    highest = 0.0
    category_totals = {}

    for tx in transactions:
        if tx["type"] == "credit":
            total_credit += tx["amount"]
        else:
            total_debit += tx["amount"]

        if tx["amount"] > highest:
            highest = tx["amount"]

        cat = tx["category"]
        if cat not in category_totals:
            category_totals[cat] = 0.0
        category_totals[cat] += tx["amount"]

    net_balance = total_credit - total_debit
    total_count = len(transactions)
    avg_amount = (total_credit + total_debit) / total_count

    print("\n" + "=" * 50)
    print("         TRANSACTION SUMMARY")
    print("=" * 50)
    print(f"  Total transactions : {total_count}")
    print(f"  Total credits      : Rs.{total_credit:,.2f}")
    print(f"  Total debits       : Rs.{total_debit:,.2f}")
    print(f"  Net balance        : Rs.{net_balance:,.2f}")
    print(f"  Highest transaction: Rs.{highest:,.2f}")
    print(f"  Average amount     : Rs.{avg_amount:,.2f}")

    print("\n  Spending by category:")
    for cat, total in category_totals.items():
        print(f"    {cat:<12}: Rs.{total:,.2f}")

    # Replace the bar chart section in print_summary with this:
    last_ten = transactions[-10:]

    # Dynamic scale: highest amount / 20 stars max
    highest_in_last_ten = max(tx["amount"] for tx in last_ten)
    scale = max(1, int(highest_in_last_ten / 20))

    print(f"\n  Bar chart (last 10 transactions | * = Rs.{scale:,}):")
    for tx in last_ten:
        print_bar(tx["amount"], tx["type"], scale)



def main():
    """Accept transactions in a while loop until user types 'done'."""
    print("\n--- Paytm Transaction Analyzer ---")
    print("Type 'done' at any prompt to finish.\n")

    transactions = []
    valid_types = ["credit", "debit"]
    valid_categories = ["food", "travel", "bills", "other"]

    while True:
        print(f"--- Transaction {len(transactions) + 1} ---")
        raw_amount = input("Amount (Rs) or 'done': ").strip().lower()

        if raw_amount == "done":
            break

        try:
            amount = float(raw_amount)
            if amount <= 0:
                print("  Error: amount must be positive.\n")
                continue
        except ValueError:
            print("  Error: enter a valid number.\n")
            continue

        tx_type = input("Type (credit/debit): ").strip().lower()
        if tx_type not in valid_types:
            print(f"  Error: choose from {valid_types}.\n")
            continue

        category = input("Category (food/travel/bills/other): ").strip().lower()
        if category not in valid_categories:
            category = "other"

        if amount > HIGH_VALUE_THRESHOLD:
            print(f"  ⚠ HIGH VALUE transaction flagged: Rs.{amount:,.2f}")

        transactions.append({
            "amount": amount,
            "type": tx_type,
            "category": category,
        })
        print("  ✓ Recorded.\n")

    print_summary(transactions)


if __name__ == "__main__":
    main()
