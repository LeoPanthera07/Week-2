"""Day 8 AM: Student Admission Decision System."""


def get_valid_float(prompt, min_val, max_val):
    """Prompt until user enters a float within [min_val, max_val]."""
    while True:
        raw = input(prompt).strip()
        try:
            value = float(raw)
        except ValueError:
            print(f"  Error: enter a number between {min_val} and {max_val}.")
            continue
        if value < min_val or value > max_val:
            print(f"  Error: value must be between {min_val} and {max_val}.")
            continue
        return value


def get_valid_choice(prompt, choices):
    """Prompt until user enters one of the valid choices."""
    while True:
        raw = input(prompt).strip().lower()
        if raw in choices:
            return raw
        print(f"  Error: enter one of {choices}.")


def get_category_cutoff(category):
    """Return minimum entrance score for a given category."""
    if category == "general":
        return 75
    if category == "obc":
        return 65
    return 55


def apply_bonuses(entrance_score, has_recommendation, extracurricular_score):
    """Apply bonus points and return (effective_score, bonus_description)."""
    bonus = 0
    bonus_parts = []

    if has_recommendation == "yes":
        bonus += 5
        bonus_parts.append("+5 (recommendation)")

    if extracurricular_score > 8:
        bonus += 3
        bonus_parts.append("+3 (extracurricular)")

    bonus_desc = " ".join(bonus_parts) if bonus_parts else "None"
    return entrance_score + bonus, bonus_desc


def evaluate_admission(entrance_score, gpa, has_recommendation, category, extracurricular_score):
    """Evaluate and return admission decision as a formatted string."""
    # Merit rule: auto-admit with scholarship
    if entrance_score >= 95:
        return (
            "Bonus Applied: None (auto-admit triggered)\n"
            "Effective Score: " + str(entrance_score) + "\n\n"
            "Result: ADMITTED (Scholarship)\n"
            "Reason: Entrance score >= 95, automatic scholarship admission."
        )

    effective_score, bonus_desc = apply_bonuses(entrance_score, has_recommendation, extracurricular_score)
    cutoff = get_category_cutoff(category)
    category_label = category.upper()

    bonus_line = f"Bonus Applied: {bonus_desc}"
    score_line = f"Effective Score: {effective_score}"

    # GPA check
    if gpa < 7.0:
        return (
            f"{bonus_line}\n{score_line}\n\n"
            f"Result: REJECTED\n"
            f"Reason: GPA too low ({gpa} < 7.0 minimum requirement)."
        )

    # Score check
    if effective_score >= cutoff:
        return (
            f"{bonus_line}\n{score_line}\n\n"
            f"Result: ADMITTED (Regular)\n"
            f"Reason: Meets {category_label} cutoff "
            f"({effective_score} >= {cutoff}) and GPA requirement ({gpa} >= 7.0)."
        )

    # Waitlist: within 5 points of cutoff
    if effective_score >= cutoff - 5:
        return (
            f"{bonus_line}\n{score_line}\n\n"
            f"Result: WAITLISTED\n"
            f"Reason: Effective score {effective_score} is close but below "
            f"{category_label} cutoff of {cutoff}."
        )

    # Rejected
    return (
        f"{bonus_line}\n{score_line}\n\n"
        f"Result: REJECTED\n"
        f"Reason: Effective score {effective_score} does not meet "
        f"{category_label} cutoff of {cutoff}."
    )


def main():
    """Collect inputs and print admission decision."""
    print("\n--- University Admission Screening System ---\n")

    entrance_score = get_valid_float("Entrance Score (0-100): ", 0, 100)
    gpa = get_valid_float("GPA (0-10): ", 0, 10)
    has_recommendation = get_valid_choice("Recommendation letter? (yes/no): ", ["yes", "no"])
    category = get_valid_choice("Category (general/obc/sc_st): ", ["general", "obc", "sc_st"])
    extracurricular_score = get_valid_float("Extracurricular Score (0-10): ", 0, 10)

    print()
    print(evaluate_admission(entrance_score, gpa, has_recommendation, category, extracurricular_score))


if __name__ == "__main__":
    main()