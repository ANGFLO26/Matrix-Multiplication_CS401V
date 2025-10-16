# BÁO CÁO CUỐI CÙNG: HIỆU SUẤT NHÂN MA TRẬN SONG SONG

## 📋 Thông tin thực hiện

**Ngày:** 16/10/2025  
**Hệ thống:** Linux 6.8.0-85-generic  
**CPU:** 12 cores  
**Ngôn ngữ:** C  
**Phương pháp:** Process-based parallel computing

### 👥 Thông tin nhóm
**CS401V - Distributed Systems Assignment 1**  
**Nhóm:** 2 thành viên
- **Phan Văn Tài** (2202081) 
- **Hà Minh Chiến** (2202095) 

## 🎯 Mục tiêu nghiên cứu

So sánh hiệu suất của 3 phương pháp nhân ma trận:
1. **Sequential**: Thuật toán tuần tự O(n³)
2. **Parallel Row**: Song song theo hàng với work-stealing O(n³/p)
3. **Parallel Element**: Song song theo phần tử với work-stealing O(n³/p)

### **Complexity Analysis:**
- **Time Complexity**: Tất cả đều O(n³) nhưng parallel giảm thời gian thực tế
- **Space Complexity**: O(n²) cho ma trận + O(p) cho processes
- **Communication Overhead**: O(p) cho semaphore operations

## 🔧 Cấu hình thử nghiệm

### Kích thước ma trận:
- **10×10**: 100 phần tử (ma trận nhỏ)
- **100×100**: 10,000 phần tử (ma trận trung bình)
- **1000×1000**: 1,000,000 phần tử (ma trận lớn)
- **2000×2000**: 4,000,000 phần tử (ma trận rất lớn)

### Số processes:
- **10 processes**: Phù hợp với ma trận trung bình
- **100 processes**: Phù hợp với ma trận lớn
- **1000 processes**: Phù hợp với ma trận rất lớn

## 📊 Kết quả thực nghiệm

### Bảng 1: Thời gian thực thi (microseconds)

| Matrix Size | Sequential | Parallel Row (10p) | Parallel Element (10p) | Parallel Row (100p) | Parallel Element (100p) | Parallel Row (1000p) | Parallel Element (1000p) |
|-------------|------------|-------------------|----------------------|-------------------|----------------------|---------------------|-------------------------|
| 10×10       | 3          | 523               | 357                  | -                 | -                    | -                   | -                       |
| 100×100     | 2,244      | 698               | 2,198                | 4,465             | 8,507                | -                   | -                       |
| 1000×1000   | 3,465,203  | 544,367           | 1,666,642            | 500,026           | 1,742,820            | 485,327             | 1,774,566               |
| 2000×2000   | 32,228,064 | -                 | -                    | 7,754,967         | 15,760,094           | 5,686,955           | 13,842,551              |

### Bảng 2: Speedup so với Sequential

| Matrix Size | Parallel Row (10p) | Parallel Element (10p) | Parallel Row (100p) | Parallel Element (100p) | Parallel Row (1000p) | Parallel Element (1000p) |
|-------------|-------------------|----------------------|-------------------|----------------------|---------------------|-------------------------|
| 10×10       | 0.006x            | 0.008x               | -                 | -                    | -                   | -                       |
| 100×100     | 3.2x              | 1.0x                 | 0.5x              | 0.3x                 | -                   | -                       |
| 1000×1000   | 6.4x              | 2.1x                 | 6.9x              | 2.0x                 | 7.1x                | 2.0x                    |
| 2000×2000   | -                 | -                    | 4.2x              | 2.0x                 | 5.7x                | 2.3x                    |

## 📈 Phân tích chi tiết

### 1. **Ma trận nhỏ (10×10)**

**Kết quả:**
- Sequential: 3μs
- Parallel Row (10p): 523μs (174x chậm hơn!)
- Parallel Element (10p): 357μs (119x chậm hơn!)

**Phân tích:**
- **Overhead cao**: Process creation và synchronization tốn nhiều thời gian
- **Work ít**: Ma trận nhỏ không đủ để justify parallel overhead
- **Kết luận**: Sequential là lựa chọn tốt nhất cho ma trận nhỏ

### 2. **Ma trận trung bình (100×100)**

**Kết quả:**
- Sequential: 2,244μs
- Parallel Row (10p): 698μs (3.2x nhanh hơn) ✅
- Parallel Element (10p): 2,198μs (1.0x - không cải thiện)
- Parallel Row (100p): 4,465μs (0.5x - chậm hơn)
- Parallel Element (100p): 8,507μs (0.3x - chậm hơn)

