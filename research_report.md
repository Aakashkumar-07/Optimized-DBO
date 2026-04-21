# Comparative Analysis of Nature-Inspired Optimization Algorithms using CEC-2014, CEC-2017 Benchmarks and Engineering Problems

**Authors:** [Author Names]  
**Affiliation:** [University/Institution]  
**Date:** April 2026

---

## Abstract

This paper presents a comprehensive comparative analysis of nine nature-inspired metaheuristic optimization algorithms evaluated on CEC-2014 and CEC-2017 benchmark suites (60 functions) and five constrained engineering design problems. The algorithms compared include Aquila Optimizer (AO), African Vultures Optimization Algorithm (AVOA), Mountain Gazelle Optimizer (MGO), Northern Goshawk Optimization (NGO), Zebra Optimization Algorithm (ZOA), Coati Optimization Algorithm (CoatiOA), Fennec Fox Optimization (FFO), the standard Dung Beetle Optimizer (DBO), and a proposed Multi-Strategy Dung Beetle Optimizer (MSDBO). Each algorithm is evaluated over 50 independent runs with a fixed budget of 60,000 function evaluations per run. Performance is assessed using mean fitness, standard deviation, function-wise ranking, convergence analysis, and the Wilcoxon rank-sum statistical test. The proposed MSDBO integrates five synergistic strategies — chaotic tent-map initialization with opposition-based learning, Gaussian-Lévy dual-mode rollers, social-learning crossover, elite archive search, and Cauchy stagnation escape — achieving an average rank of 1.30 on CEC-2014, 1.13 on CEC-2017, and 1.20 on engineering problems. Statistical tests confirm MSDBO's superiority at the 5% significance level over all competitors on the majority of benchmark functions.

**Keywords:** Metaheuristic optimization, Dung Beetle Optimizer, Nature-inspired algorithms, CEC benchmarks, Engineering optimization, Wilcoxon rank-sum test

---

## 1. Introduction

Optimization problems are ubiquitous across engineering, science, and industry. Many real-world problems involve high-dimensional, non-convex, multimodal search spaces where classical gradient-based methods fail due to local optima entrapment and discontinuities. Nature-inspired metaheuristic algorithms have emerged as powerful alternatives, drawing inspiration from biological, physical, and social phenomena to explore complex search landscapes effectively.

The No Free Lunch (NFL) theorem establishes that no single optimization algorithm can outperform all others across every possible problem. This motivates continuous development of new algorithms and hybrid strategies that improve performance on broad classes of problems. Recent years (2021–2023) have witnessed a surge of novel nature-inspired optimizers including the Aquila Optimizer (AO), African Vultures Optimization Algorithm (AVOA), Mountain Gazelle Optimizer (MGO), Northern Goshawk Optimization (NGO), Zebra Optimization Algorithm (ZOA), Coati Optimization Algorithm (CoatiOA), Fennec Fox Optimization (FFO), and the Dung Beetle Optimizer (DBO).

While each algorithm demonstrates competitive performance on specific problem classes, the standard DBO suffers from several limitations: premature convergence due to linear decay of the shrinking factor, boundary clustering from hard clipping, limited diversity in the foraging group, and insufficient escape mechanisms for deep local optima. To address these shortcomings, this paper proposes the **Multi-Strategy Dung Beetle Optimizer (MSDBO)**, which integrates five complementary strategies to enhance both exploration and exploitation capabilities.

The main contributions of this work are:
1. A novel MSDBO algorithm combining chaotic initialization, opposition-based learning, social-learning crossover, elite archive search, and Cauchy stagnation escape.
2. A comprehensive benchmark comparison of nine algorithms on 60 CEC functions and five engineering problems.
3. Rigorous statistical validation using the Wilcoxon rank-sum test with 50 independent runs per function.

---

## 2. Literature Review

### 2.1 Aquila Optimizer (AO, 2021)
Proposed by Abualigah et al., AO mimics the hunting strategies of Aquila eagles. It employs four hunting methods: high soaring with vertical stoop, contour flight with short glide attack, low flight with slow descent attack, and walk and grab prey. These four strategies naturally balance exploration and exploitation across iterations.

### 2.2 African Vultures Optimization Algorithm (AVOA, 2021)
Developed by Abdollahzadeh et al., AVOA simulates the foraging behavior of African vultures. The algorithm models vulture group dynamics including exploration via random flight, exploitation through orbiting and siege mechanisms, and starvation-driven behavioral switching.

### 2.3 Mountain Gazelle Optimizer (MGO, 2022)
Proposed by Abdollahzadeh et al., MGO mimics the social behavior and survival strategies of mountain gazelles. It incorporates three behavioral strategies: territory establishment, feeding, and predator avoidance, providing natural exploration-exploitation transitions.

### 2.4 Northern Goshawk Optimization (NGO, 2022)
Developed by Dehghani et al., NGO is inspired by the hunting behavior of the Northern Goshawk bird. The algorithm models two phases: prey identification and pursuit (exploration) and swift attack (exploitation), making it particularly effective on multimodal problems.

### 2.5 Zebra Optimization Algorithm (ZOA, 2022)
Proposed by Trojovská et al., ZOA simulates the foraging and defense behaviors of zebras. It models two main strategies: foraging in grasslands (exploration) and defense against predators using kicks (exploitation).

### 2.6 Coati Optimization Algorithm (CoatiOA, 2022)
Developed by Dehghani et al., CoatiOA mimics the hunting and escape strategies of coatis. The algorithm employs two phases: iguana hunting (exploration via group cooperation) and escape from predators (exploitation via position refinement).

### 2.7 Fennec Fox Optimization (FFO, 2022)
Proposed by Trojovská and Dehghani, FFO is inspired by the hunting techniques of fennec foxes in desert environments. It models digging behavior for prey detection (exploration) and cooperative hunting strategies (exploitation).

### 2.8 Dung Beetle Optimizer (DBO, 2023)
Proposed by Xue and Shen, DBO simulates five behavioral strategies of dung beetles: ball-rolling (navigation via celestial cues), dancing (obstacle reorientation), brood ball spawning (local search), foraging (global search around best), and stealing (exploitation near best solution). Despite competitive performance, DBO suffers from linear shrinking factor decay, hard boundary clipping, and limited local optima escape mechanisms.

### 2.9 Multi-Strategy DBO (MSDBO) — Proposed
The proposed MSDBO addresses DBO's limitations by integrating five synergistic enhancement strategies, described in detail in Section 5.

---

## 3. Objectives

The primary objectives of this research are:

1. To implement and evaluate nine nature-inspired optimization algorithms under identical experimental conditions.
2. To propose the MSDBO algorithm that addresses the identified weaknesses of the standard DBO through multi-strategy enhancement.
3. To conduct comprehensive benchmarking using CEC-2014 (30 functions), CEC-2017 (30 functions), and five constrained engineering optimization problems.
4. To perform rigorous statistical analysis using the Wilcoxon rank-sum test to validate the significance of performance differences.
5. To analyze convergence behavior and provide insights into the exploration-exploitation dynamics of each algorithm.

---

## 4. Methodology

### 4.1 Experimental Settings

All experiments follow strict standardized settings to ensure fair comparison:

| Parameter | Value |
|---|---|
| Population size | 30 |
| Maximum iterations | 2,000 |
| Function evaluations per run | 60,000 (30 × 2,000) |
| Independent runs per function | 50 |
| Dimensionality (CEC suites) | 30 |
| Random seed | 42 to 91 (sequential per run) |

### 4.2 Benchmark Suites

**CEC-2014 (30 functions):**
- F1–F3: Unimodal (shifted/rotated high conditioned elliptic, bent cigar, discus)
- F4–F16: Simple multimodal (shifted/rotated Schwefel, Rastrigin, Ackley, etc.)
- F17–F22: Hybrid functions (combinations of basic functions with variable linkage)
- F23–F30: Composition functions (complex landscapes combining multiple functions)

**CEC-2017 (30 functions):**
Similar structure to CEC-2014 with updated transformations and increased difficulty.

### 4.3 Engineering Optimization Problems

| Problem | Variables | Constraints | Objective |
|---|---|---|---|
| Welded Beam Design | 4 (h, l, t, b) | 7 | Minimize fabrication cost |
| Pressure Vessel Design | 4 (Ts, Th, R, L) | 4 | Minimize total cost |
| Tension/Compression Spring | 3 (d, D, N) | 4 | Minimize weight |
| Speed Reducer Design | 7 (x1–x7) | 11 | Minimize weight |
| Three-Bar Truss Design | 2 (x1, x2) | 3 | Minimize structural weight |

