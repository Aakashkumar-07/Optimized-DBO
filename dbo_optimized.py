import math
import numpy as np



def levy_flight(dim: int, beta: float = 1.5) -> np.ndarray:
    """Generate a Lévy flight step vector of size *dim*."""
    num   = math.gamma(1 + beta) * np.sin(np.pi * beta / 2)
    den   = math.gamma((1 + beta) / 2) * beta * 2 ** ((beta - 1) / 2)
    sigma = (num / den) ** (1 / beta)
    u = np.random.randn(dim) * sigma
    v = np.random.randn(dim)
    return u / (np.abs(v) ** (1 / beta))



def preferential_clip(x: np.ndarray, lb: np.ndarray, ub: np.ndarray,
                      x_best: np.ndarray) -> np.ndarray:
    x = x.copy()
    r = np.random.rand(x.shape[-1])
    below = x < lb
    above = x > ub
    x[below] = r[below] * x_best[below]
    x[above] = (1 - r[above]) * x_best[above]
    # Final safety clip in case X_best itself is near boundary
    return np.clip(x, lb, ub)


def split_population(n: int):
    n_rollers  = max(1, int(n * 0.20))
    n_brood    = max(1, int(n * 0.20))
    n_foragers = max(1, int(n * 0.23))
    n_thieves  = n - n_rollers - n_brood - n_foragers
    return n_rollers, n_brood, n_foragers, n_thieves


