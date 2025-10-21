#!/usr/bin/env python3
"""
Additional Chart Generation for Strassen Algorithm Analysis
Tạo các biểu đồ bổ sung để trực quan hóa hoàn thiện hơn
"""

import re
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from mpl_toolkits.mplot3d import Axes3D

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

def create_algorithm_complexity_chart(results, output_dir):
    """Biểu đồ 9: Algorithm Complexity Comparison"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    matrix_sizes = [size for size, _ in results['sequential']]
    
    # Theoretical operations count
    naive_ops = [size**3 for size in matrix_sizes]
    strassen_ops = [size**(np.log2(7)) for size in matrix_sizes]
    
    ax.plot(matrix_sizes, naive_ops, 'r-', linewidth=2, label='Naive O(n³)', marker='o')
    ax.plot(matrix_sizes, strassen_ops, 'b-', linewidth=2, label='Strassen O(n^log₂7)', marker='s')
    
    # Actual performance (scaled)
    seq_times = [time for _, time in results['sequential']]
    max_ops = max(max(naive_ops), max(strassen_ops))
    max_time = max(seq_times)
    scaled_times = [time * max_ops / max_time for time in seq_times]
    
    ax.plot(matrix_sizes, scaled_times, 'g--', linewidth=2, label='Actual Performance (scaled)', marker='^')
    
    ax.set_xlabel('Matrix Size (n×n)', fontsize=12)
    ax.set_ylabel('Operations Count (log scale)', fontsize=12)
    ax.set_title('Strassen Algorithm: Theoretical vs Actual Complexity', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/09_algorithm_complexity.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_performance_per_core_chart(results, output_dir):
    """Biểu đồ 10: Performance per Core Analysis"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    matrix_sizes = [size for size, _ in results['sequential']]
    process_counts = [10, 100, 1000]
    colors = ['red', 'green', 'blue']
    
    for i, processes in enumerate(process_counts):
        if processes in results['parallel_row']:
            times = results['parallel_row'][processes]
            time_per_core = []
            
            for size in matrix_sizes:
                time = next((t for s, t in times if s == size), None)
                if time:
                    time_per_core.append(time / processes)
                else:
                    time_per_core.append(0)
            
            ax.plot(matrix_sizes, time_per_core, f'o-', 
                    label=f'Time per Core (p={processes})', 
                    color=colors[i], linewidth=2, markersize=6)
    
    ax.set_xlabel('Matrix Size (n×n)', fontsize=12)
    ax.set_ylabel('Time per Core (microseconds)', fontsize=12)
    ax.set_title('Strassen Algorithm: Performance per Core Analysis', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    ax.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/10_performance_per_core.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_scalability_analysis_chart(results, output_dir):
    """Biểu đồ 11: Scalability Analysis"""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    
    matrix_sizes = [size for size, _ in results['sequential']]
    seq_times = [time for _, time in results['sequential']]
    
    # Speedup analysis
    for processes in [10, 100, 1000]:
        if processes in results['parallel_row']:
            times = results['parallel_row'][processes]
            speedup = []
            
            for i, size in enumerate(matrix_sizes):
                seq_time = seq_times[i]
                par_time = next((t for s, t in times if s == size), None)
                if par_time and par_time > 0:
                    speedup.append(seq_time / par_time)
                else:
                    speedup.append(0)
            
            ax1.plot(matrix_sizes, speedup, f'o-', 
                    label=f'p={processes}', linewidth=2, markersize=4)
    
    ax1.set_xlabel('Matrix Size (n×n)')
    ax1.set_ylabel('Speedup')
    ax1.set_title('Speedup vs Matrix Size')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')
    
    # Efficiency analysis
    for processes in [10, 100, 1000]:
        if processes in results['parallel_row']:
            times = results['parallel_row'][processes]
            efficiency = []
            
            for i, size in enumerate(matrix_sizes):
                seq_time = seq_times[i]
                par_time = next((t for s, t in times if s == size), None)
                if par_time and par_time > 0:
                    eff = (seq_time / par_time) / processes * 100
                    efficiency.append(eff)
                else:
                    efficiency.append(0)
            
            ax2.plot(matrix_sizes, efficiency, f's-', 
                    label=f'p={processes}', linewidth=2, markersize=4)
    
    ax2.set_xlabel('Matrix Size (n×n)')
    ax2.set_ylabel('Efficiency (%)')
    ax2.set_title('Efficiency vs Matrix Size')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log')
    
    # Throughput analysis
    for processes in [10, 100, 1000]:
        if processes in results['parallel_row']:
            times = results['parallel_row'][processes]
            throughput = []
            
            for i, size in enumerate(matrix_sizes):
                par_time = next((t for s, t in times if s == size), None)
                if par_time and par_time > 0:
                    # Throughput = operations per second
                    ops = size**3  # Approximate operations
                    throughput.append(ops / (par_time / 1000000))  # Convert to ops/sec
                else:
                    throughput.append(0)
            
            ax3.plot(matrix_sizes, throughput, f'^-', 
                    label=f'p={processes}', linewidth=2, markersize=4)
    
    ax3.set_xlabel('Matrix Size (n×n)')
    ax3.set_ylabel('Throughput (ops/sec)')
    ax3.set_title('Throughput vs Matrix Size')
    ax3.legend()
    ax3.grid(True, alpha=0.3)
    ax3.set_xscale('log')
    ax3.set_yscale('log')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/11_scalability_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_cost_benefit_analysis_chart(results, output_dir):
    """Biểu đồ 12: Cost-Benefit Analysis"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    matrix_sizes = [size for size, _ in results['sequential']]
    seq_times = [time for _, time in results['sequential']]
    
    # Calculate cost (overhead) and benefit (speedup)
    costs = []
    benefits = []
    labels = []
    
    for processes in [10, 100, 1000]:
        if processes in results['parallel_row']:
            times = results['parallel_row'][processes]
            
            for i, size in enumerate(matrix_sizes):
                seq_time = seq_times[i]
                par_time = next((t for s, t in times if s == size), None)
                
                if par_time and par_time > 0:
                    # Cost = overhead ratio
                    theoretical_min = seq_time / processes
                    if theoretical_min > 0:
                        overhead = (par_time - theoretical_min) / theoretical_min
                        costs.append(overhead)
                        
                        # Benefit = speedup
                        speedup = seq_time / par_time
                        benefits.append(speedup)
                        
                        labels.append(f'n={size}, p={processes}')
    
    # Create scatter plot
    scatter = ax.scatter(costs, benefits, s=100, alpha=0.7, c=range(len(costs)), cmap='viridis')
    
    # Add diagonal line (cost = benefit)
    max_val = max(max(costs), max(benefits))
    ax.plot([0, max_val], [0, max_val], 'r--', alpha=0.5, label='Cost = Benefit')
    
    ax.set_xlabel('Cost (Overhead Ratio)', fontsize=12)
    ax.set_ylabel('Benefit (Speedup)', fontsize=12)
    ax.set_title('Strassen Algorithm: Cost-Benefit Analysis', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    
    # Add colorbar
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Configuration Index', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/12_cost_benefit_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_3d_performance_surface_chart(results, output_dir):
    """Biểu đồ 13: 3D Performance Surface"""
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    matrix_sizes = [4, 8, 16, 32, 64, 128, 256, 512, 1024]
    process_counts = [10, 100, 1000]
    
    # Create meshgrid
    X, Y = np.meshgrid(matrix_sizes, process_counts)
    Z = np.zeros_like(X)
    
    # Fill Z with speedup values
    for i, processes in enumerate(process_counts):
        if processes in results['parallel_row']:
            times = results['parallel_row'][processes]
            for j, size in enumerate(matrix_sizes):
                seq_time = next((time for s, time in results['sequential'] if s == size), None)
                par_time = next((t for s, t in times if s == size), None)
                
                if seq_time and par_time and par_time > 0:
                    Z[i, j] = seq_time / par_time
                else:
                    Z[i, j] = 0
    
    # Create 3D surface
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.8)
    
    ax.set_xlabel('Matrix Size (n×n)', fontsize=12)
    ax.set_ylabel('Process Count', fontsize=12)
    ax.set_zlabel('Speedup', fontsize=12)
    ax.set_title('Strassen Algorithm: 3D Performance Surface', fontsize=14, fontweight='bold')
    
    # Add colorbar
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/13_3d_performance_surface.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_resource_utilization_chart(results, output_dir):
    """Biểu đồ 14: Resource Utilization Analysis"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6))
    
    matrix_sizes = [size for size, _ in results['sequential']]
    
    # Memory utilization
    memory_usage = []
    for size in matrix_sizes:
        # 3 matrices * size^2 * 8 bytes
        memory = 3 * size * size * 8 / (1024 * 1024)  # MB
        memory_usage.append(memory)
    
    ax1.plot(matrix_sizes, memory_usage, 'b-o', linewidth=2, markersize=6, label='Memory Usage')
    ax1.fill_between(matrix_sizes, memory_usage, alpha=0.3, color='blue')
    ax1.set_xlabel('Matrix Size (n×n)')
    ax1.set_ylabel('Memory Usage (MB)')
    ax1.set_title('Memory Utilization')
    ax1.grid(True, alpha=0.3)
    ax1.set_xscale('log')
    ax1.set_yscale('log')
    
    # CPU utilization (estimated)
    cpu_utilization = []
    for processes in [10, 100, 1000]:
        if processes in results['parallel_row']:
            times = results['parallel_row'][processes]
            utilization = []
            
            for size in matrix_sizes:
                time = next((t for s, t in times if s == size), None)
                if time:
                    # Estimate CPU utilization based on process count and time
                    # More processes = higher CPU utilization
                    cpu_util = min(100, processes * 10)  # Simplified model
                    utilization.append(cpu_util)
                else:
                    utilization.append(0)
            
            ax2.plot(matrix_sizes, utilization, f'o-', 
                    label=f'CPU Utilization (p={processes})', linewidth=2, markersize=4)
    
    ax2.set_xlabel('Matrix Size (n×n)')
    ax2.set_ylabel('CPU Utilization (%)')
    ax2.set_title('CPU Utilization')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    ax2.set_xscale('log')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/14_resource_utilization.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_performance_regression_chart(results, output_dir):
    """Biểu đồ 15: Performance Regression Analysis"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    matrix_sizes = [size for size, _ in results['sequential']]
    seq_times = [time for _, time in results['sequential']]
    
    # Calculate performance ratio (actual vs theoretical)
    performance_ratios = []
    
    for i, size in enumerate(matrix_sizes):
        seq_time = seq_times[i]
        
        # Theoretical time (simplified model)
        theoretical_time = size**(np.log2(7)) * 0.001  # Scaled factor
        
        if theoretical_time > 0:
            ratio = seq_time / theoretical_time
            performance_ratios.append(ratio)
        else:
            performance_ratios.append(0)
    
    ax.plot(matrix_sizes, performance_ratios, 'ro-', linewidth=2, markersize=6, label='Performance Ratio')
    
    # Add regression line
    if len(matrix_sizes) > 1:
        z = np.polyfit(matrix_sizes, performance_ratios, 1)
        p = np.poly1d(z)
        ax.plot(matrix_sizes, p(matrix_sizes), 'b--', alpha=0.7, linewidth=2, label='Regression Line')
    
    # Add threshold line
    ax.axhline(y=1.0, color='green', linestyle='--', alpha=0.7, label='Optimal Performance')
    
    ax.set_xlabel('Matrix Size (n×n)', fontsize=12)
    ax.set_ylabel('Performance Ratio (Actual/Theoretical)', fontsize=12)
    ax.set_title('Strassen Algorithm: Performance Regression Analysis', fontsize=14, fontweight='bold')
    ax.legend()
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    
    plt.tight_layout()
    plt.savefig(f'{output_dir}/15_performance_regression.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    log_file = '../../logs/strassen_comprehensive.log'
    output_dir = '../../charts'
    
    print("Generating additional charts for comprehensive Strassen Algorithm analysis...")
    
    # Parse results
    results = parse_benchmark_log(log_file)
    
    # Create additional charts
    print("9. Creating algorithm complexity comparison chart...")
    create_algorithm_complexity_chart(results, output_dir)
    
    print("11. Creating scalability analysis...")
    create_scalability_analysis_chart(results, output_dir)
    
    print("13. Creating 3D performance surface...")
    create_3d_performance_surface_chart(results, output_dir)
    
    print(f"All essential additional charts generated successfully in {output_dir}/")
    print("Generated files:")
    print("- 09_algorithm_complexity.png")
    print("- 11_scalability_analysis.png")
    print("- 13_3d_performance_surface.png")

if __name__ == "__main__":
    main()
