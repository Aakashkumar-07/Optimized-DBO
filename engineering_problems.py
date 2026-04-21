# engineering_problems.py – standard constrained engineering benchmarks
# Objective + constraints with death-penalty approach (large penalty for violations)
# Definitions follow Coello Coello, Kannan & Kramer, Belegundu, Golinski

import numpy as np
from mealpy import FloatVar
from config import PENALTY_COEFF


def _penalize(f, violations):
    """Add penalty for constraint violations."""
    penalty = PENALTY_COEFF * sum(max(0, g)**2 for g in violations)
    return f + penalty


# ============================================================
# 1. Welded Beam Design
#    Variables: x = [h, l, t, b]
#    Minimize: fabrication cost
#    Subject to: 7 inequality constraints
# ============================================================

def welded_beam_obj(x):
    h, l, t, b = x[0], x[1], x[2], x[3]
    # objective: cost
    f = 1.10471 * h**2 * l + 0.04811 * t * b * (14.0 + l)

    # intermediate calculations
    P = 6000.0; L = 14.0; E = 30e6; G = 12e6
    delta_max = 0.25; sigma_max = 30000.0; tau_max = 13600.0

    M = P * (L + l/2)
    R = np.sqrt(l**2/4 + ((t + h)/2)**2)
    J = 2 * (np.sqrt(2) * h * l * (l**2/12 + ((t + h)/2)**2))

    tau1 = P / (np.sqrt(2) * h * l)
    tau2 = M * R / J
    tau = np.sqrt(tau1**2 + 2*tau1*tau2*(l/(2*R)) + tau2**2)

    sigma = 6*P*L / (b * t**2)
    delta = 4*P*L**3 / (E * t**3 * b)
    Pc = (4.013 * E * np.sqrt(t**2 * b**6 / 36)) / (L**2) * (1 - t/(2*L) * np.sqrt(E/(4*G)))

    g1 = tau - tau_max
    g2 = sigma - sigma_max
    g3 = h - b
    g4 = 0.10471*h**2 + 0.04811*t*b*(14 + l) - 5.0
    g5 = 0.125 - h
    g6 = delta - delta_max
    g7 = P - Pc

    return _penalize(f, [g1, g2, g3, g4, g5, g6, g7])

WELDED_BEAM = {
    "name": "Welded Beam Design",
    "obj_func": welded_beam_obj,
    "bounds": FloatVar(lb=[0.1, 0.1, 0.1, 0.1], ub=[2.0, 10.0, 10.0, 2.0]),
    "minmax": "min",
}


# ============================================================
# 2. Pressure Vessel Design
#    Variables: x = [Ts, Th, R, L]
#    Minimize: total cost
#    Subject to: 4 inequality constraints
# ============================================================

def pressure_vessel_obj(x):
    x1, x2, x3, x4 = x[0], x[1], x[2], x[3]
    f = (0.6224*x1*x3*x4 + 1.7781*x2*x3**2 +
         3.1661*x1**2*x4 + 19.84*x1**2*x3)

    g1 = -x1 + 0.0193*x3
    g2 = -x2 + 0.00954*x3
    g3 = -np.pi*x3**2*x4 - (4/3)*np.pi*x3**3 + 1296000
    g4 = x4 - 240

    return _penalize(f, [g1, g2, g3, g4])

PRESSURE_VESSEL = {
    "name": "Pressure Vessel Design",
    "obj_func": pressure_vessel_obj,
    "bounds": FloatVar(lb=[0.0625, 0.0625, 10.0, 10.0],
                       ub=[6.1875, 6.1875, 200.0, 200.0]),
    "minmax": "min",
}


# ============================================================
# 3. Tension/Compression Spring Design
#    Variables: x = [d, D, N] (wire diameter, coil diameter, number of coils)
#    Minimize: weight
#    Subject to: 4 inequality constraints
# ============================================================

def spring_obj(x):
    d, D, N = x[0], x[1], x[2]
    f = (N + 2) * D * d**2

    g1 = 1 - D**3 * N / (71785 * d**4)
    g2 = (4*D**2 - d*D) / (12566*(D*d**3 - d**4)) + 1/(5108*d**2) - 1
    g3 = 1 - 140.45*d / (D**2 * N)
    g4 = (d + D) / 1.5 - 1

    return _penalize(f, [g1, g2, g3, g4])

