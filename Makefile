# Makefile for Matrix Multiplication Parallel Computing
# CS401V - Distributed Systems Assignment 1
# Group: Phan Văn Tài (2202081) & Hà Minh Chiến (2202095)

# Compiler and flags
CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -O2
PTHREAD_FLAGS = -pthread

# Directories
SRC_DIR = src
COMPILED_DIR = compiled
SCRIPTS_DIR = scripts

# Source files
SEQUENTIAL_SRC = $(SRC_DIR)/sequentialMult.c
PARALLEL_ROW_SRC = $(SRC_DIR)/parallelRowMult.c
PARALLEL_ELEMENT_SRC = $(SRC_DIR)/parallelElementMult.c
COMMON_HEADER = $(SRC_DIR)/common.h

# Executable targets
SEQUENTIAL_EXE = $(COMPILED_DIR)/sequentialMult
PARALLEL_ROW_EXE = $(COMPILED_DIR)/parallelRowMult
PARALLEL_ELEMENT_EXE = $(COMPILED_DIR)/parallelElementMult

# Default target
all: $(SEQUENTIAL_EXE) $(PARALLEL_ROW_EXE) $(PARALLEL_ELEMENT_EXE)

# Sequential implementation
$(SEQUENTIAL_EXE): $(SEQUENTIAL_SRC) $(COMMON_HEADER)
	@echo "Compiling sequential implementation..."
	$(CC) $(CFLAGS) -o $@ $<

# Parallel row implementation
$(PARALLEL_ROW_EXE): $(PARALLEL_ROW_SRC) $(COMMON_HEADER)
	@echo "Compiling parallel row implementation..."
	$(CC) $(CFLAGS) $(PTHREAD_FLAGS) -o $@ $<

# Parallel element implementation
$(PARALLEL_ELEMENT_EXE): $(PARALLEL_ELEMENT_SRC) $(COMMON_HEADER)
	@echo "Compiling parallel element implementation..."
	$(CC) $(CFLAGS) $(PTHREAD_FLAGS) -o $@ $<

# Create directories
$(COMPILED_DIR):
	mkdir -p $(COMPILED_DIR)

$(SCRIPTS_DIR):
	mkdir -p $(SCRIPTS_DIR)

# Organize scripts (scripts already in scripts/ directory)
organize-scripts: $(SCRIPTS_DIR)
	@echo "Scripts are already organized in scripts/ directory"

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
