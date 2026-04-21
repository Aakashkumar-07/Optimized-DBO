"""
Standard Benchmark Functions for Metaheuristic Evaluation
==========================================================
Functions included:
  F1  – Sphere            (unimodal)
  F2  – Schwefel 2.22     (unimodal)
  F3  – Rosenbrock (Banana)(unimodal with narrow curved valley)
  F4  – Rastrigin         (highly multimodal)
  F5  – Ackley            (multimodal, near-flat surface)
  F6  – Griewank          (multimodal)
  F7  – Levy              (multimodal)
  F8  – Zakharov          (unimodal)
  F9  – Schwefel          (multimodal)

Each entry: (name, func, lb, ub, dim, global_optimum)
"""

import numpy as np


# --------------------------------------------------------------------------- #
#  Individual functions
# --------------------------------------------------------------------------- #

def sphere(x: np.ndarray) -> float:
    return float(np.sum(x ** 2))


def schwefel_2_22(x: np.ndarray) -> float:
    return float(np.sum(np.abs(x)) + np.prod(np.abs(x)))


def rosenbrock(x: np.ndarray) -> float:
    xi = x[:-1]
    xi1 = x[1:]
    return float(np.sum(100.0 * (xi1 - xi**2)**2 + (xi - 1)**2))


def rastrigin(x: np.ndarray) -> float:
    n = len(x)
    return float(10 * n + np.sum(x**2 - 10 * np.cos(2 * np.pi * x)))


def ackley(x: np.ndarray) -> float:
    n = len(x)
    a, b, c = 20.0, 0.2, 2 * np.pi
    sum1 = np.sum(x**2)
    sum2 = np.sum(np.cos(c * x))
    return float(-a * np.exp(-b * np.sqrt(sum1 / n))
                 - np.exp(sum2 / n)
                 + a + np.e)


def griewank(x: np.ndarray) -> float:
    n = len(x)
    idx = np.arange(1, n + 1)
    return float(np.sum(x**2) / 4000
                 - np.prod(np.cos(x / np.sqrt(idx)))
                 + 1)


def levy(x: np.ndarray) -> float:
    n = len(x)
    w = 1 + (x - 1) / 4
    term1 = np.sin(np.pi * w[0]) ** 2
    term2 = np.sum((w[:-1] - 1)**2 * (1 + 10 * np.sin(np.pi * w[:-1] + 1)**2))
    term3 = (w[-1] - 1)**2 * (1 + np.sin(2 * np.pi * w[-1])**2)
    return float(term1 + term2 + term3)


def zakharov(x: np.ndarray) -> float:
    n = len(x)
    idx = np.arange(1, n + 1)
    s2 = np.sum(0.5 * idx * x)
    return float(np.sum(x**2) + s2**2 + s2**4)


def schwefel(x: np.ndarray) -> float:
    n = len(x)
    return float(418.9829 * n - np.sum(x * np.sin(np.abs(x) ** 0.5)))


# --------------------------------------------------------------------------- #
#  Registry
# --------------------------------------------------------------------------- #

BENCHMARKS = [
    {
        "id"      : "F1",
        "name"    : "Sphere",
        "func"    : sphere,
        "lb"      : -100,
        "ub"      : 100,
        "optimum" : 0.0,
        "type"    : "Unimodal",
    },
    {
        "id"      : "F2",
        "name"    : "Schwefel 2.22",
        "func"    : schwefel_2_22,
        "lb"      : -10,
        "ub"      : 10,
        "optimum" : 0.0,
        "type"    : "Unimodal",
    },
    {
        "id"      : "F3",
        "name"    : "Rosenbrock",
        "func"    : rosenbrock,
        "lb"      : -30,
        "ub"      : 30,
        "optimum" : 0.0,
        "type"    : "Unimodal (narrow valley)",
    },
    {
        "id"      : "F4",
        "name"    : "Rastrigin",
        "func"    : rastrigin,
        "lb"      : -5.12,
        "ub"      : 5.12,
        "optimum" : 0.0,
        "type"    : "Multimodal",
    },
    {
        "id"      : "F5",
        "name"    : "Ackley",
        "func"    : ackley,
        "lb"      : -32,
        "ub"      : 32,
        "optimum" : 0.0,
        "type"    : "Multimodal",
    },
    {
        "id"      : "F6",
        "name"    : "Griewank",
        "func"    : griewank,
        "lb"      : -600,
        "ub"      : 600,
        "optimum" : 0.0,
        "type"    : "Multimodal",
    },
    {
        "id"      : "F7",
        "name"    : "Levy",
        "func"    : levy,
        "lb"      : -10,
        "ub"      : 10,
        "optimum" : 0.0,
        "type"    : "Multimodal",
    },
    {
        "id"      : "F8",
        "name"    : "Zakharov",
        "func"    : zakharov,
        "lb"      : -5,
        "ub"      : 10,
        "optimum" : 0.0,
        "type"    : "Unimodal",
    },
    {
        "id"      : "F9",
        "name"    : "Schwefel",
        "func"    : schwefel,
        "lb"      : -500,
        "ub"      : 500,
        "optimum" : 0.0,
        "type"    : "Multimodal",
    },
]