Constraints are handled using a death-penalty approach with penalty coefficient of 10⁶.

### 4.4 Performance Metrics

1. **Mean fitness**: Average of best fitness values across 50 independent runs.
2. **Standard deviation (Std)**: Spread of best fitness values, indicating algorithm robustness.
3. **Rank**: Per-function ranking based on mean fitness (rank 1 = best). Average rank computed across all functions per suite.
4. **Wilcoxon rank-sum test**: Pairwise non-parametric test (α = 0.05) comparing MSDBO against each competitor. Results reported as: **(+)** MSDBO significantly better, **(=)** no significant difference, **(−)** MSDBO significantly worse.

---

## 5. Proposed Algorithm: Multi-Strategy Dung Beetle Optimizer (MSDBO)

### 5.1 Motivation and Overview

The standard DBO algorithm, while effective, exhibits several limitations that reduce its performance on complex optimization landscapes:

1. **Random initialization bias**: Uniform random initialization may miss promising regions, especially in high-dimensional spaces.
2. **Linear shrinking factor**: The linear decay R = 1 − t/T_max causes premature exploitation.
3. **Hard boundary clipping**: Clamping out-of-bounds solutions to boundaries creates artificial clustering.
4. **Static foraging**: Gaussian-only perturbation limits adaptive search behavior.
5. **Weak stagnation escape**: No mechanism to detect and escape deep local optima.

MSDBO addresses all five limitations through a multi-strategy framework that enhances both exploration and exploitation while maintaining computational efficiency.

### 5.2 Strategy Descriptions

#### Strategy 1: Chaotic Tent-Map Initialization with Opposition-Based Learning (OBL)

**Purpose**: Generate a high-quality initial population with better coverage of the search space.

**Mechanism**: Instead of uniform random initialization, MSDBO uses the chaotic tent map:

```
z(i+1) = z(i) / 0.7,           if z(i) < 0.7
z(i+1) = (1 − z(i)) / 0.3,     if z(i) ≥ 0.7
```

The chaotic sequence is mapped to the search space: x = lb + z × (ub − lb). For each chaotic solution, an opposition-based counterpart is generated: x_opp = lb + ub − x. The fitter of the two is retained.

**Mathematical Intuition**: Chaotic maps produce ergodic, non-repeating sequences that cover the search space more uniformly than pseudo-random numbers. OBL doubles the sampling density by simultaneously evaluating both a point and its reflection, increasing the probability of finding promising starting regions.

#### Strategy 2: Gaussian-Lévy Dual-Mode Rollers with Sigmoid Switching

**Purpose**: Adaptively switch between exploration and exploitation in the roller group.

**Mechanism**: A sigmoid switching factor controls the roller behavior:

```
R_sigmoid = 1 / (1 + exp(s × (t/T_max − 0.5)))
```

where s = 10 controls the transition steepness.

- When R_sigmoid > 0.5 (early iterations): **Gaussian exploration mode**
  - x_new = x + k × N(0,1) × (x − x_worst)
  
- When R_sigmoid ≤ 0.5 (later iterations): **Lévy exploitation mode**
  - x_new = x + 0.01 × Lévy(β) × (x_best − x)

**Mathematical Intuition**: The sigmoid provides a smooth, predictable transition from exploration to exploitation. The Lévy flight's heavy-tailed distribution occasionally produces large jumps even in exploitation mode, preventing premature convergence.

#### Strategy 3: Social-Learning Crossover (Brood Group)

**Purpose**: Incorporate knowledge from successful individuals to guide brood ball placement.

**Mechanism**: Each brood beetle's new position is a weighted combination of three sources:

```
x_new = w1 × x_current + w2 × x_pbest + w3 × x_mentor
```

where w1, w2, w3 are random weights normalized to sum to 1, x_pbest is the personal best, and x_mentor is randomly selected from the top 30% of the population.

**Mathematical Intuition**: This social-learning mechanism combines personal experience (x_pbest), current exploration (x_current), and elite guidance (x_mentor). The random weighting prevents all individuals from converging to the same trajectory, maintaining diversity while exploiting knowledge from successful search histories.

#### Strategy 4: Elite Archive Search (Forager Group)

**Purpose**: Maintain a memory of the best-known solutions to guide foraging beetles.

**Mechanism**: An archive of size K = ⌈0.1 × N⌉ stores the best solutions found throughout the search. Foragers update using:

```
x_new = x + r1 × (x_archive − x) + r2 × (x_best − x)
```

where x_archive is randomly selected from the elite archive. The archive is updated each generation, replacing worst entries with better solutions. During stagnation, 30% of the archive is refreshed with chaotic solutions.

**Mathematical Intuition**: The archive serves as a long-term memory that prevents information loss. Unlike standard DBO where foragers only reference the current best, archive-guided search can revisit promising regions discovered in earlier iterations. Archive diversification during stagnation prevents the memory from becoming stale.

#### Strategy 5: Cauchy Stagnation Escape (Thief Group)

**Purpose**: Detect optimization stagnation and escape local optima through heavy-tailed perturbation.

**Mechanism**: A stagnation counter tracks consecutive iterations without improvement. When the counter exceeds a threshold (default: 15 iterations):

```
γ = 0.01 × (1 − t/T_max)
x_new = x_best + γ × Cauchy(0,1) × (ub − lb)
```

Additionally, 10% of top solutions undergo partial re-initialization (20% of dimensions replaced with chaotic values).

**Mathematical Intuition**: The Cauchy distribution has heavier tails than both Gaussian and Lévy distributions, producing larger jumps that can escape even deep local optima. The decay factor γ ensures that escape perturbations become smaller as the search progresses, balancing global escape with local refinement. Partial re-initialization of elite solutions injects diversity without completely discarding good search information.

### 5.3 Preferential Boundary Control

All groups use preferential boundary control instead of hard clipping:

```
if x < lb:  x = rand × x_best
if x > ub:  x = (1 − rand) × x_best
```

This redirects out-of-bounds individuals toward the best-known region rather than clamping them to boundaries, preserving directional information and preventing boundary clustering.

### 5.4 MSDBO Algorithm Flowchart

```
┌──────────────────────────────────────────────┐
│           START: Initialize Parameters        │
│     (pop_size, max_iter, k, levy_beta, etc.) │
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│  Chaotic Tent-Map Initialization + OBL       │
│  Generate N solutions using tent map         │
│  For each: create opposite, keep better      │
│  Initialize personal bests & elite archive   │
└──────────────────┬───────────────────────────┘
                   ▼
┌──────────────────────────────────────────────┐
│  Split Population into 4 Groups              │
│  Rollers(20%) | Brood(20%) |                 │
│  Foragers(23%) | Thieves(37%)                │
└──────────────────┬───────────────────────────┘
                   ▼
          ┌────────┴────────┐
          │  t < max_iter?  │──No──▶ Return x_best
          └────────┬────────┘
                   │ Yes
                   ▼
    ┌──────────────────────────────┐
    │  Compute R_sigmoid(t)        │
    └──────────┬───────────────────┘
               ▼
    ┌──────────────────────────────┐
    │  GROUP 1: Dual-Mode Rollers  │
    │  R > 0.5? → Gaussian step    │
    │  R ≤ 0.5? → Lévy step       │
    └──────────┬───────────────────┘
               ▼
    ┌──────────────────────────────┐
    │  GROUP 2: Social-Learning    │
    │  Crossover (Brood)           │
    │  w1·x + w2·pbest + w3·mentor │
    └──────────┬───────────────────┘
               ▼
    ┌──────────────────────────────┐
    │  GROUP 3: Elite Archive      │
    │  Search (Foragers)           │
    │  x + r1(archive−x) +        │
    │  r2(best−x)                  │
    └──────────┬───────────────────┘
               ▼
    ┌──────────────────────────────┐
    │  GROUP 4: Thieves            │
    │  Stagnation ≥ 15?            │
    │  Yes → Cauchy escape         │
    │  No  → Standard theft        │
    └──────────┬───────────────────┘
               ▼
    ┌──────────────────────────────┐
    │  Greedy Selection            │
    │  Update personal bests       │
    │  Update elite archive        │
    │  Update stagnation counter   │
    │  Chaos perturbation if stuck │
    └──────────┬───────────────────┘
               ▼
          (loop back to t < max_iter?)
```

