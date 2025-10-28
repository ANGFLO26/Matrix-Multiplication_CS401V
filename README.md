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
cd Matrix-Multiplication_CS401V

# Compile all programs
make

# Or compile individually
mkdir -p compiled
gcc src/sequentialMult.c src/strassen_utils.c -o compiled/sequentialMult -O2 -lm
gcc src/parallelRowMult.c src/strassen_utils.c -o compiled/parallelRowMult -O2 -lm
gcc src/parallelElementMult.c src/strassen_utils.c -o compiled/parallelElementMult -O2 -lm
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
- **Medium (256–512)**: Parallel Row ~10–32 processes tốt nhất
- **Maximum Speedup (≤1024)**: 4.87x tại 256×256 (Row, 10 processes)
- **1024×1024**: Parallel Row 100–1000 processes
- **Large (≥1536)**: Parallel Element thường cho thời gian tốt hơn (trừ 1536)
- **Algorithm Efficiency**: O(n^log₂7) vs O(n³)

### Performance Summary (Strassen Algorithm)
| Matrix Size | Sequential | Parallel Row (p=10) | Speedup | Parallel Row (p=100) | Speedup |
|-------------|------------|---------------------|---------|----------------------|---------|
| 256×256     | 11.5ms     | 2.4ms               | 4.87x   | 5.2ms                | 2.20x   |
| 512×512     | 75.1ms     | 28.0ms              | 2.68x   | 29.4ms               | 2.56x   |
| 1024×1024   | 540.4ms    | 648.5ms             | 0.83x   | 397.0ms              | 1.36x   |

## 🏗️ Project Structure

```
📁 Matrix-Multiplication_CS401V/
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
├── 📁 compiled/                    # Executables (nếu build thủ công)
│   ├── sequentialMult
│   ├── parallelRowMult
│   └── parallelElementMult
├── 📁 tools/                       # Utility scripts (16KB)
│   ├── quick_test.sh              # Quick performance test
│   ├── benchmark.sh               # Comprehensive benchmark
│   └── benchmark_report.sh        # Report generation
├── 📁 docs/                        # Documentation (316KB)
│   └── Assignment 1 - CS401V - Distributed Systems.pdf
└── 📁 reports/                     # TẤT CẢ BÁO CÁO VÀ KẾT QUẢ
    ├── 📄 FINAL_REPORT.md          # Báo cáo chính
    ├── 📄 PERFORMANCE_REPORT.md   # Báo cáo kỹ thuật
    ├── 📄 SUMMARY_RESULTS.md       # Tóm tắt kết quả
    ├── 📁 charts/                  # Biểu đồ đã tạo
    │   ├── 01_speedup_vs_matrix_size.png
    │   ├── 02_speedup_vs_process_count.png
    │   ├── 03_row_vs_element_comparison.png
    │   ├── 04_efficiency_heatmap.png
    │   ├── 05_best_time_large.png
    │   ├── 06_algorithm_complexity.png
    │   ├── 07_scalability_analysis.png
    │   └── 08_3d_performance_surface.png
    └── 📁 visualization/           # Hệ thống tạo biểu đồ
        ├── 📁 code/                # Scripts tạo biểu đồ
        │   ├── extract_data.py
        │   └── generate_charts.py
        ├── 📁 data/                # Dữ liệu
        │   ├── raw_data.csv
        │   ├── raw_data.json
        │   ├── extended_benchmark_data.csv
        │   ├── extended_benchmark_data.json
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

### Scaling Behavior (từ dữ liệu hiện có)
- **Small** (≤64×64): Sequential nhanh nhất (overhead song song cao)
- **Medium** (256–512): Parallel Row ~10–32 processes
- **1024×1024**: Parallel Row 100–1000 processes
- **Very large** (≥1536): Parallel Element thường tốt hơn; bottleneck băng thông bộ nhớ

### Key Insights
1. **Parallel overhead** đáng kể cho ma trận nhỏ
2. **Row-level** hiệu quả ở ≤1024; **Element-level** tốt hơn ở ≥1536 (trừ 1536)
3. **Process count** phụ thuộc kích thước (10–32; 100–1000; 32–256)
4. **Memory bandwidth** giới hạn scaling cho ma trận rất lớn

## 📚 Reports & Documentation
Xem các báo cáo trong `reports/`: `FINAL_REPORT.md`, `PERFORMANCE_REPORT.md`, `SUMMARY_RESULTS.md`. Biểu đồ nằm trong `reports/charts/`.

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
