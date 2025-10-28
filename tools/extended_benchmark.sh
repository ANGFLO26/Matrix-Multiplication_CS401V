#!/bin/bash

# =============================================================================
# EXTENDED STRASSEN ALGORITHM BENCHMARK
# =============================================================================
# Mở rộng benchmark với nhiều kích thước ma trận và số process khác nhau
# Tác giả: AI Assistant
# Ngày: $(date +%Y-%m-%d)
# =============================================================================

# Cấu hình
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$ROOT_DIR/compiled"
LOG_DIR="$ROOT_DIR/reports/logs"
TIMEOUT=600  # 10 phút timeout cho mỗi test
MEMORY_LIMIT="8G"  # Giới hạn bộ nhớ

# Tạo thư mục log nếu chưa có
mkdir -p "$LOG_DIR"

# Hàm kiểm tra bộ nhớ
check_memory() {
    local required_mb=$1
    local available_mb=$(free -m | awk 'NR==2{print $7}')
    if [ "$available_mb" -lt "$required_mb" ]; then
        echo "⚠️  WARNING: Insufficient memory. Required: ${required_mb}MB, Available: ${available_mb}MB"
        return 1
    fi
    return 0
}

# Hàm chạy test với timeout và memory check
run_test() {
    local matrix_size=$1
    local num_processes=$2
    local method=$3
    local phase=$4
    
    # Ước tính bộ nhớ cần thiết (MB)
    local memory_needed=$((matrix_size * matrix_size * 8 / 1024 / 1024 * 3))  # 3 matrices
    
    echo "  Testing: $method, n=$matrix_size, p=$num_processes (Memory: ${memory_needed}MB)"
    
    # Kiểm tra bộ nhớ
    if ! check_memory "$memory_needed"; then
        echo "    ⏭️  SKIP: Insufficient memory"
        return
    fi
    
    # Chạy test với timeout
    timeout $TIMEOUT "$BUILD_DIR/${method}" "$matrix_size" "$num_processes" 2>&1 | tee -a "$LOG_DIR/extended_${phase}.log"
    local exit_code=$?
    
    if [ $exit_code -eq 124 ]; then
        echo "    ⏰ TIMEOUT: Test exceeded ${TIMEOUT}s"
    elif [ $exit_code -ne 0 ]; then
        echo "    ❌ ERROR: Test failed with exit code $exit_code"
    else
        echo "    ✅ SUCCESS: Test completed"
    fi
}

# Hàm chạy phase
run_phase() {
    local phase_name=$1
    local matrix_sizes=$2
    local process_counts=$3
    local methods=$4
    
    echo ""
    echo "🚀 STARTING $phase_name"
    echo "Matrix sizes: $matrix_sizes"
    echo "Process counts: $process_counts"
    echo "Methods: $methods"
    echo "Start time: $(date)"
    echo ""
    
    # Tạo log file cho phase
    echo "=== $phase_name BENCHMARK ===" > "$LOG_DIR/extended_${phase_name,,}.log"
    echo "Start time: $(date)" >> "$LOG_DIR/extended_${phase_name,,}.log"
    echo "Matrix sizes: $matrix_sizes" >> "$LOG_DIR/extended_${phase_name,,}.log"
    echo "Process counts: $process_counts" >> "$LOG_DIR/extended_${phase_name,,}.log"
    echo "" >> "$LOG_DIR/extended_${phase_name,,}.log"
    
    for matrix_size in $matrix_sizes; do
        echo ">>> Matrix Size = $matrix_size ($(date))" | tee -a "$LOG_DIR/extended_${phase_name,,}.log"
        
        # Sequential test (chỉ cho matrix size nhỏ)
        if [[ "$matrix_size" -le 1024 ]]; then
            echo "1) Sequential:" | tee -a "$LOG_DIR/extended_${phase_name,,}.log"
            timeout $TIMEOUT "$BUILD_DIR/sequentialMult" "$matrix_size" 2>&1 | tee -a "$LOG_DIR/extended_${phase_name,,}.log"
        else
            echo "1) Sequential: SKIP (matrix size too large)" | tee -a "$LOG_DIR/extended_${phase_name,,}.log"
        fi
        
        # Parallel tests
        for num_processes in $process_counts; do
            # Kiểm tra nếu số process hợp lý với matrix size
            if [[ "$num_processes" -le "$matrix_size" || "$matrix_size" -ge 128 ]]; then
                for method in $methods; do
                    echo "2) $method: n=$matrix_size p=$num_processes" | tee -a "$LOG_DIR/extended_${phase_name,,}.log"
                    run_test "$matrix_size" "$num_processes" "$method" "${phase_name,,}"
                done
            else
                echo "2) Parallel: SKIP (too many processes for matrix size)" | tee -a "$LOG_DIR/extended_${phase_name,,}.log"
            fi
        done
        
        echo "--- completed n=$matrix_size at $(date) ---" | tee -a "$LOG_DIR/extended_${phase_name,,}.log"
    done
    
    echo "=== $phase_name COMPLETED at $(date) ===" | tee -a "$LOG_DIR/extended_${phase_name,,}.log"
    echo "✅ $phase_name completed successfully!"
}

# Main execution
echo "============================================================================="
echo "🚀 EXTENDED STRASSEN ALGORITHM BENCHMARK"
echo "============================================================================="
echo "Start time: $(date)"
echo "Log directory: $LOG_DIR"
echo "Timeout per test: ${TIMEOUT}s"
echo "Memory limit: $MEMORY_LIMIT"
echo "============================================================================="

# Phase 1: Threshold Testing
run_phase "THRESHOLD" "2 3 5 6 7 9 10 12 15" "1 2 4 8 16" "parallelRowMult parallelElementMult"

# Phase 2: Performance Testing  
run_phase "PERFORMANCE" "24 48 96 192 320 448 576 704 832 960" "8 16 32 64 128 256" "parallelRowMult parallelElementMult"

# Phase 3: Scalability Testing
run_phase "SCALABILITY" "1536 2048 2560 3072 3584 4096" "32 64 128 256 512 768 1024" "parallelRowMult parallelElementMult"

# Phase 4: Limit Testing
run_phase "LIMIT" "5120 6144 7168 8192" "64 128 256 512 768 1024 1500 2000" "parallelRowMult parallelElementMult"

echo ""
echo "============================================================================="
echo "🎉 ALL PHASES COMPLETED!"
echo "End time: $(date)"
echo "Log files:"
ls -la "$LOG_DIR"/extended_*.log
echo "============================================================================="
