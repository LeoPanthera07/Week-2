# Titanic Survival Pattern Analysis
## Executive Insight Report

**Consultant:** Data Analytics Team  
**Client:** Historical Disaster Investigation Board  
**Date:** March 2, 2026  
**Classification:** Public Release

---

## Executive Summary

This report presents data-driven insights from the Titanic disaster (April 15, 1912) using reproducible NumPy and Pandas workflows. Our analysis reveals:

- **Gender dominated all other factors** in survival outcomes (54.3% correlation vs 25.7% for fare)
- **Children were prioritized** with 59.4% survival rate vs 22.7% for seniors
- **Age is not linearly predictive** of survival (r = -0.077, R² = 0.6%)
- **Custom scoring model** achieves 78.9% accuracy without ML algorithms
- **Class-based inequality**: 1st class survival (63%) was 2.6× higher than 3rd class (24%)

### Key Business Insight

The "women and children first" evacuation protocol completely overrode economic privilege. Even low-fare women (49% survival) outlived high-fare men (37.5% survival) by 11.5 percentage points, demonstrating that social norms trumped wealth during crisis response.

---

## Part 1: Statistical Foundations (NumPy Analysis)

### Age Demographics

| Statistic | Value |
|-----------|-------|
| Mean Age | 29.70 years |
| Median Age | 28.00 years |
| Std Deviation | 14.53 years |
| Valid Entries | 714 (80.1%) |
| Missing | 177 (19.9%) |

### Fare-Based Survival Disparity

**Top 10% Fare Passengers (≥£78.29):**
- Survival rate: **75.6%**
- Mean fare: £132.35

**Bottom 10% Fare Passengers (≤£7.55):**
- Survival rate: **29.2%**
- Mean fare: £5.92

**Wealth Survival Multiplier:** 2.59× (rich vs poor)

### Age-Group Survival Rates

| Age Group | Count | Survival Rate | Priority Evidence |
|-----------|-------|---------------|-------------------|
| Children (< 15) | 76 | **59.4%** | ✓ "Women & children first" protocol |
| Adults (15-60) | 612 | 38.9% | Majority population |
| Seniors (> 60) | 26 | **22.7%** | ✗ Mobility constraints |

### Linearity Test: Age vs Survival

**Pearson Correlation:** r = -0.0777  
**R² (Variance Explained):** 0.6%

**Conclusion:** Age is **NOT** linearly related to survival. The negligible correlation (|r| < 0.1) indicates that linear models using raw age would fail. Non-linear patterns (children prioritized, seniors disadvantaged) require categorical encoding (AgeGroup feature).

**Statistical Justification:** Only 0.6% of survival variance is explained by linear age trends. This is statistically indistinguishable from zero predictive power. The observed U-shaped pattern contradicts linearity assumptions.

---

## Part 2: Feature Engineering & Correlation Analysis

### Missing Value Treatment

| Variable | Missing % | Imputation Strategy |
|----------|-----------|---------------------|
| Age | 19.9% | Median by passenger class (class-specific demographics) |
| Embarked | 0.2% | Mode (most common port: Southampton) |
| Cabin | 77.1% | Dropped (non-recoverable) |

### Engineered Features

| Feature | Formula | Business Rationale |
|---------|---------|-------------------|
| `FamilySize` | SibSp + Parch + 1 | Larger families faced coordination challenges |
| `IsAlone` | Binary (FamilySize == 1) | Solo travelers lacked support networks |
| `FarePerPerson` | Fare / FamilySize | Normalizes spending power to individual level |
| `AgeGroup` | Child/Adult/Senior bins | Captures non-linear evacuation priority |
| `FareGroup` | Low/Medium/High quantiles | Wealth tier classification |

### Survival Correlation Ranking (Top 5 Features)

| Rank | Feature | Correlation | Direction | Interpretation |
|------|---------|-------------|-----------|----------------|
| 1 | Sex (female) | **+0.543** | Positive | Being female strongly increases survival |
| 2 | Fare | +0.257 | Positive | Higher ticket price correlates with survival |
| 3 | Pclass | **-0.338** | Negative | Lower class number (1st class) = higher survival |
| 4 | FarePerPerson | +0.224 | Positive | Individual spending power matters |
| 5 | Age | -0.070 | Negative | Weak (non-linear relationship confirmed) |

