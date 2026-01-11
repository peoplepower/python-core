#!/usr/bin/env python3
"""Generate API test coverage report from coverage.json"""

import json
import os
from datetime import datetime
from pathlib import Path
from collections import defaultdict

def get_coverage_percentage(file_data):
    """Calculate coverage percentage for a file"""
    if file_data['summary']['num_statements'] == 0:
        return 100.0
    return file_data['summary']['percent_covered']

def categorize_file(filepath):
    """Categorize API file into admin, app, bot, device, or service"""
    parts = Path(filepath).parts
    if 'admin' in parts:
        return 'admin'
    elif 'app' in parts:
        return 'app'
    elif 'bot' in parts:
        return 'bot'
    elif 'device' in parts:
        return 'device'
    elif 'service' in parts:
        return 'service'
    return 'other'

def generate_report(coverage_json_path, output_path):
    """Generate markdown coverage report"""
    with open(coverage_json_path, 'r') as f:
        data = json.load(f)
    
    files = data['files']
    totals = data['totals']
    
    # Organize files by category
    categories = defaultdict(list)
    for filepath, file_data in files.items():
        if 'src/caredaily/apis/' in filepath:
            category = categorize_file(filepath)
            if category != 'other':
                rel_path = filepath.replace('src/caredaily/apis/', '')
                coverage = get_coverage_percentage(file_data)
                categories[category].append((rel_path, coverage, file_data))
    
    # Sort files within each category
    for category in categories:
        categories[category].sort(key=lambda x: x[0])
    
    # Generate report
    report_lines = []
    report_lines.append("# API Test Coverage Report\n")
    report_lines.append(f"Generated: {datetime.now().strftime('%a %b %d %H:%M:%S %Z %Y')}\n")
    report_lines.append("\n## Summary\n")
    report_lines.append("\nThis report provides code coverage statistics for all API files in `src/caredaily/apis/` based on pytest coverage analysis.\n")
    report_lines.append(f"\n**Overall Coverage: {totals['percent_covered']:.1f}%** ({totals['num_statements']} statements, {totals['missing_lines']} missing)\n")
    report_lines.append("\n## Test Coverage Status\n")
    
    # Category mappings
    category_names = {
        'admin': 'Admin APIs',
        'app': 'App APIs',
        'bot': 'Bot APIs',
        'device': 'Device APIs',
        'service': 'Service APIs'
    }
    
    category_stats = {}
    
    for category in ['admin', 'app', 'bot', 'device', 'service']:
        if category not in categories:
            continue
            
        files_list = categories[category]
        report_lines.append(f"\n### {category_names[category]} ({len(files_list)} files)\n")
        report_lines.append("\n| API File | Code Coverage | Status |\n")
        report_lines.append("|----------|---------------|--------|\n")
        
        total_coverage = 0
        files_at_100 = 0
        files_below_50 = 0
        
        for rel_path, coverage, file_data in files_list:
            status = "✅" if coverage >= 100 else "⚠️" if coverage >= 50 else "❌"
            report_lines.append(f"| `{rel_path}` | {coverage:.0f}% | {status} |\n")
            total_coverage += coverage
            if coverage >= 100:
                files_at_100 += 1
            if coverage < 50:
                files_below_50 += 1
        
        avg_coverage = total_coverage / len(files_list) if files_list else 0
        category_stats[category] = {
            'count': len(files_list),
            'avg': avg_coverage,
            'at_100': files_at_100,
            'below_50': files_below_50
        }
        report_lines.append(f"\n**{category_names[category]} Average Coverage: {avg_coverage:.0f}%**\n")
    
    # Overall statistics
    report_lines.append("\n## Overall Statistics\n\n")
    total_files = sum(stats['count'] for stats in category_stats.values())
    report_lines.append(f"- **Total API Files:** {total_files}\n")
    report_lines.append(f"- **Code Coverage:** {totals['percent_covered']:.1f}% ({totals['num_statements']} statements, {totals['missing_lines']} missing)\n")
    
    # Coverage by category
    report_lines.append("\n## Coverage by Category\n\n")
    report_lines.append("| Category | Files | Average Coverage | Files at 100% | Files < 50% |\n")
    report_lines.append("|----------|-------|------------------|---------------|-------------|\n")
    
    for category in ['admin', 'app', 'bot', 'device', 'service']:
        if category in category_stats:
            stats = category_stats[category]
            report_lines.append(f"| {category_names[category]} | {stats['count']} | {stats['avg']:.0f}% | {stats['at_100']} | {stats['below_50']} |\n")
    
    # Files requiring attention
    report_lines.append("\n## Files Requiring Attention (Coverage < 50%)\n\n")
    
    critical_files = []
    medium_files = []
    
    for category in ['admin', 'app', 'bot', 'device', 'service']:
        if category not in categories:
            continue
        for rel_path, coverage, _ in categories[category]:
            if coverage < 30:
                critical_files.append((rel_path, coverage))
            elif coverage < 50:
                medium_files.append((rel_path, coverage))
    
    critical_files.sort(key=lambda x: x[1])
    medium_files.sort(key=lambda x: x[1])
    
    if critical_files:
        report_lines.append("### Critical Priority (< 30% coverage)\n")
        for rel_path, coverage in critical_files:
            report_lines.append(f"- `{rel_path}` - {coverage:.0f}%\n")
    
    if medium_files:
        report_lines.append("\n### Medium Priority (30-49% coverage)\n")
        for rel_path, coverage in medium_files:
            report_lines.append(f"- `{rel_path}` - {coverage:.0f}%\n")
    
    # Write report
    with open(output_path, 'w') as f:
        f.writelines(report_lines)
    
    print(f"Coverage report generated: {output_path}")

if __name__ == '__main__':
    script_dir = Path(__file__).parent
    coverage_json = script_dir / 'coverage.json'
    output_file = script_dir / 'API_TEST_COVERAGE_REPORT.md'
    
    generate_report(coverage_json, output_file)
