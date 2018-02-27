import pandas as pd
import os as os
import math as math
import matplotlib.pyplot as mpl
import numpy as np
import time
import scipy.optimize as spo


# Define functions


def error(line, data):
    """Compute error between given line model and observed data.

    Parameters
    ----------
    line: tuple/list/array (C0, C1) where C0 is slope and C1 is Y-intercept
    data: 2D array where each row is a point (x, y)

    Returns error as a single real value
    """

    # Metric: Sum of squared Y-axis differences
    err = np.sum((data[:, 1] - (line[0] * data[:, 0] + line[1])) ** 2)
    return err


def error_poly(C, data):
    """Compute error between given polynomial and observed data.

    Parameters
    ----------
    C: numpy.poly1d object or equivalent array representing polynomial coefficients
    data: 2D array where each row is a point (x, y)

    Returns error as a single real value.
    """

    # Metric: Sum of squared Y-axis differences
    err = np.sum((data[:, 1] - np.polyval(C, data[:, 0])) ** 2)
    return err


def fit_line(data, error_func):
    """Fit a line to given data, using a supplied error function.

    Parameters
    ----------
    data: 2D array where each row is a point (X0, Y)
    error_func: function that computes the error between a line and observed data

    Returns line that maximizes the error function
    """

    # Generate initial guess for line model
    l = np.float32([0, data[:, 1].mean()])  # slope = 0, intercept = mean(y_values)

    # Plot initial guess (optional)
    x_ends = np.float32([-5, 5])
    mpl.plot(x_ends, l[0] * x_ends + l[1], 'm--', linewidth=2.0, label='Initial guess')

    # Call optimizer to minimize error function
    result = spo.minimize(error_func, l, args=(data,), method='SLSQP', options={'disp': True})
    return result.x


def fit_poly(data, error_func, degree=3):
    """Fit a polynomial to given data, using supplied error function.

    Parameters
    ----------
    data: 2D array where ecah row is a point (x, y)
    error_func: function that minimizes the error function.
    degree: Degree of polynomial, default is 3

    Returns polynomial that minimizes the error function.
    """

    # Generate initial guess for polynomial model (all coeffs = 1)
    Cguess = np.poly1d(np.ones(degree + 1, dtype=np.float32))

    # Plot initial guess (optional)
    x = np.linspace(-5, 5, 21)
    mpl.plot(x, np.polyval(Cguess, x), 'm--', linewidth=2.0, label="Initial guess")

    # Call optimizer to minimize error function
    result = spo.minimize(error_func, Cguess, args=(data,), method='SLSQP', options={'disp': True})
    return np.poly1d(result.x)


def test_run():
    # Define original line
    l_orig = np.float32([4, 2])
    print("Original line: C0 = {}, C1 = {}".format(l_orig[0], l_orig[1]))
    Xorig = np.linspace(0, 10, 21)
    Yorig = l_orig[0]* Xorig + l_orig[1]
    mpl.plot(Xorig, Yorig, 'b--', linewidth=2.0, label="Original line")

    # Generate noisy data points
    noise_sigma = 3.0
    noise = np.random.normal(0, noise_sigma, Yorig.shape)
    data = np.asarray([Xorig, Yorig + noise]).T
    mpl.plot(data[:, 0], data[:, 1], 'go', label='Data points')

    # Try to fit a line to this data
    l_fit = fit_line(data, error)
    print("Fitted line: C0 = {}, C1 = {}".format(l_fit[0], l_fit[1]))
    mpl.plot(data[:, 0], l_fit[0] * data[:, 0] + l_fit[1], 'r--', linewidth=2.0, label='Fitted Line')
    mpl.show()

    # Try it for polynomial

    # Original poly line
    p_orig = np.poly1d([0.8, 0, -1.5, 4])
    Xorig_p = np.linspace(-5, 5, 21)
    Yorig_p = np.polyval(p_orig, Xorig_p)
    mpl.plot(Xorig_p, Yorig_p, 'b--', linewidth=2.0, label="Original poly")

    # Generate noisy data points
    noise_sigma = 3.0
    noise_p = np.random.normal(0, noise_sigma, Yorig_p.shape)
    data_p = np.asarray([Xorig_p, Yorig_p + noise_p]).T
    mpl.plot(data_p[:, 0], data_p[:, 1], 'go', label='Data points')

    # Try to fit a line to this data
    p_fit = fit_poly(data_p, error_poly, 3)
    mpl.plot(Xorig_p, np.polyval(p_fit, Xorig_p), 'r--', linewidth=2.0, label='Fitted poly')
    mpl.legend(loc='upper left')
    mpl.show()


if __name__ == "__main__":
    test_run()