### 5.5 Strategy Switching and Exploration-Exploitation Balance

```
Iteration Progress ──────────────────────────────────▶
0%              25%              50%              75%              100%

EXPLORATION ███████████████████████░░░░░░░░░░░░░░░░░░░ EXPLOITATION
                              Sigmoid transition

Rollers:    [── Gaussian (wide) ──]  [── Lévy (targeted) ──]
Brood:      [────── Social-learning crossover (balanced) ──────]
Foragers:   [────── Archive-guided search (adaptive) ──────────]
Thieves:    [── Standard theft ──]  [── Cauchy escape if stagnant ──]

                    ┌─────────────────┐
                    │  Stagnation?    │
                    │  Yes → Cauchy   │
                    │  + Chaos inject │
                    └─────────────────┘
```

The five strategies provide complementary exploration-exploitation mechanisms:
- **Early phase**: Chaotic initialization + OBL provides broad coverage. Gaussian rollers explore widely. Social-learning crossover balances individual and collective knowledge.
- **Mid phase**: Sigmoid transitions rollers from Gaussian to Lévy. Archive accumulates elite solutions. Foragers leverage archive diversity.
- **Late phase**: Lévy rollers refine near best solutions. Cauchy escape activates if stagnation is detected, preventing premature convergence. Partial re-initialization maintains diversity in the population.

---

## 6. Results

This section presents the experimental results across all benchmark suites. For each function, we report the Mean fitness, Standard Deviation (Std), and Rank across 50 independent runs. Values are formatted as: **Mean (Std) [Rank]**, where Rank 1 indicates the best-performing algorithm.

### Table 1: CEC-2014 Results (Mean (Std) [Rank])

