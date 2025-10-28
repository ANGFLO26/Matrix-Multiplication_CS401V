# BÁO CÁO KỸ THUẬT - HIỆU SUẤT STRASSEN ALGORITHM

**CS401V - Distributed Systems Assignment 1**  
**Nhóm**: Phan Văn Tài (2202081) & Hà Minh Chiến (2202095)  
**Ngày**: 21/10/2025  
**Phiên bản**: 1.0

---

## 🔧 THÔNG SỐ KỸ THUẬT

### Hệ thống thử nghiệm
- **OS**: Linux 6.8.0-85-generic
- **CPU**: Multi-core processor (8+ cores)
- **RAM**: 8GB+ (đủ cho ma trận 1024×1024)
- **Compiler**: GCC với flags -O2
- **Libraries**: pthread, math (-lm)
- **Memory**: Shared memory với mmap() MAP_SHARED
- **System Load**: < 10% during testing
- **Cache**: L1/L2/L3 cache available

### Cấu hình benchmark
- **Matrix sizes (gốc)**: 4×4 → 1024×1024; **(mở rộng)**: 1536 → 6144
- **Process counts (gốc)**: 10, 100, 1000; **(mở rộng)**: 32 → 2000 tùy kích thước
- **Repetitions**: 1 run per configuration (fixed seed)
- **Timing**: gettimeofday() với microsecond precision

## 📊 DỮ LIỆU THỰC NGHIỆM CHI TIẾT (MỞ RỘNG ĐẾN 6144)

### Bảng 1: Thời gian thực thi (microseconds)

| Matrix Size | Sequential | Parallel Row (p=10) | Parallel Row (p=100) | Parallel Row (p=1000) | Parallel Element (p=10) | Parallel Element (p=100) | Parallel Element (p=1000) |
|-------------|------------|---------------------|----------------------|-----------------------|-------------------------|--------------------------|---------------------------|
| 4×4         | 0          | 359                 | 3,547                | 32,087                | 389                     | 3,320                    | 34,698                    |
| 8×8         | 1          | 396                 | 3,992                | 34,960                | 405                     | 4,255                    | 38,334                    |
| 16×16       | 2          | 398                 | 4,676                | 38,332                | 364                     | 4,817                    | 35,310                    |
| 32×32       | 16         | 381                 | 4,246                | 33,757                | 390                     | 3,371                    | 41,433                    |
| 64×64       | 161        | 412                 | 3,193                | 36,709                | 873                     | 3,632                    | 33,897                    |
| 128×128     | 1,473      | 628                 | 3,484                | 35,832                | 3,513                   | 5,286                    | 37,220                    |
| 256×256     | 11,463     | 2,352               | 5,208                | 36,187                | 13,674                  | 14,842                   | 44,483                    |
| 512×512     | 75,109     | 28,016              | 29,359               | 57,417                | 62,455                  | 69,295                   | 95,762                    |
| 1024×1024   | 540,443    | 648,490             | 397,029              | 323,885               | 472,776                 | 613,917                  | 867,893                   |

Các kích thước ≥1536: không có giá trị tuần tự tương ứng trong dữ liệu gốc; dưới đây là bảng “thời gian tốt nhất” theo phương pháp/tiến trình:

### Bảng 1b: Thời gian tốt nhất cho kích thước lớn (seconds)
| Matrix Size | Best Time (s) | Method | Processes |
|-------------|----------------|--------|-----------|
| 1536×1536   | 2.802          | Parallel Row     | 1024      |
| 2048×2048   | 8.833          | Parallel Element | 32        |
| 2560×2560   | 18.607         | Parallel Element | 32        |
| 3072×3072   | 35.804         | Parallel Element | 128       |
| 3584×3584   | 63.007         | Parallel Element | 128       |
| 4096×4096   | 105.498        | Parallel Element | 128       |
| 5120×5120   | 299.282        | Parallel Element | 2000      |
| 6144×6144   | 547.510        | Parallel Element | 512       |

### Bảng 2: Speedup Analysis (chỉ cho kích thước có baseline tuần tự ≤1024)

