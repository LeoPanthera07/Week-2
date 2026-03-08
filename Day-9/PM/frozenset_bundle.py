""" FOR future understanding:


frozenset notes:

- A frozenset is like a set but immutable and hashable.[web:67][web:79]
- set: mutable (you can add/remove elements), NOT hashable → cannot be a dict key.
- frozenset: immutable (no add/remove), hashable → CAN be a dict key or member of another set.[web:67][web:73][web:81]

Real-world use cases:
- Use frozenset as a dictionary key to represent an unordered group (e.g. category bundles, feature sets).[web:69][web:73]
- Use frozenset for configuration sets or permission sets that must not change at runtime.
- Use frozenset when you need set semantics + immutability (e.g. as elements inside a larger set).
"""

from __future__ import annotations

import timeit


# 2️⃣ Bundle discount system:
# Dictionary where keys are frozensets of categories, values are discount percentages.
bundle_discounts = {
    frozenset({"Electronics", "Books"}): 10,
    frozenset({"Clothing", "Home"}): 5,
    frozenset({"Electronics", "Home"}): 8,
    frozenset({"Books", "Home"}): 7,
}


def check_bundle_discount(cart_categories):
    """
    Check if the cart contains categories matching any bundle deal.

    cart_categories: iterable of category strings (e.g. {"Electronics", "Books"})
    Returns: maximum applicable discount (int), or 0 if no bundle matches.
    """
    categories = set(cart_categories)

    applicable_discounts = [
        discount
        for bundle, discount in bundle_discounts.items()
        if bundle.issubset(categories)
    ]

    return max(applicable_discounts) if applicable_discounts else 0


# 4️⃣ Performance benchmark: set vs frozenset creation speed using timeit.[web:68][web:80]
def benchmark_creation(iterations=100000):
    """
    Compare creation time of set vs frozenset using timeit (default 100000 iterations).

    This is a simple micro-benchmark: we only time object creation, not lookups.
    """

    setup_code = "values = list(range(100))"
    stmt_set = "s = set(values)"
    stmt_frozenset = "fs = frozenset(values)"

    set_time = timeit.timeit(stmt_set, setup=setup_code, number=iterations)
    frozenset_time = timeit.timeit(stmt_frozenset, setup=setup_code, number=iterations)

    print(f"set creation:       {set_time:.6f} seconds for {iterations} iterations")
    print(f"frozenset creation: {frozenset_time:.6f} seconds for {iterations} iterations")

    # Document your results here after running this function:
    #
    # Example (fill with your actual numbers):
    #   # Results on my machine (Python 3.x):
    #   # set creation:       0.012345 seconds for 100000 iterations
    #   # frozenset creation: 0.013210 seconds for 100000 iterations
    #
    # Note: performance is usually similar; both use hash-based implementations
    # with O(1) average membership lookup.[web:71][web:73]


if __name__ == "__main__":
    # Simple manual tests for the bundle checker
    cart1 = {"Electronics", "Books"}
    cart2 = {"Electronics", "Home", "Books"}
    cart3 = {"Clothing"}
    cart4 = {"Clothing", "Home"}

    print("Cart1 categories:", cart1, "=> discount:", check_bundle_discount(cart1))
    print("Cart2 categories:", cart2, "=> discount:", check_bundle_discount(cart2))
    print("Cart3 categories:", cart3, "=> discount:", check_bundle_discount(cart3))
    print("Cart4 categories:", cart4, "=> discount:", check_bundle_discount(cart4))

    print("\nBenchmarking set vs frozenset creation...")
    benchmark_creation()