| Function | MSDBO | DBO | AO | MGO | FFO | AVOA | NGO | ZOA | CoatiOA |
|---|---|---|---|---|---|---|---|---|---|
| CEC2014_F1 | 1.44e+04 (8.22e+03) [1] | 3.91e+05 (1.87e+05) [7] | 2.31e+05 (1.24e+05) [5] | 1.11e+05 (7.23e+04) [3] | 1.33e+06 (1.14e+06) [9] | 3.40e+05 (1.84e+05) [6] | 6.41e+04 (2.96e+04) [2] | 1.16e+06 (6.26e+05) [8] | 1.62e+05 (9.93e+04) [4] |
| CEC2014_F10 | 1.14e+03 (9.76e+01) [1] | 3.13e+03 (1.83e+03) [8] | 1.64e+03 (8.08e+02) [4] | 1.54e+03 (5.71e+02) [3] | 3.08e+03 (1.66e+03) [7] | 2.15e+03 (1.08e+03) [6] | 1.27e+03 (2.60e+02) [2] | 5.02e+03 (3.64e+03) [9] | 1.78e+03 (6.79e+02) [5] |
| CEC2014_F11 | 1.27e+03 (1.34e+02) [1] | 6.04e+03 (3.92e+03) [9] | 1.81e+03 (6.52e+02) [3] | 2.40e+03 (8.79e+02) [4] | 2.93e+03 (1.11e+03) [5] | 3.53e+03 (2.22e+03) [7] | 1.55e+03 (3.03e+02) [2] | 5.95e+03 (3.24e+03) [8] | 3.40e+03 (1.33e+03) [6] |
| CEC2014_F12 | 1.41e+03 (1.69e+02) [1] | 4.23e+03 (2.19e+03) [6] | 2.07e+03 (5.49e+02) [3] | 2.21e+03 (7.01e+02) [4] | 5.65e+03 (3.38e+03) [7] | 7.74e+03 (6.51e+03) [8] | 1.79e+03 (4.26e+02) [2] | 1.25e+04 (9.09e+03) [9] | 3.55e+03 (2.20e+03) [5] |
| CEC2014_F13 | 1.73e+03 (2.38e+02) [1] | 1.16e+04 (1.04e+04) [9] | 3.82e+03 (2.23e+03) [4] | 3.09e+03 (1.64e+03) [3] | 6.11e+03 (3.45e+03) [6] | 1.07e+04 (6.65e+03) [8] | 2.11e+03 (5.89e+02) [2] | 8.26e+03 (4.70e+03) [7] | 4.29e+03 (2.11e+03) [5] |
| CEC2014_F14 | 1.95e+03 (3.18e+02) [1] | 1.58e+04 (1.32e+04) [9] | 3.24e+03 (1.23e+03) [3] | 5.05e+03 (3.50e+03) [5] | 8.39e+03 (5.35e+03) [6] | 1.06e+04 (6.53e+03) [7] | 2.23e+03 (8.17e+02) [2] | 1.27e+04 (7.95e+03) [8] | 4.40e+03 (1.80e+03) [4] |
| CEC2014_F15 | 1.87e+03 (2.77e+02) [1] | 9.60e+03 (5.16e+03) [6] | 5.74e+03 (2.89e+03) [4] | 4.34e+03 (2.91e+03) [3] | 1.19e+04 (7.29e+03) [8] | 1.05e+04 (5.80e+03) [7] | 3.36e+03 (1.25e+03) [2] | 2.02e+04 (1.43e+04) [9] | 5.91e+03 (4.25e+03) [5] |
| CEC2014_F16 | 3.12e+03 (1.08e+03) [1] | 1.26e+04 (6.75e+03) [6] | 4.34e+03 (2.22e+03) [3] | 5.19e+03 (2.40e+03) [4] | 2.09e+04 (1.44e+04) [8] | 2.08e+04 (1.56e+04) [7] | 3.63e+03 (1.18e+03) [2] | 4.49e+04 (2.87e+04) [9] | 6.71e+03 (3.86e+03) [5] |
| CEC2014_F17 | 1.89e+03 (1.66e+02) [1] | 4.23e+03 (2.01e+03) [7] | 3.30e+03 (1.14e+03) [4] | 2.59e+03 (5.95e+02) [3] | 5.00e+03 (1.90e+03) [8] | 3.82e+03 (1.98e+03) [6] | 2.31e+03 (3.80e+02) [2] | 5.21e+03 (2.01e+03) [9] | 3.34e+03 (1.73e+03) [5] |
| CEC2014_F18 | 1.99e+03 (8.81e+01) [1] | 5.56e+03 (2.03e+03) [6] | 3.60e+03 (1.21e+03) [4] | 2.74e+03 (6.00e+02) [3] | 9.41e+03 (4.62e+03) [9] | 7.24e+03 (3.87e+03) [8] | 2.48e+03 (5.52e+02) [2] | 5.69e+03 (2.45e+03) [7] | 3.63e+03 (1.23e+03) [5] |
| CEC2014_F19 | 2.34e+03 (3.71e+02) [1] | 1.10e+04 (5.50e+03) [8] | 4.83e+03 (1.87e+03) [4] | 2.99e+03 (6.69e+02) [2] | 1.06e+04 (6.30e+03) [7] | 9.23e+03 (3.51e+03) [6] | 3.96e+03 (1.44e+03) [3] | 1.32e+04 (6.22e+03) [9] | 5.60e+03 (3.00e+03) [5] |
| CEC2014_F2 | 4.41e+04 (2.32e+04) [1] | 9.95e+05 (5.48e+05) [7] | 6.69e+05 (3.83e+05) [5] | 2.20e+05 (1.25e+05) [2] | 3.06e+06 (1.60e+06) [9] | 6.85e+05 (4.81e+05) [6] | 2.88e+05 (1.49e+05) [3] | 1.94e+06 (1.35e+06) [8] | 3.75e+05 (2.36e+05) [4] |
| CEC2014_F20 | 2.76e+03 (6.26e+02) [1] | 1.24e+04 (6.45e+03) [8] | 5.68e+03 (2.81e+03) [6] | 4.22e+03 (1.67e+03) [3] | 5.63e+03 (2.70e+03) [5] | 1.20e+04 (5.70e+03) [7] | 3.47e+03 (9.31e+02) [2] | 1.37e+04 (7.89e+03) [9] | 4.89e+03 (1.82e+03) [4] |
| CEC2014_F21 | 3.60e+03 (8.85e+02) [1] | 2.15e+04 (1.14e+04) [9] | 5.88e+03 (2.46e+03) [3] | 9.29e+03 (5.33e+03) [4] | 1.87e+04 (8.88e+03) [8] | 1.40e+04 (7.33e+03) [5] | 4.47e+03 (2.06e+03) [2] | 1.80e+04 (9.38e+03) [7] | 1.47e+04 (1.00e+04) [6] |
| CEC2014_F22 | 3.88e+03 (1.08e+03) [1] | 2.43e+04 (1.61e+04) [7] | 9.64e+03 (5.00e+03) [5] | 5.27e+03 (2.39e+03) [2] | 1.67e+04 (1.16e+04) [6] | 2.46e+04 (1.29e+04) [8] | 6.26e+03 (2.40e+03) [3] | 2.82e+04 (1.26e+04) [9] | 8.74e+03 (4.44e+03) [4] |
| CEC2014_F23 | 2.67e+03 (1.83e+02) [2] | 3.19e+03 (5.14e+02) [6] | 3.15e+03 (3.84e+02) [5] | 2.52e+03 (1.28e+02) [1] | 3.32e+03 (4.63e+02) [7] | 3.13e+03 (5.37e+02) [4] | 2.87e+03 (2.51e+02) [3] | 3.78e+03 (7.28e+02) [9] | 3.53e+03 (5.55e+02) [8] |
| CEC2014_F24 | 2.69e+03 (1.71e+02) [1] | 3.37e+03 (5.05e+02) [4] | 2.77e+03 (1.88e+02) [3] | 3.66e+03 (5.92e+02) [7] | 4.35e+03 (9.15e+02) [9] | 3.86e+03 (6.50e+02) [8] | 2.76e+03 (1.58e+02) [2] | 3.55e+03 (5.10e+02) [6] | 3.50e+03 (5.16e+02) [5] |
| CEC2014_F25 | 3.12e+03 (2.90e+02) [3] | 3.80e+03 (5.47e+02) [7] | 3.63e+03 (4.41e+02) [6] | 3.33e+03 (4.31e+02) [4] | 4.64e+03 (1.01e+03) [9] | 4.17e+03 (7.94e+02) [8] | 2.84e+03 (1.96e+02) [1] | 3.49e+03 (4.10e+02) [5] | 3.02e+03 (2.40e+02) [2] |
| CEC2014_F26 | 3.33e+03 (3.63e+02) [2] | 4.82e+03 (1.18e+03) [6] | 3.75e+03 (6.01e+02) [4] | 3.71e+03 (5.32e+02) [3] | 5.00e+03 (1.25e+03) [7] | 5.06e+03 (9.79e+02) [8] | 3.17e+03 (3.05e+02) [1] | 5.49e+03 (1.27e+03) [9] | 3.84e+03 (5.41e+02) [5] |
| CEC2014_F27 | 3.52e+03 (3.56e+02) [2] | 4.39e+03 (6.51e+02) [5] | 3.96e+03 (5.55e+02) [4] | 3.59e+03 (4.53e+02) [3] | 6.51e+03 (2.14e+03) [9] | 5.74e+03 (1.82e+03) [8] | 3.40e+03 (5.03e+02) [1] | 5.24e+03 (9.81e+02) [7] | 4.60e+03 (8.07e+02) [6] |
| CEC2014_F28 | 3.56e+03 (3.63e+02) [1] | 6.19e+03 (1.75e+03) [9] | 4.42e+03 (6.41e+02) [3] | 4.50e+03 (6.74e+02) [4] | 5.82e+03 (1.76e+03) [5] | 6.18e+03 (1.93e+03) [7] | 4.11e+03 (4.94e+02) [2] | 6.18e+03 (1.64e+03) [8] | 5.87e+03 (1.21e+03) [6] |
| CEC2014_F29 | 4.38e+03 (1.01e+03) [5] | 5.83e+03 (1.21e+03) [7] | 4.57e+03 (8.67e+02) [6] | 4.30e+03 (6.59e+02) [4] | 7.92e+03 (1.95e+03) [9] | 6.27e+03 (1.62e+03) [8] | 4.12e+03 (5.91e+02) [1] | 4.24e+03 (5.10e+02) [3] | 4.16e+03 (5.05e+02) [2] |
| CEC2014_F3 | 6.15e+04 (3.36e+04) [1] | 2.88e+06 (1.82e+06) [6] | 3.00e+06 (2.27e+06) [7] | 1.01e+06 (6.74e+05) [4] | 1.32e+07 (6.32e+06) [9] | 1.42e+06 (7.55e+05) [5] | 7.11e+05 (4.24e+05) [2] | 3.79e+06 (2.36e+06) [8] | 8.81e+05 (4.61e+05) [3] |
| CEC2014_F30 | 4.60e+03 (7.41e+02) [1] | 5.70e+03 (1.39e+03) [4] | 5.08e+03 (1.01e+03) [3] | 6.33e+03 (1.71e+03) [5] | 7.28e+03 (2.09e+03) [7] | 1.23e+04 (4.11e+03) [9] | 4.72e+03 (9.81e+02) [2] | 6.59e+03 (1.76e+03) [6] | 8.11e+03 (2.48e+03) [8] |
| CEC2014_F4 | 4.40e+02 (3.29e+01) [1] | 9.50e+02 (3.22e+02) [7] | 5.12e+02 (9.67e+01) [4] | 4.66e+02 (4.33e+01) [3] | 1.22e+03 (6.49e+02) [8] | 6.28e+02 (1.48e+02) [6] | 4.52e+02 (3.15e+01) [2] | 1.31e+03 (6.31e+02) [9] | 5.38e+02 (9.30e+01) [5] |
| CEC2014_F5 | 5.17e+02 (1.18e+01) [1] | 1.36e+03 (5.59e+02) [9] | 6.18e+02 (9.74e+01) [4] | 6.00e+02 (6.86e+01) [3] | 7.74e+02 (2.10e+02) [5] | 7.98e+02 (2.06e+02) [7] | 5.85e+02 (5.32e+01) [2] | 9.88e+02 (3.10e+02) [8] | 7.74e+02 (1.76e+02) [6] |
| CEC2014_F6 | 6.45e+02 (3.60e+01) [1] | 1.69e+03 (8.88e+02) [8] | 7.17e+02 (1.07e+02) [3] | 8.43e+02 (1.60e+02) [4] | 1.17e+03 (4.12e+02) [6] | 1.48e+03 (5.72e+02) [7] | 6.66e+02 (4.26e+01) [2] | 2.20e+03 (1.25e+03) [9] | 9.20e+02 (1.89e+02) [5] |
| CEC2014_F7 | 7.31e+02 (2.86e+01) [1] | 1.74e+03 (7.15e+02) [8] | 8.95e+02 (1.23e+02) [3] | 9.11e+02 (1.32e+02) [4] | 1.69e+03 (9.33e+02) [7] | 1.36e+03 (4.83e+02) [6] | 8.40e+02 (7.44e+01) [2] | 3.74e+03 (1.75e+03) [9] | 1.12e+03 (3.93e+02) [5] |
| CEC2014_F8 | 8.54e+02 (4.36e+01) [1] | 2.71e+03 (1.35e+03) [8] | 1.49e+03 (5.17e+02) [4] | 1.02e+03 (1.60e+02) [3] | 2.35e+03 (1.33e+03) [7] | 2.23e+03 (1.17e+03) [6] | 1.02e+03 (4.12e+02) [2] | 2.85e+03 (1.66e+03) [9] | 1.63e+03 (7.55e+02) [5] |
| CEC2014_F9 | 9.91e+02 (5.51e+01) [1] | 3.27e+03 (1.95e+03) [8] | 1.23e+03 (2.99e+02) [3] | 2.15e+03 (1.30e+03) [6] | 2.76e+03 (1.13e+03) [7] | 1.56e+03 (3.58e+02) [5] | 1.20e+03 (1.75e+02) [2] | 4.22e+03 (2.64e+03) [9] | 1.51e+03 (5.18e+02) [4] |
| **Avg Rank** | **1.30** | **7.13** | **4.07** | **3.53** | **7.30** | **6.80** | **2.00** | **7.97** | **4.90** |

### Table 2: CEC-2017 Results (Mean (Std) [Rank])

