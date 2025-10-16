#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include "common.h"

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

    for (int i = 0; i < m; i++) {
        for (int j = 0; j < m; j++) {
            double sum = 0.0;
            for (int k = 0; k < m; k++) {
                sum += A[i * m + k] * B[k * m + j];
            }
            C[i * m + j] = sum;
        }
    }

    gettimeofday(&end, NULL);
    double time_taken = (end.tv_sec - start.tv_sec) * 1e6 + (end.tv_usec - start.tv_usec);

    printf("sequentialMult: m=%d, time=%.0f microseconds\n", m, time_taken);

    if (m <= 10) {
        printf("Result C:\n");
        printm(m, C);
    }

    free(A); free(B); free(C);
    return 0;
}
