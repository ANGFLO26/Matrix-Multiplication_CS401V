#!/usr/bin/env python3
"""
Data Extraction Script for Strassen Algorithm Analysis
Trích xuất dữ liệu từ log và tạo file CSV để phân tích
"""

import re
import csv
import json
from collections import defaultdict

def extract_data_from_log(log_file):
    """Trích xuất dữ liệu từ log file"""
    data = {
        'sequential': [],
        'parallel_row': [],
        'parallel_element': []
    }
    
    with open(log_file, 'r') as f:
        content = f.read()
    
    # Extract sequential data
    seq_pattern = r'sequentialMult \(Strassen\): m=(\d+), time=(\d+) microseconds'
    for match in re.finditer(seq_pattern, content):
        matrix_size = int(match.group(1))
        time_us = int(match.group(2))
        data['sequential'].append({
            'matrix_size': matrix_size,
            'time_us': time_us,
            'method': 'sequential'
        })
    
    # Extract parallel row data
    row_pattern = r'parallelRowMult \(Strassen\): m=(\d+), p=(\d+), time=(\d+) microseconds'
    for match in re.finditer(row_pattern, content):
        matrix_size = int(match.group(1))
        processes = int(match.group(2))
        time_us = int(match.group(3))
        data['parallel_row'].append({
            'matrix_size': matrix_size,
            'processes': processes,
            'time_us': time_us,
            'method': 'parallel_row'
        })
    
    # Extract parallel element data
    elem_pattern = r'parallelElementMult \(Strassen\): m=(\d+), p=(\d+), time=(\d+) microseconds'
    for match in re.finditer(elem_pattern, content):
        matrix_size = int(match.group(1))
        processes = int(match.group(2))
        time_us = int(match.group(3))
        data['parallel_element'].append({
            'matrix_size': matrix_size,
            'processes': processes,
            'time_us': time_us,
            'method': 'parallel_element'
        })
    
    return data

def save_to_csv(data, output_file):
    """Lưu dữ liệu ra file CSV"""
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['matrix_size', 'processes', 'time_us', 'method'])
        
        if isinstance(data, dict):
            for method_data in data.values():
                for row in method_data:
                    writer.writerow([
                        row['matrix_size'],
                        row.get('processes', 0),
                        row['time_us'],
                        row['method']
                    ])
        else:  # data is a list
            for row in data:
                writer.writerow([
                row['matrix_size'],
                row.get('processes', 0),
                row['time_us'],
                row['method']
            ])

def save_to_json(data, output_file):
    """Lưu dữ liệu ra file JSON"""
    with open(output_file, 'w') as f:
        json.dump(data, f, indent=2)

def calculate_speedup(data):
    """Tính toán speedup cho mỗi configuration"""
    speedup_data = []
    
    # Get sequential times
    seq_times = {row['matrix_size']: row['time_us'] for row in data['sequential']}
    
    # Calculate speedup for parallel methods
    for method in ['parallel_row', 'parallel_element']:
        for row in data[method]:
            matrix_size = row['matrix_size']
            seq_time = seq_times.get(matrix_size, 0)
            par_time = row['time_us']
            
            if seq_time > 0 and par_time > 0:
                speedup = seq_time / par_time
                speedup_data.append({
                    'matrix_size': matrix_size,
                    'processes': row['processes'],
                    'time_us': par_time,
                    'speedup': speedup,
                    'method': method
                })
    
    return speedup_data

def main():
    log_file = '../../logs/strassen_comprehensive.log'
    output_dir = '../data'
    
    print("Extracting data from benchmark log...")
    
    # Extract data
    data = extract_data_from_log(log_file)
    
    # Save raw data
    save_to_csv(data, f'{output_dir}/raw_data.csv')
    save_to_json(data, f'{output_dir}/raw_data.json')
    
    # Calculate speedup
    speedup_data = calculate_speedup(data)
    save_to_csv(speedup_data, f'{output_dir}/speedup_data.csv')
    save_to_json(speedup_data, f'{output_dir}/speedup_data.json')
    
    print(f"Data extracted successfully to {output_dir}/")
    print("Generated files:")
    print("- raw_data.csv: Raw timing data")
    print("- raw_data.json: Raw timing data (JSON)")
    print("- speedup_data.csv: Speedup calculations")
    print("- speedup_data.json: Speedup calculations (JSON)")

if __name__ == "__main__":
    main()