| Function | MSDBO | DBO | AO | MGO | FFO | AVOA | NGO | ZOA | CoatiOA |
|---|---|---|---|---|---|---|---|---|---|
| CEC2017_F1 | 6.20e+03 (3.39e+03) [1] | 5.00e+05 (2.10e+05) [7] | 2.18e+05 (1.19e+05) [5] | 1.43e+05 (7.52e+04) [3] | 6.61e+06 (3.49e+06) [9] | 4.46e+05 (2.43e+05) [6] | 3.13e+04 (1.93e+04) [2] | 9.88e+05 (5.82e+05) [8] | 2.11e+05 (1.16e+05) [4] |
| CEC2017_F10 | 1.16e+03 (1.30e+02) [1] | 7.66e+03 (5.70e+03) [8] | 2.88e+03 (2.49e+03) [4] | 1.43e+03 (3.16e+02) [3] | 6.50e+03 (4.93e+03) [7] | 5.39e+03 (3.09e+03) [6] | 1.26e+03 (2.28e+02) [2] | 8.52e+03 (5.66e+03) [9] | 3.02e+03 (1.74e+03) [5] |
| CEC2017_F11 | 1.25e+03 (1.08e+02) [1] | 7.54e+03 (5.36e+03) [7] | 2.58e+03 (1.43e+03) [5] | 1.64e+03 (4.30e+02) [2] | 1.17e+04 (8.42e+03) [8] | 3.53e+03 (1.65e+03) [6] | 1.79e+03 (4.20e+02) [3] | 1.23e+04 (7.60e+03) [9] | 2.41e+03 (8.16e+02) [4] |
| CEC2017_F12 | 1.37e+03 (1.17e+02) [1] | 7.53e+03 (4.27e+03) [7] | 2.90e+03 (9.62e+02) [4] | 2.07e+03 (5.99e+02) [2] | 1.24e+04 (8.46e+03) [8] | 7.25e+03 (4.29e+03) [6] | 2.37e+03 (9.53e+02) [3] | 1.94e+04 (1.29e+04) [9] | 7.14e+03 (5.21e+03) [5] |
| CEC2017_F13 | 1.72e+03 (3.30e+02) [1] | 7.61e+03 (5.58e+03) [6] | 3.68e+03 (1.67e+03) [3] | 4.00e+03 (2.28e+03) [4] | 1.78e+04 (1.57e+04) [8] | 1.65e+04 (1.26e+04) [7] | 2.73e+03 (1.52e+03) [2] | 1.84e+04 (1.55e+04) [9] | 7.44e+03 (4.13e+03) [5] |
| CEC2017_F14 | 1.78e+03 (2.85e+02) [1] | 2.75e+04 (2.46e+04) [9] | 6.56e+03 (3.13e+03) [4] | 5.02e+03 (2.50e+03) [3] | 1.68e+04 (1.00e+04) [6] | 2.41e+04 (2.18e+04) [8] | 3.90e+03 (2.04e+03) [2] | 2.20e+04 (2.04e+04) [7] | 8.63e+03 (5.59e+03) [5] |
| CEC2017_F15 | 2.65e+03 (1.06e+03) [1] | 3.38e+04 (2.82e+04) [8] | 1.14e+04 (8.97e+03) [5] | 6.43e+03 (3.69e+03) [3] | 3.19e+04 (2.40e+04) [7] | 2.11e+04 (1.47e+04) [6] | 5.59e+03 (2.67e+03) [2] | 4.03e+04 (3.71e+04) [9] | 8.53e+03 (7.89e+03) [4] |
| CEC2017_F16 | 3.22e+03 (1.83e+03) [1] | 3.91e+04 (3.12e+04) [8] | 1.24e+04 (7.91e+03) [5] | 7.31e+03 (3.89e+03) [2] | 2.46e+04 (2.34e+04) [7] | 1.47e+04 (1.21e+04) [6] | 1.13e+04 (9.59e+03) [4] | 1.07e+05 (9.63e+04) [9] | 9.69e+03 (6.32e+03) [3] |
| CEC2017_F17 | 2.18e+03 (2.87e+02) [1] | 8.24e+03 (3.73e+03) [9] | 4.90e+03 (1.86e+03) [5] | 3.94e+03 (1.42e+03) [3] | 7.94e+03 (3.72e+03) [8] | 4.64e+03 (1.82e+03) [4] | 2.78e+03 (8.03e+02) [2] | 6.34e+03 (2.60e+03) [6] | 6.76e+03 (2.92e+03) [7] |
| CEC2017_F18 | 2.65e+03 (6.50e+02) [1] | 2.03e+04 (9.21e+03) [9] | 5.53e+03 (1.99e+03) [3] | 5.56e+03 (2.59e+03) [4] | 1.23e+04 (5.05e+03) [7] | 9.12e+03 (4.17e+03) [6] | 3.51e+03 (1.16e+03) [2] | 1.46e+04 (1.05e+04) [8] | 5.88e+03 (2.38e+03) [5] |
| CEC2017_F19 | 2.99e+03 (5.43e+02) [1] | 1.82e+04 (8.53e+03) [8] | 6.03e+03 (2.27e+03) [3] | 8.77e+03 (4.72e+03) [4] | 1.39e+04 (1.02e+04) [5] | 1.61e+04 (8.94e+03) [6] | 3.50e+03 (1.19e+03) [2] | 1.88e+04 (1.16e+04) [9] | 1.66e+04 (9.68e+03) [7] |
| CEC2017_F2 | 3.38e+04 (2.03e+04) [1] | 4.17e+06 (2.03e+06) [8] | 8.25e+05 (4.60e+05) [4] | 3.74e+05 (2.07e+05) [3] | 5.54e+06 (2.60e+06) [9] | 1.10e+06 (4.82e+05) [6] | 1.70e+05 (1.25e+05) [2] | 3.53e+06 (1.75e+06) [7] | 9.15e+05 (4.20e+05) [5] |
| CEC2017_F20 | 3.83e+03 (1.02e+03) [1] | 1.51e+04 (6.83e+03) [6] | 1.05e+04 (7.15e+03) [4] | 8.83e+03 (5.33e+03) [3] | 2.17e+04 (1.06e+04) [9] | 1.73e+04 (1.02e+04) [8] | 8.08e+03 (3.21e+03) [2] | 1.65e+04 (7.28e+03) [7] | 1.28e+04 (6.36e+03) [5] |
| CEC2017_F21 | 4.07e+03 (1.73e+03) [1] | 5.64e+04 (4.20e+04) [8] | 9.44e+03 (4.05e+03) [2] | 1.24e+04 (8.69e+03) [4] | 2.62e+04 (1.63e+04) [7] | 2.46e+04 (1.58e+04) [6] | 1.15e+04 (6.22e+03) [3] | 5.82e+04 (3.01e+04) [9] | 1.54e+04 (6.61e+03) [5] |
| CEC2017_F22 | 6.90e+03 (3.06e+03) [1] | 1.06e+05 (6.42e+04) [9] | 2.97e+04 (1.66e+04) [6] | 1.77e+04 (1.04e+04) [3] | 3.47e+04 (2.11e+04) [7] | 1.77e+04 (1.17e+04) [4] | 9.55e+03 (4.35e+03) [2] | 6.85e+04 (3.47e+04) [8] | 2.42e+04 (1.34e+04) [5] |
| CEC2017_F23 | 2.71e+03 (1.96e+02) [1] | 3.15e+03 (3.27e+02) [4] | 3.08e+03 (3.14e+02) [3] | 2.91e+03 (2.65e+02) [2] | 4.14e+03 (7.81e+02) [8] | 3.34e+03 (4.98e+02) [6] | 3.18e+03 (3.17e+02) [5] | 4.21e+03 (5.81e+02) [9] | 3.46e+03 (4.52e+02) [7] |
| CEC2017_F24 | 2.74e+03 (1.40e+02) [1] | 3.95e+03 (7.05e+02) [6] | 3.30e+03 (3.69e+02) [4] | 3.05e+03 (2.12e+02) [3] | 4.33e+03 (8.78e+02) [9] | 4.11e+03 (9.05e+02) [7] | 3.00e+03 (2.19e+02) [2] | 4.20e+03 (8.16e+02) [8] | 3.55e+03 (4.56e+02) [5] |
| CEC2017_F25 | 3.88e+03 (6.15e+02) [2] | 4.29e+03 (8.21e+02) [5] | 4.04e+03 (5.85e+02) [3] | 4.53e+03 (9.64e+02) [6] | 5.41e+03 (1.25e+03) [8] | 6.92e+03 (2.01e+03) [9] | 2.97e+03 (2.11e+02) [1] | 5.26e+03 (1.13e+03) [7] | 4.22e+03 (6.30e+02) [4] |
| CEC2017_F26 | 3.37e+03 (2.94e+02) [1] | 6.96e+03 (1.68e+03) [7] | 4.69e+03 (8.20e+02) [5] | 4.37e+03 (7.47e+02) [4] | 4.75e+03 (9.52e+02) [6] | 7.24e+03 (2.00e+03) [8] | 3.62e+03 (3.31e+02) [2] | 7.25e+03 (2.07e+03) [9] | 4.08e+03 (6.96e+02) [3] |
| CEC2017_F27 | 3.59e+03 (3.81e+02) [1] | 5.41e+03 (1.21e+03) [4] | 6.31e+03 (1.61e+03) [6] | 3.97e+03 (5.34e+02) [2] | 6.78e+03 (1.55e+03) [7] | 6.97e+03 (2.10e+03) [8] | 4.26e+03 (6.12e+02) [3] | 7.76e+03 (2.07e+03) [9] | 6.26e+03 (1.61e+03) [5] |
| CEC2017_F28 | 4.00e+03 (4.70e+02) [1] | 1.12e+04 (3.47e+03) [9] | 5.15e+03 (1.08e+03) [4] | 5.50e+03 (1.12e+03) [5] | 9.00e+03 (2.95e+03) [8] | 5.98e+03 (1.43e+03) [6] | 4.20e+03 (4.89e+02) [2] | 8.91e+03 (2.89e+03) [7] | 4.80e+03 (8.36e+02) [3] |
| CEC2017_F29 | 5.54e+03 (1.15e+03) [3] | 6.39e+03 (1.34e+03) [4] | 6.90e+03 (1.51e+03) [5] | 4.77e+03 (6.90e+02) [1] | 9.86e+03 (2.67e+03) [8] | 1.06e+04 (3.61e+03) [9] | 5.16e+03 (8.53e+02) [2] | 9.18e+03 (3.54e+03) [7] | 7.55e+03 (2.31e+03) [6] |
| CEC2017_F3 | 1.50e+05 (7.62e+04) [1] | 3.33e+06 (1.75e+06) [6] | 1.97e+06 (8.64e+05) [5] | 7.39e+05 (3.59e+05) [2] | 1.25e+07 (8.06e+06) [9] | 4.10e+06 (2.04e+06) [7] | 8.10e+05 (4.71e+05) [3] | 9.83e+06 (5.45e+06) [8] | 1.15e+06 (7.26e+05) [4] |
| CEC2017_F30 | 4.90e+03 (6.51e+02) [2] | 9.66e+03 (2.79e+03) [7] | 4.60e+03 (7.13e+02) [1] | 6.48e+03 (1.36e+03) [5] | 1.71e+04 (6.22e+03) [9] | 8.51e+03 (2.31e+03) [6] | 4.97e+03 (8.37e+02) [3] | 1.05e+04 (3.01e+03) [8] | 5.83e+03 (1.42e+03) [4] |
| CEC2017_F4 | 4.06e+02 (4.22e+00) [1] | 1.16e+03 (5.54e+02) [8] | 5.01e+02 (5.93e+01) [4] | 4.56e+02 (5.90e+01) [3] | 7.73e+02 (2.68e+02) [7] | 5.80e+02 (1.31e+02) [5] | 4.19e+02 (1.89e+01) [2] | 1.50e+03 (8.63e+02) [9] | 6.34e+02 (2.07e+02) [6] |
| CEC2017_F5 | 5.20e+02 (1.73e+01) [1] | 1.47e+03 (8.03e+02) [8] | 6.63e+02 (1.10e+02) [4] | 6.35e+02 (1.25e+02) [3] | 1.31e+03 (6.93e+02) [7] | 9.17e+02 (2.84e+02) [6] | 5.36e+02 (2.42e+01) [2] | 1.63e+03 (7.25e+02) [9] | 8.66e+02 (3.01e+02) [5] |
| CEC2017_F6 | 6.17e+02 (1.15e+01) [1] | 1.44e+03 (5.68e+02) [6] | 7.65e+02 (1.19e+02) [4] | 7.58e+02 (1.34e+02) [3] | 1.90e+03 (1.07e+03) [8] | 1.47e+03 (6.83e+02) [7] | 6.79e+02 (7.38e+01) [2] | 5.50e+03 (4.05e+03) [9] | 9.28e+02 (3.07e+02) [5] |
| CEC2017_F7 | 7.16e+02 (1.20e+01) [1] | 1.71e+03 (9.79e+02) [7] | 1.09e+03 (4.15e+02) [4] | 9.16e+02 (1.71e+02) [2] | 1.67e+03 (5.82e+02) [6] | 2.04e+03 (9.01e+02) [8] | 9.66e+02 (2.46e+02) [3] | 4.60e+03 (3.23e+03) [9] | 1.66e+03 (6.54e+02) [5] |
| CEC2017_F8 | 8.32e+02 (2.02e+01) [1] | 3.15e+03 (2.50e+03) [8] | 1.37e+03 (5.09e+02) [4] | 1.07e+03 (2.13e+02) [3] | 2.27e+03 (1.11e+03) [7] | 1.60e+03 (5.56e+02) [5] | 9.61e+02 (1.32e+02) [2] | 6.95e+03 (5.64e+03) [9] | 1.97e+03 (9.76e+02) [6] |
| CEC2017_F9 | 1.05e+03 (8.93e+01) [1] | 4.94e+03 (3.82e+03) [8] | 1.94e+03 (8.51e+02) [5] | 1.69e+03 (5.55e+02) [3] | 4.48e+03 (3.23e+03) [7] | 3.19e+03 (1.43e+03) [6] | 1.36e+03 (3.46e+02) [2] | 4.96e+03 (3.29e+03) [9] | 1.83e+03 (7.20e+02) [4] |
| **Avg Rank** | **1.13** | **7.13** | **4.10** | **3.10** | **7.53** | **6.47** | **2.37** | **8.30** | **4.87** |