### Pivot Analysis: Gender × Passenger Class

| Gender | Class 1 | Class 2 | Class 3 | Overall |
|--------|---------|---------|---------|---------|
| Female | **96.8%** | 92.1% | 50.0% | 74.2% |
| Male | 36.9% | 15.7% | 13.5% | **18.9%** |

**Critical Insight:** Even 3rd-class females (50%) survived at a higher rate than 1st-class males (36.9%). Gender dominated class in determining survival outcomes.

### Wealth vs Gender: Final Verdict

**Cross-Tabulation Evidence:**

| Gender | Low Fare | Medium Fare | High Fare |
|--------|----------|-------------|-----------|
| Female | 49.0% | 88.5% | **96.5%** |
| Male | 11.5% | 21.8% | 37.5% |

**Critical Comparison:**  
- Low-fare females: **49.0%** survival  
- High-fare males: **37.5%** survival  
- **Gap: +11.5 percentage points** in favor of low-fare women

**Conclusion:** Gender **dominates** wealth in predicting survival. The "women and children first" protocol completely overrode economic privilege for male passengers. Wealth only mattered **within** gender groups—it could not overcome the primary sorting criterion of sex.

---

## Part 3: Handcrafted Survival Score (No ML)

### Scoring Formula

```
SurvivalScore = 0.50 × Gender + 0.25 × Pclass_norm + 0.15 × Fare_norm
                + 0.08 × AgeGroup + 0.02 × FamilySize_norm
```

**Weight Rationale:** Derived from correlation strength analysis (Part 2). Gender receives 50% weight as the strongest predictor (r = +0.543).

### Performance Metrics

| Metric | Value | Interpretation |
|--------|-------|----------------|
| **Accuracy** | **78.9%** | Correctly classified 703/891 passengers |
| Precision | 72.9% | Of predicted survivors, 72.9% were correct |
| Recall | 71.6% | Caught 71.6% of actual survivors |
| F1 Score | 0.723 | Balanced precision/recall |

### Confusion Matrix

|  | Predicted: Died | Predicted: Survived | Total |
|--|-----------------|---------------------|-------|
| **Actual: Died** | 458 (TN) | 91 (FP) | 549 |
| **Actual: Survived** | 97 (FN) | 245 (TP) | 342 |
| **Total** | 555 | 336 | 891 |

### Baseline Comparisons

| Approach | Accuracy | Improvement over Baseline |
|----------|----------|---------------------------|
| Random guessing | 50.0% | — |
| Majority class (always "died") | 61.6% | — |
| **Our handcrafted model** | **78.9%** | **+17.3 points vs majority** |

**Statistical Significance:** Z-test yields p < 0.0001 (highly significant). The model's 78.9% accuracy is **1.58× better than random** and represents a 58% relative improvement.

**Answer to Q3:** YES—the handcrafted score significantly outperforms random guessing with overwhelming statistical confidence. It demonstrates that transparent, interpretable feature engineering can achieve strong predictive performance without black-box ML algorithms.

---

## Part 4: Strategic Implications & Ethics

### Modern Rescue Prioritization

**Proposed 2026 Protocol (Vulnerability-Based):**

1. **Children (< 15 years)** — Limited self-rescue capability
2. **Elderly (> 60 years)** — Mobility constraints, medical needs
3. **Persons with disabilities** — Require assistance
4. **Families with young children** — Maintain family units
5. **Remaining passengers** — No gender/wealth discrimination

**Key Change:** Remove gender as priority factor. Modern ethics rejects 1912's "women first" policy as discriminatory. Focus on **vulnerability** (age, health, mobility) rather than gender or socioeconomic status.

### Ethical Concerns in Automated Survival Prediction

#### 1. Discrimination & Algorithmic Bias
- **Problem:** Historical data encodes societal biases (gender, class). Models perpetuate discrimination.
- **Example:** Our model uses gender as 50% weight—learned from 1912 norms, not biological necessity.
- **Impact:** Violates equal protection laws (Title VII, GDPR Article 22, EU Gender Directive).

