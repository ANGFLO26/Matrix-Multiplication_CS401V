# Makefile for Matrix Multiplication Parallel Computing
# CS401V - Distributed Systems Assignment 1
# Group: Phan Văn Tài (2202081) & Hà Minh Chiến (2202095)

# Compiler and flags
CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -O2
PTHREAD_FLAGS = -pthread
MATH_FLAGS = -lm

# Directories
SRC_DIR = src
COMPILED_DIR = compiled
SCRIPTS_DIR = tools

# Source files
SEQUENTIAL_SRC = $(SRC_DIR)/sequentialMult.c
PARALLEL_ROW_SRC = $(SRC_DIR)/parallelRowMult.c
PARALLEL_ELEMENT_SRC = $(SRC_DIR)/parallelElementMult.c
COMMON_HEADER = $(SRC_DIR)/common.h
STRASSEN_UTILS_SRC = $(SRC_DIR)/strassen_utils.c
STRASSEN_UTILS_HEADER = $(SRC_DIR)/strassen_utils.h

# Executable targets
SEQUENTIAL_EXE = $(COMPILED_DIR)/sequentialMult
PARALLEL_ROW_EXE = $(COMPILED_DIR)/parallelRowMult
PARALLEL_ELEMENT_EXE = $(COMPILED_DIR)/parallelElementMult

# Default target
all: $(SEQUENTIAL_EXE) $(PARALLEL_ROW_EXE) $(PARALLEL_ELEMENT_EXE)

# Sequential implementation with Strassen
$(SEQUENTIAL_EXE): $(SEQUENTIAL_SRC) $(COMMON_HEADER) $(STRASSEN_UTILS_HEADER) $(STRASSEN_UTILS_SRC)
	@echo "Compiling sequential implementation with Strassen algorithm..."
	$(CC) $(CFLAGS) -o $@ $(SEQUENTIAL_SRC) $(STRASSEN_UTILS_SRC) $(MATH_FLAGS)

# Parallel row implementation with Strassen
$(PARALLEL_ROW_EXE): $(PARALLEL_ROW_SRC) $(COMMON_HEADER) $(STRASSEN_UTILS_HEADER) $(STRASSEN_UTILS_SRC)
	@echo "Compiling parallel row implementation with Strassen algorithm..."
	$(CC) $(CFLAGS) $(PTHREAD_FLAGS) -o $@ $(PARALLEL_ROW_SRC) $(STRASSEN_UTILS_SRC) $(MATH_FLAGS)

# Parallel element implementation with Strassen
$(PARALLEL_ELEMENT_EXE): $(PARALLEL_ELEMENT_SRC) $(COMMON_HEADER) $(STRASSEN_UTILS_HEADER) $(STRASSEN_UTILS_SRC)
	@echo "Compiling parallel element implementation with Strassen algorithm..."
	$(CC) $(CFLAGS) $(PTHREAD_FLAGS) -o $@ $(PARALLEL_ELEMENT_SRC) $(STRASSEN_UTILS_SRC) $(MATH_FLAGS)

# Create directories
$(COMPILED_DIR):
	mkdir -p $(COMPILED_DIR)

$(SCRIPTS_DIR):
	mkdir -p $(SCRIPTS_DIR)

# Organize scripts (scripts already in tools/ directory)
organize-scripts: $(SCRIPTS_DIR)
	@echo "Scripts are already organized in tools/ directory"

# Quick test
test: all
	@echo "Running quick performance test..."
	./$(SCRIPTS_DIR)/quick_test.sh

# Full benchmark
benchmark: all
	@echo "Running full benchmark..."
	./$(SCRIPTS_DIR)/benchmark_report.sh

# Clean compiled files
clean:
	@echo "Cleaning compiled files..."
	rm -f $(COMPILED_DIR)/*
	rm -f *.o

# Clean all generated files
distclean: clean
	@echo "Cleaning all generated files..."
	rm -rf $(COMPILED_DIR)
	rm -rf $(SCRIPTS_DIR)
	rm -f *.txt
	rm -f *.log

# Install dependencies (Ubuntu/Debian)
install-deps:
	@echo "Installing dependencies..."
	sudo apt update
	sudo apt install build-essential gcc make

# Show help
help:
	@echo "Available targets:"
	@echo "  all        - Compile all programs (default)"
	@echo "  test       - Run quick performance test"
	@echo "  benchmark  - Run full benchmark"
	@echo "  organize-scripts - Check scripts organization"
	@echo "  clean      - Remove compiled files"
	@echo "  distclean  - Remove all generated files"
	@echo "  install-deps - Install system dependencies"
	@echo "  help       - Show this help message"

# Phony targets
.PHONY: all test benchmark organize-scripts clean distclean install-deps help
