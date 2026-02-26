---
name: amazon-catalog-auditor
description: Audit Amazon Category Listing Reports (CLRs) for catalog health issues. Use when analyzing CLR files (.xlsx/.xlsm), checking for missing attributes, RUFUS bullet optimization, title validation, or generating catalog audit reports. Supports JSON/CSV export and agent-native workflows.
---

# Amazon Catalog Auditor

Audit Amazon Category Listing Reports using the `amazon-catalog-cli` tool. Identifies missing attributes, RUFUS bullet issues, title problems, and other catalog health concerns.

## Overview

This skill wraps the `amazon-catalog-cli` PyPI package (v1.1.0+) to provide automated CLR analysis. When a user asks to audit a CLR, check catalog health, or analyze Amazon listings, this skill:

1. Locates the CLR file (uploaded or path provided)
2. Runs appropriate catalog queries
3. Parses and presents results in human-readable format
4. Provides actionable recommendations

**New in v1.1.0:**
- RUFUS tier scoring (Good/Fair/Weak/Critical)
- Catalog-wide RUFUS summary stats
- Automatic FBM/MFN duplicate filtering

## When to Use This Skill

Use when user asks for:
- "Audit this CLR"
- "What's wrong with my Amazon catalog?"
- "Check for missing attributes"
- "Score my RUFUS bullet points"
- "Analyze this Category Listing Report"
- "What catalog issues should I fix first?"

## Quick Start

### Installation Check

The tool should already be installed. Verify:

```bash
catalog --version
```

If not installed:

```bash
pip3 install amazon-catalog-cli
```

### Basic Usage

```bash
# Full scan (all 9 queries)
catalog scan <clr-file>

# Specific query
catalog check missing-attributes <clr-file>

# JSON output for parsing
catalog scan <clr-file> --format json
```

## Available Queries

The tool provides 9 built-in queries:

1. **missing-attributes** - Required fields missing
2. **missing-any-attributes** - All missing fields (required + conditional)
3. **long-titles** - Titles exceeding 200 characters
4. **title-prohibited-chars** - Prohibited characters in titles
5. **rufus-bullets** - RUFUS AI optimization scoring
6. **prohibited-chars** - Prohibited characters in any field
7. **product-type-mismatch** - Product type / item type keyword mismatches
8. **missing-variations** - Products that should be variations
9. **new-attributes** - Unused template fields

## Workflow

### 1. Get CLR File Path

```python
# User uploaded file
clr_path = "/path/to/uploaded/file.xlsx"

# Or user provides path
"Audit this: /Users/username/Downloads/my-clr.xlsx"
```

### 2. Run Appropriate Analysis

**Full Audit (Most Common):**
```bash
catalog scan <clr-path> --format json
```

**Specific Issue:**
```bash
catalog check rufus-bullets <clr-path> --format json
```

**Quick Summary:**
```bash
catalog scan <clr-path>
```

### 3. Parse JSON Output

Use `scripts/parse_audit.py` to process JSON results into human-readable insights.

### 4. Present Findings

**Format response as:**

```
🔍 **CLR Audit Results**

📊 **Summary:**
- Total Issues: X
- Affected SKUs: Y
- Queries Run: 9

🔥 **Top Priorities:**
1. [Most critical issue with count]
2. [Second critical issue]
3. [Third critical issue]

💡 **Recommendations:**
- [Actionable fix #1]
- [Actionable fix #2]

📁 **Export:** [mention JSON/CSV option if needed]
```

## Common Use Cases

### Use Case 1: General Audit

**User:** "Audit this CLR for me"

**Action:**
1. Run full scan: `catalog scan <file> --format json`
2. Parse results with `scripts/parse_audit.py`
3. Present prioritized findings
4. Offer to export or dive deeper

### Use Case 2: Specific Check

**User:** "Check if my bullet points are RUFUS optimized"

**Action:**
1. Run: `catalog check rufus-bullets <file> --format json`
2. Parse RUFUS scores
3. Present bullets scoring below 4/5 with suggestions
4. Highlight position-specific issues (Hero Benefit, Audience, Differentiators)

### Use Case 3: Export for Client

**User:** "Generate a report I can send to my client"

**Action:**
1. Run: `catalog scan <file> --format csv --output client-audit.csv`
2. Confirm CSV created
3. Optionally create summary document

