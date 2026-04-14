---
name: amazon-catalog-auditor
description: "Audit Amazon Category Listing Reports (CLRs) for catalog health issues. Use when analyzing CLR files (.xlsx/.xlsm), checking for missing attributes, RUFUS bullet optimization, title validation, or generating catalog audit reports. Supports JSON/CSV/NDJSON export, field masks, pagination, and agent-native workflows."
---

# Amazon Catalog Auditor

Audit Amazon Category Listing Reports using the `amazon-catalog-cli` tool (v2.0.0+). Identifies missing attributes, RUFUS bullet issues, title problems, and other catalog health concerns across 12 built-in queries.

## Prerequisites

```bash
# Verify installation
catalog --version

# Install if needed
pip3 install amazon-catalog-cli
```

## Workflow

### 1. Locate and Validate CLR File

Confirm the file exists and has a valid extension before scanning:

```bash
[[ -f "$CLR_PATH" && "$CLR_PATH" =~ \.(xlsx|xlsm)$ ]] || echo "Error: file not found or not .xlsx/.xlsm"
```

If the file is missing or has the wrong extension, ask the user to provide a valid CLR path.

### 2. Run Analysis

**Full audit (recommended):**
```bash
catalog scan <clr-path> --format json --fields sku,severity,details --limit 50
```

**Specific query:**
```bash
catalog check <query-name> <clr-path> --format json --limit 20
```

**Structured JSON input:**
```bash
catalog scan --json '{"file": "<clr-path>", "queries": ["missing-attributes", "rufus-bullets"], "fields": ["sku", "severity", "details"], "limit": 20}'
```

If `catalog scan` returns a non-zero exit code, check that the file is a valid CLR (not a regular spreadsheet) and that `catalog --version` shows v2.0.0+.

### 3. Parse Results

Use `scripts/parse_audit.py` to process JSON output into human-readable insights:

```bash
catalog scan <clr-path> --format json --output results.json
python3 scripts/parse_audit.py results.json
```

If the scan produced no issues (`total_issues: 0`), report a clean bill of health — no further parsing needed.

### 4. Present Findings

Format response as:

```
**CLR Audit Results**

**Summary:**
- Total Issues: X
- Affected SKUs: Y

**Top Priorities:**
1. [Most critical issue with count]
2. [Second critical issue]

**Recommendations:**
- [Actionable fix #1]
- [Actionable fix #2]
```

Prioritize by severity: required (Amazon rejects) → critical (suppression risk) → conditional → warning → info.

## Available Queries

12 built-in queries in three categories:

**Attribute Audits:** `missing-attributes`, `missing-any-attributes`, `new-attributes`

**Content Quality:** `rufus-bullets`, `bullet-prohibited-content`, `bullet-formatting`, `bullet-awareness`, `long-titles`, `title-prohibited-chars`, `prohibited-chars`

**Catalog Structure:** `product-type-mismatch`, `missing-variations`

See `references/queries.md` for detailed documentation on each query, including severity levels, common issues, and fix examples.

## Example: General Audit

**User:** "Audit this CLR for me"

1. Validate file: confirm `.xlsx`/`.xlsm` extension and file exists
2. Run full scan: `catalog scan <file> --format json --fields sku,severity,details --limit 50`
3. Parse results: `python3 scripts/parse_audit.py results.json`
4. Present prioritized findings (required issues first)
5. Offer to export or dive deeper into specific queries

## Agent-Optimized Usage

For large catalogs or automated pipelines:

```bash
# Field masks reduce output size
catalog scan <file> --format json --fields sku,severity,details --limit 20

# NDJSON streaming for line-by-line processing
catalog scan <file> --format ndjson --limit 50

# Schema introspection for auto-discovery
catalog schema --format json

# Piped input
echo '{"file": "<clr-path>"}' | catalog scan --stdin --format json
```

For CLRs with 1000+ SKUs, use `--limit` to cap results (expect 10–15s processing time).

## Troubleshooting

If `catalog` is not found, add Python bin to PATH:

```bash
export PATH="$HOME/Library/Python/3.14/bin:$PATH"
# Or run directly: python3 -m catalog.surfaces.cli scan <file>
```

## Resources

- `references/queries.md` — detailed query documentation with fix examples
- `scripts/parse_audit.py` — JSON output processing helper
