#!/usr/bin/env python3
"""
Parse amazon-catalog-cli JSON output into human-readable insights
"""

import json
import sys
from collections import defaultdict


def parse_audit_json(json_path):
    """Parse audit JSON and extract key insights"""
    
    with open(json_path, 'r') as f:
        data = json.load(f)
    
    insights = {
        'total_issues': data.get('total_issues', 0),
        'total_skus': data.get('total_affected_skus', 0),
        'by_query': {},
        'by_severity': defaultdict(int),
        'top_skus': defaultdict(int),
        'critical_issues': []
    }
    
    # Process each query
    for query in data.get('queries', []):
        query_name = query['query_name']
        total = query['total_issues']
        
        insights['by_query'][query_name] = {
            'total': total,
            'affected_skus': query['affected_skus']
        }
        
        # Count by severity
        for issue in query.get('issues', []):
            severity = issue.get('severity', 'unknown')
            insights['by_severity'][severity] += 1
            
            # Track problematic SKUs
            sku = issue.get('sku', 'N/A')
            insights['top_skus'][sku] += 1
            
            # Flag critical issues
            if severity == 'required':
                insights['critical_issues'].append({
                    'sku': sku,
                    'field': issue.get('field', ''),
                    'details': issue.get('details', '')
                })
    
    return insights


def format_insights(insights):
    """Format insights into human-readable text"""
    
    output = []
    
    # Header
    output.append("🔍 CLR AUDIT INSIGHTS\n")
    output.append("=" * 50)
    
    # Summary
    output.append(f"\n📊 SUMMARY:")
    output.append(f"  Total Issues: {insights['total_issues']}")
    output.append(f"  Affected SKUs: {insights['total_skus']}")
    
    # By severity
    output.append(f"\n⚠️  BY SEVERITY:")
    for severity, count in sorted(insights['by_severity'].items()):
        icon = {
            'required': '🔴',
            'conditional': '🟡',
            'warning': '🟠',
            'info': '🔵'
        }.get(severity, '⚪')
        output.append(f"  {icon} {severity.title()}: {count}")
    
    # Top queries
    output.append(f"\n🔍 TOP ISSUES:")
    sorted_queries = sorted(
        insights['by_query'].items(),
        key=lambda x: x[1]['total'],
        reverse=True
    )[:5]
    
    for query_name, data in sorted_queries:
        if data['total'] > 0:
            output.append(f"  • {query_name}: {data['total']} issues ({data['affected_skus']} SKUs)")
    
    # Top problematic SKUs
    if insights['top_skus']:
        output.append(f"\n🎯 TOP PROBLEMATIC SKUs:")
        sorted_skus = sorted(
            insights['top_skus'].items(),
            key=lambda x: x[1],
            reverse=True
        )[:5]
        
        for sku, count in sorted_skus:
            output.append(f"  • {sku}: {count} issues")
    
    # Critical issues sample
    if insights['critical_issues']:
        output.append(f"\n🚨 CRITICAL ISSUES (Sample):")
        for issue in insights['critical_issues'][:5]:
            output.append(f"  • {issue['sku']}: {issue['field']} - {issue['details'][:60]}")
        
        if len(insights['critical_issues']) > 5:
            output.append(f"  ... and {len(insights['critical_issues']) - 5} more")
    
    output.append("\n" + "=" * 50)
    
    return "\n".join(output)


def main():
    if len(sys.argv) < 2:
        print("Usage: parse_audit.py <json-file>")
        print("\nExample:")
        print("  parse_audit.py results.json")
        sys.exit(1)
    
    json_path = sys.argv[1]
    
    try:
        insights = parse_audit_json(json_path)
        output = format_insights(insights)
        print(output)
    
    except FileNotFoundError:
        print(f"Error: File not found: {json_path}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"Error: Invalid JSON file: {json_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
