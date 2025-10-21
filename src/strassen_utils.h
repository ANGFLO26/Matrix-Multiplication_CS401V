#ifndef STRASSEN_UTILS_H
#define STRASSEN_UTILS_H

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>

// Check if n is a power of 2
static inline int is_power_of_2(int n) {
    return n > 0 && (n & (n - 1)) == 0;
}

// Get next power of 2
static inline int next_power_of_2(int n) {
    if (n <= 0) return 1;
    if (is_power_of_2(n)) return n;
    return 1 << (int)ceil(log2(n));
}

// Matrix addition: C = A + B
void matrix_add(double *A, double *B, double *C, int n);

// Matrix subtraction: C = A - B  
void matrix_sub(double *A, double *B, double *C, int n);

// Get submatrix from parent matrix
void get_submatrix(double *parent, double *sub, int parent_size, int sub_size, int start_row, int start_col);

// Set submatrix to parent matrix
void set_submatrix(double *parent, double *sub, int parent_size, int sub_size, int start_row, int start_col);

// Strassen matrix multiplication: C = A * B
void strassen_multiply(double *A, double *B, double *C, int n);

// Naive matrix multiplication for small matrices (fallback)
void naive_multiply(double *A, double *B, double *C, int n);

// Pad matrix to power of 2 size
double* pad_matrix(double *matrix, int original_size, int padded_size);

// Unpad matrix from power of 2 size
void unpad_matrix(double *padded_matrix, double *result, int padded_size, int original_size);

#endif
