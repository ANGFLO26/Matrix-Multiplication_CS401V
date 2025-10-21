#!/usr/bin/env python3
"""
Advanced Chart Generation for Strassen Algorithm Performance Analysis
Tạo các biểu đồ chi tiết từ dữ liệu benchmark
"""

import re
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# Set style
plt.style.use('default')

def parse_benchmark_log(log_file):
    """Parse benchmark log và trích xuất dữ liệu timing"""
    results = {
        'sequential': [],
        'parallel_row': defaultdict(list),
        'parallel_element': defaultdict(list)
    }
    
    with open(log_file, 'r') as f:
        content = f.read()
    
    # Extract sequential results
    seq_pattern = r'sequentialMult \(Strassen\): m=(\d+), time=(\d+) microseconds'
    for match in re.finditer(seq_pattern, content):
        matrix_size = int(match.group(1))
        time_us = int(match.group(2))
        results['sequential'].append((matrix_size, time_us))
    
    # Extract parallel row results
    row_pattern = r'parallelRowMult \(Strassen\): m=(\d+), p=(\d+), time=(\d+) microseconds'
    for match in re.finditer(row_pattern, content):
        matrix_size = int(match.group(1))
        processes = int(match.group(2))
        time_us = int(match.group(3))
        results['parallel_row'][processes].append((matrix_size, time_us))
    
    # Extract parallel element results
    elem_pattern = r'parallelElementMult \(Strassen\): m=(\d+), p=(\d+), time=(\d+) microseconds'
    for match in re.finditer(elem_pattern, content):
        matrix_size = int(match.group(1))
        processes = int(match.group(2))
        time_us = int(match.group(3))
        results['parallel_element'][processes].append((matrix_size, time_us))
    
    return results

