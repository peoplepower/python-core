# Coverage Report Maintenance Instructions

## Overview

The API test coverage report (`API_TEST_COVERAGE_REPORT.md`) is automatically generated from pytest coverage data. This document explains how to update and maintain the report.

## Prerequisites

- Python virtual environment (`venv`) must be activated
- `pytest-cov` must be installed (included in `dev` dependencies)

## Updating the Coverage Report

### Quick Update (Recommended)

Run the following command from the project root:

```bash
source venv/bin/activate
pytest --cov=src/caredaily/apis --cov-report=term-missing --cov-report=html:htmlcov --cov-report=json:tests/coverage.json -v
python tests/generate_coverage_report.py
```

This will:
1. Run all tests with coverage analysis
2. Generate coverage data in JSON format
3. Automatically generate the updated markdown report in `tests/API_TEST_COVERAGE_REPORT.md`

### Step-by-Step Process

1. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```

2. **Run pytest with coverage:**
   ```bash
   pytest --cov=src/caredaily/apis --cov-report=term-missing --cov-report=html:htmlcov --cov-report=json:tests/coverage.json -v
   ```
   
   This generates:
   - Terminal output with coverage summary
   - HTML report in `htmlcov/` directory (for detailed browsing)
   - JSON data in `tests/coverage.json` (used by the report generator)

3. **Generate the markdown report:**
   ```bash
   python generate_coverage_report.py
   ```
   
   This reads `tests/coverage.json` and generates `tests/API_TEST_COVERAGE_REPORT.md`

4. **Cleanup coverate:**
   ```bash
   rm tests/coverage.json
   ```

   This removes the coverage.json file for the next report.

## Report Contents

The generated report includes:

- **Summary**: Overall coverage percentage and statistics
- **Test Coverage Status**: Detailed coverage by API category (Admin, App, Bot, Device, Service)
- **Overall Statistics**: Total files and coverage metrics
- **Coverage by Category**: Summary table with averages
- **Files Requiring Attention**: Lists files with coverage below 50%, prioritized by severity

## When to Update

Update the coverage report:

- **After adding new API files** - To ensure new files are tracked
- **After adding new tests** - To reflect improved coverage
- **Before releases** - To document current test coverage status
- **Periodically** - As part of regular maintenance (e.g., weekly/monthly)

## Notes

- The HTML coverage report (`htmlcov/`) provides detailed line-by-line coverage and can be opened in a browser
- The JSON coverage data (`tests/coverage.json`) is used by the report generator and can be analyzed programmatically
- Coverage percentages are rounded to whole numbers in the report for readability
- Files with 100% coverage are marked with ✅, 50-99% with ⚠️, and <50% with ❌