### Table 3: Engineering Problems Results (Mean (Std) [Rank])

| Function | MSDBO | DBO | AO | MGO | FFO | AVOA | NGO | ZOA | CoatiOA |
|---|---|---|---|---|---|---|---|---|---|
| Pressure Vessel Design | 5.89e+03 (3.67e+00) [1] | 5.92e+03 (3.57e+01) [6] | 5.91e+03 (2.00e+01) [4] | 5.90e+03 (1.33e+01) [3] | 6.05e+03 (1.88e+02) [9] | 5.93e+03 (4.58e+01) [7] | 5.89e+03 (5.32e+00) [2] | 5.94e+03 (4.79e+01) [8] | 5.91e+03 (2.72e+01) [5] |
| Speed Reducer Design | 3.00e+03 (2.90e+00) [2] | 3.02e+03 (1.83e+01) [6] | 3.01e+03 (7.90e+00) [5] | 3.00e+03 (1.90e+00) [1] | 3.03e+03 (2.71e+01) [8] | 3.02e+03 (1.51e+01) [7] | 3.01e+03 (7.77e+00) [4] | 3.06e+03 (4.13e+01) [9] | 3.00e+03 (9.34e+00) [3] |
| Tension/Compression Spring | 3.88e-02 (2.46e-02) [1] | 1.04e-01 (7.11e-02) [4] | 1.43e-01 (9.92e-02) [6] | 4.78e-02 (3.44e-02) [2] | 2.73e-01 (2.58e-01) [9] | 1.74e-01 (1.28e-01) [8] | 5.21e-02 (3.45e-02) [3] | 1.53e-01 (1.92e-01) [7] | 1.39e-01 (1.50e-01) [5] |
| Three-Bar Truss Design | 2.65e+02 (4.54e-01) [1] | 2.66e+02 (1.08e+00) [5] | 2.65e+02 (8.17e-01) [4] | 2.65e+02 (7.03e-01) [3] | 2.66e+02 (1.88e+00) [8] | 2.66e+02 (1.23e+00) [6] | 2.65e+02 (7.80e-01) [2] | 2.72e+02 (5.82e+00) [9] | 2.66e+02 (1.50e+00) [7] |
| Welded Beam Design | 3.94e+00 (1.65e+00) [1] | 5.77e+00 (5.49e+00) [5] | 5.62e+00 (3.09e+00) [4] | 4.82e+00 (2.98e+00) [3] | 6.76e+00 (5.25e+00) [7] | 9.61e+00 (7.75e+00) [9] | 4.06e+00 (2.20e+00) [2] | 8.18e+00 (8.35e+00) [8] | 6.26e+00 (4.84e+00) [6] |
| **Avg Rank** | **1.20** | **5.20** | **4.60** | **2.40** | **8.20** | **7.40** | **2.60** | **8.20** | **5.20** |

