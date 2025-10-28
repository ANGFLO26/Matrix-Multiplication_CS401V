# CHARTS - STRASSEN ALGORITHM VISUALIZATION

## 📊 Tổng quan

Thư mục này chứa các biểu đồ và code để trực quan hóa hiệu suất của Strassen Algorithm trong việc nhân ma trận song song.

## 🗂️ Cấu trúc thư mục

```
reports/visualization/
├── README.md                    # Tài liệu này
├── code/                        # Code để tạo biểu đồ
│   ├── generate_charts.py      # Script chính tạo biểu đồ
│   └── extract_data.py         # Script trích xuất dữ liệu
├── data/                        # Dữ liệu
│   ├── raw_data.csv            # Dữ liệu thô từ log (≤1024)
│   ├── raw_data.json           # Dữ liệu thô (JSON)
│   ├── extended_benchmark_data.csv # Dữ liệu mở rộng (đến 6144)
│   ├── extended_benchmark_data.json
│   ├── speedup_data.csv        # Dữ liệu speedup (≤1024 có baseline)
│   └── speedup_data.json       # Dữ liệu speedup (JSON)
└── ../charts/                   # Biểu đồ đã tạo (đặt tại reports/charts/)
    ├── 01_speedup_vs_matrix_size.png
    ├── 02_speedup_vs_process_count.png
    ├── 03_row_vs_element_comparison.png
    ├── 04_efficiency_heatmap.png
    ├── 06_best_time_large.png
    ├── 09_algorithm_complexity.png
    ├── 11_scalability_analysis.png
    └── 13_3d_performance_surface.png
```

## 📈 Các biểu đồ được tạo

### 1. **Speedup vs Matrix Size** (`01_speedup_vs_matrix_size.png`)
- **Mục đích**: Thấy xu hướng speedup theo kích thước ma trận
- **Loại**: Line chart với multiple series
- **X-axis**: Matrix size (4 → 1024; chỉ phạm vi có baseline tuần tự)
- **Y-axis**: Speedup
- **Series**: Parallel Row (p=10, p=100, p=1000), Parallel Element (p=10, p=100, p=1000)

### 2. **Speedup vs Process Count** (`02_speedup_vs_process_count.png`)
- **Mục đích**: Tìm optimal process count
- **Loại**: Line chart
- **X-axis**: Process count (10, 100, 1000)
- **Y-axis**: Speedup
- **Series**: Different matrix sizes (256, 512, 1024)

### 3. **Row vs Element Comparison** (`03_row_vs_element_comparison.png`)
- **Mục đích**: So sánh trực tiếp hiệu quả
- **Loại**: Bar chart
- **X-axis**: Matrix size
- **Y-axis**: Execution time (μs, s)
- **Series**: Sequential (≤1024), Parallel Row (Best), Parallel Element (Best)
- **Lưu ý**: Với ≥1536 chỉ so sánh thời gian giữa Row/Element do thiếu baseline tuần tự

### 4. **Efficiency Heatmap** (`04_efficiency_heatmap.png`)
- **Mục đích**: Thấy pattern hiệu quả
- **Loại**: Heatmap
- **X-axis**: Process count
- **Y-axis**: Matrix size
- **Color**: Speedup value

### 6. **Best Time for Large Sizes** (`06_best_time_large.png`)
- **Mục đích**: Thể hiện thời gian tốt nhất cho dải ≥1536, và phương pháp thắng (Row/Element)
- **Loại**: Line + annotations
- **X-axis**: Matrix size (≥1536)
- **Y-axis**: Best time (s, log scale)
- **Ghi chú**: Nhãn chú thích tại mỗi điểm nêu rõ phương pháp thắng

### 9. **Algorithm Complexity** (`09_algorithm_complexity.png`)
- **Mục đích**: So sánh độ phức tạp lý thuyết (Naive vs Strassen) và hiệu năng thực tế (scaled)
- **Loại**: Line chart (log-log)

### 11. **Scalability Analysis** (`11_scalability_analysis.png`)
- **Mục đích**: Phân tích speedup, efficiency (%), throughput (ops/sec) theo kích thước và số tiến trình
- **Loại**: 3 subplot (line)

### 13. **3D Performance Surface** (`13_3d_performance_surface.png`)
- **Mục đích**: Bề mặt 3D thể hiện speedup theo (size, processes)
- **Loại**: 3D surface

## 🚀 Cách sử dụng

### 1. Trích xuất dữ liệu (tùy chọn nếu có log)
```bash
cd reports/visualization/code
python3 extract_data.py
```

### 2. Tạo biểu đồ
```bash
cd reports/visualization/code
python3 generate_charts.py  # đọc trực tiếp từ data/*.json, không cần logs
```

### 3. Xem kết quả
```bash
ls ../charts/
```

## 📋 Yêu cầu hệ thống

- **Python 3.6+**
- **matplotlib**: `pip install matplotlib`
- **numpy**: `pip install numpy`
- **pandas**: `pip install pandas`
- **seaborn**: `pip install seaborn`

## 🔧 Tùy chỉnh biểu đồ

### Thay đổi màu sắc
```python
# Trong generate_charts.py
colors = ['red', 'green', 'blue', 'orange', 'purple', 'brown']
```

### Thay đổi kích thước
```python
# Trong generate_charts.py
fig, ax = plt.subplots(figsize=(12, 8))  # width, height
```

### Thay đổi style
```python
# Trong generate_charts.py
plt.style.use('seaborn-v0_8')  # hoặc 'default', 'ggplot', etc.
```

## 📊 Phân tích kết quả

### Xu hướng chính
1. **Speedup tăng theo matrix size**: Ma trận lớn hơn → speedup tốt hơn (≤1024)
2. **Optimal process count**: 10-100 processes cho ma trận trung bình (≤1024); ≥1536 xem “best time”
3. **Parallel Row** hiệu quả hơn ở ≤1024; **Parallel Element** tốt hơn ở ≥1536
4. **Memory bottleneck**: Với ma trận ≥1024×1024

### Bottleneck patterns
1. **Memory usage**: Tăng tuyến tính với matrix size
2. **Overhead**: Tăng với số processes
3. **Cache efficiency**: Giảm với ma trận lớn

## 🎯 Mục tiêu đạt được

- ✅ **Trực quan hóa xu hướng**: Speedup theo matrix size và process count
- ✅ **So sánh hiệu quả**: Row vs Element performance  
- ✅ **Tìm optimal point**: Process count tối ưu cho từng matrix size
- ✅ **Phát hiện bottleneck**: Memory bandwidth, overhead patterns

## 📞 Liên hệ

**Thành viên nhóm **
- **Phan Văn Tài (2202081)**
- **Hà Minh Chiến (2202095)**


