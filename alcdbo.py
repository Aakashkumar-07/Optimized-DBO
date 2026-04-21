import math
import numpy as np
from mealpy import Optimizer


class MSDBO(Optimizer):

    def __init__(self, epoch=2000, pop_size=30, k=0.1, levy_beta=1.5,
                 stag_thresh=15, archive_ratio=0.1, sigmoid_s=10.0, **kwargs):
        super().__init__(**kwargs)
        self.epoch = self.validator.check_int("epoch", epoch, [1, 100000])
        self.pop_size = self.validator.check_int("pop_size", pop_size, [5, 10000])
        self.k = k
        self.levy_beta = levy_beta
        self.stag_thresh = stag_thresh
        self.archive_ratio = archive_ratio
        self.sigmoid_s = sigmoid_s
        self.set_parameters(["epoch", "pop_size", "k", "levy_beta",
                             "stag_thresh", "archive_ratio", "sigmoid_s"])
        self.sort_flag = False

    def _tent_map(self, n, dim):
        z = np.zeros((n, dim))
        z[0] = self.generator.random(dim) * 0.999 + 0.001
        for i in range(1, n):
            z[i] = np.where(z[i-1] < 0.7,
                            z[i-1] / 0.7,
                            (1.0 - z[i-1]) / 0.3)
            z[i] = np.clip(z[i], 1e-10, 1.0 - 1e-10)
        return z

    def _levy(self, dim):
        beta = self.levy_beta
        num = math.gamma(1 + beta) * np.sin(np.pi * beta / 2)
        den = math.gamma((1 + beta) / 2) * beta * 2**((beta - 1) / 2)
        sigma = (num / den) ** (1 / beta)
        u = self.generator.standard_normal(dim) * sigma
        v = self.generator.standard_normal(dim)
        return u / (np.abs(v) ** (1 / beta))

    def _sigmoid_R(self, epoch):
        t_ratio = epoch / self.epoch
        return 1.0 / (1.0 + np.exp(self.sigmoid_s * (t_ratio - 0.5)))

    def _split_groups(self):
        n = self.pop_size
        nr = max(1, int(n * 0.20))
        nb = max(1, int(n * 0.20))
        nf = max(1, int(n * 0.23))
        nt = n - nr - nb - nf
        return nr, nb, nf, nt

    def _prefclip(self, pos, g_best_pos):
        lb = self.problem.lb
        ub = self.problem.ub
        r = self.generator.random(len(pos))
        below = pos < lb
        above = pos > ub
        pos[below] = r[below] * g_best_pos[below]
        pos[above] = (1 - r[above]) * g_best_pos[above]
        return np.clip(pos, lb, ub)

    def after_initialization(self):
        lb = self.problem.lb
        ub = self.problem.ub
        dim = self.problem.n_dims

        chaos = self._tent_map(self.pop_size, dim)
        for i in range(self.pop_size):
            pos_chaos = lb + chaos[i] * (ub - lb)
            pos_chaos = self.correct_solution(pos_chaos)
            agent_c = self.generate_empty_agent(pos_chaos)
            agent_c.target = self.get_target(pos_chaos)

            pos_opp = lb + ub - pos_chaos
            pos_opp = self.correct_solution(pos_opp)
            agent_o = self.generate_empty_agent(pos_opp)
            agent_o.target = self.get_target(pos_opp)

            better = self.get_better_agent(agent_c, agent_o, self.problem.minmax)
            self.pop[i] = self.get_better_agent(better, self.pop[i], self.problem.minmax)

        self.pbest = [agent.solution.copy() for agent in self.pop]
        self.pbest_fit = [agent.target.fitness for agent in self.pop]

        k = max(1, int(self.pop_size * self.archive_ratio))
        sorted_pop = sorted(self.pop, key=lambda a: a.target.fitness)
        if self.problem.minmax == "max":
            sorted_pop = sorted_pop[::-1]
        self.archive = [(a.solution.copy(), a.target.fitness) for a in sorted_pop[:k]]
        self.archive_size = k

        super().after_initialization()
        self.stag_counter = 0
        self.prev_best_fit = self.g_best.target.fitness

    def evolve(self, epoch):
        nr, nb, nf, nt = self._split_groups()
        R = self._sigmoid_R(epoch)
        g_pos = self.g_best.solution.copy()
        dim = self.problem.n_dims
        lb, ub = self.problem.lb, self.problem.ub

        _, _, list_worst = self.get_special_agents(self.pop, n_best=1,
                                                   minmax=self.problem.minmax)
        worst_pos = list_worst[0].solution

        pop_new = []
        idx = 0

        for i in range(nr):
            pos = self.pop[idx].solution.copy()
            if R > 0.5:
                step = self.generator.standard_normal(dim)
                new_pos = pos + self.k * step * (pos - worst_pos)
            else:
                lev = self._levy(dim)
                new_pos = pos + 0.01 * lev * (g_pos - pos)
            new_pos = self._prefclip(new_pos, g_pos)
            agent = self.generate_empty_agent(new_pos)
            pop_new.append(agent)
            idx += 1

        sorted_pop = sorted(self.pop, key=lambda a: a.target.fitness)
        if self.problem.minmax == "max":
            sorted_pop = sorted_pop[::-1]
        top30 = max(1, int(self.pop_size * 0.3))
        mentors = sorted_pop[:top30]

        for i in range(nb):
            pos = self.pop[idx].solution.copy()
            pb = self.pbest[idx]
            mentor = mentors[self.generator.integers(0, len(mentors))].solution

            r1, r2, r3 = self.generator.random(3)
            s = r1 + r2 + r3
            w1, w2, w3 = r1/s, r2/s, r3/s
            new_pos = w1 * pos + w2 * pb + w3 * mentor
            new_pos = self._prefclip(new_pos, g_pos)
            agent = self.generate_empty_agent(new_pos)
            pop_new.append(agent)
            idx += 1

        for i in range(nf):
            pos = self.pop[idx].solution.copy()
            arc_idx = self.generator.integers(0, len(self.archive))
            arc_pos = self.archive[arc_idx][0]

            r1 = self.generator.random(dim)
            r2 = self.generator.random(dim)
            new_pos = pos + r1 * (arc_pos - pos) + r2 * (g_pos - pos)
            new_pos = self._prefclip(new_pos, g_pos)
            agent = self.generate_empty_agent(new_pos)
            pop_new.append(agent)
            idx += 1

        for i in range(nt):
            pos = self.pop[idx].solution.copy()
            if self.stag_counter >= self.stag_thresh:
                gamma = 0.01 * (1.0 - epoch / self.epoch)
                cauchy = self.generator.standard_cauchy(dim)
                new_pos = g_pos + gamma * cauchy * (ub - lb)
            else:
                g = self.generator.standard_normal(dim)
                x_local = sorted_pop[0].solution
                new_pos = g_pos + 0.5 * g * (np.abs(pos - x_local) + np.abs(pos - g_pos))
            new_pos = self._prefclip(new_pos, g_pos)
            agent = self.generate_empty_agent(new_pos)
            pop_new.append(agent)
            idx += 1

        if self.mode not in self.AVAILABLE_MODES:
            for i in range(len(pop_new)):
                pop_new[i].target = self.get_target(pop_new[i].solution)
                self.pop[i] = self.get_better_agent(pop_new[i], self.pop[i],
                                                     self.problem.minmax)
        else:
            pop_new = self.update_target_for_population(pop_new)
            self.pop = self.greedy_selection_population(self.pop, pop_new,
                                                        self.problem.minmax)

        for i in range(self.pop_size):
            fit = self.pop[i].target.fitness
            if self._is_better(fit, self.pbest_fit[i]):
                self.pbest[i] = self.pop[i].solution.copy()
                self.pbest_fit[i] = fit

        for i in range(self.pop_size):
            fit = self.pop[i].target.fitness
            worst_idx = 0
            worst_fit = self.archive[0][1]
            for j, arc in enumerate(self.archive):
                if self.problem.minmax == "min" and arc[1] > worst_fit:
                    worst_idx = j
                    worst_fit = arc[1]
                elif self.problem.minmax == "max" and arc[1] < worst_fit:
                    worst_idx = j
                    worst_fit = arc[1]
                    
            if self._is_better(fit, worst_fit):
                self.archive.pop(worst_idx)
                self.archive.append((self.pop[i].solution.copy(), fit))

        if epoch % 20 == 0 and self.stag_counter >= self.stag_thresh:
            n_replace = max(1, int(len(self.archive) * 0.3))
            chaos = self._tent_map(n_replace, dim)
            if self.problem.minmax == "min":
                self.archive.sort(key=lambda x: x[1])
            else:
                self.archive.sort(key=lambda x: -x[1])
            for j in range(n_replace):
                new_sol = lb + chaos[j] * (ub - lb)
                new_sol = self.correct_solution(new_sol)
                tgt = self.get_target(new_sol)
                self.archive[-(j+1)] = (new_sol.copy(), tgt.fitness)

        cur_best = self.g_best.target.fitness
        if abs(cur_best - self.prev_best_fit) < 1e-15:
            self.stag_counter += 1
        else:
            self.stag_counter = 0
        self.prev_best_fit = cur_best

        if self.stag_counter >= self.stag_thresh:
            n_perturb = max(1, int(self.pop_size * 0.1))
            sorted_idx = sorted(range(self.pop_size),
                                key=lambda i: self.pop[i].target.fitness)
            if self.problem.minmax == "max":
                sorted_idx = sorted_idx[::-1]
            for j in range(n_perturb):
                ci = sorted_idx[j]
                pos = self.pop[ci].solution.copy()
                n_dims_change = max(1, int(dim * 0.2))
                dims_to_change = self.generator.choice(dim, n_dims_change, replace=False)
                chaos_vals = self._tent_map(1, n_dims_change)[0]
                for d_idx, d in enumerate(dims_to_change):
                    pos[d] = lb[d] + chaos_vals[d_idx] * (ub[d] - lb[d])
                pos = self.correct_solution(pos)
                agent = self.generate_empty_agent(pos)
                agent.target = self.get_target(pos)
                self.pop[ci] = self.get_better_agent(agent, self.pop[ci],
                                                      self.problem.minmax)

    def _is_better(self, fit1, fit2):
        if self.problem.minmax == "min":
            return fit1 < fit2
        return fit1 > fit2
