from collections import defaultdict


# Data structure: catalog = {sku: {name, price, category, stock, rating, tags: [...]}}
CATALOG = {
    # Electronics
    'SKU001': {'name': 'Laptop', 'price': 65000, 'category': 'electronics', 'stock': 15, 'rating': 4.5, 'tags': ['computer', 'work']},
    'SKU002': {'name': 'Smartphone', 'price': 45000, 'category': 'electronics', 'stock': 8, 'rating': 4.2, 'tags': ['phone', 'mobile']},
    'SKU003': {'name': 'Headphones', 'price': 3000, 'category': 'electronics', 'stock': 25, 'rating': 4.1, 'tags': ['audio', 'wireless']},
    'SKU004': {'name': 'Tablet', 'price': 25000, 'category': 'electronics', 'stock': 12, 'rating': 4.0, 'tags': ['tablet', 'work']},

    # Clothing
    'SKU005': {'name': 'T-Shirt', 'price': 800, 'category': 'clothing', 'stock': 100, 'rating': 3.8, 'tags': ['casual', 'cotton']},
    'SKU006': {'name': 'Jeans', 'price': 2000, 'category': 'clothing', 'stock': 50, 'rating': 4.0, 'tags': ['denim', 'casual']},
    'SKU007': {'name': 'Jacket', 'price': 3500, 'category': 'clothing', 'stock': 30, 'rating': 4.3, 'tags': ['winter', 'formal']},
    'SKU008': {'name': 'Sneakers', 'price': 4000, 'category': 'clothing', 'stock': 40, 'rating': 4.2, 'tags': ['sports', 'running']},

    # Books
    'SKU009': {'name': 'Clean Code', 'price': 600, 'category': 'books', 'stock': 75, 'rating': 4.7, 'tags': ['programming', 'software']},
    'SKU010': {'name': 'Python Crash Course', 'price': 700, 'category': 'books', 'stock': 60, 'rating': 4.6, 'tags': ['python', 'programming']},
    'SKU011': {'name': 'Deep Work', 'price': 550, 'category': 'books', 'stock': 80, 'rating': 4.4, 'tags': ['productivity', 'self-help']},
    'SKU012': {'name': 'Atomic Habits', 'price': 650, 'category': 'books', 'stock': 90, 'rating': 4.5, 'tags': ['habits', 'self-help']},

    # Food
    'SKU013': {'name': 'Organic Almonds', 'price': 500, 'category': 'food', 'stock': 200, 'rating': 4.1, 'tags': ['nuts', 'organic']},
    'SKU014': {'name': 'Dark Chocolate', 'price': 300, 'category': 'food', 'stock': 150, 'rating': 4.3, 'tags': ['chocolate', 'snack']},
    'SKU015': {'name': 'Green Tea', 'price': 250, 'category': 'food', 'stock': 120, 'rating': 4.0, 'tags': ['tea', 'health']},
    'SKU016': {'name': 'Protein Bar', 'price': 150, 'category': 'food', 'stock': 180, 'rating': 4.2, 'tags': ['protein', 'snack']},
}


# All functions use .get() for safe access and handle edge cases

def search_by_tag(tag):
    """
    Returns all products containing that tag.
    Uses defaultdict(list) to group by tag.
    """
    tag_products = defaultdict(list)
    for sku, product in CATALOG.items():
        tags = product.get('tags', [])
        if tag.lower() in [t.lower() for t in tags]:
            tag_products[sku].append(product)
    return dict(tag_products)


def out_of_stock():
    """
    Returns products with stock == 0 using dict comprehension with filter.
    """
    return {
        sku: product
        for sku, product in CATALOG.items()
        if product.get('stock', 0) == 0
    }


def price_range(min_price, max_price):
    """
    Filter products by price range using dict comprehension.
    """
    return {
        sku: product
        for sku, product in CATALOG.items()
        if min_price <= product.get('price', 0) <= max_price
    }


def category_summary():
    """
    For each category: count, avg price, avg rating.
    Uses defaultdict(list) to collect prices and ratings.
    """
    summary = defaultdict(lambda: {'prices': [], 'ratings': []})
    
    for product in CATALOG.values():
        cat = product.get('category', 'unknown')
        summary[cat]['prices'].append(product.get('price', 0))
        summary[cat]['ratings'].append(product.get('rating', 0))
    
    result = {}
    for cat, data in summary.items():
        prices = data['prices']
        ratings = data['ratings']
        result[cat] = {
            'count': len(prices),
            'avg_price': sum(prices) / len(prices) if prices else 0,
            'avg_rating': sum(ratings) / len(ratings) if ratings else 0,
        }
    
    return result


def apply_discount(category, percent):
    """
    Reduce prices for a category by percent (returns NEW catalog slice).
    Uses dict comprehension to create new prices.
    """
    return {
        sku: {
            **product,  # copy all fields
            'price': product.get('price', 0) * (1 - percent / 100)
        }
        for sku, product in CATALOG.items()
        if product.get('category', '') == category
    }


def merge_catalogs(catalog1, catalog2):
    """
    Merge two catalogs, handling duplicate SKUs.
    catalog2 overwrites catalog1 for duplicate SKUs.
    Uses | operator (Python 3.9+).
    """
    return catalog1 | catalog2


# Demo
if __name__ == "__main__":
    print("=== Out of stock:", out_of_stock())
    print("=== Electronics summary:", category_summary()['electronics'])
    print("=== Price range 1000-5000:", len(price_range(1000, 5000)), "products")
    print("=== Laptop tag search:", len(search_by_tag('computer')))
    print("=== Clothing 10% discount:", list(apply_discount('clothing', 10).values())[0])
