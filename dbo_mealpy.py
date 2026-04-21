"""
Base Dung Beetle Optimizer (DBO) – mealpy Optimizer wrapper
============================================================
Reference: Xue, J. & Shen, B. (2023). "Dung beetle optimizer: a new
meta-heuristic algorithm for global optimization."
The Journal of Supercomputing, 79, 7305-7336.

Wraps the standard DBO as a mealpy-compatible Optimizer so it can be
benchmarked alongside other mealpy algorithms.
"""

import numpy as np
from mealpy import Optimizer


class OriginalDBO(Optimizer):
    """
    Standard Dung Beetle Optimizer (DBO).

    Parameters
    ----------
    epoch : int
        Maximum number of iterations (default 2000).
    pop_size : int
        Population size (default 30).
    k : float
        Deflection coefficient for ball-rolling beetles (default 0.1).
    b : float
        Light-intensity weight for ball-rolling beetles (default 0.3).
    S : float
        Thief step scale (default 0.5).
    """

    def __init__(self, epoch=2000, pop_size=30, k=0.1, b=0.3, S=0.5, **kwargs):
        super().__init__(**kwargs)
        self.epoch = self.validator.check_int("epoch", epoch, [1, 100_000])
        self.pop_size = self.validator.check_int("pop_size", pop_size, [5, 10_000])
        self.k = k
        self.b = b
        self.S = S
        self.set_parameters(["epoch", "pop_size", "k", "b", "S"])
        self.sort_flag = False

    # ---- population split ----

    def _split(self):
        n = self.pop_size
        nr = max(1, int(n * 0.20))
        nb = max(1, int(n * 0.20))
        nf = max(1, int(n * 0.23))
        nt = n - nr - nb - nf
        return nr, nb, nf, nt

    # ---- initialisation bookkeeping ----

    def after_initialization(self):
        super().after_initialization()
        self.prev_pop = [agent.solution.copy() for agent in self.pop]

    # ---- main evolution step ----

    def evolve(self, epoch):
        nr, nb, nf, nt = self._split()
        g_pos = self.g_best.solution.copy()
        dim = self.problem.n_dims
        lb, ub = self.problem.lb, self.problem.ub

        # linear shrinking factor
        R = 1.0 - epoch / self.epoch

        # find current worst and local best
        _, _, list_worst = self.get_special_agents(
            self.pop, n_best=1, minmax=self.problem.minmax
        )
        worst_pos = list_worst[0].solution
        local_best_pos = self.g_best.solution.copy()

        pop_new = []
        idx = 0

        # --- GROUP 1: Ball-rolling dung beetles ---
        for i in range(nr):
            pos = self.pop[idx].solution.copy()
            prev = self.prev_pop[idx]
            alpha = 1 if self.generator.random() < 0.5 else -1
            if self.generator.random() > 0.1:
                delta_x = np.abs(pos - worst_pos)
                new_pos = pos + alpha * self.k * prev + self.b * delta_x
            else:
                theta = self.generator.uniform(0, np.pi)
                if theta in (0, np.pi / 2, np.pi):
                    theta += 1e-6
                new_pos = pos + np.tan(theta) * np.abs(pos - prev)
            new_pos = np.clip(new_pos, lb, ub)
            pop_new.append(self.generate_empty_agent(new_pos))
            idx += 1

        # --- GROUP 2: Brood balls ---
        Lb_star = np.maximum(local_best_pos * (1 - R), lb)
        Ub_star = np.minimum(local_best_pos * (1 + R), ub)
        for i in range(nb):
            pos = self.pop[idx].solution.copy()
            b1 = self.generator.random(dim)
            b2 = self.generator.random(dim)
            new_pos = local_best_pos + b1 * (pos - Lb_star) + b2 * (pos - Ub_star)
            new_pos = np.clip(new_pos, lb, ub)
            pop_new.append(self.generate_empty_agent(new_pos))
            idx += 1

        # --- GROUP 3: Small (foraging) dung beetles ---
        Lbb = np.maximum(g_pos * (1 - R), lb)
        Ubb = np.minimum(g_pos * (1 + R), ub)
        for i in range(nf):
            pos = self.pop[idx].solution.copy()
            C1 = self.generator.standard_normal(dim)
            C2 = self.generator.random(dim)
            new_pos = pos + C1 * (pos - Lbb) + C2 * (pos - Ubb)
            new_pos = np.clip(new_pos, lb, ub)
            pop_new.append(self.generate_empty_agent(new_pos))
            idx += 1

        # --- GROUP 4: Thief dung beetles ---
        for i in range(nt):
            pos = self.pop[idx].solution.copy()
            g = self.generator.standard_normal(dim)
            new_pos = g_pos + self.S * g * (
                np.abs(pos - local_best_pos) + np.abs(pos - g_pos)
            )
            new_pos = np.clip(new_pos, lb, ub)
            pop_new.append(self.generate_empty_agent(new_pos))
            idx += 1

        # --- Evaluate and greedy select ---
        self.prev_pop = [agent.solution.copy() for agent in self.pop]

        if self.mode not in self.AVAILABLE_MODES:
            for i in range(len(pop_new)):
                pop_new[i].target = self.get_target(pop_new[i].solution)
                self.pop[i] = self.get_better_agent(
                    pop_new[i], self.pop[i], self.problem.minmax
                )
        else:
            pop_new = self.update_target_for_population(pop_new)
            self.pop = self.greedy_selection_population(
                self.pop, pop_new, self.problem.minmax
            )
