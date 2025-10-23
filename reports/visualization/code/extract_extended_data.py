#!/usr/bin/env python3
"""
Extract data from extended benchmark logs
Author: AI Assistant
Date: 2025-10-22
"""

import re
import json
import csv
from pathlib import Path

def extract_time_microseconds(line):
    """Extract time in microseconds from log line"""
    # Pattern: "time=1234567 microseconds"
    match = re.search(r'time=(\d+)\s*microseconds', line)
    if match:
        return int(match.group(1))
    return None

def extract_matrix_size(line):
    """Extract matrix size from log line"""
    # Pattern: "m=123" or "n=123"
    match = re.search(r'[mn]=(\d+)', line)
    if match:
        return int(match.group(1))
    return None

def extract_process_count(line):
    """Extract process count from log line"""
    # Pattern: "p=123"
    match = re.search(r'p=(\d+)', line)
    if match:
        return int(match.group(1))
    return None

def extract_method(line):
    """Extract method name from log line"""
    if 'sequentialMult' in line:
        return 'sequential'
    elif 'parallelRowMult' in line:
        return 'parallel_row'
    elif 'parallelElementMult' in line:
        return 'parallel_element'
    return None

def parse_extended_logs():
    """Parse all extended benchmark logs"""
    log_dir = Path('reports/logs')
    data = []
    
    # Extended log files
    extended_files = [
        'extended_threshold.log',
        'extended_performance.log', 
        'extended_scalability.log',
        'extended_limit.log'
    ]
    
    for log_file in extended_files:
        log_path = log_dir / log_file
        if not log_path.exists():
            continue
            
        print(f"Processing {log_file}...")
        
        with open(log_path, 'r') as f:
            lines = f.readlines()
        
        current_matrix_size = None
        current_process_count = None
        
        for line in lines:
            line = line.strip()
            
            # Extract matrix size from ">>> Matrix Size = X"
            matrix_match = re.search(r'>>> Matrix Size = (\d+)', line)
            if matrix_match:
                current_matrix_size = int(matrix_match.group(1))
                continue
            
            # Extract process count from "n=X p=Y"
            process_match = re.search(r'n=(\d+)\s+p=(\d+)', line)
            if process_match:
                current_matrix_size = int(process_match.group(1))
                current_process_count = int(process_match.group(2))
                continue
            
            # Extract timing data
            if 'time=' in line and 'microseconds' in line:
                time_us = extract_time_microseconds(line)
                method = extract_method(line)
                
                if time_us and method and current_matrix_size:
                    data.append({
                        'matrix_size': current_matrix_size,
                        'process_count': current_process_count or 1,
                        'method': method,
                        'time_microseconds': time_us,
                        'time_seconds': time_us / 1_000_000,
                        'source': 'extended'
                    })
    
    return data

def parse_original_log():
    """Parse original comprehensive log"""
    log_path = Path('reports/logs/strassen_comprehensive.log')
    data = []
    
    if not log_path.exists():
        return data
        
    print(f"Processing {log_path.name}...")
    
    with open(log_path, 'r') as f:
        lines = f.readlines()
    
    current_matrix_size = None
    current_process_count = None
    
    for line in lines:
        line = line.strip()
        
        # Extract matrix size
        matrix_match = re.search(r'>>> Matrix Size = (\d+)', line)
        if matrix_match:
            current_matrix_size = int(matrix_match.group(1))
            continue
        
        # Extract process count
        process_match = re.search(r'n=(\d+)\s+p=(\d+)', line)
        if process_match:
            current_matrix_size = int(process_match.group(1))
            current_process_count = int(process_match.group(2))
            continue
        
        # Extract timing data
        if 'time=' in line and 'microseconds' in line:
            time_us = extract_time_microseconds(line)
            method = extract_method(line)
            
            if time_us and method and current_matrix_size:
                data.append({
                    'matrix_size': current_matrix_size,
                    'process_count': current_process_count or 1,
                    'method': method,
                    'time_microseconds': time_us,
                    'time_seconds': time_us / 1_000_000,
                    'source': 'original'
                })
    
    return data

def merge_data(original_data, extended_data):
    """Merge original and extended data"""
    print(f"Merging data: {len(original_data)} original + {len(extended_data)} extended = {len(original_data) + len(extended_data)} total")
    
    # Combine all data
    all_data = original_data + extended_data
    
    # Remove duplicates (keep extended data if duplicate)
    seen = set()
    unique_data = []
    
    for item in all_data:
        key = (item['matrix_size'], item['process_count'], item['method'])
        if key not in seen:
            seen.add(key)
            unique_data.append(item)
        elif item['source'] == 'extended':
            # Replace with extended data
            for i, existing in enumerate(unique_data):
                if (existing['matrix_size'], existing['process_count'], existing['method']) == key:
                    unique_data[i] = item
                    break
    
    return unique_data

def save_data(data, output_dir):
    """Save data to CSV and JSON files"""
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    # Save as CSV
    csv_path = output_path / 'extended_benchmark_data.csv'
    with open(csv_path, 'w', newline='') as f:
        if data:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    
    # Save as JSON
    json_path = output_path / 'extended_benchmark_data.json'
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=2)
    
    print(f"Data saved to:")
    print(f"  CSV: {csv_path}")
    print(f"  JSON: {json_path}")
    
    return csv_path, json_path

def main():
    print("=== EXTRACTING EXTENDED BENCHMARK DATA ===")
    
    # Parse original data
    original_data = parse_original_log()
    print(f"Original data: {len(original_data)} records")
    
    # Parse extended data
    extended_data = parse_extended_logs()
    print(f"Extended data: {len(extended_data)} records")
    
    # Merge data
    merged_data = merge_data(original_data, extended_data)
    print(f"Merged data: {len(merged_data)} records")
    
    # Save data
    csv_path, json_path = save_data(merged_data, 'reports/visualization/data')
    
    # Summary statistics
    print("\n=== DATA SUMMARY ===")
    matrix_sizes = sorted(set(item['matrix_size'] for item in merged_data))
    methods = set(item['method'] for item in merged_data)
    sources = set(item['source'] for item in merged_data)
    
    print(f"Matrix sizes: {len(matrix_sizes)} ({min(matrix_sizes)} to {max(matrix_sizes)})")
    print(f"Methods: {', '.join(methods)}")
    print(f"Sources: {', '.join(sources)}")
    
    # Count by source
    original_count = sum(1 for item in merged_data if item['source'] == 'original')
    extended_count = sum(1 for item in merged_data if item['source'] == 'extended')
    print(f"Original records: {original_count}")
    print(f"Extended records: {extended_count}")
    
    print("\n✅ Data extraction completed!")

if __name__ == "__main__":
    main()
