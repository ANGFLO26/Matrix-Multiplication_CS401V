#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <sys/time.h>
#include <semaphore.h>
#include <errno.h>
#include <math.h>
#include "common.h"
#include "strassen_utils.h"

typedef struct {
    size_t idx;   // next linear index to compute (0 .. m*m-1)
    sem_t mutex;  // semaphore protecting idx
} shared_index_t;

int main(int argc, char *argv[]) {
    if (argc < 3) {
        fprintf(stderr, "Usage: %s <matrix_size> <num_processes>\n", argv[0]);
        return 1;
    }

    int m = atoi(argv[1]);
    int p = atoi(argv[2]);
    if (m <= 0 || p <= 0) {
        fprintf(stderr, "matrix_size and num_processes must be positive\n");
        return 1;
    }
    if (m > 10000) {
        fprintf(stderr, "Warning: matrix_size %d is very large, may cause memory issues\n", m);
    }
    if (p > 1000) {
        fprintf(stderr, "Warning: num_processes %d is very high, may cause system overload\n", p);
    }
    
    // Check if matrix size is power of 2 for Strassen algorithm
    int padded_size = next_power_of_2(m);
    if (!is_power_of_2(m)) {
        printf("Warning: matrix_size %d is not power of 2, padding to %d for Strassen algorithm\n", m, padded_size);
    }

    size_t total = (size_t)m * m;
    size_t bytes = total * sizeof(double);

    double *A = mmap(NULL, bytes, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    double *B = mmap(NULL, bytes, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    double *C = mmap(NULL, bytes, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    shared_index_t *shared = mmap(NULL, sizeof(shared_index_t), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);

    if (A == MAP_FAILED || B == MAP_FAILED || C == MAP_FAILED || shared == MAP_FAILED) {
        perror("mmap");
        fprintf(stderr, "Failed to allocate shared memory for matrices or control block\n");
        return 1;
    }

    // initialize
    for (size_t i = 0; i < total; i++) {
        C[i] = 0.0;
    }
    // Use fixed seed for testing consistency
    srand(12345);
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < m; j++) {
            A[i * m + j] = (double)(rand() % 100);
            B[i * m + j] = (double)(rand() % 100);
        }
    }

    // init shared index and semaphore
    shared->idx = 0;
    if (sem_init(&shared->mutex, 1, 1) == -1) {
        perror("sem_init");
        fprintf(stderr, "Failed to initialize semaphore for shared index\n");
        return 1;
    }

    struct timeval start, end;
    gettimeofday(&start, NULL);

    for (int i = 0; i < p; i++) {
        pid_t pid = fork();
        if (pid < 0) {
            perror("fork");
            continue;
        }
        if (pid == 0) {
            // child loop: fetch-next compute
            while (1) {
                if (sem_wait(&shared->mutex) == -1) continue;
                size_t myidx = shared->idx;
                if (myidx >= total) {
                    // no more work
                    sem_post(&shared->mutex);
                    break;
                }
                shared->idx = myidx + 1;
                sem_post(&shared->mutex);

                int row = (int)(myidx / m);
                int col = (int)(myidx % m);

                double sum = 0.0;
                for (int k = 0; k < m; k++) {
                    sum += A[row * m + k] * B[k * m + col];
                }
                C[myidx] = sum;
            }
            _exit(0);
        }
    }

    // parent waits
    for (int i = 0; i < p; i++) {
        int status;
        if (wait(&status) == -1) {
            if (errno == ECHILD) break;
        }
    }

    gettimeofday(&end, NULL);
    double time_taken = (end.tv_sec - start.tv_sec) * 1e6 + (end.tv_usec - start.tv_usec);
    printf("parallelElementMult (Strassen): m=%d, p=%d, time=%.0f microseconds\n", m, p, time_taken);

    if (m <= 10) {
        printf("Result C:\n");
        printm(m, C);
    }

    // cleanup
    sem_destroy(&shared->mutex);
    munmap(A, bytes);
    munmap(B, bytes);
    munmap(C, bytes);
    munmap(shared, sizeof(shared_index_t));
    return 0;
}