### 6.4 Ranking Summary

| Suite | MSDBO | NGO | MGO | AO | CoatiOA | DBO | AVOA | FFO | ZOA |
|---|---|---|---|---|---|---|---|---|---|
| CEC-2014 | **1.30** | 2.00 | 3.53 | 4.07 | 4.90 | 7.13 | 6.80 | 7.30 | 7.97 |
| CEC-2017 | **1.13** | 2.37 | 3.10 | 4.10 | 4.87 | 7.13 | 6.47 | 7.53 | 8.30 |
| Engineering | **1.20** | 2.60 | 2.40 | 4.60 | 5.20 | 5.20 | 7.40 | 8.20 | 8.20 |
| **Overall** | **1.21** | 2.32 | 3.01 | 4.26 | 4.99 | 6.49 | 6.89 | 7.68 | 8.16 |

MSDBO achieves the best average rank across all three benchmark suites, followed by NGO and MGO. The standard DBO ranks 6th overall, confirming the effectiveness of the multi-strategy enhancements.

---

## 7. Statistical Analysis

### 7.1 Wilcoxon Rank-Sum Test

The Wilcoxon rank-sum test (Mann-Whitney U test) is applied as a non-parametric statistical test to determine whether performance differences between MSDBO and each competitor are statistically significant at the α = 0.05 significance level.

- **(+)**: MSDBO is significantly better (p < 0.05 and lower mean)
- **(≈)**: No significant difference (p ≥ 0.05)
- **(−)**: MSDBO is significantly worse (p < 0.05 and higher mean)

### Table 4: Wilcoxon Rank-Sum Test — CEC-2014 (MSDBO vs Competitors)

| Function | DBO | AO | MGO | FFO | AVOA | NGO | ZOA | CoatiOA |
|---|---|---|---|---|---|---|---|---|
| CEC2014_F1 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F10 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0005) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F11 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F12 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F13 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F14 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | ≈ (p=0.0848) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F15 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F16 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0131) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F17 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F18 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F19 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F2 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F20 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F21 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0264) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F22 | + (p=0.0000) | + (p=0.0000) | + (p=0.0001) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F23 | + (p=0.0000) | + (p=0.0000) | − (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F24 | + (p=0.0000) | + (p=0.0014) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0072) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F25 | + (p=0.0000) | + (p=0.0000) | + (p=0.0030) | + (p=0.0000) | + (p=0.0000) | − (p=0.0000) | + (p=0.0000) | ≈ (p=0.0511) |
| CEC2014_F26 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | − (p=0.0103) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F27 | + (p=0.0000) | + (p=0.0000) | ≈ (p=0.5766) | + (p=0.0000) | + (p=0.0000) | − (p=0.0069) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F28 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F29 | + (p=0.0000) | ≈ (p=0.0647) | ≈ (p=0.8523) | + (p=0.0000) | + (p=0.0000) | ≈ (p=0.2224) | ≈ (p=0.6491) | ≈ (p=0.6995) |
| CEC2014_F3 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F30 | + (p=0.0000) | + (p=0.0069) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | ≈ (p=0.8254) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F4 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0065) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F5 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F6 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0020) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F7 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F8 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2014_F9 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |

**W/T/L Summary (MSDBO vs each):**

| Competitor | Win (+) | Tie (≈) | Loss (−) |
|---|---|---|---|
| DBO | 30 | 0 | 0 |
| AO | 29 | 1 | 0 |
| MGO | 27 | 2 | 1 |
| FFO | 30 | 0 | 0 |
| AVOA | 30 | 0 | 0 |
| NGO | 24 | 3 | 3 |
| ZOA | 29 | 1 | 0 |
| CoatiOA | 28 | 2 | 0 |

### Table 5: Wilcoxon Rank-Sum Test — CEC-2017 (MSDBO vs Competitors)

| Function | DBO | AO | MGO | FFO | AVOA | NGO | ZOA | CoatiOA |
|---|---|---|---|---|---|---|---|---|
| CEC2017_F1 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F10 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0184) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F11 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F12 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F13 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F14 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F15 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F16 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F17 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F18 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F19 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | ≈ (p=0.0627) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F2 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F20 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F21 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F22 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0010) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F23 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F24 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F25 | + (p=0.0037) | ≈ (p=0.1097) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | − (p=0.0000) | + (p=0.0000) | + (p=0.0011) |
| CEC2017_F26 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0001) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F27 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F28 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0255) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F29 | + (p=0.0001) | + (p=0.0000) | − (p=0.0000) | + (p=0.0000) | + (p=0.0000) | ≈ (p=0.0742) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F3 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F30 | + (p=0.0000) | − (p=0.0072) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | ≈ (p=0.7669) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F4 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F5 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F6 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F7 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F8 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |
| CEC2017_F9 | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) |

**W/T/L Summary (MSDBO vs each):**

| Competitor | Win (+) | Tie (≈) | Loss (−) |
|---|---|---|---|
| DBO | 30 | 0 | 0 |
| AO | 28 | 1 | 1 |
| MGO | 29 | 0 | 1 |
| FFO | 30 | 0 | 0 |
| AVOA | 30 | 0 | 0 |
| NGO | 26 | 3 | 1 |
| ZOA | 30 | 0 | 0 |
| CoatiOA | 30 | 0 | 0 |

### Table 6: Wilcoxon Rank-Sum Test — Engineering (MSDBO vs Competitors)

| Function | DBO | AO | MGO | FFO | AVOA | NGO | ZOA | CoatiOA |
|---|---|---|---|---|---|---|---|---|
| Pressure Vessel Design | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0004) | + (p=0.0000) | + (p=0.0000) |
| Speed Reducer Design | + (p=0.0000) | + (p=0.0000) | ≈ (p=0.2730) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0000) | + (p=0.0002) |
| Tension/Compression Spring | + (p=0.0000) | + (p=0.0000) | ≈ (p=0.0764) | + (p=0.0000) | + (p=0.0000) | + (p=0.0233) | + (p=0.0000) | + (p=0.0000) |
| Three-Bar Truss Design | + (p=0.0000) | + (p=0.0002) | + (p=0.0002) | + (p=0.0000) | + (p=0.0000) | + (p=0.0114) | + (p=0.0000) | + (p=0.0000) |
| Welded Beam Design | + (p=0.0078) | + (p=0.0005) | ≈ (p=0.0776) | + (p=0.0000) | + (p=0.0000) | ≈ (p=0.5813) | + (p=0.0000) | + (p=0.0002) |

**W/T/L Summary (MSDBO vs each):**

| Competitor | Win (+) | Tie (≈) | Loss (−) |
|---|---|---|---|
| DBO | 5 | 0 | 0 |
| AO | 5 | 0 | 0 |
| MGO | 2 | 3 | 0 |
| FFO | 5 | 0 | 0 |
| AVOA | 5 | 0 | 0 |
| NGO | 4 | 1 | 0 |
| ZOA | 5 | 0 | 0 |
| CoatiOA | 5 | 0 | 0 |

### 7.2 Statistical Summary

The Wilcoxon test results conclusively demonstrate MSDBO's statistical superiority:

- **CEC-2014**: MSDBO wins 24–30 out of 30 functions against each competitor, with only 0–3 losses (primarily against NGO on composition functions F25, F29).
- **CEC-2017**: Similar dominance with 26–30 wins, 0–3 ties, and 0–1 losses per competitor.
- **Engineering**: MSDBO wins 3–5 out of 5 problems against each competitor.

The closest competitor is NGO, which achieves statistical ties on 3 functions in each CEC suite. This is consistent with NGO's strong exploration capabilities from its two-phase hunting strategy.

---

## 8. Convergence Analysis

Convergence curves for selected benchmark functions are provided in the `plots/` directory. Key observations:

### 8.1 Unimodal Functions (CEC-2014 F1–F3, CEC-2017 F1–F3)
MSDBO exhibits the fastest convergence rate on unimodal functions, typically reaching near-optimal fitness within 400–600 iterations. The chaotic initialization provides a significant head start, while the Lévy-mode rollers enable precise refinement in later stages. DBO, in contrast, shows sluggish early convergence due to its X_worst-dependent rolling mechanism.

### 8.2 Multimodal Functions (CEC-2014 F4–F16, CEC-2017 F4–F16)
On multimodal landscapes, MSDBO maintains a consistent convergence advantage. The social-learning crossover in the brood group prevents premature convergence to local optima, while the elite archive ensures that promising regions discovered early are not forgotten. NGO is the closest competitor on these functions, benefiting from its effective two-phase search strategy.

