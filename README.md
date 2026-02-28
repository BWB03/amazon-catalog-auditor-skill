# Amazon Catalog Auditor - OpenClaw Skill

**OpenClaw skill for auditing Amazon Category Listing Reports**

This skill wraps the [amazon-catalog-cli](https://github.com/BWB03/amazon-catalog-cli) tool to provide automated CLR analysis within OpenClaw workflows.

## What It Does

Enables OpenClaw agents to audit Amazon CLRs with natural language commands:

- "Audit this CLR"
- "Check for missing attributes"
- "What RUFUS issues do I have?"
- "Analyze my catalog health"

The skill automatically:
- Runs catalog queries
- Parses results
- Presents prioritized insights
- Provides actionable recommendations

**New in CLI v1.2.0:**
- ✅ **Bullet point compliance** - Comprehensive validation against Amazon's official requirements
- 🚫 **Prohibited content detection** - Finds banned chars, emojis, placeholder text, prohibited claims
- 📝 **Formatting validation** - Checks capitalization, length, punctuation rules
- 🐛 **Critical bug fix** - Product descriptions no longer incorrectly flagged

**Previous updates (v1.1.0):**
- 🎯 **RUFUS tier scoring** - Each SKU gets a health rating (Good/Fair/Weak/Critical)
- 📊 **Catalog-wide summary** - Overall score + distribution stats
- 🧹 **FBM duplicate filtering** - Auto-skips redundant FBM/MFN SKUs (cleaner reports)

## Installation

### Prerequisites

1. **OpenClaw** installed and running
2. **amazon-catalog-cli** installed:
   ```bash
   pip install amazon-catalog-cli
   ```

### Install Skill

1. Download `amazon-catalog-auditor.skill`
2. Add to your OpenClaw skills directory
3. Restart OpenClaw

**Or via OpenClaw CLI:**
```bash
# Coming soon: OpenClaw skill install command
```

## Usage

### Basic Audit

```
You: Audit this CLR
[attach CLR file]

Agent: 🔍 CLR Audit Results

📊 Summary:
- 47 issues found
- 23 SKUs affected

🔥 Top Priorities:
1. Missing Brand (12 SKUs)
2. RUFUS Bullets scoring low (8 SKUs)
3. Titles exceeding 200 chars (3 SKUs)

💡 Recommendations:
- Add brand to 12 SKUs
- Rewrite Bullet 1 for 8 products
- Trim 3 titles under 200 characters
```

### Specific Checks

```
You: Check my RUFUS bullet optimization

Agent: 📝 RUFUS Bullet Analysis

15 SKUs scoring below 4/5

Common Issues:
1. Bullet 1 missing Hero Benefit (8 SKUs)
2. Bullet 2 missing target audience (5 SKUs)
3. No specific data points (12 SKUs)

Top 3 to fix:
- ABC-123: Score 2/5 (no benefits)
- XYZ-456: Score 2.5/5 (vague language)
- DEF-789: Score 3/5 (needs specifics)
```

### Export for Clients

```
You: Generate a report I can send to my client

Agent: Created client-audit.csv with all 47 issues.
Summary report ready to share.
```

## Features

### 11 Built-in Checks

1. **Missing Attributes** - Required fields
2. **Missing Any Attributes** - Required + conditional
3. **Long Titles** - Over 200 characters
4. **Title Prohibited Chars** - Invalid characters
5. **RUFUS Bullets** - AI optimization scoring
6. **Prohibited Chars** - Invalid characters in title/brand
7. **Bullet Prohibited Content** - Detects banned chars, emojis, claims, placeholders (NEW v1.2.0)
8. **Bullet Formatting** - Validates capitalization, length, punctuation (NEW v1.2.0)
9. **Product Type Mismatch** - Type/keyword alignment
10. **Missing Variations** - Variation opportunities
11. **New Attributes** - Unused template fields

### Intelligent Analysis

- **Prioritization** - Critical issues first
- **Context-aware** - Understands Amazon requirements
- **Actionable** - Specific fix recommendations
- **Export options** - JSON, CSV, or human-readable

## Examples

### Example 1: Full Audit

**User:** "Audit this CLR and prioritize what needs fixing"

**Agent analyzes and responds:**
```
🔍 PlantFusion CLR Audit

📊 Summary: 47 issues, 23 SKUs

🔥 Critical (Fix Now):
• Missing Brand (12 SKUs) - Required field
• Prohibited characters (3 SKUs) - Blocks listing

⚡ Important (Fix Soon):
• RUFUS scores <3 (8 SKUs) - Poor conversion
• Missing conditional fields (15 SKUs) - Product type specific

💡 Optimize (When Time Allows):
• RUFUS scores 3-4 (12 SKUs) - Good, can be great
• Variation opportunities (4 SKUs) - Bundle related products

Quick wins: Fix brand + prohibited chars = 15 issues resolved
```

### Example 2: RUFUS Deep Dive

**User:** "Why are my bullet points scoring low?"

**Agent explains:**
```
📝 RUFUS Analysis for 8 low-scoring SKUs

Position-specific issues:

Bullet 1 (Hero Benefit):
❌ "Premium quality hair gel with amazing hold"
✅ "Reduce frizz by 80% and add lasting shine"

Bullet 2 (Target Audience):
❌ "Great for styling"
✅ "Ideal for curly or wavy hair, perfect for all-day hold"

Common problems:
• Vague marketing (5 SKUs) - "premium", "amazing", "best"
• Missing data points (7 SKUs) - Add %, oz, count, time
• Too short (3 SKUs) - Expand with specifics

Want me to rewrite examples for your top 3 SKUs?
```

## Requirements

- **OpenClaw** 2024.2+
- **amazon-catalog-cli** 1.2.0+ (recommended for bullet validation features)
- **Python** 3.7+

## How It Works

1. User uploads CLR or provides file path
2. Skill runs `catalog scan` command
3. Parses JSON output
4. Analyzes by severity and priority
5. Presents human-readable insights
6. Offers export options if needed

The skill uses the CLI tool under the hood, so all 11 queries stay up-to-date automatically when the CLI is updated.

## Security & Safety

**This skill is designed with security in mind:**

### What It Does ✅
- **Read-only operations** - Only reads CLR files from your workspace
- **Deterministic parsing** - Pure Python logic, no AI model calls
- **Local execution** - All processing happens on your machine
- **Output files only** - Creates reports in workspace, nothing else
- **Open source** - Full code transparency

### What It Doesn't Do ❌
- **No network calls** - Doesn't phone home or transmit data
- **No credential storage** - Doesn't ask for or store API keys
- **No system modifications** - Doesn't touch files outside workspace
- **No external dependencies** - Only uses `amazon-catalog-cli` (also open source)
- **No telemetry** - Zero tracking or analytics

### Skill Safety Best Practices

When evaluating **any** OpenClaw skill (including this one):

1. **Review the code** - Check `SKILL.md` and `scripts/` folder
2. **Verify dependencies** - Fewer is better, inspect what gets installed
3. **Check the source** - Install from trusted developers/official repos
4. **Understand permissions** - Know what file access the skill needs
5. **Monitor behavior** - Watch what commands it runs

### Worst-Case Scenario

If this skill had a bug or was compromised:
- ❌ **NOT possible:** System compromise, data theft, malicious execution
- ✅ **Possible:** Incorrect audit results, file path errors, skill crashes

**Why it's safe:** The skill is a thin wrapper around a deterministic CLI tool. It doesn't make decisions, doesn't connect to external services, and operates entirely within your workspace sandbox.

### Trust Chain

1. **amazon-catalog-cli** - Open source Python package on PyPI
2. **This skill** - Wraps the CLI with OpenClaw-friendly interface
3. **Your OpenClaw instance** - Executes within your configured sandbox

All three layers are auditable, transparent, and under your control.

### Questions or Concerns?

Open an issue on GitHub or review the code yourself. Security through transparency.

## Related Projects

- **[amazon-catalog-cli](https://github.com/BWB03/amazon-catalog-cli)** - Standalone CLI tool (required)
- **[clr-auditor](https://github.com/BWB03/clr-auditor)** - Original Python auditor
- **[amazon-tool](https://github.com/BWB03/amazon-tool)** - Variation creator

## Contributing

Contributions welcome! To improve this skill:

1. Fork the repo
2. Update SKILL.md or add examples
3. Test with real CLRs
4. Submit PR

## Updates

When the CLI tool adds new features:
- The skill automatically uses them (no update needed)

When the skill documentation improves:
- Download the latest `.skill` file
- Replace in your skills directory

## Support

- **Issues:** [GitHub Issues](https://github.com/BWB03/amazon-catalog-auditor-skill/issues)
- **CLI Issues:** [amazon-catalog-cli Issues](https://github.com/BWB03/amazon-catalog-cli/issues)
- **OpenClaw:** [OpenClaw Discord](https://discord.com/invite/clawd)

## License

MIT License - Free to use, modify, and distribute.

## Author

Built by Brett Bohannon ([@BWB03](https://github.com/BWB03))

Amazon consulting veteran, AI automation enthusiast, OpenClaw power user.

---

**First OpenClaw skill for Amazon catalog management.** Built for consultants automating client work.
