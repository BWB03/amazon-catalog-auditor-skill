# Query Reference

Detailed documentation for all 9 catalog queries.

## 1. missing-attributes

**What it checks:** Required attributes missing from listings

**Severity:** Critical (required)

**Common issues:**
- Brand
- Item Type Keyword
- Bullet Points
- Product Description
- Country of Origin

**Fix:** Add missing required fields in Seller Central or bulk upload

---

## 2. missing-any-attributes

**What it checks:** All missing attributes (required + conditional)

**Severity:** Required or Conditional

**When to use:** Comprehensive attribute audit

**Fix:** Review conditional fields based on product type

---

## 3. long-titles

**What it checks:** Titles exceeding 200 characters

**Severity:** Warning

**Impact:** Amazon truncates titles >200 chars, hurting SEO

**Fix:** Trim to under 200 characters, front-load keywords

---

## 4. title-prohibited-chars

**What it checks:** Prohibited characters in titles: `!$?_{}^¬¦`

**Severity:** Warning

**Impact:** Amazon may suppress or reject listings

**Fix:** Remove prohibited characters, use allowed punctuation (- , .)

---

## 5. rufus-bullets

**What it checks:** Bullet point optimization against Amazon's RUFUS AI framework

**Severity:** Warning

**Scoring:** 1-5 per bullet (5 = perfect)

**Framework:**
- **Bullet 1:** Hero Benefit (why buy this?)
- **Bullet 2:** Target Audience (who is it for?)
- **Bullet 3:** Differentiators (why this vs. competitors?)
- **All bullets:** Specific data, no vague marketing, proper length

**Issues flagged:**
- Too short (<50 chars) or too long (>500 chars)
- Vague marketing language ("premium quality", "best in class")
- Excessive ALL CAPS
- Missing specifics (numbers, measurements, data)
- Position-specific issues (Bullet 1 lacks benefits, etc.)

**Fix Examples:**

**Bad Bullet 1:**
> "Premium quality hair gel with amazing hold"

**Good Bullet 1:**
> "Reduce frizz by 80% and add lasting shine with our humidity-resistant formula"

**Bad Bullet 2:**
> "Great for styling"

**Good Bullet 2:**
> "Ideal for curly or wavy hair types, perfect for men and women seeking all-day hold"

---

## 6. prohibited-chars

**What it checks:** Prohibited characters in any field (Title, Bullets, Description)

**Severity:** Warning

**Prohibited:** `!$?_{}^¬¦<>`

**Fix:** Remove or replace with allowed characters

---

## 7. product-type-mismatch

**What it checks:** Mismatches between Product Type and Item Type Keyword

**Severity:** Warning

**Example Issue:**
- Product Type: `HAIR_STYLING_AGENT`
- Item Type: `cleaning-wipes` ❌

**Impact:** Incorrect categorization, poor search placement

**Fix:** Ensure Item Type Keyword aligns with Product Type

---

## 8. missing-variations

**What it checks:** Products that should be variations but aren't

**Severity:** Info

**Detection logic:**
- Groups products by brand + normalized name
- Flags standalone SKUs that look like size/color variants

**Example:**
- SKU-001: "Brand X Shampoo 8oz"
- SKU-002: "Brand X Shampoo 16oz"
- **Suggestion:** Create parent-child variation

**Fix:** Create variation family in Seller Central

---

## 9. new-attributes

**What it checks:** Template fields that exist but aren't being used

**Severity:** Info

**Use case:** Discover new attributes Amazon added to templates

**Example:**
- Template has "Sustainability Features" field (new)
- No listings use it
- **Opportunity:** Add sustainability info to improve discoverability

**Fix:** Review unused fields, add data if valuable

---

## Query Selection Guide

### Quick Health Check
```bash
catalog check missing-attributes file.xlsx
catalog check long-titles file.xlsx
```

### Content Quality Audit
```bash
catalog check rufus-bullets file.xlsx
catalog check prohibited-chars file.xlsx
```

### Comprehensive Audit
```bash
catalog scan file.xlsx
```

### Optimization Opportunities
```bash
catalog check missing-variations file.xlsx
catalog check new-attributes file.xlsx
```
