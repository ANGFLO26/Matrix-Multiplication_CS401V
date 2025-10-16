# TÓM TẮT KẾT QUẢ BENCHMARK

## 👥 Thông tin nhóm
**CS401V - Distributed Systems Assignment 1**  
**Nhóm:** 2 thành viên
- **Phan Văn Tài** (2202081) 
- **Hà Minh Chiến** (2202095) 

## 📊 Kết quả chính

### Thời gian thực thi (microseconds)

| Matrix Size | Sequential | Row(10p) | Element(10p) | Row(100p) | Element(100p) | Row(1000p) | Element(1000p) |
|-------------|------------|----------|--------------|----------|---------------|------------|----------------|
| 10×10       | 3          | 523      | 357          | -        | -             | -          | -              |
| 100×100     | 2,244      | 698      | 2,198        | 4,465    | 8,507         | -          | -              |
| 1000×1000   | 3,465,203  | 544,367  | 1,666,642    | 500,026  | 1,742,820     | 485,327    | 1,774,566      |
| 2000×2000   | 32,228,064 | -        | -            | 7,754,967| 15,760,094    | 5,686,955  | 13,842,551     |

### Speedup so với Sequential

| Matrix Size | Row(10p) | Element(10p) | Row(100p) | Element(100p) | Row(1000p) | Element(1000p) |
|-------------|----------|--------------|----------|---------------|------------|----------------|
| 10×10       | 0.006x   | 0.008x       | -        | -             | -          | -              |
| 100×100     | 3.2x     | 1.0x         | 0.5x     | 0.3x          | -          | -              |
| 1000×1000   | 6.4x     | 2.1x         | 6.9x     | 2.0x          | **7.1x**   | 2.0x           |
| 2000×2000   | -        | -            | 4.2x     | 2.0x          | **5.7x**   | 2.3x           |

## 🎯 Kết luận chính

1. **Sequential tốt nhất** cho ma trận nhỏ (< 100×100)
2. **Parallel Row hiệu quả nhất** cho ma trận lớn
3. **1000 processes tối ưu** cho ma trận 1000×1000 và 2000×2000
4. **Parallel Element kém hiệu quả** do overhead cao
5. **Memory bandwidth** trở thành bottleneck với ma trận rất lớn

### 🧪 Reproducibility
- Tất cả phép đo dùng seed cố định (12345) để đảm bảo cùng input, so sánh công bằng

### ⚠️ Limitations
- Overhead của process cao với ma trận nhỏ
- Speedup bị giới hạn bởi băng thông bộ nhớ khi n lớn
- Kết quả phụ thuộc cấu hình phần cứng hệ thống

## 📈 Phát hiện quan trọng

- **1000×1000**: Speedup tối đa 7.1x với 1000 processes
- **2000×2000**: Speedup giảm xuống 5.7x do memory bottleneck
- **Scaling**: Nhiều processes giúp cải thiện hiệu suất đến một điểm nhất định
- **Overhead**: Process-based parallel có overhead cao với ma trận nhỏ

## ⏱️ Thời gian thực tế

- **1000×1000 Sequential**: 3.47 giây → **Parallel Row (1000p)**: 0.49 giây
- **2000×2000 Sequential**: 32.23 giây → **Parallel Row (1000p)**: 5.69 giây

**Tiết kiệm thời gian**: 26.54 giây cho ma trận 2000×2000!

## 👥 Thông tin nhóm

**CS401V - Distributed Systems Assignment 1**  
**Nhóm:** 2 thành viên
- **Phan Văn Tài** (2202081) 
- **Hà Minh Chiến** (2202095)
