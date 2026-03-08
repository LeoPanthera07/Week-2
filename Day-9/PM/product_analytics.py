from collections import namedtuple

# 1️⃣ Named tuple definition (tuple creation + named fields)
# namedtuple comes from collections and creates lightweight, immutable tuple subclasses.[web:26]
Product = namedtuple("Product", ["id", "name", "category", "price"])

# Single-element tuple gotcha (just to demonstrate): requires trailing comma
single_category_tuple = ("Electronics",)  # without comma it's just a string, not a tuple

# 2️⃣ Product catalog: at least 15 products across 4 categories
CATALOG = (
    # Electronics
    Product(1, "Laptop", "Electronics", 75000),
    Product(2, "Smartphone", "Electronics", 45000),
    Product(3, "Headphones", "Electronics", 3000),
    Product(4, "Smartwatch", "Electronics", 8000),

    # Clothing
    Product(5, "T-Shirt", "Clothing", 800),
    Product(6, "Jeans", "Clothing", 2000),
    Product(7, "Jacket", "Clothing", 3500),
    Product(8, "Sneakers", "Clothing", 4000),

    # Books
    Product(9, "Clean Code", "Books", 600),
    Product(10, "Python Crash Course", "Books", 700),
    Product(11, "Deep Work", "Books", 550),
    Product(12, "Atomic Habits", "Books", 650),

    # Home
    Product(13, "Blender", "Home", 2500),
    Product(14, "Vacuum Cleaner", "Home", 5000),
    Product(15, "Table Lamp", "Home", 1500),
    Product(16, "Coffee Maker", "Home", 3200),
)

# Example of tuple unpacking with namedtuple
# for pid, name, category, price in CATALOG:
#     print(pid, name, category, price)

# Example of tuple-as-dictionary-key (Product is hashable; also normal tuples can be keys)
product_price_lookup = { (p.id, p.name): p.price for p in CATALOG }


# 3️⃣ Customer carts: each is a set of Product tuples
customer_1_cart = {
    CATALOG[0],  # Laptop
    CATALOG[2],  # Headphones
    CATALOG[5],  # Jeans
    CATALOG[9],  # Python Crash Course
    CATALOG[13], # Blender
}

customer_2_cart = {
    CATALOG[0],  # Laptop
    CATALOG[3],  # Smartwatch
    CATALOG[6],  # Jacket
    CATALOG[9],  # Python Crash Course
    CATALOG[14], # Vacuum Cleaner
}

customer_3_cart = {
    CATALOG[1],  # Smartphone
    CATALOG[2],  # Headphones
    CATALOG[7],  # Sneakers
    CATALOG[10], # Deep Work
    CATALOG[13], # Blender
}

customer_4_cart = {
    CATALOG[0],  # Laptop
    CATALOG[2],  # Headphones
    CATALOG[8],  # Clean Code
    CATALOG[11], # Atomic Habits
    CATALOG[15], # Coffee Maker
}

customer_5_cart = {
    CATALOG[0],  # Laptop
    CATALOG[2],  # Headphones
    CATALOG[5],  # Jeans
    CATALOG[10], # Deep Work
    CATALOG[15], # Coffee Maker
}

ALL_CARTS = [
    customer_1_cart,
    customer_2_cart,
    customer_3_cart,
    customer_4_cart,
    customer_5_cart,
]


# 4️⃣ Shopping behaviour analytics

def bestsellers(carts):
    """
    Products appearing in ALL carts.
    Uses set intersection.
    """
    if not carts:
        return set()
    # Start with first cart and intersect with the rest
    result = carts[0].copy()
    for c in carts[1:]:
        result &= c
    return result


def catalog_reach(carts):
    """
    Products appearing in ANY cart.
    Uses set union.
    """
    result = set()
    for c in carts:
        result |= c
    return result


def exclusive_purchases(main_cart, other_carts):
    """
    Products only main_cart bought, compared against all other carts.
    Uses set difference.
    """
    others_union = set()
    for c in other_carts:
        others_union |= c
    return main_cart - others_union


# 5️⃣ Product recommendation

def recommend_products(customer_cart, all_carts):
    """
    Recommend products that other customers bought but this customer didn't.
    Uses set difference logic on union of all carts.
    """
    union_all = set()
    for c in all_carts:
        union_all |= c
    return union_all - customer_cart


# 6️⃣ Category summary using set comprehension

def category_summary():
    """
    Return dict:
    {
      "Electronics": {"Laptop", "Smartphone", ...},
      "Books": {"Clean Code", ...},
      ...
    }
    Uses set comprehension and a dict comprehension (set comprehension syntax:
    {expr for item in iterable if condition}).[web:59]
    """
    categories = {p.category for p in CATALOG}  # set of unique categories
    return {
        category: {p.name for p in CATALOG if p.category == category}
        for category in categories
    }


# Simple demo when run directly
def _print_product_set(title, products):
    print(f"\n{title}")
    if not products:
        print("  (none)")
        return
    for p in products:
        print(f"  [{p.id}] {p.name} - {p.category} - ₹{p.price}")


if __name__ == "__main__":
    # Bestsellers: in ALL carts
    _print_product_set("Bestsellers (in all carts):", bestsellers(ALL_CARTS))

    # Catalog reach: in ANY cart
    _print_product_set("Catalog reach (in any cart):", catalog_reach(ALL_CARTS))

    # Exclusive to customer 1
    exclusive_c1 = exclusive_purchases(customer_1_cart, ALL_CARTS[1:])
    _print_product_set("Exclusive purchases (customer 1 only):", exclusive_c1)

    # Recommendations for customer 1
    recs_c1 = recommend_products(customer_1_cart, ALL_CARTS)
    _print_product_set("Recommended for customer 1:", recs_c1)

    # Category summary
    print("\nCategory summary:")
    summary = category_summary()
    for cat, names in summary.items():
        print(f"  {cat}: {sorted(names)}")
