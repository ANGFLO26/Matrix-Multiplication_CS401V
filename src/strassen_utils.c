#include "strassen_utils.h"

// Matrix addition: C = A + B
void matrix_add(double *A, double *B, double *C, int n) {
    for (int i = 0; i < n * n; i++) {
        C[i] = A[i] + B[i];
    }
}

// Matrix subtraction: C = A - B
void matrix_sub(double *A, double *B, double *C, int n) {
    for (int i = 0; i < n * n; i++) {
        C[i] = A[i] - B[i];
    }
}

// Get submatrix from parent matrix
void get_submatrix(double *parent, double *sub, int parent_size, int sub_size, int start_row, int start_col) {
    for (int i = 0; i < sub_size; i++) {
        for (int j = 0; j < sub_size; j++) {
            sub[i * sub_size + j] = parent[(start_row + i) * parent_size + (start_col + j)];
        }
    }
}

// Set submatrix to parent matrix
void set_submatrix(double *parent, double *sub, int parent_size, int sub_size, int start_row, int start_col) {
    for (int i = 0; i < sub_size; i++) {
        for (int j = 0; j < sub_size; j++) {
            parent[(start_row + i) * parent_size + (start_col + j)] = sub[i * sub_size + j];
        }
    }
}

// Naive matrix multiplication for small matrices (fallback)
void naive_multiply(double *A, double *B, double *C, int n) {
    for (int i = 0; i < n; i++) {
        for (int j = 0; j < n; j++) {
            double sum = 0.0;
            for (int k = 0; k < n; k++) {
                sum += A[i * n + k] * B[k * n + j];
            }
            C[i * n + j] = sum;
        }
    }
}

// Strassen matrix multiplication: C = A * B
void strassen_multiply(double *A, double *B, double *C, int n) {
    // Base case: use naive multiplication for small matrices
    if (n <= 64) {
        naive_multiply(A, B, C, n);
        return;
    }
    
    int half = n / 2;
    int size = half * half;
    
    // Allocate submatrices
    double *A11 = malloc(size * sizeof(double));
    double *A12 = malloc(size * sizeof(double));
    double *A21 = malloc(size * sizeof(double));
    double *A22 = malloc(size * sizeof(double));
    
    double *B11 = malloc(size * sizeof(double));
    double *B12 = malloc(size * sizeof(double));
    double *B21 = malloc(size * sizeof(double));
    double *B22 = malloc(size * sizeof(double));
    
    double *C11 = malloc(size * sizeof(double));
    double *C12 = malloc(size * sizeof(double));
    double *C21 = malloc(size * sizeof(double));
    double *C22 = malloc(size * sizeof(double));
    
    // Extract submatrices
    get_submatrix(A, A11, n, half, 0, 0);
    get_submatrix(A, A12, n, half, 0, half);
    get_submatrix(A, A21, n, half, half, 0);
    get_submatrix(A, A22, n, half, half, half);
    
    get_submatrix(B, B11, n, half, 0, 0);
    get_submatrix(B, B12, n, half, 0, half);
    get_submatrix(B, B21, n, half, half, 0);
    get_submatrix(B, B22, n, half, half, half);
    
    // Allocate temporary matrices for Strassen's algorithm
    double *temp1 = malloc(size * sizeof(double));
    double *temp2 = malloc(size * sizeof(double));
    double *P1 = malloc(size * sizeof(double));
    double *P2 = malloc(size * sizeof(double));
    double *P3 = malloc(size * sizeof(double));
    double *P4 = malloc(size * sizeof(double));
    double *P5 = malloc(size * sizeof(double));
    double *P6 = malloc(size * sizeof(double));
    double *P7 = malloc(size * sizeof(double));
    
    // Strassen's 7 multiplications
    // P1 = A11 * (B12 - B22)
    matrix_sub(B12, B22, temp1, half);
    strassen_multiply(A11, temp1, P1, half);
    
    // P2 = (A11 + A12) * B22
    matrix_add(A11, A12, temp1, half);
    strassen_multiply(temp1, B22, P2, half);
    
    // P3 = (A21 + A22) * B11
    matrix_add(A21, A22, temp1, half);
    strassen_multiply(temp1, B11, P3, half);
    
    // P4 = A22 * (B21 - B11)
    matrix_sub(B21, B11, temp1, half);
    strassen_multiply(A22, temp1, P4, half);
    
    // P5 = (A11 + A22) * (B11 + B22)
    matrix_add(A11, A22, temp1, half);
    matrix_add(B11, B22, temp2, half);
    strassen_multiply(temp1, temp2, P5, half);
    
    // P6 = (A12 - A22) * (B21 + B22)
    matrix_sub(A12, A22, temp1, half);
    matrix_add(B21, B22, temp2, half);
    strassen_multiply(temp1, temp2, P6, half);
    
    // P7 = (A11 - A21) * (B11 + B12)
    matrix_sub(A11, A21, temp1, half);
    matrix_add(B11, B12, temp2, half);
    strassen_multiply(temp1, temp2, P7, half);
    
    // Calculate result submatrices
    // C11 = P5 + P4 - P2 + P6
    matrix_add(P5, P4, temp1, half);
    matrix_sub(temp1, P2, temp2, half);
    matrix_add(temp2, P6, C11, half);
    
    // C12 = P1 + P2
    matrix_add(P1, P2, C12, half);
    
    // C21 = P3 + P4
    matrix_add(P3, P4, C21, half);
    
    // C22 = P5 + P1 - P3 - P7
    matrix_add(P5, P1, temp1, half);
    matrix_sub(temp1, P3, temp2, half);
    matrix_sub(temp2, P7, C22, half);
    
    // Combine result submatrices
    set_submatrix(C, C11, n, half, 0, 0);
    set_submatrix(C, C12, n, half, 0, half);
    set_submatrix(C, C21, n, half, half, 0);
    set_submatrix(C, C22, n, half, half, half);
    
    // Free all allocated memory
    free(A11); free(A12); free(A21); free(A22);
    free(B11); free(B12); free(B21); free(B22);
    free(C11); free(C12); free(C21); free(C22);
    free(temp1); free(temp2);
    free(P1); free(P2); free(P3); free(P4); free(P5); free(P6); free(P7);
}

// Pad matrix to power of 2 size
double* pad_matrix(double *matrix, int original_size, int padded_size) {
    double *padded = calloc(padded_size * padded_size, sizeof(double));
    for (int i = 0; i < original_size; i++) {
        for (int j = 0; j < original_size; j++) {
            padded[i * padded_size + j] = matrix[i * original_size + j];
        }
    }
    return padded;
}

// Unpad matrix from power of 2 size
void unpad_matrix(double *padded_matrix, double *result, int padded_size, int original_size) {
    for (int i = 0; i < original_size; i++) {
        for (int j = 0; j < original_size; j++) {
            result[i * original_size + j] = padded_matrix[i * padded_size + j];
        }
    }
}