**Phân tích:**
- **Parallel Row (10p) tối ưu**: 3.2x speedup
- **Quá nhiều processes**: 100p làm chậm do overhead
- **Parallel Element kém hiệu quả**: Overhead cao hơn lợi ích

### 3. **Ma trận lớn (1000×1000)**

**Kết quả:**
- Sequential: 3,465,203μs (3.47 giây)
- Parallel Row (10p): 544,367μs (0.54 giây) - 6.4x speedup
- Parallel Element (10p): 1,666,642μs (1.67 giây) - 2.1x speedup
- Parallel Row (100p): 500,026μs (0.50 giây) - 6.9x speedup
- Parallel Element (100p): 1,742,820μs (1.74 giây) - 2.0x speedup
- Parallel Row (1000p): 485,327μs (0.49 giây) - 7.1x speedup ✅
- Parallel Element (1000p): 1,774,566μs (1.77 giây) - 2.0x speedup

**Phân tích:**
- **Parallel Row (1000p) tối ưu**: 7.1x speedup
- **Parallel Row hiệu quả hơn Parallel Element**: Ít overhead hơn
- **Scaling tốt**: Nhiều processes giúp cải thiện hiệu suất

### 4. **Ma trận rất lớn (2000×2000)**

**Kết quả:**
- Sequential: 32,228,064μs (32.23 giây)
- Parallel Row (100p): 7,754,967μs (7.75 giây) - 4.2x speedup
- Parallel Element (100p): 15,760,094μs (15.76 giây) - 2.0x speedup
- Parallel Row (1000p): 5,686,955μs (5.69 giây) - 5.7x speedup ✅
- Parallel Element (1000p): 13,842,551μs (13.84 giây) - 2.3x speedup

**Phân tích:**
- **Parallel Row (1000p) tối ưu**: 5.7x speedup
- **Giảm hiệu suất so với 1000×1000**: Do memory bandwidth bottleneck
- **Parallel Element cải thiện nhẹ**: 2.3x vs 2.0x với 100p
- **Memory-bound**: Ma trận lớn bị giới hạn bởi memory bandwidth

## 🔍 Phân tích sâu

### **Tại sao Parallel Row hiệu quả hơn Parallel Element?**

1. **Granularity phù hợp**:
   - Row-level: Mỗi process xử lý toàn bộ hàng (nhiều phần tử)
   - Element-level: Mỗi process xử lý 1 phần tử

2. **Overhead thấp hơn**:
   - Ít semaphore operations (1 lần/hàng vs 1 lần/phần tử)
   - Ít context switching
   - Ít memory allocation

3. **Cache locality tốt hơn**:
   - Xử lý liên tiếp các phần tử trong cùng hàng
   - Tận dụng CPU cache hiệu quả
   - Ít cache misses

4. **Work distribution tốt hơn**:
   - Row-level: Work được phân chia đều hơn
   - Element-level: Có thể có load imbalance

### **Tại sao quá nhiều processes làm chậm?**

1. **Process creation overhead**: Tạo 1000 processes tốn ~100ms
2. **Context switching**: Hệ thống phải chuyển đổi giữa quá nhiều processes
3. **Memory overhead**: Mỗi process cần stack riêng (~8MB)
4. **Synchronization overhead**: Semaphore operations tăng theo số processes
5. **Resource contention**: CPU cores bị oversubscribed

### **Tại sao ma trận nhỏ không phù hợp với parallel?**

1. **Work ít**: 100 phần tử vs overhead của 10 processes
2. **Communication cost**: Process communication > computation time
3. **Memory overhead**: Shared memory setup tốn nhiều thời gian

## 📊 Biểu đồ hiệu suất (Text-based)

### Speedup vs Matrix Size
```
Speedup
   7x |     ● Parallel Row (100p)
   6x |   ● ● Parallel Row (10p)
   5x | ●
   4x |
   3x |   ●
   2x |     ● ● Parallel Element
   1x |       ● ●
   0x |_________●
      10   100  1000
      Matrix Size
```

### Execution Time (log scale)
```
Time (μs)
3.5M | ● Sequential
    |   ●
    |     ●
    |       ● Parallel Row (10p)
    |         ●
    |           ●
    |             ● Parallel Element (10p)
    |_______________
      10   100  1000
      Matrix Size
```

