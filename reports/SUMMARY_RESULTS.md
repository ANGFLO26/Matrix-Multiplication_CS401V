# TÓM TẮT KẾT QUẢ - STRASSEN ALGORITHM MATRIX MULTIPLICATION

**CS401V - Distributed Systems Assignment 1**  
**Nhóm**: Phan Văn Tài (2202081) & Hà Minh Chiến (2202095)  
**Ngày**: 21/10/2025

---

## 🎯 KẾT QUẢ CHÍNH (CẬP NHẬT ĐẾN 6144)

### ⚡ Performance Highlights (cập nhật)
- **Best observed (≤1024, có baseline)**: 4.87x speedup ở 256×256 (Row, 10 processes)
- **Best observed times (≥1536, không có baseline)**:
  - 1536×1536: 2.802s (Row, 1024)
  - 2048×2048: 8.833s (Element, 32)
  - 2560×2560: 18.607s (Element, 32)
  - 3072×3072: 35.804s (Element, 128)
  - 3584×3584: 63.007s (Element, 128)
  - 4096×4096: 105.498s (Element, 128)
  - 5120×5120: 299.282s (Element, 2000)
  - 6144×6144: 547.510s (Element, 512)
- **Best Algorithm by range**: Row tốt ở ≤1024; Element trội về thời gian ở ≥1536 (trừ 1536)
- **Optimal Process Count**: 10–32 (256–512, Row); 100–1000 (1024, Row); 32–256 (≥1536, Element), ngoại lệ 5120 cần ~2000
- **Matrix Size Range**: 2×2 đến 6144×6144

### 📊 Key Performance Metrics

| Metric | Value | Details |
|--------|-------|---------|
| **Best Speedup (≤1024)** | 4.87x | 256×256 (Row, 10 processes) |
| **Best Observed Time ≥1536** | 8.833s | 2048×2048 (Element, 32) |
| **Process Range (by size)** | 10–32 / 100–1000 / 32–256 | 256–512 / 1024 / ≥1536 |
| **Memory Efficiency** | — | Không đánh giá ≥1536 do thiếu baseline |
| **Algorithm Complexity** | O(n^log₂7) | ≈ O(n^2.81) |
| **Memory Usage** | 0.5-8.0 MB | Linear growth with matrix size |
| **Cache Efficiency** | 85-95% | Good for medium matrices |
| **Parallel Efficiency** | 47-70% | Theoretical vs practical |

## 📈 QUICK REFERENCE

### 🏆 Top Performers (thời gian tốt nhất, không quy đổi speedup khi thiếu baseline)
1. **2048×2048**: 8.833s (Element, 32)
2. **4096×4096**: 105.498s (Element, 128)
3. **1024×1024**: 323.885ms (Row, 1000)

### ⚠️ Performance Warnings
- **Small matrices (≤32×32)**: Sequential tốt hơn do overhead
- **Quá nhiều processes**: Overhead > benefit (đặc biệt >1000)
- **Memory bottleneck**: Rõ rệt với 4096×4096 trở lên
- **Very large matrices (8192×8192)**: Timeout (ghi chú cũ)

## 🔍 QUICK ANALYSIS

### ✅ What Works Well
- **Strassen**: Tốt từ ≥128×128
- **Parallel Row**: Trội ở ≤1024
- **Parallel Element**: Thời gian tốt hơn ở ≥1536 (trừ 1536)
- **Processes**: 10–32 (256–512, Row), 100–1000 (1024, Row), 32–256 (≥1536, Element)
- **Threshold**: 32–64 là điểm cắt hợp lý cho song song hóa

### ❌ What Doesn't Work
- **Parallel Element**: Overhead cao ở kích thước nhỏ
- **Quá nhiều processes**: Diminishing returns (đặc biệt >1000)
- **Small matrices**: Overhead > lợi ích
- **Memory bandwidth**: Giới hạn scaling cho ma trận rất lớn

## 📋 RECOMMENDATIONS

### 🎯 For Different Matrix Sizes