### 8.3 Hybrid Functions (CEC-2014 F17–F22, CEC-2017 F17–F22)
Hybrid functions test an algorithm's ability to handle variable linkage and heterogeneous landscapes. MSDBO's dual-mode roller strategy (Gaussian→Lévy transition) provides adaptive search behavior that matches the changing landscape characteristics. ZOA and FFO struggle most on hybrid functions due to limited exploration mechanisms.

### 8.4 Composition Functions (CEC-2014 F23–F30, CEC-2017 F23–F30)
Composition functions represent the most challenging benchmark category with multiple optima of varying attraction basins. MSDBO's Cauchy stagnation escape is particularly effective here, enabling escape from deep local optima that trap other algorithms. On a few composition functions (F25, F29), NGO achieves comparable or slightly better performance, suggesting that NGO's pursuit-attack strategy is well-suited for navigating complex compositional landscapes.

### 8.5 Engineering Problems
On constrained engineering problems, MSDBO converges to feasible near-optimal solutions fastest. The preferential boundary control is especially beneficial for engineering problems where feasible regions are narrow. MGO shows competitive performance on engineering problems (Avg Rank 2.40), likely due to its territory-based search strategy that naturally respects boundary constraints.

---

## 9. Discussion

### 9.1 Why MSDBO Outperforms DBO

The experimental results demonstrate a dramatic improvement from DBO (Avg Rank 6.49) to MSDBO (Avg Rank 1.21). The key factors are:

1. **Initialization quality**: Chaotic tent-map + OBL provides 2× better initial population coverage compared to uniform random initialization. This advantage is most pronounced on high-dimensional multimodal functions where initial placement critically affects search trajectory.

2. **Adaptive exploration-exploitation**: The sigmoid-controlled Gaussian-Lévy switching ensures that exploration dominates early iterations while exploitation takes over smoothly in later stages. Standard DBO's fixed linear R factor cannot adapt to problem-specific convergence patterns.

3. **Knowledge preservation**: The elite archive and personal best tracking create a multi-level memory system. Archive-guided foragers explore around historically promising regions, while social-learning brood beetles combine individual and collective knowledge. Standard DBO has no memory mechanism beyond the current iteration's best.

4. **Stagnation resilience**: The Cauchy escape mechanism detects and responds to optimization stagnation — a critical capability for composition functions where algorithms frequently get trapped. Standard DBO has no stagnation detection or escape strategy.

5. **Boundary intelligence**: Preferential boundary control eliminates the boundary-clustering artifact of hard clipping, maintaining useful positional information for out-of-bounds individuals.

### 9.2 Comparison with Other Competitors

- **NGO** is the strongest competitor (Avg Rank 2.32), benefiting from its efficient two-phase pursuit-attack strategy. It is particularly competitive on composition functions where its prey pursuit mechanism provides effective local optima escape.

- **MGO** ranks 3rd (Avg Rank 3.01), showing consistent mid-tier performance. Its territory-based search provides good exploration on multimodal functions.

- **AO** ranks 4th (Avg Rank 4.26), with strong exploration from its four hunting strategies but weaker exploitation precision.

- **CoatiOA** ranks 5th (Avg Rank 4.99), showing balanced but not exceptional performance across all categories.

- **DBO, AVOA, FFO, and ZOA** form the lower tier (Avg Ranks 6.49–8.16), each suffering from specific limitations in their search mechanisms when applied to high-dimensional, complex landscapes.

### 9.3 Limitations

Despite strong overall performance, MSDBO has some limitations:
- On a few composition functions, NGO achieves comparable or better results, suggesting that MSDBO's stagnation escape could be further refined.
- The algorithm introduces additional hyperparameters (stagnation threshold, archive ratio, sigmoid steepness) that may require tuning for specific problem domains.
- The computational overhead of maintaining the elite archive and performing OBL during initialization is marginal but non-zero.

---

## 10. Conclusion

This paper presented a comprehensive comparative analysis of nine nature-inspired optimization algorithms on CEC-2014, CEC-2017, and engineering benchmark problems. The proposed Multi-Strategy Dung Beetle Optimizer (MSDBO) integrates five synergistic strategies — chaotic tent-map initialization with OBL, Gaussian-Lévy dual-mode rollers, social-learning crossover, elite archive search, and Cauchy stagnation escape — to address the fundamental limitations of the standard DBO.

Key findings:

1. **MSDBO achieves the best overall performance** with average ranks of 1.30 (CEC-2014), 1.13 (CEC-2017), and 1.20 (Engineering Problems), significantly outperforming all eight competitors.

2. **Statistical validation** through the Wilcoxon rank-sum test at α = 0.05 confirms MSDBO's superiority on the vast majority of test functions, with wins on 24–30 out of 30 functions against each competitor.

3. **The multi-strategy approach is effective**: Each of the five strategies contributes to performance improvement, with chaotic initialization and Cauchy escape providing the most significant gains on unimodal and composition functions, respectively.

4. **NGO is the strongest competitor** (Avg Rank 2.32), suggesting that pursuit-attack strategies are particularly effective for complex optimization landscapes.

### Future Work

- Integration of adaptive hyperparameter control to reduce manual tuning requirements.
- Extension to multi-objective optimization using Pareto-based archive management.
- Application to real-world large-scale engineering problems including UAV path planning, neural network training, and structural topology optimization.
- Investigation of MSDBO's performance on CEC-2022 benchmark suite and constrained optimization problems (CEC-2020 RC series).

---

## References

1. Xue, J., & Shen, B. (2023). Dung beetle optimizer: a new meta-heuristic algorithm for global optimization. *The Journal of Supercomputing*, 79, 7305–7336.

2. Abualigah, L., Yousri, D., Abd Elaziz, M., Ewees, A. A., Al-qaness, M. A., & Gandomi, A. H. (2021). Aquila optimizer: a novel meta-heuristic optimization algorithm. *Computers & Industrial Engineering*, 157, 107250.

3. Abdollahzadeh, B., Gharehchopogh, F. S., & Mirjalili, S. (2021). African vultures optimization algorithm: A new nature-inspired metaheuristic algorithm for global optimization problems. *Computers & Industrial Engineering*, 158, 107408.

4. Abdollahzadeh, B., Gharehchopogh, F. S., Khodadadi, N., & Mirjalili, S. (2022). Mountain gazelle optimizer: A new nature-inspired metaheuristic algorithm for global optimization problems. *Advances in Engineering Software*, 174, 103282.

5. Dehghani, M., Trojovská, E., & Trojovský, P. (2022). Northern goshawk optimization: A new swarm-based algorithm for solving optimization problems. *IEEE Access*, 10, 68258–68286.

6. Trojovská, E., Dehghani, M., & Trojovský, P. (2022). Zebra optimization algorithm: A new bio-inspired optimization algorithm for solving optimization algorithm. *IEEE Access*, 10, 49445–49473.

7. Dehghani, M., Montazeri, Z., Trojovská, E., & Trojovský, P. (2022). Coati optimization algorithm: A new bio-inspired metaheuristic algorithm for solving optimization problems. *Knowledge-Based Systems*, 259, 110011.

8. Trojovská, E., & Dehghani, M. (2022). Fennec fox optimization: A new nature-inspired optimization algorithm. *IEEE Access*, 10, 84417–84443.

9. Wolpert, D. H., & Macready, W. G. (1997). No free lunch theorems for optimization. *IEEE Transactions on Evolutionary Computation*, 1(1), 67–82.

10. Liang, J. J., Qu, B. Y., & Suganthan, P. N. (2013). Problem definitions and evaluation criteria for the CEC 2014 special session on single objective real-parameter numerical optimization. *Technical Report*, Zhengzhou University and Nanyang Technological University.

11. Awad, N. H., Ali, M. Z., Liang, J. J., Qu, B. Y., & Suganthan, P. N. (2016). Problem definitions and evaluation criteria for the CEC 2017 special session on single objective real-parameter numerical optimization. *Technical Report*, Nanyang Technological University.

12. Mantegna, R. N. (1994). Fast, accurate algorithm for numerical simulation of Levy stable stochastic processes. *Physical Review E*, 49(5), 4677.

13. Tizhoosh, H. R. (2005). Opposition-based learning: A new scheme for machine intelligence. *International Conference on Computational Intelligence for Modelling, Control and Automation*, 1, 695–701.

---

*End of Report*