def create_speedup_vs_matrix_size_chart(results, output_dir):
    """Biểu đồ 1: Speedup vs Matrix Size"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    matrix_sizes = [size for size, _ in results['sequential']]
    seq_times = [time for _, time in results['sequential']]
    
    # Calculate speedup for each configuration
    colors = ['red', 'green', 'blue', 'orange', 'purple', 'brown']
    markers = ['o', 's', '^', 'D', 'v', '<']
    
    for i, (processes, times) in enumerate(results['parallel_row'].items()):
        sizes = [size for size, _ in times]
        times_list = [time for _, time in times]
        speedup = []
        
        for j, size in enumerate(sizes):
            seq_time = next((time for s, time in results['sequential'] if s == size), None)
            if seq_time and times_list[j] > 0:
                speedup.append(seq_time / times_list[j])
            else:
                speedup.append(0)
        
        ax.plot(sizes, speedup, f'{markers[i]}-', 
                label=f'Parallel Row (p={processes})', 
                color=colors[i], linewidth=2, markersize=6)
    
    for i, (processes, times) in enumerate(results['parallel_element'].items()):
        sizes = [size for size, _ in times]
        times_list = [time for _, time in times]
        speedup = []
        
        for j, size in enumerate(sizes):
            seq_time = next((time for s, time in results['sequential'] if s == size), None)
            if seq_time and times_list[j] > 0:
                speedup.append(seq_time / times_list[j])
            else:
                speedup.append(0)
        
        ax.plot(sizes, speedup, f'{markers[i+3]}--', 
                label=f'Parallel Element (p={processes})', 
                color=colors[i+3], linewidth=2, markersize=6)
    
    ax.set_xlabel('Matrix Size (n×n)', fontsize=12)
    ax.set_ylabel('Speedup', fontsize=12)
    ax.set_title('Strassen Algorithm: Speedup vs Matrix Size', fontsize=14, fontweight='bold')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/01_speedup_vs_matrix_size.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_speedup_vs_process_count_chart(results, output_dir):
    """Biểu đồ 2: Speedup vs Process Count"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Focus on key matrix sizes
    key_sizes = [256, 512, 1024]
    colors = ['red', 'green', 'blue']
    
    for i, size in enumerate(key_sizes):
        if size in [s for s, _ in results['sequential']]:
            seq_time = next(time for s, time in results['sequential'] if s == size)
            
            # Parallel Row data
            row_speedup = []
            processes = [10, 100, 1000]
            
            for p in processes:
                if p in results['parallel_row']:
                    time = next((t for s, t in results['parallel_row'][p] if s == size), None)
                    if time and time > 0:
                        row_speedup.append(seq_time / time)
                    else:
                        row_speedup.append(0)
                else:
                    row_speedup.append(0)
            
            ax.plot(processes, row_speedup, f'o-', 
                    label=f'Parallel Row (n={size})', 
                    color=colors[i], linewidth=2, markersize=8)
    
    ax.set_xlabel('Process Count', fontsize=12)
    ax.set_ylabel('Speedup', fontsize=12)
    ax.set_title('Strassen Algorithm: Speedup vs Process Count', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/02_speedup_vs_process_count.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_row_vs_element_comparison_chart(results, output_dir):
    """Biểu đồ 3: Row vs Element Comparison"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    matrix_sizes = [size for size, _ in results['sequential']]
    seq_times = [time for _, time in results['sequential']]
    
    # Get best parallel times for each matrix size
    row_times = []
    elem_times = []
    
    for size in matrix_sizes:
        # Find best parallel row time
        best_row_time = float('inf')
        for processes, times in results['parallel_row'].items():
            time = next((t for s, t in times if s == size), None)
            if time and time < best_row_time:
                best_row_time = time
        
        # Find best parallel element time
        best_elem_time = float('inf')
        for processes, times in results['parallel_element'].items():
            time = next((t for s, t in times if s == size), None)
            if time and time < best_elem_time:
                best_elem_time = time
        
        row_times.append(best_row_time if best_row_time != float('inf') else 0)
        elem_times.append(best_elem_time if best_elem_time != float('inf') else 0)
    
    x = np.arange(len(matrix_sizes))
    width = 0.25
    
    ax.bar(x - width, seq_times, width, label='Sequential', alpha=0.8)
    ax.bar(x, row_times, width, label='Parallel Row (Best)', alpha=0.8)
    ax.bar(x + width, elem_times, width, label='Parallel Element (Best)', alpha=0.8)
    
    ax.set_xlabel('Matrix Size (n×n)', fontsize=12)
    ax.set_ylabel('Execution Time (microseconds)', fontsize=12)
    ax.set_title('Strassen Algorithm: Performance Comparison', fontsize=14, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(matrix_sizes)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/03_row_vs_element_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_efficiency_heatmap(results, output_dir):
    """Biểu đồ 4: Efficiency Heatmap"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Create efficiency matrix
    matrix_sizes = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
    process_counts = [10, 100, 1000]
    
    efficiency_matrix = np.zeros((len(matrix_sizes), len(process_counts)))
    
    for i, size in enumerate(matrix_sizes):
        seq_time = next((time for s, time in results['sequential'] if s == size), None)
        if seq_time:
            for j, processes in enumerate(process_counts):
                if processes in results['parallel_row']:
                    time = next((t for s, t in results['parallel_row'][processes] if s == size), None)
                    if time and time > 0:
                        efficiency_matrix[i][j] = seq_time / time
                    else:
                        efficiency_matrix[i][j] = 0
    
    # Create heatmap
    im = ax.imshow(efficiency_matrix, cmap='RdYlGn', aspect='auto')
    
    # Set labels
    ax.set_xticks(range(len(process_counts)))
    ax.set_xticklabels(process_counts)
    ax.set_yticks(range(len(matrix_sizes)))
    ax.set_yticklabels(matrix_sizes)
    
    ax.set_xlabel('Process Count', fontsize=12)
    ax.set_ylabel('Matrix Size', fontsize=12)
    ax.set_title('Strassen Algorithm: Efficiency Heatmap', fontsize=14, fontweight='bold')
    
    # Add colorbar
    cbar = plt.colorbar(im, ax=ax)
    cbar.set_label('Speedup', fontsize=12)
    
    # Add text annotations
    for i in range(len(matrix_sizes)):
        for j in range(len(process_counts)):
            text = ax.text(j, i, f'{efficiency_matrix[i, j]:.1f}',
                          ha="center", va="center", color="black", fontsize=8)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/04_efficiency_heatmap.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_optimal_process_analysis(results, output_dir):
    """Biểu đồ 5: Optimal Process Count Analysis"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    matrix_sizes = []
    optimal_processes = []
    
    for size, seq_time in results['sequential']:
        if seq_time > 0:
            best_speedup = 0
            best_processes = 10
            
            for processes in [10, 100, 1000]:
                if processes in results['parallel_row']:
                    time = next((t for s, t in results['parallel_row'][processes] if s == size), None)
                    if time and time > 0:
                        speedup = seq_time / time
                        if speedup > best_speedup:
                            best_speedup = speedup
                            best_processes = processes
            
            matrix_sizes.append(size)
            optimal_processes.append(best_processes)
    
    if len(matrix_sizes) > 0 and len(optimal_processes) > 0:
        # Create scatter plot
        ax.scatter(matrix_sizes, optimal_processes, s=100, alpha=0.7, c='red')
        
        # Add trend line if we have enough points
        if len(matrix_sizes) > 1:
            z = np.polyfit(matrix_sizes, optimal_processes, 1)
            p = np.poly1d(z)
            ax.plot(matrix_sizes, p(matrix_sizes), "r--", alpha=0.8, linewidth=2)
    
    ax.set_xlabel('Matrix Size (n×n)', fontsize=12)
    ax.set_ylabel('Optimal Process Count', fontsize=12)
    ax.set_title('Strassen Algorithm: Optimal Process Count Analysis', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/05_optimal_process_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_memory_usage_analysis(results, output_dir):
    """Biểu đồ 7: Memory Usage Analysis"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    matrix_sizes = [size for size, _ in results['sequential']]
    
    # Calculate memory usage (assuming double precision)
    memory_usage = []
    for size in matrix_sizes:
        # 3 matrices (A, B, C) * size^2 * 8 bytes (double)
        memory = 3 * size * size * 8 / (1024 * 1024)  # Convert to MB
        memory_usage.append(memory)
    
    ax.plot(matrix_sizes, memory_usage, 'o-', linewidth=2, markersize=6, color='blue')
    ax.fill_between(matrix_sizes, memory_usage, alpha=0.3, color='blue')
    
    ax.set_xlabel('Matrix Size (n×n)', fontsize=12)
    ax.set_ylabel('Memory Usage (MB)', fontsize=12)
    ax.set_title('Strassen Algorithm: Memory Usage Analysis', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    # Add memory threshold line
    ax.axhline(y=100, color='red', linestyle='--', alpha=0.7, label='100MB threshold')
    ax.axhline(y=1000, color='orange', linestyle='--', alpha=0.7, label='1GB threshold')
    ax.legend()
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/07_memory_usage_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_overhead_analysis(results, output_dir):
    """Biểu đồ 8: Overhead Analysis"""
    fig, ax = plt.subplots(figsize=(14, 8))
    
    matrix_sizes = [size for size, _ in results['sequential']]
    seq_times = [time for _, time in results['sequential']]
    
    # Calculate overhead for different process counts
    process_counts = [10, 100, 1000]
    colors = ['red', 'green', 'blue']
    
    for i, processes in enumerate(process_counts):
        if processes in results['parallel_row']:
            times = results['parallel_row'][processes]
            parallel_times = []
            overhead_times = []
            
            for size in matrix_sizes:
                seq_time = next((time for s, time in results['sequential'] if s == size), None)
                par_time = next((time for s, time in times if s == size), None)
                
                if seq_time and par_time:
                    parallel_times.append(par_time)
                    # Estimate overhead as difference between parallel and theoretical minimum
                    theoretical_min = seq_time / processes  # Ideal speedup
                    overhead = max(0, par_time - theoretical_min)
                    overhead_times.append(overhead)
                else:
                    parallel_times.append(0)
                    overhead_times.append(0)
            
            # Create stacked bar chart
            ax.bar([x + i*0.25 for x in range(len(matrix_sizes))], 
                   parallel_times, 0.25, 
                   label=f'Parallel Time (p={processes})', 
                   color=colors[i], alpha=0.7)
            ax.bar([x + i*0.25 for x in range(len(matrix_sizes))], 
                   overhead_times, 0.25, 
                   bottom=parallel_times,
                   label=f'Overhead (p={processes})', 
                   color=colors[i], alpha=0.3)
    
    ax.set_xlabel('Matrix Size (n×n)', fontsize=12)
    ax.set_ylabel('Time (microseconds)', fontsize=12)
    ax.set_title('Strassen Algorithm: Overhead Analysis', fontsize=14, fontweight='bold')
    ax.set_xticks(range(len(matrix_sizes)))
    ax.set_xticklabels(matrix_sizes)
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/08_overhead_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    log_file = '../../logs/strassen_comprehensive.log'
    output_dir = '../../charts'
    
    print("Generating advanced charts for Strassen Algorithm analysis...")
    
    # Parse results
    results = parse_benchmark_log(log_file)
    
    # Create all charts
    print("1. Creating speedup vs matrix size chart...")
    create_speedup_vs_matrix_size_chart(results, output_dir)
    
    print("2. Creating speedup vs process count chart...")
    create_speedup_vs_process_count_chart(results, output_dir)
    
    print("3. Creating row vs element comparison chart...")
    create_row_vs_element_comparison_chart(results, output_dir)
    
    print("4. Creating efficiency heatmap...")
    create_efficiency_heatmap(results, output_dir)
    
    # Removed redundant charts (5, 7, 8) - keeping only essential ones
    
    print(f"All essential charts generated successfully in {output_dir}/")
    print("Generated files:")
    print("- 01_speedup_vs_matrix_size.png")
    print("- 02_speedup_vs_process_count.png") 
    print("- 03_row_vs_element_comparison.png")
    print("- 04_efficiency_heatmap.png")

if __name__ == "__main__":
    main()
