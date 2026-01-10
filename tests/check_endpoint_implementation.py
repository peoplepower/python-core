#!/usr/bin/env python3
"""
Script to check that all endpoints defined in cloud.yaml, bots.yaml, and admin.yaml are implemented in the codebase.
"""

import re
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

import yaml


def extract_base_url_from_yaml(yaml_path: Path) -> str:
    """
    Extract the base URL from the servers section in cloud.yaml.
    
    Returns:
        Base URL string (defaults to production URL)
    """
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # Extract first server URL from servers section
    if 'servers' in data and isinstance(data['servers'], list) and len(data['servers']) > 0:
        first_server = data['servers'][0]
        if isinstance(first_server, dict) and 'url' in first_server:
            return first_server['url'].rstrip('/')
    
    # Default fallback
    return "https://app.peoplepowerco.com"


def extract_endpoints_from_yaml(yaml_path: Path) -> Tuple[Dict[str, List[str]], str]:
    """
    Extract all endpoint paths and their HTTP methods from a YAML file using YAML parsing.
    
    Returns:
        Tuple of (endpoints dict mapping path to list of HTTP methods, source filename)
    """
    endpoints = defaultdict(list)
    source_file = yaml_path.name
    
    with open(yaml_path, 'r', encoding='utf-8') as f:
        data = yaml.safe_load(f)
    
    # OpenAPI structure: paths section contains all endpoints
    if 'paths' not in data:
        return dict(endpoints), source_file
    
    paths = data['paths']
    
    # Iterate through each path
    for path, path_item in paths.items():
        if not isinstance(path_item, dict):
            continue
        
        # Check for HTTP methods in the path item
        # Standard HTTP methods in OpenAPI
        http_methods = ['get', 'post', 'put', 'delete', 'patch', 'head', 'options']
        
        for method in http_methods:
            if method in path_item:
                endpoints[path].append(method)
    
    return dict(endpoints), source_file


def normalize_endpoint_path(path: str) -> str:
    """
    Normalize endpoint path for comparison.
    Removes path parameters like {locationId} -> locationId
    """
    # Replace {param} with param for matching
    normalized = re.sub(r'\{([^}]+)\}', r'\1', path)
    return normalized


