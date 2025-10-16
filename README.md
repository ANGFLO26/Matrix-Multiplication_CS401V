# Matrix Multiplication Parallel Computing

**CS401V - Distributed Systems Assignment 1**  
**Group Members:** Phan Văn Tài (2202081) & Hà Minh Chiến (2202095)

## 📋 Project Overview

This project implements and compares three different approaches to matrix multiplication:

1. **Sequential**: Traditional O(n³) algorithm using single process
2. **Parallel Row**: Row-level parallelization with work-stealing using multiple processes
3. **Parallel Element**: Element-level parallelization with work-stealing using multiple processes

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
./scripts/quick_test.sh

# Full benchmark with all configurations
./scripts/benchmark_report.sh
```

## 📊 Performance Results

### Key Findings
- **Best Performance**: Parallel Row with 1000 processes
- **Maximum Speedup**: 7.1x for 1000×1000 matrices
- **Memory Bottleneck**: Observed with 2000×2000 matrices

### Performance Summary
| Matrix Size | Sequential | Parallel Row (1000p) | Speedup |
|-------------|------------|---------------------|---------|
| 100×100     | 2.2ms      | 0.7ms               | 3.2x    |
| 1000×1000   | 3.47s      | 0.49s               | 7.1x    |
| 2000×2000   | 32.23s     | 5.69s               | 5.7x    |

## 🏗️ Project Structure

```
assignment1_code/
├── src/                    # Source code
│   ├── sequentialMult.c    # Sequential implementation
│   ├── parallelRowMult.c   # Row-level parallel implementation
│   ├── parallelElementMult.c # Element-level parallel implementation
│   └── common.h           # Common utilities
├── compiled/               # Compiled executables
├── scripts/                # Utility scripts
├── reports/                # Performance analysis reports
├── docs/                   # Assignment documentation
├── requirements.txt        # System requirements
└── README.md              # This file
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

- **FINAL_REPORT.md**: Comprehensive performance analysis
- **PERFORMANCE_REPORT.md**: Technical implementation details
- **SUMMARY_RESULTS.md**: Quick reference for key results

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
./scripts/benchmark_report.sh

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

## 👥 Team Members

- **Phan Văn Tài** (2202081) - Implementation & Testing
- **Hà Minh Chiến** (2202095) - Analysis & Documentation

## 📄 License

This project is part of CS401V - Distributed Systems coursework.

---

*For detailed performance analysis and technical implementation, see the reports in the `reports/` directory.*
# Matrix-Multiplication_CS401V
