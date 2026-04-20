---
name: amazon-catalog-auditor
description: Audit Amazon Category Listing Reports (CLRs) for catalog health issues. Use when analyzing CLR files (.xlsx/.xlsm), checking for missing attributes, RUFUS bullet optimization, title validation, or generating catalog audit reports. Supports JSON/CSV/NDJSON export, field masks, pagination, and agent-native workflows.
---

# Amazon Catalog Auditor

> Deprecated wrapper skill as of April 20, 2026.
> The maintained implementation now lives in `amazon-catalog-cli`.
> Route fixes, features, and new pull requests to `https://github.com/BWB03/amazon-catalog-cli`.

Audit Amazon Category Listing Reports using the `amazon-catalog-cli` tool. Identifies missing attributes, RUFUS bullet issues, title problems, and other catalog health concerns.

## Overview

This skill is a legacy wrapper around the `amazon-catalog-cli` PyPI package. When a user asks to audit a CLR, check catalog health, or analyze Amazon listings, prefer the CLI directly where possible:

1. Locates the CLR file (uploaded or path provided)
2. Runs appropriate catalog queries
3. Parses and presents results in human-readable format
4. Provides actionable recommendations
5. Detects marketplace and flags non-US CLRs

> **Note:** v2.0 of amazon-catalog-cli now includes a built-in MCP server (`catalog mcp`) and `SKILL.md`. For MCP-compatible clients (Claude Desktop, CLR Pro), the CLI itself is a first-class agent surface. This OpenClaw skill remains useful for OpenClaw-specific workflows.

**v2.0.0 (Agent-First Redesign):**
- **MCP server** - `catalog mcp` exposes tools for Claude Desktop and MCP clients
- **JSON/stdin input** - `--json` and `--stdin` flags for structured agent input
- **Schema introspection** - `catalog schema --format json` for auto-discovery
- **Field masks** - `--fields sku,severity,details` to reduce output
- **Pagination** - `--limit` and `--offset` for large catalogs
- **NDJSON streaming** - `--format ndjson` for line-by-line output
- **Input validation** - Rejects path traversal, injection, malformed input

**v1.3.0:**
- Marketplace detection - Auto-detects US/CA/UK/DE/etc from CLR
- Bullet awareness checks - Soft violations (excessive caps, problematic chars)
- 12 total queries

**v1.2.0:**
- Comprehensive bullet point validation (prohibited content, formatting)

**v1.1.0:**
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
# Full scan (all 12 queries)
catalog scan <clr-file>

# Specific query
catalog check missing-attributes <clr-file>

# JSON output for parsing
catalog scan <clr-file> --format json
```

### Agent-Optimized Usage (v2.0)

```bash
# JSON with field mask and limit (recommended for agents)
catalog scan <clr-file> --format json --fields sku,severity,details --limit 20

# Structured JSON input
catalog scan --json '{"file": "<clr-file>", "queries": ["missing-attributes"], "limit": 10}'

# Piped input
echo '{"file": "<clr-file>"}' | catalog scan --stdin --format json

# NDJSON streaming for large results
catalog scan <clr-file> --format ndjson --limit 50

# Schema introspection (discover available queries and params)
catalog schema --format json
```

## Available Queries

The tool provides 12 built-in queries:

### Attribute Audits
1. **missing-attributes** - Required fields missing
2. **missing-any-attributes** - All missing fields (required + conditional)
3. **new-attributes** - Unused template fields

### Content Quality
4. **rufus-bullets** - RUFUS AI optimization scoring
5. **bullet-prohibited-content** - Prohibited chars, emojis, claims, placeholders in bullets
6. **bullet-formatting** - Capitalization, length, punctuation rules
7. **bullet-awareness** - Soft violations (excessive caps, problematic special chars)
8. **long-titles** - Titles exceeding 200 characters
9. **title-prohibited-chars** - Prohibited characters in titles
10. **prohibited-chars** - Basic character validation (title/brand)

### Catalog Structure
11. **product-type-mismatch** - Product type / item type keyword mismatches
12. **missing-variations** - Products that should be variations

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
catalog scan <clr-path> --format json --fields sku,severity,details --limit 50
```

**Specific Issue:**
```bash
catalog check rufus-bullets <clr-path> --format json --limit 20
```

**Quick Summary:**
```bash
catalog scan <clr-path>
```

**Structured Input (v2.0):**
```bash
catalog scan --json '{"file": "<clr-path>", "queries": ["missing-attributes", "rufus-bullets"], "fields": ["sku", "severity", "details"], "limit": 20}'
```

### 3. Parse JSON Output

Use `scripts/parse_audit.py` to process JSON results into human-readable insights.

### 4. Present Findings

**Format response as:**