def find_endpoint_in_codebase(endpoint_path: str, method: str, codebase_path: Path) -> List[str]:
    """
    Search for endpoint implementation in the codebase.
    
    Returns:
        List of file paths where the endpoint is found
    """
    found_files = []
    
    # Normalize endpoint path for searching
    # The YAML has paths like /cloud/json/login but code uses /espapi/cloud/json/login
    # Also handle /espapi/watch, /espapi/version, /admin/json/*, /cloud/developer/*, /analytic/*
    if endpoint_path.startswith('/espapi/'):
        search_paths = [endpoint_path]  # Use as-is
    else:
        search_paths = [f"/espapi{endpoint_path}", endpoint_path]
    
    # Search for the endpoint path in Python files
    for py_file in codebase_path.rglob('*.py'):
        if 'test' in str(py_file):
            continue
            
        try:
            with open(py_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Look for the endpoint path in adapter calls
            # Patterns like: self.adapter.get("/espapi/cloud/json/login", ...)
            # or: self.adapter.post("/espapi/cloud/json/login", ...)
            
            for search_path in search_paths:
                # Escape special regex characters in the path
                escaped_path = re.escape(search_path)
                
                # Match adapter method calls with the endpoint
                # Allow for optional whitespace (including newlines) and different quote types
                # Pattern: adapter.{method}(...whitespace including newlines..."path")
                pattern = rf'adapter\.{method}\s*\(\s*["\']{escaped_path}["\']'
                if re.search(pattern, content, re.IGNORECASE | re.MULTILINE | re.DOTALL):
                    rel_path = str(py_file.relative_to(codebase_path))
                    if rel_path not in found_files:
                        found_files.append(rel_path)
                    break  # Found it, no need to check other search paths
                
                # Also check for f-string patterns with variables
                # Match patterns like f"/espapi/cloud/json/devices/{device_id}" 
                # The YAML uses camelCase (e.g., {fileId}) but code uses snake_case (e.g., {file_id})
                fstring_base = search_path
                # Split the path into parts, handling {param} placeholders
                parts = re.split(r'(\{[^}]+\})', fstring_base)
                escaped_parts = []
                for part in parts:
                    if part.startswith('{') and part.endswith('}'):
                        # Extract the parameter name from YAML (e.g., "fileId" from "{fileId}")
                        param_name = part[1:-1]
                        # Convert camelCase to snake_case for matching
                        # e.g., "fileId" -> "file_id", "locationId" -> "location_id"
                        camel_to_snake = re.sub(r'([a-z])([A-Z])', r'\1_\2', param_name).lower()
                        # Match variable names that could be:
                        # - snake_case: file_id (most common in code)
                        # - camelCase: fileId (if code uses it)
                        # - Or any valid Python identifier as fallback
                        # Build pattern that matches snake_case version (primary) or camelCase
                        snake_pattern = re.escape(camel_to_snake)
                        camel_pattern = re.escape(param_name)
                        # Match either snake_case or camelCase variable name
                        var_pattern = rf'\{{({snake_pattern}|{camel_pattern}|[a-zA-Z_][a-zA-Z0-9_]*)\}}'
                        escaped_parts.append(var_pattern)
                    else:
                        escaped_parts.append(re.escape(part))
                
                # Build the full f-string pattern
                fstring_pattern_full = rf'f["\']{"".join(escaped_parts)}["\']'
                # Match adapter.{method}( with optional whitespace (including newlines) before the f-string
                adapter_pattern = rf'adapter\.{method}\s*\(\s*{fstring_pattern_full}'
                if re.search(adapter_pattern, content, re.IGNORECASE | re.MULTILINE | re.DOTALL):
                    rel_path = str(py_file.relative_to(codebase_path))
                    if rel_path not in found_files:
                        found_files.append(rel_path)
                    break
        except Exception:
            # Skip files that can't be read
            continue
    
    return found_files


def main():
    # Paths
    repo_root = Path(__file__).parent.parent
    api_docs_path = repo_root / 'docs' / 'api'
    codebase_path = repo_root / 'src' / 'caredaily' / 'apis'
    
    # List of YAML files to process
    yaml_files = [
        api_docs_path / 'cloud.yaml',
        api_docs_path / 'bots.yaml',
        api_docs_path / 'admin.yaml'
    ]
    
    # Check if codebase exists
    if not codebase_path.exists():
        print(f"Error: {codebase_path} not found")
        return
    
    # Check which YAML files exist
    existing_yaml_files = []
    for yaml_file in yaml_files:
        if yaml_file.exists():
            existing_yaml_files.append(yaml_file)
        else:
            print(f"Warning: {yaml_file} not found, skipping...")
    
    if not existing_yaml_files:
        print("Error: No YAML files found")
        return
    
    print(f"Extracting endpoints from {len(existing_yaml_files)} YAML file(s)...")
    
    # Extract endpoints from all YAML files
    all_endpoints = defaultdict(list)  # path -> list of methods
    endpoint_sources = defaultdict(list)  # (path, method) -> list of source_files
    base_url = None
    
    for yaml_path in existing_yaml_files:
        print(f"  Processing {yaml_path.name}...")
        endpoints, source_file = extract_endpoints_from_yaml(yaml_path)
        
        # Get base URL from first file (they should all have the same base URL)
        if base_url is None:
            base_url = extract_base_url_from_yaml(yaml_path)
        
        # Add endpoints with source tracking
        for endpoint_path, methods in endpoints.items():
            for method in methods:
                endpoint_key = (endpoint_path, method)
                # Track all sources for this endpoint
                if source_file not in endpoint_sources[endpoint_key]:
                    endpoint_sources[endpoint_key].append(source_file)
                all_endpoints[endpoint_path].append(method)
    
    # Remove duplicate methods per path
    for path in all_endpoints:
        all_endpoints[path] = list(set(all_endpoints[path]))
    
    # Detect duplicate endpoints (same path+method in multiple source files)
    duplicate_endpoints = []
    for (endpoint_path, method), sources in endpoint_sources.items():
        if len(sources) > 1:
            duplicate_endpoints.append({
                'path': endpoint_path,
                'method': method,
                'sources': sources
            })
    
    # Endpoints to ignore (endpoint_path, method)
    ignored_endpoints = {
        ('/cli', 'post'),
    }
    
    print(f"\nFound {len(all_endpoints)} unique endpoint paths")
    print(f"Base URL: {base_url}")
    # Calculate total operations excluding ignored endpoints
    total_operations = sum(
        len([m for m in methods if (path, m) not in ignored_endpoints])
        for path, methods in all_endpoints.items()
    )
    print(f"Total operations: {total_operations} (excluding {len(ignored_endpoints)} ignored)")
    
    print("\nChecking implementations...")
    
    implemented = []
    missing = []
    missing_with_address = []  # Store endpoint with full address and source
    implementation_map = defaultdict(list)
    
    for endpoint_path, methods in sorted(all_endpoints.items()):
        for method in methods:
            # Skip ignored endpoints
            if (endpoint_path, method) in ignored_endpoints:
                continue
            
            found_files = find_endpoint_in_codebase(endpoint_path, method, codebase_path)
            
            endpoint_key = f"{method.upper()} {endpoint_path}"
            # Build full endpoint address
            full_address = f"{base_url}{endpoint_path}"
            sources = endpoint_sources.get((endpoint_path, method), ["unknown"])
            source_file = sources[0]  # Use first source for backward compatibility
            
            if found_files:
                implemented.append(endpoint_key)
                implementation_map[endpoint_key] = found_files
            else:
                missing.append(endpoint_key)
                missing_with_address.append({
                    'method': method.upper(),
                    'path': endpoint_path,
                    'address': full_address,
                    'source': source_file
                })
    
    # Generate report
    print("\n" + "="*80)
    print("ENDPOINT IMPLEMENTATION REPORT")
    print("="*80)
    
    print(f"\n✅ Implemented: {len(implemented)}/{total_operations} ({100*len(implemented)/total_operations:.1f}%)")
    print(f"❌ Missing: {len(missing)}/{total_operations} ({100*len(missing)/total_operations:.1f}%)")
    
    if duplicate_endpoints:
        print("\n" + "="*80)
        print("DUPLICATE ENDPOINTS")
        print("="*80)
        print(f"⚠️  Found {len(duplicate_endpoints)} endpoint(s) defined in multiple source files:")
        for dup in sorted(duplicate_endpoints, key=lambda x: (x['path'], x['method'])):
            print(f"  ⚠️  {dup['method'].upper()} {dup['path']}")
            print(f"     Defined in: {', '.join(dup['sources'])}")
            print("     Note: This endpoint appears in multiple YAML files. Consider consolidating to a single source.")
    
    if missing:
        print("\n" + "="*80)
        print("MISSING ENDPOINTS")
        print("="*80)
        # Sort by source file, then method, then path
        missing_with_address.sort(key=lambda x: (x['source'], x['method'], x['path']))
        for item in missing_with_address:
            print(f"  ❌ {item['method']} {item['path']}")
            print(f"     Address: {item['address']}")
            print(f"     Source: {item['source']}")
    
    # Group by source file, then by endpoint
    print("\n" + "="*80)
    print("IMPLEMENTATION STATUS BY SOURCE FILE")
    print("="*80)
    
    # Group endpoints by source file
    endpoints_by_source = defaultdict(lambda: defaultdict(list))
    for endpoint_path, methods in all_endpoints.items():
        for method in methods:
            # Skip ignored endpoints
            if (endpoint_path, method) in ignored_endpoints:
                continue
            sources = endpoint_sources.get((endpoint_path, method), ["unknown"])
            source_file = sources[0]  # Use first source for grouping
            endpoints_by_source[source_file][endpoint_path].append(method)
    
    for source_file in sorted(endpoints_by_source.keys()):
        print(f"\n{'='*80}")
        print(f"Source: {source_file}")
        print(f"{'='*80}")
        for endpoint_path, methods in sorted(endpoints_by_source[source_file].items()):
            print(f"\n{endpoint_path}:")
            for method in sorted(methods):
                endpoint_key = f"{method.upper()} {endpoint_path}"
                if endpoint_key in implemented:
                    files = implementation_map[endpoint_key]
                    print(f"  ✅ {method.upper()}: {', '.join(files[:2])}" + 
                          (f" (+{len(files)-2} more)" if len(files) > 2 else ""))
                else:
                    print(f"  ❌ {method.upper()}: NOT IMPLEMENTED")
    
    # Save detailed report
    report_path = repo_root / 'tests' / 'ENDPOINT_IMPLEMENTATION_REPORT.md'
    with open(report_path, 'w') as f:
        f.write("# Endpoint Implementation Report\n\n")
        f.write(f"Generated: {__import__('datetime').datetime.now()}\n\n")
        f.write(f"**Total Endpoints:** {len(all_endpoints)}\n")
        f.write(f"**Total Operations:** {total_operations}\n")
        f.write(f"**Source Files:** {', '.join(sorted(set([s for sources in endpoint_sources.values() for s in sources])))}\n")
        f.write(f"**Implemented:** {len(implemented)} ({100*len(implemented)/total_operations:.1f}%)\n")
        f.write(f"**Missing:** {len(missing)} ({100*len(missing)/total_operations:.1f}%)\n")
        f.write(f"**Duplicate Endpoints:** {len(duplicate_endpoints)}\n\n")
        
        if duplicate_endpoints:
            f.write("## Duplicate Endpoints\n\n")
            f.write("⚠️  The following endpoints are defined in multiple source YAML files. ")
            f.write("Consider consolidating these definitions to a single source file to avoid confusion and potential conflicts.\n\n")
            for dup in sorted(duplicate_endpoints, key=lambda x: (x['path'], x['method'])):
                f.write(f"- ⚠️  **{dup['method'].upper()}** `{dup['path']}`\n")
                f.write(f"  - Defined in: {', '.join(dup['sources'])}\n")
            f.write("\n")
        
        f.write("## Missing Endpoints\n\n")
        if missing:
            # Sort by source file, then method, then path
            missing_with_address.sort(key=lambda x: (x['source'], x['method'], x['path']))
            for item in missing_with_address:
                f.write(f"- ❌ **{item['method']}** `{item['path']}`\n")
                f.write(f"  - Address: `{item['address']}`\n")
                f.write(f"  - Source: `{item['source']}`\n")
        else:
            f.write("✅ All endpoints are implemented!\n")
        
        f.write("\n## Implementation Details by Source File\n\n")
        
        # Group endpoints by source file
        endpoints_by_source = defaultdict(lambda: defaultdict(list))
        for endpoint_path, methods in all_endpoints.items():
            for method in methods:
                # Skip ignored endpoints
                if (endpoint_path, method) in ignored_endpoints:
                    continue
                sources = endpoint_sources.get((endpoint_path, method), ["unknown"])
                source_file = sources[0]  # Use first source for grouping
                endpoints_by_source[source_file][endpoint_path].append(method)
        
        for source_file in sorted(endpoints_by_source.keys()):
            f.write(f"### {source_file}\n\n")
            for endpoint_path, methods in sorted(endpoints_by_source[source_file].items()):
                f.write(f"#### {endpoint_path}\n\n")
                for method in sorted(methods):
                    endpoint_key = f"{method.upper()} {endpoint_path}"
                    if endpoint_key in implemented:
                        files = implementation_map[endpoint_key]
                        f.write(f"- ✅ **{method.upper()}**: Implemented in:\n")
                        for file in files:
                            f.write(f"  - `{file}`\n")
                    else:
                        f.write(f"- ❌ **{method.upper()}**: NOT IMPLEMENTED\n")
                f.write("\n")
    
    print(f"\n📄 Detailed report saved to: {report_path}")


if __name__ == '__main__':
    main()
