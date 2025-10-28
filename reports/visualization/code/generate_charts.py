#!/usr/bin/env python3
"""
Advanced Chart Generation for Strassen Algorithm Performance Analysis
Tạo các biểu đồ chi tiết từ dữ liệu benchmark
"""

import json
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict
from pathlib import Path

# Set style
plt.style.use('default')

def load_results_from_data(data_dir):
    """Load benchmark results from data JSON files (raw_data.json + extended_benchmark_data.json)."""
    data_path = Path(data_dir)
    results = {
        'sequential': [],
        'parallel_row': defaultdict(list),
        'parallel_element': defaultdict(list)
    }

    # Load baseline/raw data (<=1024)
    raw_json = data_path / 'raw_data.json'
    if raw_json.exists():
        with open(raw_json, 'r') as f:
            raw = json.load(f)
        # sequential
        for row in raw.get('sequential', []):
            results['sequential'].append((row['matrix_size'], row['time_us']))
        # parallel_row
        for row in raw.get('parallel_row', []):
            results['parallel_row'][row['processes']].append((row['matrix_size'], row['time_us']))
        # parallel_element
        for row in raw.get('parallel_element', []):
            results['parallel_element'][row['processes']].append((row['matrix_size'], row['time_us']))

    # Load extended data (>=1536 and any extra)
    ext_json = data_path / 'extended_benchmark_data.json'
    if ext_json.exists():
        with open(ext_json, 'r') as f:
            ext = json.load(f)
        for row in ext:
            size = row.get('matrix_size') or row.get('n')
            proc = row.get('process_count') or row.get('processes') or 0
            method = row.get('method')
            time_us = row.get('time_microseconds') or row.get('time_us')
            if not (size and method and time_us is not None):
                continue
            if method == 'sequential':
                # If extended contains any sequential (rare), include
                results['sequential'].append((size, int(time_us)))
            elif method == 'parallel_row':
                results['parallel_row'][int(proc)].append((size, int(time_us)))
            elif method == 'parallel_element':
                results['parallel_element'][int(proc)].append((size, int(time_us)))

    # Deduplicate and sort
    results['sequential'] = sorted(list({(s, t) for (s, t) in results['sequential']}), key=lambda x: x[0])
    for k in list(results['parallel_row'].keys()):
        uniq = sorted(list({(s, t) for (s, t) in results['parallel_row'][k]}), key=lambda x: x[0])
        results['parallel_row'][k] = uniq
    for k in list(results['parallel_element'].keys()):
        uniq = sorted(list({(s, t) for (s, t) in results['parallel_element'][k]}), key=lambda x: x[0])
        results['parallel_element'][k] = uniq

    return results

def create_speedup_vs_matrix_size_chart(results, output_dir):
    """Biểu đồ 1: Speedup vs Matrix Size"""
    fig, ax = plt.subplots(figsize=(12, 8))
    
    matrix_sizes = [size for size, _ in results['sequential']]
    seq_times = [time for _, time in results['sequential']]
    
    # Calculate speedup for each configuration
    colors = ['red', 'green', 'blue', 'orange', 'purple', 'brown']
    markers = ['o', 's', '^', 'D', 'v', '<']
    
    row_keys = [p for p in sorted(results['parallel_row'].keys()) if p in (10, 100, 1000)]
    for idx, processes in enumerate(row_keys):
        times = results['parallel_row'][processes]
        sizes = [size for size, _ in times]
        times_list = [time for _, time in times]
        speedup = []
        
        for j, size in enumerate(sizes):
            seq_time = next((time for s, time in results['sequential'] if s == size), None)
            if seq_time and times_list[j] > 0:
                speedup.append(seq_time / times_list[j])
            else:
                speedup.append(0)
        
        ax.plot(sizes, speedup, f'{markers[idx % len(markers)]}-', 
                label=f'Parallel Row (p={processes})', 
                color=colors[idx % len(colors)], linewidth=2, markersize=6)
    
    elem_keys = [p for p in sorted(results['parallel_element'].keys()) if p in (10, 100, 1000)]
    for idx, processes in enumerate(elem_keys):
        times = results['parallel_element'][processes]
        sizes = [size for size, _ in times]
        times_list = [time for _, time in times]
        speedup = []
        
        for j, size in enumerate(sizes):
            seq_time = next((time for s, time in results['sequential'] if s == size), None)
            if seq_time and times_list[j] > 0:
                speedup.append(seq_time / times_list[j])
            else:
                speedup.append(0)
        
        marker_style = markers[(idx + 3) % len(markers)]
        color_style = colors[(idx + 3) % len(colors)]
        ax.plot(sizes, speedup, f'{marker_style}--', 
                label=f'Parallel Element (p={processes})', 
                color=color_style, linewidth=2, markersize=6)
    
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

