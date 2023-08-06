import numpy as np

def GLV(t, x, A, r, tol):
    return (x*(r + A@x)).T

def single_extinction(t, n, A, r, tol):
    n = n[n!=0]
    return np.any(abs(n) < tol) -1

