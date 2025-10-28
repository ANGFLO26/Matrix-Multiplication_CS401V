#!/bin/bash
# Quick test script for Strassen Algorithm matrix multiplication performance

echo "=========================================="
echo "QUICK PERFORMANCE TEST"
echo "=========================================="
echo "Date: $(date)"
echo ""

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BUILD_DIR="$ROOT_DIR/compiled"
if [ ! -f "$BUILD_DIR/sequentialMult" ] || [ ! -f "$BUILD_DIR/parallelRowMult" ] || [ ! -f "$BUILD_DIR/parallelElementMult" ]; then
    echo "Compiling programs..."
    make -C "$ROOT_DIR" clean >/dev/null 2>&1 || true
    make -C "$ROOT_DIR" >/dev/null
    echo "Compilation completed at $BUILD_DIR!"
    echo ""
fi

# Test function
run_test() {
    local size=$1
    local procs=$2
    echo "Matrix Size: $size"
    echo "Sequential: $($BUILD_DIR/sequentialMult $size 2>&1 | grep 'time=' | awk '{print $NF}')"
    echo "Parallel Row ($procs procs): $($BUILD_DIR/parallelRowMult $size $procs 2>&1 | grep 'time=' | awk '{print $NF}')"
    echo "Parallel Element ($procs procs): $($BUILD_DIR/parallelElementMult $size $procs 2>&1 | grep 'time=' | awk '{print $NF}')"
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
echo "Sequential: $($BUILD_DIR/sequentialMult 1000 2>&1 | grep 'time=' | awk '{print $NF}')"
echo "Parallel Row (100 procs): $($BUILD_DIR/parallelRowMult 1000 100 2>&1 | grep 'time=' | awk '{print $NF}')"
echo "Parallel Element (100 procs): $($BUILD_DIR/parallelElementMult 1000 100 2>&1 | grep 'time=' | awk '{print $NF}')"

echo ""
echo "=========================================="
echo "TEST COMPLETED"
echo "=========================================="
