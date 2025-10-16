#!/bin/bash
# Benchmark script for matrix multiplication assignment
# Tests all three implementations with required matrix sizes and process counts

set -e

echo "=== Matrix Multiplication Benchmark ==="
echo "Compiling all programs..."

# Compile all programs
gcc sequentialMult.c -o sequentialMult
gcc parallelRowMult.c -o parallelRowMult -pthread
gcc parallelElementMult.c -o parallelElementMult -pthread

echo "Compilation completed successfully!"
echo ""

# Matrix sizes to test (as required in assignment)
MATRIX_SIZES=(10 100 1000 10000)
# Process counts to test (as required in assignment)  
PROCESS_COUNTS=(10 100 1000)

echo "=== Sequential Implementation ==="
echo "Matrix Size | Time (microseconds)"
echo "------------|-------------------"
for size in "${MATRIX_SIZES[@]}"; do
    if [ $size -le 1000 ]; then
        time_output=$(./sequentialMult $size 2>&1 | grep "time=" | awk '{print $NF}' | sed 's/microseconds//')
        printf "%11d | %s\n" $size "$time_output"
    else
        echo "Skipping size $size (too large for sequential)"
    fi
done

echo ""
echo "=== Parallel Row Implementation ==="
echo "Matrix Size | Processes | Time (microseconds)"
echo "------------|-----------|-------------------"
for size in "${MATRIX_SIZES[@]}"; do
    for procs in "${PROCESS_COUNTS[@]}"; do
        if [ $size -le 1000 ] && [ $procs -le 100 ]; then
            time_output=$(./parallelRowMult $size $procs 2>&1 | grep "time=" | awk '{print $NF}' | sed 's/microseconds//')
            printf "%11d | %9d | %s\n" $size $procs "$time_output"
        else
            echo "Skipping size $size with $procs processes (too large)"
        fi
    done
done

echo ""
echo "=== Parallel Element Implementation ==="
echo "Matrix Size | Processes | Time (microseconds)"
echo "------------|-----------|-------------------"
for size in "${MATRIX_SIZES[@]}"; do
    for procs in "${PROCESS_COUNTS[@]}"; do
        if [ $size -le 1000 ] && [ $procs -le 100 ]; then
            time_output=$(./parallelElementMult $size $procs 2>&1 | grep "time=" | awk '{print $NF}' | sed 's/microseconds//')
            printf "%11d | %9d | %s\n" $size $procs "$time_output"
        else
            echo "Skipping size $size with $procs processes (too large)"
        fi
    done
done

echo ""
echo "=== Benchmark completed ==="
echo "Note: Large matrix sizes (10000+) and high process counts (1000+) are skipped"
echo "to prevent system overload. Adjust limits in script if needed."