```
**CLR Audit Results**

**Summary:**
- Total Issues: X
- Affected SKUs: Y
- Queries Run: 12

**Top Priorities:**
1. [Most critical issue with count]
2. [Second critical issue]
3. [Third critical issue]

**Recommendations:**
- [Actionable fix #1]
- [Actionable fix #2]

**Export:** [mention JSON/CSV option if needed]
```

## Common Use Cases

### Use Case 1: General Audit

**User:** "Audit this CLR for me"

**Action:**
1. Run full scan: `catalog scan <file> --format json --fields sku,severity,details --limit 50`
2. Parse results with `scripts/parse_audit.py`
3. Present prioritized findings
4. Offer to export or dive deeper

### Use Case 2: Specific Check

**User:** "Check if my bullet points are RUFUS optimized"

**Action:**
1. Run: `catalog check rufus-bullets <file> --format json --limit 20`
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

### Use Case 5: Multi-Marketplace Detection

**User:** "Audit this CLR - is it for Canada or US?"

**Action:**
1. Run: `catalog scan <file> --format json`
2. Check `marketplace` field in output
3. If not US, flag any US-specific issues that may not apply
4. Present findings with marketplace context

### Use Case 6: Agent-Optimized Large Catalog (v2.0)

**User:** "Audit this large CLR but just show me the worst issues"

**Action:**
1. Run: `catalog scan <file> --format json --queries missing-attributes,rufus-bullets --fields sku,severity,details --limit 10`
2. Present top 10 most critical issues
3. Offer to show more with increased limit or different queries

## Output Interpretation

### JSON Structure (v2.0)

```json
{
  "timestamp": "2026-03-05T10:30:00Z",
  "marketplace": "US",
  "is_us_marketplace": true,
  "total_queries": 12,
  "total_issues": 5904,
  "total_affected_skus": 95,
  "results": [
    {
      "query_name": "missing-attributes",
      "description": "Find mandatory attributes missing from listings",
      "total_issues": 444,
      "affected_skus": 37,
      "issues": [
        {
          "row": 7,
          "sku": "ABC-123",
          "field": "brand",
          "severity": "required",
          "details": "Missing required field: brand",
          "product_type": "HAIR_STYLING_AGENT",
          "extra": {}
        }
      ],
      "metadata": {
        "total_listings": 150,
        "marketplace": "US",
        "is_us_marketplace": true,
        "params": {}
      }
    }
  ]
}
```

### Severity Levels

- **required** - Must fix (Amazon rejects listings)
- **conditional** - Fix based on product type
- **critical** - Amazon can suppress listings (prohibited content)
- **warning** - Best practice issue (RUFUS, title length)
- **awareness** - Soft violations (worth reviewing but not critical)
- **info** - Suggestions (unused fields, variations)

### Prioritization Logic

1. **Critical (Fix First):**
   - Missing required attributes
   - Prohibited characters / content
   - Title issues

2. **Important (Fix Soon):**
   - RUFUS scores < 3
   - Missing conditional attributes
   - Product type mismatches

3. **Optimize (When Time Allows):**
   - RUFUS scores 3-4
   - Variation opportunities
   - Unused attributes

## Troubleshooting

### Issue: Command not found

```bash
# Add Python bin to PATH
export PATH="$HOME/Library/Python/3.14/bin:$PATH"

# Or run directly
python3 -m catalog.surfaces.cli scan <file>
```

### Issue: Permission denied

```bash
# Make sure CLI is executable
which catalog
pip3 show amazon-catalog-cli
```

### Issue: Large CLR slow

For CLRs with 1000+ SKUs, expect 10-15 second processing time. Use `--limit` to cap results.

## Resources

See `references/queries.md` for detailed documentation on each query type and `scripts/parse_audit.py` for JSON processing helper.

For maintained docs and active development, use `https://github.com/BWB03/amazon-catalog-cli`.

---

**Quick Reference:**

```bash
# Full audit (all 12 queries)
catalog scan file.xlsx

# Agent-optimized (v2.0 - recommended)
catalog scan file.xlsx --format json --fields sku,severity,details --limit 20

# Structured JSON input (v2.0)
catalog scan --json '{"file": "file.xlsx", "queries": ["missing-attributes"], "limit": 10}'

# Specific checks
catalog check missing-attributes file.xlsx
catalog check rufus-bullets file.xlsx --format json --limit 10

# Schema discovery (v2.0)
catalog schema --format json

# NDJSON streaming (v2.0)
catalog scan file.xlsx --format ndjson --limit 50

# JSON export
catalog scan file.xlsx --format json --output results.json

# List all queries
catalog list-queries --format json
```

**Version:** Requires amazon-catalog-cli v2.0.0+

**Upgrade:**
```bash
pip3 install --upgrade amazon-catalog-cli
```