## 🎯 Kết luận và khuyến nghị

### **Kết luận chính:**

1. **Sequential phù hợp** với ma trận nhỏ (< 100×100)
2. **Parallel Row hiệu quả nhất** với ma trận lớn
3. **Số processes tối ưu** phụ thuộc vào kích thước ma trận
4. **Parallel Element** có overhead quá cao, không khuyến nghị

### **Khuyến nghị cụ thể:**

| Matrix Size | Phương pháp tối ưu | Số processes | Speedup | Thời gian |
|-------------|-------------------|--------------|---------|-----------|
| < 100×100   | Sequential        | 1            | 1.0x    | < 1ms     |
| 100×100     | Parallel Row      | 10           | 3.2x    | 0.7ms     |
| 1000×1000   | Parallel Row      | 1000         | 7.1x    | 0.49s     |
| 2000×2000   | Parallel Row      | 1000         | 5.7x    | 5.69s     |
| > 2000×2000 | Parallel Row      | 1000+        | 5-6x    | Memory-bound |

### **Cải tiến có thể:**

1. **Thread-based parallelization**: Giảm overhead so với process-based
2. **Block-based parallelization**: Chia ma trận thành blocks
3. **Memory optimization**: Tối ưu cache locality
4. **Load balancing**: Phân chia công việc thông minh hơn
5. **NUMA awareness**: Tận dụng memory topology

### **Limitations của nghiên cứu:**

1. **Process-based overhead**: Tạo process tốn nhiều tài nguyên hơn thread
2. **Memory bandwidth bottleneck**: Với ma trận rất lớn, memory trở thành giới hạn
3. **System-dependent**: Kết quả phụ thuộc vào hardware và OS
4. **Fixed seed**: Chỉ test với một bộ dữ liệu, không đại diện cho tất cả trường hợp
5. **Single machine**: Không test trên distributed system thực tế

## 📝 Ghi chú kỹ thuật

### **Implementation details:**
- **Synchronization**: Semaphore cho shared variables
- **Memory sharing**: mmap() với MAP_SHARED
- **Process management**: fork() và wait()
- **Timing**: gettimeofday() với độ chính xác microsecond
- **Data consistency**: Fixed seed (12345) để đảm bảo cùng input

### **Lý do sử dụng seed cố định:**
Để đảm bảo tính công bằng trong việc so sánh hiệu suất, tất cả 3 phương pháp đều sử dụng cùng một seed cố định (12345). Điều này đảm bảo:
- Tất cả chương trình tạo ra cùng ma trận A và B
- Kết quả khác nhau chỉ do thuật toán, không do dữ liệu đầu vào
- Việc so sánh hiệu suất có ý nghĩa và chính xác
- **Reproducibility**: Kết quả có thể tái tạo trên các hệ thống khác nhau

### **System requirements:**
- **OS**: Linux với POSIX support
- **Memory**: 
  - 10×10: ~2KB
  - 100×100: ~240KB  
  - 1000×1000: ~24MB
  - 2000×2000: ~96MB
- **CPU**: Multi-core processor (khuyến nghị 8+ cores)
- **Compiler**: GCC với pthread support

## 🏆 Tóm tắt

Nghiên cứu này chứng minh rằng **parallel computing có thể cải thiện đáng kể hiệu suất nhân ma trận**, nhưng chỉ khi:
1. **Ma trận đủ lớn** để justify parallel overhead
2. **Số processes phù hợp** với kích thước ma trận
3. **Chọn phương pháp parallel phù hợp** (Row-level tốt hơn Element-level)

**Kết quả tốt nhất**: 
- **1000×1000**: Parallel Row với 1000 processes đạt **7.1x speedup**, giảm thời gian từ 3.47 giây xuống 0.49 giây
- **2000×2000**: Parallel Row với 1000 processes đạt **5.7x speedup**, giảm thời gian từ 32.23 giây xuống 5.69 giây

**Phát hiện quan trọng**: Với ma trận rất lớn (2000×2000), hiệu suất bắt đầu giảm do memory bandwidth bottleneck, cho thấy giới hạn của parallel computing với process-based approach.

## 👥 Thông tin nhóm

**CS401V - Distributed Systems Assignment 1**  
**Nhóm:** 2 thành viên
- **Phan Văn Tài** (2202081) 
- **Hà Minh Chiến** (2202095) 

---
*Báo cáo được tạo từ kết quả benchmark thực tế trên hệ thống Linux*
