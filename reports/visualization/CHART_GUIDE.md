# 📊 STRASSEN ALGORITHM - CHART VISUALIZATION GUIDE

## **Tổng quan**
Dự án này bao gồm **7 biểu đồ cốt lõi** để phân tích hiệu suất của Strassen Algorithm trong các phương pháp nhân ma trận song song.

---

## **📈 BIỂU ĐỒ CỐT LÕI (7 biểu đồ)**

### **1. Speedup vs Matrix Size** ⭐ **CỐT LÕI**
- **File**: `01_speedup_vs_matrix_size.png`
- **Mục đích**: Thấy xu hướng speedup theo kích thước ma trận
- **Insight**: Tìm matrix size tối ưu cho từng phương pháp

### **2. Speedup vs Process Count** ⭐ **CỐT LÕI**
- **File**: `02_speedup_vs_process_count.png` 
- **Mục đích**: Phân tích speedup theo số process
- **Insight**: Tìm số process tối ưu

### **3. Row vs Element Comparison** ⭐ **CỐT LÕI**
- **File**: `03_row_vs_element_comparison.png`
- **Mục đích**: So sánh hiệu quả Row vs Element
- **Insight**: Chọn phương pháp tốt nhất

### **4. Efficiency Heatmap** ⭐ **CỐT LÕI**
- **File**: `04_efficiency_heatmap.png`
- **Mục đích**: Heatmap hiệu quả theo matrix size và process count
- **Insight**: Tìm vùng tối ưu (màu xanh)

### **9. Algorithm Complexity Comparison** ⭐ **QUAN TRỌNG**
- **File**: `09_algorithm_complexity.png`
- **Mục đích**: So sánh Strassen O(n^log₂7) vs Naive O(n³)
- **Insight**: Thấy lợi ích lý thuyết của Strassen

### **11. Scalability Analysis** ⭐ **QUAN TRỌNG**
- **File**: `11_scalability_analysis.png`
- **Mục đích**: Phân tích khả năng mở rộng (3 subplots)
- **Insight**: Speedup, Efficiency, Throughput trends

### **13. 3D Performance Surface** ⭐ **ẤN TƯỢNG**
- **File**: `13_3d_performance_surface.png`
- **Mục đích**: Surface 3D của performance
- **Insight**: Tìm optimal region trong không gian 3D

---

## **🎯 CÁCH SỬ DỤNG BIỂU ĐỒ**

### **Cho Báo cáo Kỹ thuật:**
- Sử dụng biểu đồ 1-8 cho phân tích cơ bản
- Biểu đồ 9, 11, 15 cho phân tích algorithm
- Biểu đồ 10, 14 cho phân tích system

### **Cho Presentation:**
- Biểu đồ 1, 3, 4, 13 cho overview
- Biểu đồ 2, 5, 12 cho optimization
- Biểu đồ 6, 7, 8, 14 cho bottleneck analysis

### **Cho Research Paper:**
- Tất cả 15 biểu đồ cho comprehensive analysis
- Biểu đồ 9, 11, 15 cho theoretical validation
- Biểu đồ 1-8 cho experimental results

---

## **📁 CẤU TRÚC THƯ MỤC**

```
reports/visualization/
├── README.md                           # Hướng dẫn tổng quan
├── CHART_GUIDE.md                      # Hướng dẫn chi tiết (file này)
├── code/                               # Scripts tạo biểu đồ
│   ├── generate_charts.py             # Script cơ bản (1-4)
│   ├── generate_additional_charts.py  # Script nâng cao (9,11,13)
│   └── extract_data.py                # Script trích xuất dữ liệu
└── data/                              # Dữ liệu đã xử lý
    ├── raw_data.csv                  # Dữ liệu thô
    ├── raw_data.json                 # Dữ liệu thô (JSON)
    ├── speedup_data.csv              # Dữ liệu speedup
    └── speedup_data.json             # Dữ liệu speedup (JSON)

reports/charts/                        # Biểu đồ chính
├── 01_speedup_vs_matrix_size.png
├── 02_speedup_vs_process_count.png
├── 03_row_vs_element_comparison.png
├── 04_efficiency_heatmap.png
├── 05_optimal_process_analysis.png
├── 07_memory_usage_analysis.png
├── 08_overhead_analysis.png
├── 09_algorithm_complexity.png
├── 10_performance_per_core.png
├── 11_scalability_analysis.png
├── 12_cost_benefit_analysis.png
├── 13_3d_performance_surface.png
├── 14_resource_utilization.png
└── 15_performance_regression.png
```

---

## **🔧 TẠO LẠI BIỂU ĐỒ**

### **Tạo tất cả biểu đồ:**
```bash
cd reports/visualization/code
python3 generate_charts.py              # Biểu đồ 1-8
python3 generate_additional_charts.py   # Biểu đồ 9-15
```

### **Tạo biểu đồ riêng lẻ:**
Chỉnh sửa script để chỉ tạo biểu đồ cần thiết.

---

## **📊 THỐNG KÊ BIỂU ĐỒ**

- **Tổng số**: 7 biểu đồ cốt lõi
- **Kích thước**: 2.4MB
- **Độ phân giải**: 300 DPI
- **Format**: PNG
- **Chất lượng**: High-resolution, publication-ready

---

## **🎨 THIẾT KẾ BIỂU ĐỒ**

- **Color scheme**: Viridis, plasma, husl
- **Style**: Professional, clean
- **Font**: Default matplotlib fonts
- **Grid**: Enabled với alpha=0.3
- **Legend**: Positioned optimally
- **Title**: Bold, descriptive

---

## **📈 INSIGHTS CHÍNH**

1. **Strassen Algorithm** cho thấy speedup tốt với matrix size lớn
2. **Parallel Row** thường tốt hơn **Parallel Element** 
3. **Optimal process count** tăng theo matrix size
4. **Memory usage** tăng theo O(n²)
5. **Overhead** tăng với số process cao
6. **3D surface** cho thấy vùng tối ưu rõ ràng
7. **Cost-benefit** analysis giúp tìm sweet spot

---

**📝 Lưu ý**: Tất cả biểu đồ được tạo từ dữ liệu thực tế benchmark và sẵn sàng sử dụng cho báo cáo, presentation, hoặc research paper.