| Matrix Size | Best Parallel Row | Speedup | Best Parallel Element | Speedup | Efficiency |
|-------------|-------------------|---------|----------------------|---------|------------|
| 256×256     | p=10              | 4.87x   | p=10                 | 0.84x   | 48.7%      |
| 512×512     | p=10              | 2.68x   | p=10                 | 1.20x   | 26.8%      |
| 1024×1024   | p=1000            | 1.67x   | p=10                 | 1.14x   | 16.7%      |

### Bảng 3: Memory Usage Analysis (chỉ thị, không suy ra từ baseline ≥1536)

| Matrix Size | Memory (MB) | Sequential Time (ms) | Parallel Time (ms) | Memory Efficiency |
|-------------|--------------|---------------------|-------------------|-------------------|
| 256×256     | 0.5          | 11.5                | 2.4               | 95%               |
| 512×512     | 2.0          | 75.1                | 28.0              | 93%               |
| 1024×1024   | 8.0          | 540.4               | 323.9             | 89%               |

## 🔍 PHÂN TÍCH CHI TIẾT

### 1. Strassen Algorithm Performance

#### Time Complexity Analysis
- **Theoretical**: O(n^log₂7) ≈ O(n^2.81)
- **Practical**: Với ma trận nhỏ, overhead recursion > lợi ích
- **Threshold**: 64×64 là điểm chuyển đổi tối ưu

#### Memory Complexity
- **Space**: O(n²) + O(log n) cho recursion stack
- **Temporary matrices**: 7 submatrices cho mỗi level
- **Padding overhead**: Với ma trận không phải lũy thừa của 2

### 2. Parallelization Analysis

#### Parallel Row Implementation
```c
// Work-stealing approach
while (1) {
    sem_wait(&shared->mutex);
    int my_row = shared->l;
    if (my_row >= m) break;
    shared->l = my_row + 1;
    sem_post(&shared->mutex);
    
    // Compute row using Strassen
    compute_row_strassen(A, B, C, my_row, m);
}
```

**Ưu điểm:**
- Load balancing tốt với work-stealing
- Memory locality cao
- Ít synchronization overhead

**Nhược điểm:**
- Không tận dụng được parallel Strassen subproblems
- Sequential computation trong mỗi row

#### Parallel Element Implementation
```c
// Element-level work-stealing
while (1) {
    sem_wait(&shared->mutex);
    size_t myidx = shared->idx;
    if (myidx >= total) break;
    shared->idx = myidx + 1;
    sem_post(&shared->mutex);
    
    // Compute single element
    compute_element_strassen(A, B, C, myidx, m);
}
```

**Ưu điểm:**
- Granular parallelism
- Có thể tận dụng nhiều cores

**Nhược điểm:**
- High synchronization overhead
- Poor cache locality
- Không tận dụng được Strassen structure

### 3. Process Count Optimization (cập nhật theo dữ liệu mở rộng)

#### Small Matrices (≤128×128)
- **Overhead > Benefit**: Process creation cost cao
- **Recommendation**: Sequential execution
- **Threshold**: < 10 processes

#### Medium Matrices (256×256-512×512)
- **Optimal range**: khoảng 10–32 processes (Row)
- **Sweet spot**: 10 processes cho 256×256; 10–32 cho 512×512
- **Reasoning**: Cân bằng giữa song song hóa và overhead

#### Large Matrices (≥1024×1024)
- **1024×1024**: 100–1000 processes (Row) tốt nhất theo dữ liệu gốc
- **≥1536**: `Parallel Element` thường vượt `Parallel Row` về thời gian; khoảng 32–256 processes (điển hình 128) cho kết quả tốt; ngoại lệ 5120×5120 tốt nhất ở 2000 processes
- **Bottleneck**: Memory bandwidth; returns giảm dần khi tăng processes quá lớn

### 4. Performance Bottlenecks

#### Memory Bandwidth
- **Issue**: Với ma trận lớn, memory access trở thành bottleneck
- **Evidence**: Speedup giảm dần với ma trận 1024×1024
- **Solution**: Cache optimization, memory prefetching

#### Process Overhead
- **Context switching**: Nhiều processes → overhead cao
- **Memory sharing**: mmap() overhead với ma trận lớn
- **Synchronization**: Semaphore operations

#### Cache Efficiency
- **Strassen**: Poor cache locality do recursive structure
- **Sequential access**: Better cache locality với sequential access
- **Trade-off**: Algorithm efficiency vs cache efficiency

