# Part C — Interview Ready

## Q1 — Tuple Mutability Trap

**Question**

Given:

```python
t = (, )
```

Can we run:

```python
t = 99
```

Explain:

- Why it works or fails  
- What this reveals about tuple immutability  

---

**Answer**

Yes, `t[0][0] = 99` **works** and does **not** raise an error.

- `t` is a tuple of two elements.  
- Each element is a **list**, and lists are mutable.[web:86][web:96]  
- Tuple immutability means you **cannot change which objects** the tuple indices point to (you cannot do `t[0] = [9, 9]`), but you *can* mutate the object stored at that index if that object itself is mutable (like a list).[web:82][web:84]

Example:

```python
t = (, )

t = 99   # mutate the inner list, not the tuple slot

print(t)       # (, )
```

What this reveals:

- Tuples are immutable at the **container level**: you cannot reassign, append, remove, or replace elements in the tuple.[web:94][web:96]  
- But tuples can **contain mutable objects**, and those objects can change their internal state. The tuple still points to the same list object; only the list’s contents changed.[web:82][web:84]

This is the classic trap: “tuple immutable” does **not** mean “everything reachable from the tuple is immutable”.

---

## Q2 — Coding: Duplicate Detection

**Question**

Write:

```python
def find_duplicates(lst):
    ...
```

Return a **set** of elements appearing more than once.

Rules:

- Use **set operations only**
- No `Counter`
- No nested counting loops
- Target complexity: **O(n)**

---

**Answer**

We can use two sets:

- `seen` for elements we have seen once  
- `duplicates` for elements we see again  

Set membership tests are average \(O(1)\), so the whole function is \(O(n)\) in the length of `lst`.[web:69][web:91]

```python
def find_duplicates(lst):
    seen = set()
    duplicates = set()

    for item in lst:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)

    return duplicates


# Examples:
# find_duplicates() -> {2, 3}
# find_duplicates(['a', 'b', 'a', 'c', 'b']) -> {'a', 'b'}
```

This uses only:

- `set()` creation  
- membership `in`  
- `add()`  

No counters, no nested loops.

---

## Q3 — Debug: `unique_to_each`

**Question**

Buggy code:

```python
def unique_to_each(a, b):
    result = set(a) - set(b)
    return list(result)

print(unique_to_each(, ))
```

Expected:

```
undefined
```

Actual:

```
undefined
```

Tasks:

- Explain why this happens  
- Fix the function  

---

**Answer**

### Why the bug happens

- `set(a) - set(b)` computes the **difference**: elements in `a` that are **not** in `b`.[web:91]  
- For `a = [1, 2, 3]`, `b = [3, 4, 5]`:

  - `set(a) = {1, 2, 3}`  
  - `set(b) = {3, 4, 5}`  
  - `set(a) - set(b) = {1, 2}` (only the elements unique to `a`)  

- This completely ignores elements that are **unique to `b`** (i.e. `4` and `5`), so you only get `[1, 2]`.

The expected behaviour is “elements unique to **each** list”, which is the **symmetric difference**: items that are in either `a` or `b` but not in both.[web:87][web:89][web:91]

### Corrected function using symmetric difference

We should use:

- `set(a) ^ set(b)` or  
- `set(a).symmetric_difference(set(b))`  

Both compute the symmetric difference: elements in exactly one of the sets.[web:87][web:89][web:91]

```python
def unique_to_each(a, b):
    """
    Return elements that are unique to each list:
    present in a or b, but not in both.
    """
    return list(set(a) ^ set(b))


# Example:
# unique_to_each(, ) ->  (order may vary)
```

This matches the requirement:

- Uses set operations
- Uses symmetric difference concept
- Returns both sides’ unique elements in one list.