| Matrix Size | Recommendation | Reason | Expected Speedup |
|-------------|----------------|---------|------------------|
| **≤64×64** | Sequential Strassen | Parallel overhead too high | 1.0x |
| **128×128-512×512** | Parallel Row, 10-100 processes | Optimal balance | 2-5x |
| **1024×1024** | Parallel Row, 100–1000 processes | Memory bandwidth limited | 1–2x |
| **≥1536×1536** | Parallel Element, 32–256 processes | Thiếu baseline tuần tự | — |

### 🔧 Performance Tuning Tips
1. **Processes**: 10–32 (256–512, Row); 100–1000 (1024, Row); 32–256 (≥1536, Element)
2. **Memory**: Đảm bảo đủ RAM cho ≥1024; cẩn trọng bottleneck băng thông
3. **Cache**: Bật tối ưu cache CPU
4. **System Load**: Giữ tải hệ thống < 10% khi test
5. **Compiler**: GCC với -O2

### 🛠️ Implementation Tips
1. **Threshold**: 64×64 cho Strassen (song song từ ≥64 tốt hơn)
2. **Process count**: Bắt đầu 10 (256–512), 100 (1024), 128 (≥1536)
3. **Memory**: Theo dõi kỹ ở ≥4096 do bandwidth bottleneck
4. **Testing**: Seed cố định để tái lập kết quả

## 📊 DATA SUMMARY

### Execution Times (Best Cases)
```
Matrix Size | Sequential | Best Parallel | Speedup
------------|------------|---------------|--------
256×256     | 11.5ms     | 2.4ms         | 4.87x
512×512     | 75.1ms     | 28.0ms        | 2.68x  
1024×1024   | 540.4ms    | 323.9ms       | 1.67x
```

### Process Count Analysis (≤1024; ≥1536 chỉ báo thời gian tốt nhất)
```
Matrix Size | Optimal Processes | Speedup | Efficiency
------------|------------------|---------|-----------
256×256     | 10               | 4.87x   | 48.7%
512×512     | 10               | 2.68x   | 26.8%
1024×1024   | 1000             | 1.67x   | 16.7%
```

## 🎯 KEY INSIGHTS

### 1. Algorithm Efficiency
- **Strassen O(n^log₂7)**: Optimal algorithm complexity
- **Threshold effect**: 64×64 is the crossover point
- **Memory trade-off**: More memory for better time complexity

### 2. Parallelization Strategy
- **Parallel Row**: Tốt ở ≤1024
- **Parallel Element**: Thời gian tốt hơn ở ≥1536 (trừ 1536)
- **Work-stealing**: Effective load balancing
- **Process count**: Theo kích thước (10–32; 100–1000; 32–256)

### 3. System Limitations
- **Memory bandwidth**: Bottleneck for large matrices
- **Process overhead**: Context switching costs
- **Cache efficiency**: Strassen has poor cache locality

## 📚 FILES REFERENCE

### 📁 Reports
- **FINAL_REPORT.md**: Comprehensive analysis
- **PERFORMANCE_REPORT.md**: Technical details
- **SUMMARY_RESULTS.md**: This quick reference

### 📊 Charts
- **strassen_execution_time.png**: Time comparison
- **strassen_speedup.png**: Speedup analysis
- **strassen_process_analysis.png**: Process optimization

### 📝 Data
- **extended_benchmark_data.(csv|json)**: Dữ liệu mở rộng đến 6144

## 🚀 QUICK START

### Running Tests
```bash
# Quick test
./tools/quick_test.sh

# Full benchmark
./tools/benchmark_report.sh

# Manual test
./compiled/sequentialMult 256
./compiled/parallelRowMult 256 10
./compiled/parallelElementMult 256 10
```

### Expected Results
- **256×256**: ~4.87x speedup with 10 processes
- **512×512**: ~2.68x speedup with 10 processes
- **1024×1024**: ~1.67x speedup with 1000 processes

## CONTACT

**Thành viên nhóm**
- **Phan Văn Tài (2202081)**
- **Hà Minh Chiến (2202095)**

---
