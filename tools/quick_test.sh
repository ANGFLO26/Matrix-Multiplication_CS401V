#!/bin/bash
# Quick test script for Strassen Algorithm matrix multiplication performance

echo "=========================================="
echo "QUICK PERFORMANCE TEST"
echo "=========================================="
echo "Date: $(date)"
echo ""

# Compile if needed
if [ ! -f "sequentialMult" ] || [ ! -f "parallelRowMult" ] || [ ! -f "parallelElementMult" ]; then
    echo "Compiling programs..."
    gcc sequentialMult.c -o sequentialMult
    gcc parallelRowMult.c -o parallelRowMult -pthread
    gcc parallelElementMult.c -o parallelElementMult -pthread
    echo "Compilation completed!"
    echo ""
fi

# Test function
run_test() {
    local size=$1
    local procs=$2
    echo "Matrix Size: $size"
    echo "Sequential: $(./sequentialMult $size 2>&1 | grep 'time=' | awk '{print $NF}')"
    echo "Parallel Row ($procs procs): $(./parallelRowMult $size $procs 2>&1 | grep 'time=' | awk '{print $NF}')"
    echo "Parallel Element ($procs procs): $(./parallelElementMult $size $procs 2>&1 | grep 'time=' | awk '{print $NF}')"
    echo ""
}

# Run tests
echo "=== Test 1: Small Matrix (10x10) ==="
run_test 10 10

echo "=== Test 2: Medium Matrix (100x100) ==="
run_test 100 10

echo "=== Test 3: Large Matrix (1000x1000) ==="
run_test 1000 10

echo "=== Test 4: Large Matrix with More Processes (1000x1000, 100 procs) ==="
echo "Matrix Size: 1000"
echo "Sequential: $(./sequentialMult 1000 2>&1 | grep 'time=' | awk '{print $NF}')"
echo "Parallel Row (100 procs): $(./parallelRowMult 1000 100 2>&1 | grep 'time=' | awk '{print $NF}')"
echo "Parallel Element (100 procs): $(./parallelElementMult 1000 100 2>&1 | grep 'time=' | awk '{print $NF}')"

echo ""
echo "=========================================="
echo "TEST COMPLETED"
echo "=========================================="
