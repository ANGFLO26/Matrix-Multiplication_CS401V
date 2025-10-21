#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <math.h>
#include "common.h"
#include "strassen_utils.h"

int main(int argc, char *argv[]) {
    if (argc < 2) {
        fprintf(stderr, "Usage: %s <matrix_size>\n", argv[0]);
        return 1;
    }

    int m = atoi(argv[1]);
    if (m <= 0) {
        fprintf(stderr, "matrix_size must be positive\n");
        return 1;
    }
    if (m > 10000) {
        fprintf(stderr, "Warning: matrix_size %d is very large, may cause memory issues\n", m);
    }
    
    // Check if matrix size is power of 2 for Strassen algorithm
    int padded_size = next_power_of_2(m);
    if (!is_power_of_2(m)) {
        printf("Warning: matrix_size %d is not power of 2, padding to %d for Strassen algorithm\n", m, padded_size);
    }
    size_t n = (size_t)m * m;

    double *A = malloc(n * sizeof(double));
    double *B = malloc(n * sizeof(double));
    double *C = calloc(n, sizeof(double));
    if (!A || !B || !C) {
        perror("malloc");
        return 1;
    }

    // Use fixed seed for testing consistency across implementations
    srand(12345);
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < m; j++) {
            A[i * m + j] = (double)(rand() % 100);
            B[i * m + j] = (double)(rand() % 100);
        }
    }

    struct timeval start, end;
    gettimeofday(&start, NULL);

    // Use Strassen algorithm for matrix multiplication
    if (is_power_of_2(m)) {
        // Direct Strassen multiplication
        strassen_multiply(A, B, C, m);
    } else {
        // Pad matrices to power of 2 and use Strassen
        double *A_padded = pad_matrix(A, m, padded_size);
        double *B_padded = pad_matrix(B, m, padded_size);
        double *C_padded = calloc(padded_size * padded_size, sizeof(double));
        
        strassen_multiply(A_padded, B_padded, C_padded, padded_size);
        
        // Unpad result
        unpad_matrix(C_padded, C, padded_size, m);
        
        free(A_padded); free(B_padded); free(C_padded);
    }

    gettimeofday(&end, NULL);
    double time_taken = (end.tv_sec - start.tv_sec) * 1e6 + (end.tv_usec - start.tv_usec);

    printf("sequentialMult (Strassen): m=%d, time=%.0f microseconds\n", m, time_taken);

    if (m <= 10) {
        printf("Result C:\n");
        printm(m, C);
    }

    free(A); free(B); free(C);
    return 0;
}
