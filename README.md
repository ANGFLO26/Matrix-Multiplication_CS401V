# Matrix Multiplication Parallel Computing

**CS401V - Distributed Systems Assignment 1**  
**Nhóm**: Phan Văn Tài (2202081) & Hà Minh Chiến (2202095)

## 📋 Project Overview

This project implements and compares three different approaches to matrix multiplication using **Strassen Algorithm**:

1. **Sequential**: Strassen Algorithm O(n^log₂7) using single process
2. **Parallel Row**: Row-level parallelization with Strassen Algorithm using multiple processes
3. **Parallel Element**: Element-level parallelization with Strassen Algorithm using multiple processes

## 🎯 Objectives

- Implement matrix multiplication using process-based parallel computing
- Compare performance of sequential vs parallel approaches
- Analyze scalability with different matrix sizes and process counts
- Demonstrate understanding of parallel programming concepts (fork, mmap, semaphores)

## 🚀 Quick Start

### Prerequisites
- Linux system with GCC compiler
- pthread library support
- Multi-core CPU (recommended 8+ cores)

### Installation & Compilation
```bash
# Clone the repository
git clone <repository-url>
cd assignment1_code

# Compile all programs
make all

# Or compile individually
gcc src/sequentialMult.c -o compiled/sequentialMult
gcc src/parallelRowMult.c -o compiled/parallelRowMult -pthread
gcc src/parallelElementMult.c -o compiled/parallelElementMult -pthread
```

### Running Tests
```bash
# Quick performance test
./tools/quick_test.sh

# Full benchmark with all configurations
./tools/benchmark_report.sh
```

## 📊 Performance Results

### Key Findings (Strassen Algorithm)
- **Best Performance**: Parallel Row with 10-100 processes for medium matrices
- **Maximum Speedup**: 4.87x for 256×256 matrices with 10 processes
- **Algorithm Efficiency**: O(n^log₂7) vs O(n³) for large matrices

### Performance Summary (Strassen Algorithm)
| Matrix Size | Sequential | Parallel Row (p=10) | Speedup | Parallel Row (p=100) | Speedup |
|-------------|------------|---------------------|---------|----------------------|---------|
| 256×256     | 11.5ms     | 2.4ms               | 4.87x   | 5.2ms                | 2.20x   |
| 512×512     | 75.1ms     | 28.0ms              | 2.68x   | 29.4ms               | 2.56x   |
| 1024×1024   | 540.4ms    | 648.5ms             | 0.83x   | 397.0ms              | 1.36x   |

## 🏗️ Project Structure (Fully Optimized)

```
📁 assignment1_code/
├── 📄 README.md                    # Tài liệu chính
├── 📄 requirements.txt             # Yêu cầu hệ thống
├── 📄 Makefile                     # Build automation
├── 📁 src/                         # Source code (40KB)
│   ├── sequentialMult.c           # Sequential implementation
│   ├── parallelRowMult.c          # Parallel row implementation
│   ├── parallelElementMult.c      # Parallel element implementation
│   ├── common.h                   # Common utilities
│   ├── strassen_utils.h           # Strassen utilities header
│   └── strassen_utils.c           # Strassen utilities implementation
├── 📁 compiled/                    # Executables (76KB) ⭐ CẦN THIẾT
│   ├── sequentialMult
│   ├── parallelRowMult
│   └── parallelElementMult
├── 📁 tools/                       # Utility scripts (16KB)
│   ├── quick_test.sh              # Quick performance test
│   ├── benchmark.sh               # Comprehensive benchmark
│   └── benchmark_report.sh        # Report generation
├── 📁 docs/                        # Documentation (316KB)
│   └── Assignment 1 - CS401V - Distributed Systems.pdf
└── 📁 reports/                     # TẤT CẢ BÁO CÁO VÀ KẾT QUẢ (2.6MB)
    ├── 📄 FINAL_REPORT.md          # Báo cáo chính
    ├── 📄 PERFORMANCE_REPORT.md   # Báo cáo kỹ thuật
    ├── 📄 SUMMARY_RESULTS.md       # Tóm tắt kết quả
    ├── 📁 charts/                  # Biểu đồ đã tạo (7 files)
    │   ├── 01_speedup_vs_matrix_size.png
    │   ├── 02_speedup_vs_process_count.png
    │   ├── 03_row_vs_element_comparison.png
    │   ├── 04_efficiency_heatmap.png
    │   ├── 09_algorithm_complexity.png
    │   ├── 11_scalability_analysis.png
    │   └── 13_3d_performance_surface.png
    ├── 📁 logs/                    # Benchmark logs
    │   └── strassen_comprehensive.log
    └── 📁 visualization/           # Hệ thống tạo biểu đồ
        ├── 📁 code/                # Scripts tạo biểu đồ
        │   ├── extract_data.py     # Data extraction
        │   ├── generate_charts.py  # Basic charts (1-4)
        │   └── generate_additional_charts.py # Advanced charts (9,11,13)
        ├── 📁 data/                # Dữ liệu đã xử lý
        │   ├── raw_data.csv
        │   ├── raw_data.json
        │   ├── speedup_data.csv
        │   └── speedup_data.json
        ├── 📄 README.md            # Hướng dẫn charts
        └── 📄 CHART_GUIDE.md       # Chi tiết charts
```