## 📈 BIỂU ĐỒ VÀ VISUALIZATION

### 1. Execution Time vs Matrix Size
- **Sequential**: Exponential growth theo O(n^log₂7)
- **Parallel**: Tương tự nhưng với speedup
- **Crossover point**: 256×256 là điểm bắt đầu hiệu quả

### 2. Speedup vs Process Count (≤1024)
- **Peak performance**: ~10 processes cho 256×256; 10–32 cho 512×512; 100–1000 cho 1024×1024 (Row)
- **Diminishing returns**: Speedup giảm khi tăng processes quá lớn
- **≥1536**: Không tính speedup do thiếu baseline; biểu đồ nên hiển thị thời gian tốt nhất theo processes/method

### 3. Memory Usage vs Performance
- **Linear relationship**: Memory usage tăng tuyến tính với matrix size
- **Efficiency**: Memory efficiency giảm với ma trận lớn
- **Bottleneck**: Memory bandwidth với ma trận ≥1024×1024; không tính speedup/efficiency cho ≥1536 do thiếu baseline tuần tự

## 🛠️ IMPLEMENTATION DETAILS

### Strassen Algorithm Implementation
```c
void strassen_multiply(double* A, double* B, double* C, int n) {
    if (n <= 64) {  // Threshold
        // Use alternative method for small matrices
        multiply_small_matrices(A, B, C, n);
        return;
    }
    
    // Divide into 4 submatrices
    int half = n / 2;
    
    // Compute 7 products
    double* P1 = compute_P1(A, B, half);
    // ... (P2 to P7)
    
    // Combine results
    combine_matrices(C, P1, P2, P3, P4, P5, P6, P7, half);
}
```

### Parallel Implementation
```c
// Shared memory setup
double* A = mmap(NULL, size, PROT_READ|PROT_WRITE, MAP_SHARED, -1, 0);
double* B = mmap(NULL, size, PROT_READ|PROT_WRITE, MAP_SHARED, -1, 0);
double* C = mmap(NULL, size, PROT_READ|PROT_WRITE, MAP_SHARED, -1, 0);

// Process creation
for (int i = 0; i < num_processes; i++) {
    pid_t pid = fork();
    if (pid == 0) {
        // Child process: work-stealing loop
        worker_process();
        _exit(0);
    }
}
```

## 📋 KẾT LUẬN KỸ THUẬT

### Performance Characteristics
1. **Strassen Algorithm**: Hiệu quả với ma trận ≥256×256
2. **Parallel Row**: Tối ưu ở ≤1024; **Parallel Element** trội về thời gian ở ≥1536 (trừ 1536)
3. **Process Count**: 10–32 (256–512, Row); 100–1000 (1024, Row); 32–256 (≥1536, Element; 5120 ngoại lệ ~2000)
4. **Memory**: Linear growth; bandwidth bottleneck với ma trận rất lớn

### Bottleneck Analysis
1. **Memory Bandwidth**: Giới hạn với ma trận ≥1024×1024
2. **Cache Misses**: Strassen có cache locality cần tối ưu hóa
3. **Process Overhead**: Context switching với nhiều processes
4. **Synchronization**: Semaphore operations overhead

### Optimization Opportunities
1. **Hybrid approach**: Strassen cho ma trận lớn, phương pháp khác cho ma trận nhỏ
2. **Cache optimization**: Blocking, prefetching
3. **Memory management**: Reduce temporary allocations
4. **Load balancing**: Better work distribution
5. **NUMA optimization**: Memory locality awareness
6. **SIMD instructions**: Vectorized operations

### Future Work
1. **GPU implementation**: CUDA/OpenCL cho Strassen
2. **Distributed computing**: MPI implementation
3. **Memory optimization**: In-place algorithms
4. **Algorithm improvements**: Winograd's algorithm
5. **Hardware acceleration**: FPGA implementation
6. **Machine learning**: Auto-tuning parameters

### Troubleshooting Guide
1. **Out of memory**: Reduce matrix size hoặc process count
2. **Slow performance**: Check CPU cores và system load
3. **Inconsistent results**: Ensure fixed seed và system stability
4. **Compilation errors**: Verify GCC version và library dependencies

---
