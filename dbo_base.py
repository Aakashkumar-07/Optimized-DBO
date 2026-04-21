"""
Base Dung Beetle Optimizer (DBO)
=================================
Reference: Xue, J. & Shen, B. (2023). "Dung beetle optimizer: a new meta-heuristic
algorithm for global optimization." The Journal of Supercomputing, 79, 7305-7336.
https://doi.org/10.1007/s11227-022-04959-6

Five agent types:
  1. Ball-rolling dung beetle  -- explores away from global worst
  2. Dancing (obstacle) update -- tangent-based reorientation
  3. Brood ball                -- local search around local best
  4. Small (foraging) beetle   -- searches around global best
  5. Thief beetle              -- steals near global best
"""

import math
import numpy as np


# --------------------------------------------------------------------------- #
#  Utility
# --------------------------------------------------------------------------- #

def clip(x: np.ndarray, lb: np.ndarray, ub: np.ndarray) -> np.ndarray:
    """Clip position to search bounds."""
    return np.clip(x, lb, ub)


def levy_flight(dim: int, beta: float = 1.5) -> np.ndarray:
    """Mantegna's Lévy flight step (not used in base DBO, but kept for reference)."""
    sigma = (
        math.gamma(1 + beta) * np.sin(np.pi * beta / 2)
        / (math.gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2))
    ) ** (1 / beta)
    u = np.random.randn(dim) * sigma
    v = np.random.randn(dim)
    return u / (np.abs(v) ** (1 / beta))


# --------------------------------------------------------------------------- #
#  Agent-group split helper
# --------------------------------------------------------------------------- #

def split_population(n: int):
    """
    Split N agents into four groups following the paper's recommended ratio
    for a population of 30. Ratios: rollers≈20%, brood≈20%, foragers≈23%, thieves≈37%.
    """
    n_rollers = max(1, int(n * 0.20))
    n_brood   = max(1, int(n * 0.20))
    n_foragers = max(1, int(n * 0.23))
    n_thieves = n - n_rollers - n_brood - n_foragers
    return n_rollers, n_brood, n_foragers, n_thieves


# --------------------------------------------------------------------------- #
#  DBO
# --------------------------------------------------------------------------- #

class DBO:
    """
    Base Dung Beetle Optimizer.

    Parameters
    ----------
    obj_func   : callable   -- objective function f(x) -> float
    lb, ub     : array-like -- lower/upper bounds per dimension
    dim        : int        -- search space dimensionality
    n_pop      : int        -- population size
    max_iter   : int        -- maximum iterations
    k          : float      -- deflection coefficient for rolling beetle (0, 0.2]
    b          : float      -- light-intensity weight
    S          : float      -- thief step scale
    """

    def __init__(
        self,
        obj_func,
        lb, ub,
        dim: int,
        n_pop: int = 30,
        max_iter: int = 500,
        k: float = 0.1,
        b: float = 0.3,
        S: float = 0.5,
    ):
        self.obj_func = obj_func
        self.lb  = np.array(lb, dtype=float)
        self.ub  = np.array(ub, dtype=float)
        self.dim = dim
        self.n_pop    = n_pop
        self.max_iter = max_iter
        self.k = k
        self.b = b
        self.S = S

    # ------------------------------------------------------------------ #
    #  Initialisation
    # ------------------------------------------------------------------ #

    def _init_population(self):
        pop = self.lb + np.random.rand(self.n_pop, self.dim) * (self.ub - self.lb)
        fitness = np.array([self.obj_func(pop[i]) for i in range(self.n_pop)])
        return pop, fitness

    # ------------------------------------------------------------------ #
    #  Main loop
    # ------------------------------------------------------------------ #

    def optimize(self):
        pop, fitness = self._init_population()
        prev_pop     = pop.copy()          # x(t-1) for rolling beetle

        best_idx   = np.argmin(fitness)
        worst_idx  = np.argmax(fitness)
        X_best     = pop[best_idx].copy()  # global best (Xb)
        X_local    = pop[best_idx].copy()  # local best  (X*)
        X_worst    = pop[worst_idx].copy() # global worst (Xw)
        best_score = fitness[best_idx]

        # convergence history
        convergence = np.full(self.max_iter, best_score)

        n_r, n_b, n_f, n_t = split_population(self.n_pop)
        idx_r = slice(0,        n_r)
        idx_b = slice(n_r,      n_r + n_b)
        idx_f = slice(n_r+n_b,  n_r + n_b + n_f)
        idx_t = slice(n_r+n_b+n_f, self.n_pop)

        for t in range(self.max_iter):
            R = 1.0 - t / self.max_iter          # shrinking factor

            new_pop  = pop.copy()

            # -------- 1. Ball-rolling dung beetles -------- #
            for i in range(*idx_r.indices(self.n_pop)):
                alpha = 1 if np.random.rand() < 0.5 else -1
                if np.random.rand() > 0.1:       # 90% chance: normal rolling
                    delta_x = np.abs(pop[i] - X_worst)
                    new_x   = pop[i] + alpha * self.k * prev_pop[i] + self.b * delta_x
                else:                             # 10% chance: dance (obstacle)
                    theta   = np.random.uniform(0, np.pi)
                    if theta in (0, np.pi / 2, np.pi):
                        theta += 1e-6
                    new_x = pop[i] + np.tan(theta) * np.abs(pop[i] - prev_pop[i])
                new_pop[i] = clip(new_x, self.lb, self.ub)

            # -------- 2. Brood balls -------- #
            Lb_star = np.maximum(X_local * (1 - R), self.lb)
            Ub_star = np.minimum(X_local * (1 + R), self.ub)
            for i in range(*idx_b.indices(self.n_pop)):
                b1 = np.random.rand(self.dim)
                b2 = np.random.rand(self.dim)
                new_x = X_local + b1 * (pop[i] - Lb_star) + b2 * (pop[i] - Ub_star)
                new_pop[i] = clip(new_x, self.lb, self.ub)

            # -------- 3. Small (foraging) dung beetles -------- #
            Lbb = np.maximum(X_best * (1 - R), self.lb)
            Ubb = np.minimum(X_best * (1 + R), self.ub)
            for i in range(*idx_f.indices(self.n_pop)):
                C1 = np.random.randn(self.dim)
                C2 = np.random.rand(self.dim)
                new_x = pop[i] + C1 * (pop[i] - Lbb) + C2 * (pop[i] - Ubb)
                new_pop[i] = clip(new_x, self.lb, self.ub)

            # -------- 4. Thief dung beetles -------- #
            for i in range(*idx_t.indices(self.n_pop)):
                g     = np.random.randn(self.dim)
                new_x = X_best + self.S * g * (
                    np.abs(pop[i] - X_local) + np.abs(pop[i] - X_best)
                )
                new_pop[i] = clip(new_x, self.lb, self.ub)

            # -------- Evaluate & update -------- #
            prev_pop = pop.copy()
            pop      = new_pop.copy()

            new_fitness = np.array([self.obj_func(pop[i]) for i in range(self.n_pop)])
            improved    = new_fitness < fitness
            fitness     = np.where(improved, new_fitness, fitness)

            best_idx  = np.argmin(fitness)
            worst_idx = np.argmax(fitness)
            if fitness[best_idx] < best_score:
                best_score = fitness[best_idx]
                X_best     = pop[best_idx].copy()

            X_local = pop[best_idx].copy()
            X_worst = pop[worst_idx].copy()
            convergence[t] = best_score

        return X_best, best_score, convergence
