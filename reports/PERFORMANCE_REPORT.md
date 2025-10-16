# BÁO CÁO HIỆU SUẤT NHÂN MA TRẬN SONG SONG

## 📋 Tóm tắt thực hiện

**Ngày thực hiện:** 16/10/2025  
**Hệ thống:** Linux 6.8.0-85-generic, 12 CPU cores  
**Ngôn ngữ:** C  
**Phương pháp:** Process-based parallel computing với fork() và mmap()

### 👥 Thông tin nhóm
**CS401V - Distributed Systems Assignment 1**  
**Nhóm:** 2 thành viên
- **Phan Văn Tài** (2202081)
- **Hà Minh Chiến** (2202095) 

## 🎯 Mục tiêu

So sánh hiệu suất của 3 phương pháp nhân ma trận:
1. **Sequential**: Thuật toán tuần tự truyền thống
2. **Parallel Row**: Song song theo hàng với work-stealing
3. **Parallel Element**: Song song theo phần tử với work-stealing

### 📐 Complexity Analysis
- Time complexity: O(n^3) cho cả 3 phương pháp; parallel giảm thời gian thực tế theo p (số process)
- Space complexity: O(n^2) cho dữ liệu ma trận, O(p) cho quản lý process
- Synchronization overhead: tỉ lệ theo số lần lock/unlock (ít hơn với Row, nhiều hơn với Element)

## 🔧 Cấu hình thử nghiệm

### Kích thước ma trận:
- 10×10 (100 phần tử)
- 100×100 (10,000 phần tử)  
- 1000×1000 (1,000,000 phần tử)

### Số processes:
- 10 processes
- 100 processes

### 🎲 Reproducibility & Seed
- Sử dụng seed cố định (12345) để tất cả phương pháp dùng cùng dữ liệu đầu vào (A, B)
- Đảm bảo so sánh công bằng giữa các phương pháp và dễ tái lập kết quả

## 📊 Kết quả thực nghiệm

### Bảng 1: Thời gian thực thi (microseconds)

| Matrix Size | Sequential | Parallel Row (10p) | Parallel Element (10p) | Parallel Row (100p) | Parallel Element (100p) |
|-------------|------------|-------------------|----------------------|-------------------|----------------------|
| 10×10       | 3          | 523               | 357                  | -                 | -                    |
| 100×100     | 2,244      | 698               | 2,198                | 4,465             | 8,507                |
| 1000×1000   | 3,465,203  | 544,367           | 1,666,642            | 500,026           | 1,742,820            |

### Bảng 2: Speedup so với Sequential

| Matrix Size | Parallel Row (10p) | Parallel Element (10p) | Parallel Row (100p) | Parallel Element (100p) |
|-------------|-------------------|----------------------|-------------------|----------------------|
| 10×10       | 0.006x            | 0.008x               | -                 | -                    |
| 100×100     | 3.2x              | 1.0x                 | 0.5x              | 0.3x                 |
| 1000×1000   | 6.4x              | 2.1x                 | 6.9x              | 2.0x                 |

## 📈 Phân tích kết quả

### 1. **Ma trận nhỏ (10×10)**
- **Sequential nhanh nhất**: 3μs
- **Parallel chậm hơn**: Do overhead của process creation và synchronization
- **Kết luận**: Với ma trận nhỏ, overhead song song lớn hơn lợi ích

### 2. **Ma trận trung bình (100×100)**
- **Parallel Row (10p) tốt nhất**: 3.2x speedup
- **Parallel Element (10p)**: Không cải thiện (1.0x)
- **Parallel Row (100p)**: Chậm hơn do quá nhiều processes
- **Kết luận**: 10 processes là tối ưu cho ma trận 100×100

### 3. **Ma trận lớn (1000×1000)**
- **Parallel Row (100p) tốt nhất**: 6.9x speedup
- **Parallel Row (10p)**: 6.4x speedup
- **Parallel Element**: Chậm hơn do overhead cao
- **Kết luận**: Parallel Row hiệu quả hơn Parallel Element

## 🔍 Phân tích chi tiết

### **Tại sao Parallel Row hiệu quả hơn Parallel Element?**

1. **Granularity phù hợp**: 
   - Row-level: Mỗi process xử lý nhiều phần tử
   - Element-level: Mỗi process xử lý 1 phần tử

2. **Overhead thấp hơn**:
   - Ít semaphore operations hơn
   - Ít context switching hơn

3. **Cache locality tốt hơn**:
   - Xử lý liên tiếp các phần tử trong cùng hàng
   - Tận dụng cache hiệu quả

### **Tại sao quá nhiều processes làm chậm?**

1. **Process creation overhead**: Tạo 1000 processes tốn nhiều thời gian
2. **Context switching**: Hệ thống phải chuyển đổi giữa quá nhiều processes
3. **Memory overhead**: Mỗi process cần stack riêng
4. **Synchronization overhead**: Semaphore operations tăng theo số processes

## 📊 Biểu đồ hiệu suất

### Speedup vs Matrix Size (10 processes)
```
Speedup
   7x |     ●
   6x |   ●
   5x | ●
   4x |
   3x |   ●
   2x |     ●
   1x |       ●
   0x |_________●
      10   100  1000
      Matrix Size
```

### Time vs Matrix Size
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
4. **Parallel Element** có overhead quá cao

### **Khuyến nghị:**

1. **Ma trận nhỏ**: Sử dụng Sequential
2. **Ma trận trung bình**: Parallel Row với 10-50 processes
3. **Ma trận lớn**: Parallel Row với 50-100 processes
4. **Tránh Parallel Element** trừ khi có lý do đặc biệt

### **Cải tiến có thể:**

1. **Thread-based** thay vì process-based để giảm overhead
2. **Block-based parallelization** cho ma trận rất lớn
3. **Memory optimization** để tận dụng cache tốt hơn
4. **Load balancing** thông minh hơn

## 📝 Ghi chú kỹ thuật

- **Synchronization**: Sử dụng semaphore cho shared variables
- **Memory sharing**: mmap() với MAP_SHARED
- **Process management**: fork() và wait()
- **Timing**: gettimeofday() với độ chính xác microsecond
- **Data consistency**: Fixed seed (12345) để đảm bảo cùng input

### 💾 Memory Requirements (ước tính)
- 10×10: ~2KB
- 100×100: ~240KB
- 1000×1000: ~24MB
- 2000×2000: ~96MB

### ⚠️ Limitations
- Process-based overhead cao hơn thread-based
- Bị giới hạn bởi memory bandwidth khi n lớn
- Kết quả phụ thuộc cấu hình phần cứng/OS
- Seed cố định giúp tái lập nhưng không bao phủ tất cả phân phối dữ liệu

## 👥 Thông tin nhóm

**CS401V - Distributed Systems Assignment 1**  
**Nhóm:** 2 thành viên
- **Phan Văn Tài** (2202081) 
- **Hà Minh Chiến** (2202095) 

---
*Báo cáo được tạo tự động từ kết quả benchmark thực tế*
