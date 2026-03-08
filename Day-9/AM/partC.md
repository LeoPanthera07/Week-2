### Q1: Conceptual — Shallow Copy vs Deep Copy

**Question**

Explain the difference between:

- Shallow Copy  
- Deep Copy  

Include:

- Example with nested lists  
- Why shallow copy fails  
- When deep copy is required  

**Answer**

In Python, a **shallow** copy creates a new outer container (like a list), but the inner objects are still the same references as in the original. For nested lists, this means both the original and the copy share the same inner lists.

In contrast, a **deep** copy creates a completely independent copy of the original object and all nested objects inside it. Changes in one deep‑copied structure do not affect the other.

Example with nested lists:

```python
import copy

original = [, ]

# Shallow copy (only outer list is copied)
shallow = original[:]          # or list(original) / copy.copy(original)

# Deep copy (outer + inner lists copied)
deep = copy.deepcopy(original)

shallow = 99

print(original)  # [, ]  <-- changed
print(shallow)  # [, ]

deep = 42

print(original)  # [, ]  <-- unchanged now
print(deep)      # [, ]