class ODBO:
    """
    Optimized Dung Beetle Optimizer.

    Parameters
    ----------
    obj_func   : callable   -- objective function f(x) -> float
    lb, ub     : array-like -- lower/upper bounds per dimension
    dim        : int        -- problem dimensionality
    n_pop      : int        -- population size (default 30)
    max_iter   : int        -- maximum iterations (default 500)
    k          : float      -- deflection coefficient for rollers (0, 0.2]
    b          : float      -- light-intensity weight for rollers
    S          : float      -- thief step scale
    levy_beta  : float      -- Lévy exponent (1 < beta ≤ 2)
    p_forager  : float      -- probability of using Pelican foraging vs larval
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
        levy_beta: float = 1.5,
        p_forager: float = 0.5,
    ):
        self.obj_func  = obj_func
        self.lb        = np.array(lb, dtype=float)
        self.ub        = np.array(ub, dtype=float)
        self.dim       = dim
        self.n_pop     = n_pop
        self.max_iter  = max_iter
        self.k         = k
        self.b         = b
        self.S         = S
        self.levy_beta = levy_beta
        self.p_forager = p_forager


    def _init_population(self):
        pop = self.lb + np.random.rand(self.n_pop, self.dim) * (self.ub - self.lb)
        fitness = np.array([self.obj_func(pop[i]) for i in range(self.n_pop)])
        return pop, fitness


    def _R(self, t: int) -> float:
        """
        R = 1 – rand × (t/Tmax)^2
        Nonlinear quadratic decay with stochastic perturbation.
        Preserves broad exploration in early iterations; narrows search later.
        """
        return 1.0 - np.random.rand() * (t / self.max_iter) ** 2


    def optimize(self):
        pop, fitness = self._init_population()
        prev_pop     = pop.copy()

        best_idx   = np.argmin(fitness)
        worst_idx  = np.argmax(fitness)
        X_best     = pop[best_idx].copy()   # global best (X_b)
        X_local    = pop[best_idx].copy()   # local best  (X*)
        best_score = fitness[best_idx]

        convergence = np.full(self.max_iter, best_score)

        n_r, n_b, n_f, n_t = split_population(self.n_pop)
        idx_r = (0,        n_r)
        idx_b = (n_r,      n_r + n_b)
        idx_f = (n_r+n_b,  n_r + n_b + n_f)
        idx_t = (n_r+n_b+n_f, self.n_pop)

        for t in range(self.max_iter):
            R = self._R(t)                       # nonlinear stochastic factor
            new_pop = pop.copy()

            
            for i in range(*idx_r):
                alpha = 1 if np.random.rand() < 0.5 else -1
                if np.random.rand() > 0.1:
                    # EDBO optimal-value guidance (Eq. 9 in EDBO paper)
                    delta_x = np.abs(pop[i] + np.random.rand() * X_best)
                    new_x   = pop[i] + alpha * self.k * prev_pop[i] + self.b * delta_x
                else:
                    # Dancing / obstacle-hit reorientation (unchanged)
                    theta = np.random.uniform(0, np.pi)
                    if theta in (0, np.pi / 2, np.pi):
                        theta += 1e-6
                    new_x = pop[i] + np.tan(theta) * np.abs(pop[i] - prev_pop[i])
                new_pop[i] = preferential_clip(new_x, self.lb, self.ub, X_best)

            
            Lb_star = np.maximum(X_local * (1 - R), self.lb)
            Ub_star = np.minimum(X_local * (1 + R), self.ub)
            for i in range(*idx_b):
                b1 = np.random.rand(self.dim)
                b2 = np.random.rand(self.dim)
                new_x = X_local + b1 * (pop[i] - Lb_star) + b2 * (pop[i] - Ub_star)
                new_pop[i] = preferential_clip(new_x, self.lb, self.ub, X_best)

            
            Lbb = np.maximum(X_best * (1 - R), self.lb)
            Ubb = np.minimum(X_best * (1 + R), self.ub)
            for i in range(*idx_f):
                if np.random.rand() < self.p_forager:
                    # (a) Larval growth – experiential exploration
                    new_x = pop[i] + (Lbb + (Ubb - Lbb) * np.random.rand(self.dim))
                else:
                    # (b) Pelican-guided foraging – exploitation with diversity
                    l     = np.random.choice([1, 2])
                    new_x = pop[i] + np.random.rand() * (X_best - l * pop[i])
                new_pop[i] = preferential_clip(new_x, self.lb, self.ub, X_best)

            
            for i in range(*idx_t):
                r1 = np.random.randn()
                r2 = np.random.randn()
                s  = r1 * 20 + r2 * 20
                r  = np.random.rand()
                j  = i - idx_t[0] + 1    # 1-indexed position in thief group
                n_thieves = idx_t[1] - idx_t[0]

                if r < 0.5 and s < 20:
                    # Reproduction-teaching mode
                    m   = (j / n_thieves) * 2
                    p   = (np.sin(Ubb - Lbb) * 2 + (Ubb - Lbb) * m)
                    XG  = X_best * 0.8
                    new_x = XG + (X_best * pop[i]) * p
                elif r < 0.5 and s >= 20:
                    # Predator-Lévy escape mode
                    w   = (np.pi / 2) * (j / n_thieves)
                    k_s = 0.2 * np.sin(np.pi / 2 - w)
                    lev = levy_flight(self.dim, self.levy_beta)
                    new_x = X_best * lev * k_s
                else:
                    # Standard DBO theft
                    g   = np.random.randn(self.dim)
                    new_x = X_best + self.S * g * (
                        np.abs(pop[i] - X_local) + np.abs(pop[i] - X_best)
                    )
                new_pop[i] = preferential_clip(new_x, self.lb, self.ub, X_best)

            prev_pop    = pop.copy()
            pop         = new_pop.copy()
            new_fitness = np.array([self.obj_func(pop[i]) for i in range(self.n_pop)])

            improved = new_fitness < fitness
            fitness  = np.where(improved, new_fitness, fitness)
            

            best_idx  = np.argmin(fitness)
            worst_idx = np.argmax(fitness)
            if fitness[best_idx] < best_score:
                best_score = fitness[best_idx]
                X_best     = pop[best_idx].copy()

            X_local = pop[best_idx].copy()
            convergence[t] = best_score

        return X_best, best_score, convergence