### Use Case 4: Compare Multiple CLRs

**User:** "Compare these two CLRs"

**Action:**
1. Run both: `catalog scan file1.xlsx --format json` + `catalog scan file2.xlsx --format json`
2. Compare issue counts, affected SKUs
3. Highlight improvements or new issues

## Output Interpretation

### JSON Structure

```json
{
  "total_issues": 5904,
  "total_affected_skus": 95,
  "queries": [
    {
      "query_name": "missing-attributes",
      "total_issues": 444,
      "affected_skus": 37,
      "issues": [
        {
          "row": 7,
          "sku": "ABC-123",
          "field": "brand",
          "severity": "required",
          "details": "Missing required field: brand"
        }
      ]
    }
  ]
}
```

### Severity Levels

- **required** - Must fix (Amazon rejects listings)
- **conditional** - Fix based on product type
- **warning** - Best practice issue (RUFUS, title length)
- **info** - Suggestions (unused fields, variations)

### Prioritization Logic

1. **Critical (Fix First):**
   - Missing required attributes
   - Prohibited characters
   - Title issues

2. **Important (Fix Soon):**
   - RUFUS scores < 3
   - Missing conditional attributes
   - Product type mismatches

3. **Optimize (When Time Allows):**
   - RUFUS scores 3-4
   - Variation opportunities
   - Unused attributes

## Examples

### Example 1: Quick Audit

**Input:**
```
"Audit this CLR and tell me what needs fixing"
[file: plantfusion-clr.xlsx]
```

**Response:**
```
🔍 **PlantFusion CLR Audit**

📊 **Summary:**
- 47 issues found
- 23 SKUs affected

🔥 **Top Priorities:**
1. Missing Brand (12 SKUs) - Amazon requires this field
2. RUFUS Bullets scoring low (8 SKUs) - Bullet 1 needs Hero Benefit
3. Titles exceeding 200 chars (3 SKUs) - Will be truncated

💡 **Quick Wins:**
- Add brand name to 12 SKUs
- Rewrite Bullet 1 for 8 products (lead with benefits)
- Trim 3 titles under 200 characters

Want me to export a detailed CSV for you to work from?
```

### Example 2: RUFUS Deep Dive

**Input:**
```
"Check my RUFUS bullet optimization"
[file: client-clr.xlsx]
```

**Response:**
```
📝 **RUFUS Bullet Analysis**

**Overall:** 15 SKUs with bullets scoring below 4/5

**Common Issues:**
1. **Bullet 1** (Hero Benefit) - 8 SKUs missing benefit keywords
   - Current: "Premium quality hair gel..."
   - Fix: "Reduce frizz and add shine with..."

2. **Bullet 2** (Audience) - 5 SKUs don't state who it's for
   - Add: "Ideal for [target audience]"

3. **Missing Specifics** - 12 SKUs lack data points
   - Add: measurements, counts, percentages

**Top 3 SKUs to Fix:**
- ABC-123: Score 2/5 (no benefits, no audience)
- XYZ-456: Score 2.5/5 (vague marketing language)
- DEF-789: Score 3/5 (needs specifics)

Want details on all 15?
```

## Troubleshooting

### Issue: Command not found

```bash
# Add Python bin to PATH
export PATH="$HOME/Library/Python/3.14/bin:$PATH"

# Or run directly
python3 -m catalog.cli scan <file>
```

### Issue: Permission denied

```bash
# Make sure CLI is executable
which catalog
pip3 show amazon-catalog-cli
```

### Issue: Large CLR slow

For CLRs with 1000+ SKUs, expect 10-15 second processing time. This is normal.

## Integration with Other Tools

### With Google Sheets

If CLR data is in Google Sheets:
1. Export as Excel (.xlsx)
2. Run audit
3. Update Sheet with findings

### With Client Reporting

1. Run audit with JSON export
2. Use parsed insights to generate client-facing report
3. Attach CSV for detailed breakdown

## Resources

See `references/queries.md` for detailed documentation on each query type and `scripts/parse_audit.py` for JSON processing helper.

---

**Quick Reference:**

```bash
# Full audit
catalog scan file.xlsx

# Specific check
catalog check [query-name] file.xlsx

# JSON export
catalog scan file.xlsx --format json --output results.json

# List all queries
catalog list-queries file.xlsx
```
