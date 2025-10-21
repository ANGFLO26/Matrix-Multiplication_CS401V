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
├── data/                        # Dữ liệu đã xử lý
│   ├── raw_data.csv            # Dữ liệu thô từ log
│   ├── raw_data.json           # Dữ liệu thô (JSON)
│   ├── speedup_data.csv        # Dữ liệu speedup
│   └── speedup_data.json       # Dữ liệu speedup (JSON)
└── output/                      # Biểu đồ đã tạo
    ├── 01_speedup_vs_matrix_size.png
    ├── 02_speedup_vs_process_count.png
    ├── 03_row_vs_element_comparison.png
    ├── 04_efficiency_heatmap.png
    ├── 05_optimal_process_analysis.png
    ├── 07_memory_usage_analysis.png
    └── 08_overhead_analysis.png
```

## 📈 Các biểu đồ được tạo

### 1. **Speedup vs Matrix Size** (`01_speedup_vs_matrix_size.png`)
- **Mục đích**: Thấy xu hướng speedup theo kích thước ma trận
- **Loại**: Line chart với multiple series
- **X-axis**: Matrix size (4, 8, 16, 32, 64, 128, 256, 512, 1024)
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
- **Y-axis**: Execution time (μs)
- **Series**: Sequential, Parallel Row (Best), Parallel Element (Best)

### 4. **Efficiency Heatmap** (`04_efficiency_heatmap.png`)
- **Mục đích**: Thấy pattern hiệu quả
- **Loại**: Heatmap
- **X-axis**: Process count
- **Y-axis**: Matrix size
- **Color**: Speedup value

### 5. **Optimal Process Analysis** (`05_optimal_process_analysis.png`)
- **Mục đích**: Tìm quy luật optimal process count
- **Loại**: Scatter plot với trend line
- **X-axis**: Matrix size
- **Y-axis**: Optimal process count

### 7. **Memory Usage Analysis** (`07_memory_usage_analysis.png`)
- **Mục đích**: Phát hiện memory bottleneck
- **Loại**: Line chart
- **X-axis**: Matrix size
- **Y-axis**: Memory usage (MB)

### 8. **Overhead Analysis** (`08_overhead_analysis.png`)
- **Mục đích**: Phân tích overhead
- **Loại**: Stacked bar chart
- **X-axis**: Matrix size
- **Y-axis**: Time breakdown
- **Stacks**: Computation time, Overhead time

## 🚀 Cách sử dụng

### 1. Trích xuất dữ liệu
```bash
cd reports/visualization/code
python3 extract_data.py
```

### 2. Tạo biểu đồ
```bash
cd reports/visualization/code
python3 generate_charts.py
```

### 3. Xem kết quả
```bash
ls ../output/
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
1. **Speedup tăng theo matrix size**: Ma trận lớn hơn → speedup tốt hơn
2. **Optimal process count**: 10-100 processes cho ma trận trung bình
3. **Parallel Row hiệu quả hơn**: So với Parallel Element
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


