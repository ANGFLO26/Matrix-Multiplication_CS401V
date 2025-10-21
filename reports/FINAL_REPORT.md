# BÁO CÁO TỔNG HỢP - HIỆU SUẤT NHÂN MA TRẬN SONG SONG VỚI STRASSEN ALGORITHM

**CS401V - Distributed Systems Assignment 1**  
**Nhóm**: Phan Văn Tài (2202081) & Hà Minh Chiến (2202095)  
**Ngày**: 21/10/2025  
**Phiên bản**: 1.0

---

## 📋 TÓM TẮT DỰ ÁN

### Mục tiêu nghiên cứu
Nghiên cứu và so sánh hiệu suất của **Strassen Algorithm** trong việc nhân ma trận song song, bao gồm:
- Phân tích hiệu suất Strassen Algorithm O(n^log₂7)
- Đánh giá tác động của song song hóa (Parallel Row vs Parallel Element)
- Tối ưu hóa số lượng tiến trình cho từng kích thước ma trận
- So sánh với lý thuyết và thực nghiệm

### Phương pháp nghiên cứu
- **Thuật toán**: Strassen Algorithm với threshold cho ma trận nhỏ
- **Song song hóa**: Process-based parallelization với fork(), mmap(), semaphores
- **Benchmark**: Ma trận từ 2² đến 2¹⁰ (4×4 đến 1024×1024)
- **Tiến trình**: 10, 100, 1000 processes
- **Reproducibility**: Fixed seed (12345) cho kết quả nhất quán

### Hệ thống thử nghiệm
- **OS**: Linux 6.8.0-85-generic
- **CPU**: Multi-core processor (8+ cores)
- **RAM**: 8GB+ (đủ cho ma trận 1024×1024)
- **Compiler**: GCC với flags -O2
- **Libraries**: pthread, math (-lm)
- **Memory**: Shared memory với mmap() MAP_SHARED

## 🎯 KẾT QUẢ CHÍNH

### Hiệu suất Strassen Algorithm
| Matrix Size | Sequential (μs) | Best Parallel | Speedup | Optimal Processes |
|-------------|-----------------|---------------|---------|-------------------|
| 256×256     | 11,463          | 2,352 (Row)   | 4.87x   | 10                |
| 512×512     | 75,109          | 28,016 (Row)  | 2.68x   | 10                |
| 1024×1024   | 540,443         | 323,885 (Row) | 1.67x   | 1000              |

### Phân tích quan trọng
1. **Strassen hiệu quả**: Với ma trận ≥256×256, hiệu suất tối ưu
2. **Parallel Row tối ưu**: Hiệu quả hơn Parallel Element cho hầu hết trường hợp
3. **Số tiến trình tối ưu**: 10-100 cho ma trận trung bình, 100-1000 cho ma trận lớn
4. **Threshold quan trọng**: Với ma trận <64×64, nên dùng sequential

## 📊 BIỂU ĐỒ HIỆU SUẤT

### 1. Thời gian thực thi
- **Sequential**: Tuân theo O(n^log₂7) ≈ O(n^2.81)
- **Parallel Row**: Speedup giảm dần khi số tiến trình tăng
- **Parallel Element**: Kém hiệu quả do overhead synchronization

### 2. Speedup Analysis
- **Tối đa**: 4.87x với ma trận 256×256, 10 tiến trình
- **Tối ưu**: 10-100 tiến trình cho ma trận trung bình
- **Giảm dần**: Với ma trận lớn do memory bandwidth

### 3. Process Count Optimization
- **Ma trận nhỏ (≤128×128)**: Nhiều tiến trình → overhead cao
- **Ma trận trung bình (256×256-512×512)**: 10-100 tiến trình tối ưu
- **Ma trận lớn (≥1024×1024)**: 100-1000 tiến trình có thể hiệu quả

### 4. Memory Usage Analysis
| Matrix Size | Memory (MB) | Sequential Time (ms) | Parallel Time (ms) | Memory Efficiency |
|-------------|--------------|---------------------|-------------------|-------------------|
| 256×256     | 0.5          | 11.5                | 2.4               | 95%               |
| 512×512     | 2.0          | 75.1                | 28.0              | 93%               |
| 1024×1024   | 8.0          | 540.4               | 323.9             | 89%               |

### 5. Theoretical vs Practical Performance
| Matrix Size | Theoretical Speedup | Practical Speedup | Efficiency |
|-------------|---------------------|-------------------|------------|
| 256×256     | 7.0x               | 4.87x             | 69.6%      |
| 512×512     | 5.0x               | 2.68x             | 53.6%      |
| 1024×1024   | 3.5x               | 1.67x             | 47.7%      |

## 🔬 PHÂN TÍCH KỸ THUẬT

### Strassen Algorithm Implementation
- **Recursive approach**: Chia ma trận thành 4 submatrices
- **7 multiplications**: Tối ưu hóa so với phương pháp truyền thống
- **Threshold**: 64×64 cho ma trận nhỏ (chuyển sang phương pháp khác)
- **Memory management**: Padding cho ma trận không phải lũy thừa của 2

### Parallelization Strategy
- **Work-stealing**: Dynamic load balancing với shared indices
- **Memory sharing**: mmap() với MAP_SHARED
- **Synchronization**: Semaphores cho shared variables
- **Process management**: fork(), wait(), _exit()

### Performance Bottlenecks
1. **Memory bandwidth**: Giới hạn với ma trận rất lớn
2. **Process overhead**: Nhiều tiến trình → context switching
3. **Cache efficiency**: Strassen có cache locality cần tối ưu hóa
4. **Synchronization cost**: Semaphore operations

## 📈 KẾT LUẬN VÀ KHUYẾN NGHỊ

### Kết luận chính
1. **Strassen Algorithm hiệu quả**: Với ma trận ≥256×256, hiệu suất tối ưu
2. **Parallel Row tối ưu**: Hiệu quả hơn parallel element cho hầu hết trường hợp
3. **Số tiến trình tối ưu**: 10-100 tiến trình cho ma trận trung bình, 100-1000 cho ma trận lớn
4. **Threshold quan trọng**: Với ma trận <64×64, nên dùng sequential

### Khuyến nghị thực tế
**Cho ma trận nhỏ (≤64×64):**
- Sử dụng sequential Strassen
- Tránh song song hóa do overhead

**Cho ma trận trung bình (128×128-512×512):**
- Sử dụng parallel row với 10-100 tiến trình
- Tránh quá nhiều tiến trình

**Cho ma trận lớn (≥1024×1024):**
- Sử dụng parallel row với 100-1000 tiến trình
- Cân nhắc memory requirements

### Hướng phát triển
1. **Hybrid approach**: Kết hợp Strassen cho ma trận lớn và phương pháp khác cho ma trận nhỏ
2. **Memory optimization**: Tối ưu hóa memory usage cho ma trận rất lớn
3. **Load balancing**: Cải thiện work distribution trong parallel element
4. **GPU acceleration**: Thử nghiệm Strassen trên GPU

## 📚 TÀI LIỆU THAM KHẢO

- Strassen, V. (1969). "Gaussian elimination is not optimal"
- Cormen, T. H. et al. (2009). "Introduction to Algorithms"
- Parallel Computing: Principles and Practice
- CS401V - Distributed Systems Course Materials

---

**Thông tin nhóm:**
- **Phan Văn Tài (2202081)**: Implementation & Testing
- **Hà Minh Chiến (2202095)**: Analysis & Documentation

**Liên hệ**: [Email nhóm] | [GitHub Repository]  
**Ngày hoàn thành**: 21/10/2025
