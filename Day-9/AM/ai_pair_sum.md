# AI Pair Sum Analysis

## 1. Exact Prompt
Write a Python function that finds all pairs in a list that sum to a target number using list comprehensions.

## 2. AI Code
```python
def find_pairs(nums, target):
    return [(nums[i], nums[j]) for i in range(len(nums)) 
            for j in range(len(nums)) if i != j and nums[i] + nums[j] == target]
```

## 3. Test Results
Test	Input	AI Output	Issue
1	[1,2,3,4,5], 6	[(1,5),(5,1),(2,4),(4,2)]	Reversed duplicates
2	[1,1,1], 2	[(1,1),(1,1),(1,1),(1,1),(1,1),(1,1)]	Repeated pairs

## 4. My Fixes
O(n²) with i < j:
```python
def find_unique_pairs(nums, target):
    return [(min(nums[i], nums[j]), max(nums[i], nums[j])) 
            for i in range(len(nums)) 
            for j in range(i + 1, len(nums)) 
            if nums[i] + nums[j] == target]
```

O(n) with sets:
```python
def find_pairs_linear(nums, target):
    seen, pairs = set(), set()
    for num in nums:
        complement = target - num
        if complement in seen:
            pairs.add(tuple(sorted((num, complement))))
        seen.add(num)
    return list(pairs)
```

Tests pass cleanly:

, 6 → [(1, 5), (2, 4)]

, 2 → [(1, 1)]