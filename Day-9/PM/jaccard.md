## Part D — AI-Augmented Task: Jaccard Similarity

### 1. Exact Prompt Used

> Write a Python function that calculates the Jaccard similarity between two sets of strings. Explain what Jaccard similarity is and where it is used in industry.

---

### 2. AI Output

#### 2.1 AI-Generated Code

```python
def jaccard_similarity(set_a, set_b):
    """
    Calculate Jaccard similarity between two sets of strings.
    """
    intersection = set_a.intersection(set_b)
    union = set_a.union(set_b)

    if not union:
        return 0.0

    return len(intersection) / len(union)
```

#### 2.2 AI Explanation (as given)

- Jaccard similarity is a measure of similarity between two sets.  
- It is defined as the size of the intersection divided by the size of the union of the sets.  
- It is commonly used in applications like recommendation systems, document similarity, and plagiarism detection.

---

### 3. Testing and Verification

#### 3.1 Test Case 1

```python
set_a = {'python', 'java', 'sql'}
set_b = {'python', 'sql', 'docker', 'aws'}

print(jaccard_similarity(set_a, set_b))
```

- Intersection: `{'python', 'sql'}` → size = 2  
- Union: `{'python', 'java', 'sql', 'docker', 'aws'}` → size = 5  
- Expected Jaccard similarity: \(2 / 5 = 0.4\)[web:101][web:105][web:109]  

**Observed output:** `0.4`  
→ The function matches the standard Jaccard formula.

#### 3.2 Test Case 2 (One empty, one non-empty)

```python
print(jaccard_similarity(set(), {'python'}))
```

- Intersection size = 0  
- Union size = 1  
- Expected similarity: `0 / 1 = 0.0`  

**Observed output:** `0.0`  
→ Correct.

#### 3.3 Test Case 3 (Both empty sets)

```python
print(jaccard_similarity(set(), set()))
```

- Intersection size = 0  
- Union size = 0  
- The function checks `if not union: return 0.0`, so result is `0.0`.  

This is a reasonable convention for the “both empty” case, as long as it is documented (some definitions choose 1, but 0 is also used in practice).[web:109][web:111]

#### 3.4 Jaccard Formula Correctness

The AI used:

```python
len(intersection) / len(union)
```

which matches the standard Jaccard similarity definition:

\[
J(A, B) = \frac{|A \cap B|}{|A \cup B|}
\]

where \(|A \cap B|\) is the number of common elements and \(|A \cup B|\) is the number of unique elements across both sets.[web:101][web:105][web:109]  

So:

- The **formula is correct**.  
- Edge cases with empty sets are handled by explicitly checking if the union is empty.

---

### 4. Where Jaccard Similarity Is Used in Industry

1. **Recommendation systems**  
   User behaviour (clicked, viewed, or purchased items) can be represented as sets, and Jaccard similarity is used to measure similarity between users or items based on overlapping interactions, which helps generate recommendations.[web:99][web:101][web:107]  

2. **Text and document similarity (NLP)**  
   Documents or queries are often converted into sets of tokens, n‑grams, or shingles; Jaccard similarity on these sets is used to detect near-duplicate documents, cluster similar texts, and compare search queries.[web:99][web:101][web:110]  

3. **Plagiarism and near-duplicate detection**  
   Many plagiarism systems represent each document as a set of shingles or hashed features and then use Jaccard similarity to detect high-overlap pairs, flagging potential plagiarism or near-duplicate content.[web:98][web:100][web:102]  

4. **Image segmentation and classification**  
   In computer vision and classification tasks, Jaccard similarity (often called the Jaccard index or Intersection over Union) compares predicted vs. true sets of pixels, labels, or features to evaluate model performance.[web:97][web:103][web:104]  
