#define _GNU_SOURCE
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/mman.h>
#include <sys/wait.h>
#include <sys/time.h>
#include <semaphore.h>
#include <errno.h>
#include "common.h"

typedef struct {
    int l;        // next row index to compute (0 .. m-1)
    sem_t mutex;  // semaphore protecting l
} shared_row_t;

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

    size_t n = (size_t)m * m;
    size_t bytes = n * sizeof(double);

    double *A = mmap(NULL, bytes, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    double *B = mmap(NULL, bytes, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    double *C = mmap(NULL, bytes, PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);
    shared_row_t *shared = mmap(NULL, sizeof(shared_row_t), PROT_READ | PROT_WRITE, MAP_SHARED | MAP_ANONYMOUS, -1, 0);

    if (A == MAP_FAILED || B == MAP_FAILED || C == MAP_FAILED || shared == MAP_FAILED) {
        perror("mmap");
        fprintf(stderr, "Failed to allocate shared memory for matrices or control block\n");
        return 1;
    }

    // initialize C to zeros
    for (size_t i = 0; i < n; i++) C[i] = 0.0;

    // Use fixed seed for testing consistency
    srand(12345);
    for (int i = 0; i < m; i++) {
        for (int j = 0; j < m; j++) {
            A[i * m + j] = (double)(rand() % 100);
            B[i * m + j] = (double)(rand() % 100);
        }
    }

    // initialize shared row index and semaphore
    shared->l = 0;
    if (sem_init(&shared->mutex, 1, 1) == -1) {
        perror("sem_init");
        fprintf(stderr, "Failed to initialize semaphore for shared row index\n");
        return 1;
    }

    struct timeval start, end;
    gettimeofday(&start, NULL);

    for (int proc = 0; proc < p; proc++) {
        pid_t pid = fork();
        if (pid < 0) {
            perror("fork");
            fprintf(stderr, "Failed to create process %d\n", proc);
            // continue creating others or exit
            continue;
        }
        if (pid == 0) {
            // child: work-stealing approach with shared row index
            while (1) {
                if (sem_wait(&shared->mutex) == -1) continue;
                int my_row = shared->l;
                if (my_row >= m) {
                    // no more work
                    sem_post(&shared->mutex);
                    break;
                }
                shared->l = my_row + 1;
                sem_post(&shared->mutex);

                // compute row my_row
                for (int j = 0; j < m; j++) {
                    double sum = 0.0;
                    for (int k = 0; k < m; k++) {
                        sum += A[my_row * m + k] * B[k * m + j];
                    }
                    C[my_row * m + j] = sum;
                }
            }
            _exit(0);
        }
        // parent continues to spawn
    }

    // parent waits for children
    for (int i = 0; i < p; i++) {
        int status;
        if (wait(&status) == -1) {
            if (errno == ECHILD) break;
        }
    }

    gettimeofday(&end, NULL);
    double time_taken = (end.tv_sec - start.tv_sec) * 1e6 + (end.tv_usec - start.tv_usec);
    printf("parallelRowMult: m=%d, p=%d, time=%.0f microseconds\n", m, p, time_taken);

    if (m <= 10) {
        printf("Result C:\n");
        printm(m, C);
    }

    // cleanup
    sem_destroy(&shared->mutex);
    munmap(A, bytes);
    munmap(B, bytes);
    munmap(C, bytes);
    munmap(shared, sizeof(shared_row_t));
    return 0;
}
