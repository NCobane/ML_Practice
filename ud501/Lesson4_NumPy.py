# Load relevant libraries
import pandas as pd
import os as os
import matplotlib.pyplot as mpl
import numpy as np
import time


# Define Functions


def manual_mean(arr):
    sum = 0
    for i in range(0, arr.shape[0]):
        for j in range(0, arr.shape[1]):
            sum = sum + arr[i, j]
    return sum / arr.size


def numpy_mean(arr):
    return arr.mean()


def test_run():
    print(np.array([(2, 3, 4), (5, 6, 7)]))

    # Empty array
    print(np.empty(5))
    print(np.empty((5, 4)))

    # Array of ones
    print(np.ones((5, 4), dtype=np.int))

    # Random Numbers
    print(np.random.random((5, 4)))
    print(np.random.rand(5, 4))
    print(np.random.normal(size=(2, 3)))
    print(np.random.randint(0, 10, size=(2, 3)))

    # Array Attributes
    a = np.random.random((6, 4))
    a.shape[0]  # Number of rows
    a.shape[1]  # Number of columns
    print(a.size)

    # Operations on ndarrays
    print(a.sum(axis=0))  # Sum over columns
    print(a.sum(axis=1))  # Sum over rows
    print(a.min(axis=0))  # Max over columns
    print(a.mean(axis=1))  # Mean over rows
    print(np.argmax(a, axis=0))  # Index of max value

    # Timing operations (incomplete)
    nd1 = np.random.random((1000, 10000))
    t1 = time.time()
    t2 = time.time()
    tot_time = t2-t1
    print("Time: ", tot_time)

    # Accessing Array elements
    element = a[3, 2]
    print(a[0, 1:3])
    # Note: n:m:t slice does range n:m for every t element
    print(a[:, 0:3:2])

if __name__ == "__main__":
    test_run()
