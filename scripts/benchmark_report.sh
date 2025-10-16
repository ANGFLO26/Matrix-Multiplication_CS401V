#!/bin/bash
# Comprehensive benchmark script for matrix multiplication report
# Tests: matrix_size = 10, 100, 1000
# Tests: num_processes = 10, 100, 1000

set -e

echo "=========================================="
echo "MATRIX MULTIPLICATION PERFORMANCE REPORT"
echo "=========================================="
echo "Date: $(date)"
echo "System: $(uname -a)"
echo "CPU Cores: $(nproc)"
echo ""

# Compile all programs
echo "Compiling programs..."
gcc sequentialMult.c -o sequentialMult
gcc parallelRowMult.c -o parallelRowMult -pthread
gcc parallelElementMult.c -o parallelElementMult -pthread
echo "Compilation completed!"
echo ""

# Matrix sizes to test
MATRIX_SIZES=(10 100 1000)
# Process counts to test
PROCESS_COUNTS=(10 100 1000)

# Create results file
RESULTS_FILE="benchmark_results.txt"
echo "Matrix Size | Method | Processes | Time (microseconds)" > $RESULTS_FILE
echo "------------|--------|-----------|-------------------" >> $RESULTS_FILE

echo "=== SEQUENTIAL IMPLEMENTATION ==="
echo "Matrix Size | Time (microseconds)"
echo "------------|-------------------"

for size in "${MATRIX_SIZES[@]}"; do
    echo "Testing sequential with matrix size: $size"
    time_output=$(./sequentialMult $size 2>&1 | grep "time=" | awk '{print $NF}' | sed 's/microseconds//')
    printf "%11d | %s\n" $size "$time_output"
    echo "$size | Sequential | 1 | $time_output" >> $RESULTS_FILE
done

echo ""
echo "=== PARALLEL ROW IMPLEMENTATION ==="
echo "Matrix Size | Processes | Time (microseconds)"
echo "------------|-----------|-------------------"

for size in "${MATRIX_SIZES[@]}"; do
    for procs in "${PROCESS_COUNTS[@]}"; do
        echo "Testing parallel row with matrix size: $size, processes: $procs"
        time_output=$(./parallelRowMult $size $procs 2>&1 | grep "time=" | awk '{print $NF}' | sed 's/microseconds//')
        printf "%11d | %9d | %s\n" $size $procs "$time_output"
        echo "$size | ParallelRow | $procs | $time_output" >> $RESULTS_FILE
    done
done

echo ""
echo "=== PARALLEL ELEMENT IMPLEMENTATION ==="
echo "Matrix Size | Processes | Time (microseconds)"
echo "------------|-----------|-------------------"

for size in "${MATRIX_SIZES[@]}"; do
    for procs in "${PROCESS_COUNTS[@]}"; do
        echo "Testing parallel element with matrix size: $size, processes: $procs"
        time_output=$(./parallelElementMult $size $procs 2>&1 | grep "time=" | awk '{print $NF}' | sed 's/microseconds//')
        printf "%11d | %9d | %s\n" $size $procs "$time_output"
        echo "$size | ParallelElement | $procs | $time_output" >> $RESULTS_FILE
    done
done

echo ""
echo "=== BENCHMARK COMPLETED ==="
echo "Results saved to: $RESULTS_FILE"
echo "=========================================="