## 🔧 Technical Implementation

### Key Technologies
- **Process Management**: `fork()`, `wait()`, `_exit()`
- **Memory Sharing**: `mmap()` with `MAP_SHARED`
- **Synchronization**: Semaphores for shared variables
- **Timing**: `gettimeofday()` for microsecond precision

### Parallelization Strategy
- **Row-level**: Each process computes entire rows
- **Element-level**: Each process computes individual elements
- **Work-stealing**: Dynamic load balancing using shared indices

## 📈 Performance Analysis

### Scaling Behavior
- **Small matrices** (< 100×100): Sequential is fastest due to parallel overhead
- **Medium matrices** (100×1000): Parallel Row with 10-100 processes optimal
- **Large matrices** (1000×1000+): Parallel Row with 1000 processes optimal
- **Very large matrices** (2000×2000+): Memory bandwidth becomes bottleneck

### Key Insights
1. **Parallel overhead** significant for small matrices
2. **Row-level parallelization** more efficient than element-level
3. **Process count optimization** depends on matrix size
4. **Memory bandwidth** limits scaling for very large matrices

## 📚 Reports & Documentation

- **FINAL_STRASSEN_REPORT.md**: Comprehensive Strassen Algorithm performance analysis
- **strassen_analysis_report.md**: Detailed analysis report
- **charts/**: Performance visualization charts
  - strassen_execution_time.png: Execution time comparison
  - strassen_speedup.png: Speedup analysis
  - strassen_process_analysis.png: Process optimization
- **logs/**: Benchmark execution logs
  - strassen_comprehensive.log: Complete benchmark results

## 🛠️ Usage Examples

### Basic Usage
```bash
# Sequential matrix multiplication
./compiled/sequentialMult 1000

# Parallel row multiplication
./compiled/parallelRowMult 1000 10

# Parallel element multiplication
./compiled/parallelElementMult 1000 10
```

### Advanced Benchmarking
```bash
# Test all configurations
./tools/benchmark_report.sh

# Custom matrix sizes
./compiled/sequentialMult 2000
./compiled/parallelRowMult 2000 1000
```

## 🐛 Troubleshooting

### Common Issues
- **Compilation errors**: Ensure GCC and pthread are installed
- **Out of memory**: Reduce matrix size or process count
- **Slow performance**: Check CPU core count and system load

### Performance Tips
- Use 10-100 processes for most cases
- Ensure sufficient RAM for large matrices
- Close unnecessary applications during benchmarking

## 📋 Requirements

See `requirements.txt` for detailed system requirements and installation instructions.

## 🎯 Structure Optimization

### **✅ Optimizations Applied:**
1. **Consolidated Structure**: All results in `reports/` directory
2. **Created `reports/visualization/`**: Contains chart generation system
3. **Maintained `reports/charts/`**: Contains generated charts
4. **Renamed**: `scripts/` → `tools/` (clearer naming)
5. **Removed Duplicates**: Eliminated redundant files and folders
6. **Updated Paths**: All scripts work with new structure

### **📊 Final Statistics:**
- **Total Size**: 3.7MB
- **Main Directories**: 6 (streamlined)
- **Key Files**: ~25 important files
- **Charts**: 7 core visualizations
- **Reports**: 3 comprehensive reports
- **Visualization**: Complete chart generation system

### **✨ Benefits of Optimized Structure:**
1. **🎯 Clean**: Eliminated duplicates, only 6 main directories
2. **📁 Logical**: All results in `reports/`, no confusion
3. **🔍 Easy Navigation**: Intuitive structure, easy to find files
4. **⚡ Efficient**: Reduced complexity, increased usability
5. **📊 Complete**: Maintains all functionality
6. **🚀 Optimized**: Scripts work perfectly, accurate paths

## 👥 Team Members

- **Phan Văn Tài (2202081)**: Implementation & Testing
- **Hà Minh Chiến (2202095)**: Analysis & Documentation

## 📄 License

This project is part of CS401V - Distributed Systems coursework.

---

*For detailed performance analysis and technical implementation, see the reports in the `reports/` directory.*
# Matrix-Multiplication_CS401V
