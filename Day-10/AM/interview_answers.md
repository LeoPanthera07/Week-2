## Q1: Conceptual — Dict Time Complexity

**Question:**  
Explain the time complexity of dict operations: lookup, insert, delete. Why is average O(1)? What causes worst-case O(n)? How does Python's hash function work for strings vs integers? When would you choose a dict over a list?

**Answer:**

### Time Complexity
| Operation | Average Case | Worst Case |
|-----------|--------------|------------|
| Lookup (`d[key]`) | O(1) | O(n) |
| Insert (`d[key] = value`) | O(1) | O(n) |
| Delete (`del d[key]`) | O(1) | O(n) |

### Why Average O(1)?
- Python dicts use **open addressing with linear probing** (hash table).
- `hash(key)` → index in internal array → store/retrieve value.
- Good hash distribution → few collisions → constant-time access.

### Worst-case O(n): Hash Collisions
- **Hash collision**: Multiple keys hash to same index.
- Python probes linearly (`index + 1`, `index + 2`, ...) until empty slot.
- If all keys hash to same index → degenerate to linked list → O(n).

### Hash Function: Strings vs Integers
- **Integers**: `hash(int) = int % table_size` (trivial, fast).
- **Strings**: SipHash (cryptographic, collision-resistant):
hash("abc") = siphash24("abc", seed) % table_size

text
- Prevents **hash flooding attacks** (malicious inputs causing O(n) perf).
- SipHash is slower but secure.

### Dict vs List: When to Choose Dict
| Use Case | Dict ✅ | List ❌ |
|----------|---------|---------|
| `user_id → profile` | O(1) lookup | O(n) scan |
| `word → frequency` | Natural key-value | Awkward indexing |
| Membership test | `if x in d` → O(1) | `if x in lst` → O(n) |
| Ordered access | Needs `OrderedDict` | Natural `lst[i]` |

**Rule**: Use dict when you have **key → value** mappings or need **fast lookups**.

---

## Q2: Coding — Group Anagrams

**Question:**  
```python
def group_anagrams(words: list[str]) -> dict[str, list[str]]:
```
Example:

```python
group_anagrams(['eat', 'tea', 'tan', 'ate', 'nat', 'bat'])
# {'aet': ['eat', 'tea', 'ate'], 'ant': ['tan', 'nat'], 'abt': ['bat']}
```

Answer:

```python
from collections import defaultdict

def group_anagrams(words: list[str]) -> dict[str, list[str]]:
    """
    Group words by anagram signature using sorted(word) as key.
    """
    groups = defaultdict(list)
    
    for word in words:
        # sorted(word) → consistent signature for anagrams
        key = ''.join(sorted(word))
        groups[key].append(word)
    
    return dict(groups)

# Test:
result = group_anagrams(['eat', 'tea', 'tan', 'ate', 'nat', 'bat'])
print(result)
# {'aet': ['eat', 'tea', 'ate'], 'ant': ['tan', 'nat'], 'abt': ['bat']}
```

Why this works:

Anagrams have identical character counts → sorted() produces same string.

defaultdict(list) auto-initializes empty lists.

Time: O(n × m log m) where n=words, m=max word length.

Q3: Debug — Char Frequency Bugs
Question:
Find and fix two bugs:

```python
def char_freq(text):
    freq = {}
    for char in text:
        freq[char] += 1      # Bug 1: KeyError on first occurrence
    sorted_freq = sorted(freq, key=freq.get, reverse=True)
    return sorted_freq         # Bug 2: Returns keys only, not (key, count) pairs
```
Answer:

Bug 1: KeyError on First Occurrence
```python
freq[char] += 1  # KeyError if char not in freq!
```
Fix: Use get() with default 0 or setdefault():

```python
freq[char] = freq.get(char, 0) + 1
```
Bug 2: Returns Keys Only
```python
sorted_freq = sorted(freq, key=freq.get, reverse=True)
return sorted_freq  # ['e', 'a', 't'] ❌ only chars, no counts
```
Fix: Return (char, count) tuples:

```python
sorted_freq = sorted(freq.items(), key=lambda x: x, reverse=True)
return sorted_freq  # [('e', 3), ('a', 2), ('t', 1)] ✅
```
Complete Fixed Version
```python
def char_freq(text):
    """
    Return sorted list of (char, frequency) tuples, most frequent first.
    """
    freq = {}
    for char in text:
        freq[char] = freq.get(char, 0) + 1  # Fix 1: Safe increment
    
    # Fix 2: Sort items() by count, return (char, count) tuples
    sorted_freq = sorted(freq.items(), key=lambda x: x, reverse=True)
    return sorted_freq

# Test:
print(char_freq("hello world"))
# [('l', 3), ('o', 2), (' ', 1), ('h', 1), ('e', 1), ('w', 1), ('r', 1), ('d', 1)]
```

Summary of fixes:

1. freq.get(char, 0) + 1 → no KeyError
2. sorted(freq.items(), ...) → returns (char, count) pairs