def create_best_time_large_chart(results, output_dir):
    """Biểu đồ 06: Best time for large sizes (>=1536), chọn tốt nhất giữa Row/Element."""
    fig, ax = plt.subplots(figsize=(12, 8))

    # Build best time per size for sizes >= 1536
    sizes = sorted({s for plist in list(results['parallel_row'].values()) + list(results['parallel_element'].values()) for (s, _) in plist if s >= 1536})
    best_times = []
    best_methods = []

    for size in sizes:
        # best row
        best_row = min([t for p, lst in results['parallel_row'].items() for (s, t) in lst if s == size], default=None)
        # best element
        best_elem = min([t for p, lst in results['parallel_element'].items() for (s, t) in lst if s == size], default=None)
        if best_row is None and best_elem is None:
            continue
        if best_elem is None or (best_row is not None and best_row < best_elem):
            best_times.append(best_row)
            best_methods.append('Row')
        else:
            best_times.append(best_elem)
            best_methods.append('Element')

    if sizes and best_times:
        ax.plot(sizes, [t/1e6 for t in best_times], 'o-', linewidth=2, markersize=6, label='Best Time (s)')
        for i, m in enumerate(best_methods):
            ax.annotate(m, (sizes[i], best_times[i]/1e6), textcoords="offset points", xytext=(0,6), ha='center', fontsize=8)

    ax.set_xlabel('Matrix Size (n×n)', fontsize=12)
    ax.set_ylabel('Best Execution Time (seconds)', fontsize=12)
    ax.set_title('Best Time for Large Sizes (>=1536): Row vs Element', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.set_xscale('log')
    ax.set_yscale('log')

    plt.tight_layout()
    plt.savefig(f'{output_dir}/05_best_time_large.png', dpi=300, bbox_inches='tight')
    plt.close()

def create_algorithm_complexity_chart(results, output_dir):
    """Biểu đồ 9: Algorithm Complexity Comparison (theoretical vs actual)."""
    if not results['sequential']:
        return
    fig, ax = plt.subplots(figsize=(12, 8))
    matrix_sizes = [size for size, _ in results['sequential']]
    naive_ops = [size**3 for size in matrix_sizes]
    strassen_ops = [size**(np.log2(7)) for size in matrix_sizes]
    ax.plot(matrix_sizes, naive_ops, 'r-o', linewidth=2, label='Naive O(n³)')
    ax.plot(matrix_sizes, strassen_ops, 'b-s', linewidth=2, label='Strassen O(n^log₂7)')
    seq_times = [time for _, time in results['sequential']]
    max_ops = max(max(naive_ops), max(strassen_ops))
    max_time = max(seq_times)
    scaled_times = [time * max_ops / max_time for time in seq_times]
    ax.plot(matrix_sizes, scaled_times, 'g-^', linewidth=2, label='Actual (scaled)')
    ax.set_xlabel('Matrix Size (n×n)')
    ax.set_ylabel('Operations Count (log scale)')
    ax.set_title('Theoretical vs Actual Complexity')
    ax.legend(); ax.grid(True, alpha=0.3); ax.set_xscale('log'); ax.set_yscale('log')
    plt.tight_layout(); plt.savefig(f'{output_dir}/06_algorithm_complexity.png', dpi=300, bbox_inches='tight'); plt.close()

def create_scalability_analysis_chart(results, output_dir):
    """Biểu đồ 11: Scalability Analysis (speedup, efficiency, throughput)."""
    if not results['sequential']:
        return
    import math
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    matrix_sizes = [size for size, _ in results['sequential']]
    seq_times = [time for _, time in results['sequential']]
    for processes in sorted(results['parallel_row'].keys()):
        if processes not in [10, 100, 1000]:
            continue
        times = results['parallel_row'][processes]
        # speedup
        speedup = []
        for i, size in enumerate(matrix_sizes):
            seq_time = seq_times[i]
            par_time = next((t for s, t in times if s == size), None)
            speedup.append((seq_time / par_time) if par_time and par_time > 0 else 0)
        ax1.plot(matrix_sizes, speedup, 'o-', label=f'p={processes}', linewidth=2, markersize=4)
        # efficiency
        efficiency = [ (sp / processes) * 100 if processes > 0 else 0 for sp in speedup ]
        ax2.plot(matrix_sizes, efficiency, 's-', label=f'p={processes}', linewidth=2, markersize=4)
        # throughput (approx ops/sec)
        throughput = []
        for i, size in enumerate(matrix_sizes):
            par_time = next((t for s, t in times if s == size), None)
            if par_time and par_time > 0:
                ops = size**3
                throughput.append(ops / (par_time / 1_000_000))
            else:
                throughput.append(0)
        ax3.plot(matrix_sizes, throughput, '^-', label=f'p={processes}', linewidth=2, markersize=4)
    ax1.set_xlabel('Matrix Size (n×n)'); ax1.set_ylabel('Speedup'); ax1.set_title('Speedup vs Matrix Size'); ax1.legend(); ax1.grid(True, alpha=0.3); ax1.set_xscale('log')
    ax2.set_xlabel('Matrix Size (n×n)'); ax2.set_ylabel('Efficiency (%)'); ax2.set_title('Efficiency vs Matrix Size'); ax2.legend(); ax2.grid(True, alpha=0.3); ax2.set_xscale('log')
    ax3.set_xlabel('Matrix Size (n×n)'); ax3.set_ylabel('Throughput (ops/sec)'); ax3.set_title('Throughput vs Matrix Size'); ax3.legend(); ax3.grid(True, alpha=0.3); ax3.set_xscale('log'); ax3.set_yscale('log')
    plt.tight_layout(); plt.savefig(f'{output_dir}/07_scalability_analysis.png', dpi=300, bbox_inches='tight'); plt.close()

def create_3d_performance_surface_chart(results, output_dir):
    """Biểu đồ 13: 3D Performance Surface (speedup over size/process)."""
    from mpl_toolkits.mplot3d import Axes3D  # noqa: F401
    import matplotlib.pyplot as plt
    import numpy as np
    if not results['sequential']:
        return
    fig = plt.figure(figsize=(14, 10))
    ax = fig.add_subplot(111, projection='3d')
    matrix_sizes = sorted({s for s, _ in results['sequential'] if s in [4,8,16,32,64,128,256,512,1024]})
    process_counts = [p for p in [10, 100, 1000] if p in results['parallel_row']]
    if not matrix_sizes or not process_counts:
        plt.close(fig); return
    X, Y = np.meshgrid(matrix_sizes, process_counts)
    Z = np.zeros_like(X, dtype=float)
    for i, p in enumerate(process_counts):
        times = results['parallel_row'][p]
        for j, size in enumerate(matrix_sizes):
            seq_time = next((t for s, t in results['sequential'] if s == size), None)
            par_time = next((t for s, t in times if s == size), None)
            Z[i, j] = (seq_time / par_time) if seq_time and par_time and par_time > 0 else 0
    surf = ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.85)
    ax.set_xlabel('Matrix Size (n×n)'); ax.set_ylabel('Process Count'); ax.set_zlabel('Speedup'); ax.set_title('3D Performance Surface')
    fig.colorbar(surf, ax=ax, shrink=0.5, aspect=5)
    plt.tight_layout(); plt.savefig(f'{output_dir}/08_3d_performance_surface.png', dpi=300, bbox_inches='tight'); plt.close()

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
    data_dir = '../data'
    output_dir = '../../charts'
    
    print("Generating charts from data files (no logs required)...")
    
    # Load results from data
    results = load_results_from_data(data_dir)
    
    # Create all charts
    print("1. Creating speedup vs matrix size chart...")
    create_speedup_vs_matrix_size_chart(results, output_dir)
    
    print("2. Creating speedup vs process count chart...")
    create_speedup_vs_process_count_chart(results, output_dir)
    
    print("3. Creating row vs element comparison chart (<=1024 baseline sizes)...")
    create_row_vs_element_comparison_chart(results, output_dir)
    
    print("4. Creating efficiency heatmap...")
    create_efficiency_heatmap(results, output_dir)
    
    print("5. Creating best-time chart for large sizes (>=1536)...")
    create_best_time_large_chart(results, output_dir)
    
    print("6. Creating algorithm complexity comparison chart...")
    create_algorithm_complexity_chart(results, output_dir)

    print("7. Creating scalability analysis...")
    create_scalability_analysis_chart(results, output_dir)

    print("8. Creating 3D performance surface...")
    create_3d_performance_surface_chart(results, output_dir)

    print(f"All charts generated successfully in {output_dir}/")
    print("Generated files:")
    print("- 01_speedup_vs_matrix_size.png")
    print("- 02_speedup_vs_process_count.png") 
    print("- 03_row_vs_element_comparison.png")
    print("- 04_efficiency_heatmap.png")
    print("- 05_best_time_large.png")
    print("- 06_algorithm_complexity.png")
    print("- 07_scalability_analysis.png")
    print("- 08_3d_performance_surface.png")

if __name__ == "__main__":
    main()
