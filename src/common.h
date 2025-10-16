#ifndef COMMON_H
#define COMMON_H

#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <unistd.h>

static inline void populate(int size, double *A, double *B) {
    srand((unsigned)time(NULL) ^ (unsigned)getpid());
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++) {
            A[i * size + j] = (double)(rand() % 100);
            B[i * size + j] = (double)(rand() % 100);
        }
    }
}

static inline void printm(int size, double *M) {
    for (int i = 0; i < size; i++) {
        for (int j = 0; j < size; j++)
            printf("%6.1f ", M[i * size + j]);
        printf("\n");
    }
}

#endif // COMMON_H