TENSION_SPRING = {
    "name": "Tension/Compression Spring",
    "obj_func": spring_obj,
    "bounds": FloatVar(lb=[0.05, 0.25, 2.0], ub=[2.0, 1.3, 15.0]),
    "minmax": "min",
}


# ============================================================
# 4. Speed Reducer Design
#    Variables: x = [x1..x7]
#    Minimize: weight
#    Subject to: 11 inequality constraints
# ============================================================

def speed_reducer_obj(x):
    x1, x2, x3, x4, x5, x6, x7 = x[0], x[1], x[2], x[3], x[4], x[5], x[6]

    f = (0.7854*x1*x2**2 * (3.3333*x3**2 + 14.9334*x3 - 43.0934)
         - 1.508*x1*(x6**2 + x7**2)
         + 7.4777*(x6**3 + x7**3)
         + 0.7854*(x4*x6**2 + x5*x7**2))

    g1 = 27/(x1*x2**2*x3) - 1
    g2 = 397.5/(x1*x2**2*x3**2) - 1
    g3 = 1.93*x4**3/(x2*x3*x6**4) - 1
    g4 = 1.93*x5**3/(x2*x3*x7**4) - 1

    A = (745*x4/x2/x3)**2 + 16.9e6
    g5 = np.sqrt(A)/(110*x6**3) - 1

    B = (745*x5/x2/x3)**2 + 157.5e6
    g6 = np.sqrt(B)/(85*x7**3) - 1

    g7 = x2*x3/40 - 1
    g8 = 5*x2/x1 - 1
    g9 = x1/(12*x2) - 1
    g10 = (1.5*x6 + 1.9)/x4 - 1
    g11 = (1.1*x7 + 1.9)/x5 - 1

    return _penalize(f, [g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11])

SPEED_REDUCER = {
    "name": "Speed Reducer Design",
    "obj_func": speed_reducer_obj,
    "bounds": FloatVar(lb=[2.6, 0.7, 17.0, 7.3, 7.3, 2.9, 5.0],
                       ub=[3.6, 0.8, 28.0, 8.3, 8.3, 3.9, 5.5]),
    "minmax": "min",
}


# ============================================================
# 5. Three-Bar Truss Design
#    Variables: x = [x1, x2]  (cross-section areas)
#    Minimize: weight = (2*sqrt(2)*x1 + x2) * L
#    Subject to: 3 inequality constraints (stress limits)
# ============================================================

def three_bar_truss_obj(x):
    x1, x2 = x[0], x[1]
    L = 100.0   # length
    P = 2.0     # applied load (kips)
    sigma_max = 2.0  # max stress (ksi)

    # objective: weight
    f = (2 * np.sqrt(2) * x1 + x2) * L

    # stress constraints
    denom1 = 2 * np.sqrt(2) * x1 + x2
    denom2 = x2
    denom3 = 2 * x1 + np.sqrt(2) * x2

    s1 = (2 * np.sqrt(2) * x1 + x2) / (denom1 * (x1 + np.sqrt(2) * x2)) * P if denom1 != 0 else 1e10
    s2 = 1.0 / (denom1) * P if denom1 != 0 else 1e10
    s3 = 1.0 / (denom3) * P if denom3 != 0 else 1e10

    g1 = abs(s1) - sigma_max
    g2 = abs(s2) - sigma_max
    g3 = abs(s3) - sigma_max

    return _penalize(f, [g1, g2, g3])

THREE_BAR_TRUSS = {
    "name": "Three-Bar Truss Design",
    "obj_func": three_bar_truss_obj,
    "bounds": FloatVar(lb=[0.0, 0.0], ub=[1.0, 1.0]),
    "minmax": "min",
}


# all engineering problems
ENGINEERING_PROBLEMS = [WELDED_BEAM, PRESSURE_VESSEL, TENSION_SPRING, SPEED_REDUCER, THREE_BAR_TRUSS]


def test_all_constraints():
    """Quick sanity check: evaluate each problem at lb midpoint."""
    for prob in ENGINEERING_PROBLEMS:
        lb = prob["bounds"].lb
        ub = prob["bounds"].ub
        mid = [(a+b)/2 for a, b in zip(lb, ub)]
        val = prob["obj_func"](mid)
        print(f"{prob['name']:30s} | f(mid) = {val:.4e}")
    print("All constraint functions evaluated successfully.")


if __name__ == "__main__":
    test_all_constraints()