#### 2. Opacity & Accountability Gap
- **Problem:** Who is responsible when an algorithm makes a lethal decision? Families cannot understand why loved ones were not prioritized.
- **Example:** If a bug in the scoring function reduces a passenger's score by 0.2, causing death, is the data scientist, company, or captain liable?
- **Impact:** Legal frameworks lack clarity on algorithmic accountability in life-or-death contexts.

#### 3. Dehumanization & Context Blindness
- **Problem:** Reducing human life to a numerical score ignores intrinsic dignity, relationships, and context.
- **Example:** Algorithm assigns elderly surgeon (score 0.25) lower priority than young passenger (0.75), but surgeon could save others post-rescue.
- **Impact:** Removes human judgment, empathy, and moral reasoning from triage decisions.

### Insurance Underwriting Adaptation

**If this were insurance pricing, our model would be:**

1. **ILLEGAL** — Uses gender (50% weight), banned in EU and some US states
2. **INEFFECTIVE** — Wrong features (no health data), wrong time horizon (immediate vs decades)
3. **NOT ADVERSARIALLY ROBUST** — Easily gamed (customers hide health issues)

**Required Changes:**

| Aspect | Disaster Model | Insurance Model |
|--------|----------------|-----------------|
| **Features** | Demographics (gender, age, class) | Health metrics (BMI, smoking, cholesterol) |
| **Gender Use** | 50% weight | **PROHIBITED** (EU Gender Directive 2012) |
| **Time Horizon** | Immediate (hours) | Long-term (decades, survival analysis) |
| **Regulation** | None (emergency) | Strict (GDPR, GINA, IRDAI compliance) |
| **Explainability** | Optional | **REQUIRED** (right to explanation) |
| **Adversarial** | No incentive to lie | Must prevent fraud (medical exams) |

**Conclusion:** Insurance requires actuarial science + regulatory compliance + fraud prevention—fundamentally different from disaster survival prediction.

---

## Recommendations

### For Disaster Response (Modern Context)
1. **Eliminate gender-based prioritization** — Focus on vulnerability (children, elderly, disabled)
2. **Maintain lifeboat proximity equity** — Class-based access disparities caused 2.6× survival gap
3. **Family unit protocols** — Keep parents with children during evacuation

### For Predictive Modeling Ethics
1. **Mandate transparency** — Black-box models unacceptable for life-or-death decisions
2. **Establish accountability frameworks** — Clear liability chains for algorithmic harm
3. **Require bias audits** — Prevent perpetuation of historical discrimination

### For Data Science Practice
1. **Feature engineering > complex models** — Our 78.9% accuracy achieved with weighted linear formula
2. **Correlation analysis first** — Identify key predictors before jumping to ML
3. **Validate against baselines** — Always compare to random/majority class performance

---

## Conclusion

This analysis demonstrates that **transparent, interpretable models** can achieve strong predictive performance (78.9% accuracy) without black-box ML algorithms. Key findings:

- **Gender was the strongest predictor** (r = +0.543), overriding wealth and class
- **Age is non-linear**—categorical bins outperform continuous age
- **Class-based inequality** was systemic—3rd class survival was 2.6× lower than 1st class
- **Handcrafted scoring** significantly outperforms random guessing (p < 0.0001)

**Ethical Imperative:** Automated survival prediction raises profound questions about discrimination, accountability, and human dignity. While technically feasible, deployment requires regulatory frameworks addressing bias, transparency, and liability—none of which currently exist.

**Final Insight:** The Titanic disaster teaches us that social norms (1912's "women first") can completely override economic advantage during crisis. In 2026, our norms have evolved—modern rescue protocols must prioritize **vulnerability over gender**, **need over wealth**, and **equality over chivalry**.

---

**Report prepared using:** Python 3.9 · NumPy 1.24 · Pandas 2.0  
**Methodology:** Reproducible workflows, no AutoML, transparent feature engineering  
**Data source:** Kaggle Titanic Dataset (891 passengers, 12 features)

**END OF REPORT**
