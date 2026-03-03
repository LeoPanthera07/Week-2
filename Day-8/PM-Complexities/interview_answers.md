# Day 8 PM — Interview Ready

## Q1: break vs continue, and loop-else

### break vs continue

`break` exits the loop entirely — no more iterations run.
`continue` skips the rest of the current iteration and moves to the next one.

```python
# break example
for i in range(5):
    if i == 3:
        break
    print(i)
# Output: 0 1 2

# continue example
for i in range(5):
    if i == 3:
        continue
    print(i)
# Output: 0 1 2 4
```

### else clause in loops

The `else` block runs only if the loop completed WITHOUT hitting a `break`.
If `break` was triggered, the `else` is skipped entirely.

```python
for i in range(5):
    if i == 10:
        break
else:
    print("Loop finished normally")   # This runs — no break was hit
```

**Practical use case — search pattern:**
```python
def find_prime(numbers):
    for n in numbers:
        for i in range(2, n):
            if n % i == 0:
                break
        else:
            print(f"{n} is prime")   # only runs if inner loop didn't break
```
This is the cleanest way to detect "no divisor found" without a flag variable.


## Q2: find_pairs — O(n²) and O(n) versions

### O(n²) — nested loops
```python
def find_pairs(numbers, target):
    """Return all pairs that sum to target using nested loops — O(n²)."""
    pairs = []
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            if numbers[i] + numbers[j] == target:
                pairs.append((numbers[i], numbers[j]))
    return pairs

# find_pairs(, 6) → [(1, 5), (2, 4)][1][2][3][4][5]
```

**Why O(n²):** For every element we scan all remaining elements — n × n operations.

### O(n) — using a set
```python
def find_pairs_fast(numbers, target):
    """Return all pairs that sum to target using a set — O(n)."""
    seen = set()
    pairs = []
    for num in numbers:
        complement = target - num
        if complement in seen:
            pairs.append((complement, num))
        seen.add(num)
    return pairs
```

**Why O(n):** We iterate once. For each number we check if its complement
already exists in `seen` — set lookup is O(1), so the whole loop is O(n).


## Q3: Debug is_prime

```python
# ORIGINAL — has performance bug
def is_prime(n):
    if n < 2:
        return False
    for i in range(2, n):      # checks ALL numbers up to n — O(n)
        if n % i == 0:
            return False
    return True
```

**Bug:** `range(2, n)` checks every number up to n. We only need to check
up to √n — if n has a factor larger than √n, its paired factor must be
smaller than √n and would have been found already.

**Fixed version — O(√n):**
```python
import math

def is_prime(n):
    """Return True if n is prime."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):   # odd numbers up to √n only
        if n % i == 0:
            return False
    return True
```

**Improvements made:**
- `range(2, n)` → `range(3, sqrt(n)+1, 2)` — reduces iterations from n to √n
- Added early exit for even numbers — halves remaining checks
- Added special case for n=2 (the only even prime)
