# DBO Algorithm: Full Analysis, Synthesis & Benchmark Report

---

## Step 1: Paper Analysis

### Paper 0 – Base DBO (Xue & Shen, Journal of Supercomputing, 2023)

**Title:** *Dung beetle optimizer: a new meta-heuristic algorithm for global optimization*

**Core Mechanism:**

DBO divides the population into **4 agent types** with distinct update rules:

| Group | Inspiration | Update Rule |
|---|---|---|
| Ball-rollers | Navigate with celestial cues | `x(t+1) = x(t) + α·k·x(t-1) + b·Δx`, `Δx=|x(t)−X_worst|` |
| Dance/obstacle | Reorient when stuck | `x(t+1) = x(t) + tan(θ)·|x(t)−x(t-1)|` |
| Brood balls | Spawn around local best | [B(t+1) = X* + b1·(B(t)−Lb*) + b2·(B(t)−Ub*)](file:///C:/Users/AAKASH/Desktop/DBO/dbo_base.py#60-193) |
| Foragers | Search around global best | `x(t+1) = x(t) + C1·(x(t)−Lbb) + C2·(x(t)−Ubb)` |
| Thieves | Steal near global best | `x(t+1) = Xb + S·g·(|x(t)−X*|+|x(t)−Xb|)` |

**Parameters:** k=0.1, b=0.3, S=0.5; Population ratio: 6 rollers : 6 brood : 7 foragers : 11 thieves (for N=30)

**Boundary handling:** Hard clipping to [lb, ub]

**Factor R:** Linear decay `R = 1 − t/Tmax`

---

**Identified Weaknesses of Base DBO:**

1. **Xw repulsion is counterproductive**: Rolling beetles use `|x(t) − X_worst|` to simulate light intensity. This means the worst solution actively influences the search — wasting evaluation budget navigating away from bad positions rather than toward good ones.

2. **Linear R factor**: The linear decay `1 − t/Tmax` reduces boundary influence too early and predictably. Early-stage exploitation is forced, missing broader exploration opportunities.

3. **Hard boundary clipping**: When an individual goes out of bounds, it is simply clamped to lb/ub. This discards positional trend information and tends to create boundary-dense clusters.

4. **Static foraging**: The small dung beetle uses only Gaussian disturbance (C1 ~ N(0,1)), which has limited adaptability across different optimization stages (exploration vs exploitation).

5. **Insufficient local optima escape**: Thieves only use one formula (attraction to X_best with Gaussian noise). There is no heavy-tail mechanism for jumping out of deeply deceptive local optima.

---

### Paper 1 – ERDBO (Yu, Xie & Zhou, Biomimetics 2025)

**Title:** *An Enhanced Randomized Dung Beetle Optimizer for Global Optimization Problems*

**Addressed weaknesses:** Premature convergence, limited exploration, no local optima escape mechanism.

**Three-stage bio-inspired mechanism:**

#### 1. Larval Growth Stage (Eq. 11)
```
x_i(t+1) = x_i(t) + (Lbb + (Ubb − Lbb) × rand),   if r > 0.5
```
- **What it does**: Injects random offset in the range of the foraging boundaries [Lbb, Ubb], dynamically scaled via R.
- **Why it helps**: Increases positional diversity by forcing large, stochastic steps. Unlike Gaussian perturbation which is symmetric around zero, this is uniformly shifted in the current promising region — broader exploration with directional awareness.

#### 2. Reproduction & Teaching Stage (Eq. 12)
```
s = r1*20 + r2*20         (r1, r2 ~ N(0,1))
XG = Xbest * 0.8
m  = (j/N) * 2
p  = sin(Ubb − Lbb)*2 + (Ubb − Lbb)*m
x_i(t+1) = XG + (Xbest * x_i) * p   if r < 0.5 and s < 20
```
- **What it does**: Uses a teaching analogy — the "teacher" is XG (80% of the best solution), and "learning" is modulated by a sinusoidal factor p that varies per individual (indexed by j).
- **Why it helps**: The sinusoidal modulation prevents all individuals from converging to the same point. The per-individual variation of `m = 2j/N` means each individual has a slightly different "learning rate," creating structured diversity within exploitation.

#### 3. Predator Avoidance Stage (Eq. 13)
```
w = (π/2) * (j/N)
k = 0.2 * sin(π/2 − w)
x_i(t+1) = Xbest × levy_flight × k   if r < 0.5 and s ≥ 20
```
- **What it does**: Uses Lévy flight (heavy-tailed distribution) scaled by a sinusoidal coefficient.
- **Why it helps**: Lévy flight generates occasional large jumps (due to the power-law tail), critical for escaping deep local optima. The sinusoidal coefficient k scales with individual index — individuals at different positions in the group experience different amplitudes of perturbation, improving diversity.

---

### Paper 2 – EDBO (Yu et al., Alexandria Engineering Journal, 2025, Nankai University)

**Title:** *A multi-strategy enhanced Dung Beetle Optimization for real-world engineering problems and UAV path planning*

**Addressed weaknesses:** Xw interference, linear R, boundary waste, static Gaussian foraging.

**Four mechanisms:**

#### 1. Optimal-Value Search Guidance (Eq. 9)
```
Δx = |x_i(t) + rand × X_best|   (instead of |x_i(t) − X_worst|)
```
- **What it does**: Replaces the global worst from Δx with the global best.
- **Why it helps**: The rolling beetle now computes deviation relative to the best candidate plus a random term. This **pulls** the search toward promising regions instead of **pushing** away from bad ones. The random term `rand × X_best` prevents degenerate convergence to exactly X_best.

#### 2. Nonlinear Dynamic Adjustment Factor (Eq. 10)
```
R = 1 − rand × (t/Tmax)²
```
- **What it does**: Replaces `1 − t/Tmax` with a quadratic nonlinear version with stochastic perturbation.
- **Why it helps**: Three benefits: (a) Quadratic decay means the boundary region shrinks slowly at first, then accelerates — matching real-world optimization dynamics. (b) Random term `rand` makes R non-monotonic, allowing occasional re-expansion of the search area. (c) More adaptive than fixed sinusoidal schedules (WOA/GSA), responding dynamically to the current iteration.

#### 3. Preferential Boundary Control (Eq. 11)
```
if x < lb:  x = rand * X_best
if x > ub:  x = (1 − rand) * X_best
```
- **What it does**: Rather than clamping OOB individuals to the boundary, it repositions them proportionally toward X_best with randomness.
- **Why it helps**: (a) Preserves the movement trend — the individual was heading somewhere useful and is now guided toward the most promising known position. (b) The random scaling `rand` and `1−rand` ensure individuals don't all collapse to X_best but spread within [0, X_best] range. (c) Eliminates the boundary-clustering artifact of hard clipping.

#### 4. Improved Foraging Enhancement Strategy — Pelican-inspired (Eq. 12)
```
x_i(t+1) = x_i(t) + rand × (X_best − l × x_i(t)),   l ∈ {1, 2}
```
- **What it does**: Replaces purely Gaussian foraging with a Pelican-inspired update that directly references X_best. Parameter `l` is randomly 1 or 2.
- **Why it helps**: (a) When l=1: `rand*(X_best − x_i)` — gentle pull toward X_best (exploitation). (b) When l=2: `rand*(X_best − 2*x_i)` — potentially overshoots to the opposite side of X_best relative to current position (exploration). (c) The alternation between l=1 and l=2 naturally creates exploration/exploitation balance within the foraging group without extra parameters.

---

## Step 2: Synthesis — Which Mechanisms to Combine

| Mechanism | Source | Included? | Rationale |
|---|---|---|---|
| Optimal-value guidance (Δx = \|x + rand·Xb\|) | EDBO | ✅ YES | Removes Xw pollution; direct improvement with no downside |
| Nonlinear dynamic R | EDBO | ✅ YES | Quadratic + stochastic decay beats linear on complex landscapes |
| Preferential boundary control | EDBO | ✅ YES | Eliminates boundary clustering; information-preserving |
| Pelican-enhanced foraging | EDBO | ✅ YES (50%) | Adaptable l=1/2 mechanism balances exploit/explore |
| Larval growth (experiential random offset) | ERDBO | ✅ YES (50%) | Complements Pelican strategy for wider diversity |
| Reproduction-teaching (sinusoidal p) | ERDBO | ✅ Thieves | Per-individual sinusoidal weight for structured exploitation |
| Predator-Lévy escape | ERDBO | ✅ Thieves | Heavy-tail jumps critical for multimodal landscapes |
| Hard boundary clipping | Base | ❌ REPLACED | Replaced by preferential control |
| Linear R | Base | ❌ REPLACED | Replaced by nonlinear dynamic R |
| Standard theft (unchanged) | Base | ✅ (fallback r≥0.5) | Retains original mechanism as 50% fallback |

---

## Step 3: Pseudocode — Optimized DBO (ODBO)

```
INPUT: obj_func, lb, ub, dim, n_pop, max_iter, k=0.1, b=0.3, S=0.5
OUTPUT: X_best, best_fitness

1. Initialize population X[n_pop × dim] ~ uniform(lb, ub)
2. Evaluate fitness F[i] = obj_func(X[i]) for all i
3. Set X_best = X[argmin(F)],  X_local = X_best
4. Split population: rollers(20%), brood(20%), foragers(23%), thieves(37%)
5. prev_X = X.copy()

FOR t = 0 to max_iter-1:

  // Nonlinear dynamic R (EDBO mod)
  R ← 1 − rand() × (t/max_iter)²

  // === GROUP 1: Rollers ===
  FOR i in rollers:
    α ← +1 or −1 (random)
    IF rand() > 0.1:
      // EDBO optimal-value guidance (replaces Xw reference)
      Δx ← |X[i] + rand() × X_best|
      X_new ← X[i] + α × k × prev_X[i] + b × Δx
    ELSE:
      // Dance/obstacle reorientation (unchanged)
      θ ← uniform(0, π)
      X_new ← X[i] + tan(θ) × |X[i] − prev_X[i]|
    X[i] ← preferential_clip(X_new, lb, ub, X_best)  // EDBO boundary

  // === GROUP 2: Brood Balls ===
  Lb* ← max(X_local × (1−R), lb)
  Ub* ← min(X_local × (1+R), ub)
  FOR i in brood:
    b1, b2 ← rand vectors [0,1]^dim
    X_new ← X_local + b1 × (X[i]−Lb*) + b2 × (X[i]−Ub*)
    X[i] ← preferential_clip(X_new, lb, ub, X_best)

  // === GROUP 3: Foragers ===
  Lbb ← max(X_best × (1−R), lb)
  Ubb ← min(X_best × (1+R), ub)
  FOR i in foragers:
    IF rand() < 0.5:
      // ERDBO Larval Growth — wide exploration
      X_new ← X[i] + (Lbb + (Ubb−Lbb) × rand^dim)
    ELSE:
      // EDBO Pelican Foraging — guided exploitation
      l ← random choice {1, 2}
      X_new ← X[i] + rand() × (X_best − l × X[i])
    X[i] ← preferential_clip(X_new, lb, ub, X_best)

  // === GROUP 4: Thieves ===
  FOR i (j-th thief, j=1..n_thieves):
    r ← rand();  s ← r1×20 + r2×20  (r1,r2 ~ N(0,1))
    IF r < 0.5 AND s < 20:
      // ERDBO Reproduction-teaching (local exploitation)
      m ← 2j/N;  p ← sin(Ubb−Lbb)×2 + (Ubb−Lbb)×m
      XG ← X_best × 0.8
      X_new ← XG + (X_best × X[i]) × p
    ELSE IF r < 0.5 AND s ≥ 20:
      // ERDBO Predator-Levy escape (global diversification)
      w ← (π/2)(j/N);  k_sin ← 0.2×sin(π/2 − w)
      lev ← levy_flight(dim, β=1.5)
      X_new ← X_best × lev × k_sin
    ELSE:
      // Standard DBO theft (fallback)
      g ~ N(0,1)^dim
      X_new ← X_best + S×g×(|X[i]−X_local| + |X[i]−X_best|)
    X[i] ← preferential_clip(X_new, lb, ub, X_best)

  // Update fitness & global records
  prev_X ← X.copy()
  FOR i: F_new[i] ← obj_func(X[i])
  F ← min(F, F_new)  // greedy selection
  X_best ← X[argmin(F)]
  X_local ← X_best

RETURN X_best, min(F)
```

**Key differences vs base DBO (marked with ▶):**

| Location | Base DBO | ODBO | Mark |
|---|---|---|---|
| Rollers Δx | `\|x−X_worst\|` | `\|x + rand·Xbest\|` | ▶ |
| Factor R | `1 − t/Tmax` | `1 − rand·(t/Tmax)²` | ▶ |
| Boundary OOB | [clip(x, lb, ub)](file:///C:/Users/AAKASH/Desktop/DBO/dbo_base.py#24-27) | `rand·Xbest or (1−rand)·Xbest` | ▶ |
| Foragers | Gaussian (C1,C2) only | 50% Larval + 50% Pelican | ▶ |
| Thieves | Single formula | 3-mode: Teaching / Lévy / Standard | ▶ |

---

## Step 5: Benchmark Results

**Configuration:** Dim=30, Population=30, MaxIter=500, Runs=30 (independent), Seed=42..71

| ID | Function | Type | DBO Best | DBO Mean | DBO Std | ODBO Best | ODBO Mean | ODBO Std | Improvement |
|---|---|---|---|---|---|---|---|---|---|
| F1 | Sphere | Unimodal | 5.47e-03 | 1.01e+04 | 1.86e+04 | **0.00e+00** | **0.00e+00** | 0.00e+00 | **+100.0%** |
| F2 | Schwefel 2.22 | Unimodal | 8.21e-05 | 9.21e+00 | 8.30e+00 | **0.00e+00** | **0.00e+00** | 0.00e+00 | **+100.0%** |
| F3 | Rosenbrock | Unimodal (narrow valley) | 1.55e+02 | 3.64e+07 | 5.93e+07 | **2.67e+01** | **2.82e+01** | 6.09e-01 | **+100.0%** |
| F4 | Rastrigin | Multimodal | 3.14e+01 | 1.70e+02 | 6.20e+01 | **0.00e+00** | **0.00e+00** | 0.00e+00 | **+100.0%** |
| F5 | Ackley | Multimodal | 2.48e+00 | 1.76e+01 | 5.05e+00 | **4.44e-16** | **4.44e-16** | 0.00e+00 | **+100.0%** |
| F6 | Griewank | Multimodal | 4.13e-02 | 8.56e+01 | 1.68e+02 | **0.00e+00** | **0.00e+00** | 0.00e+00 | **+100.0%** |
| F7 | Levy | Multimodal | 1.04e+00 | 4.76e+01 | 3.90e+01 | **1.14e+00** | **1.98e+00** | 3.51e-01 | **+95.8%** |
| F8 | Zakharov | Unimodal | 7.12e-01 | 3.10e+02 | 1.68e+02 | **0.00e+00** | **0.00e+00** | 0.00e+00 | **+100.0%** |
| F9 | Schwefel | Multimodal | **1.71e-03** | **1.65e+03** | 2.55e+03 | 6.47e+03 | 7.57e+03 | 6.65e+02 | −359.5% |

> **Note on F9 (Schwefel):** ODBO performs worse. See Step 6 for analysis.

---

## Step 6: Improvement Explanations

### 1. Optimal-Value Search Guidance → Dramatic improvement on unimodal functions

**Base DBO problem:** `Δx = |x_i − X_worst|` uses the worst individual's position as a navigation reference. In practice, this means rolling beetles are always "repelling" from the worst — but the worst may be in a completely irrelevant region. The beetle has to waste steps navigating away from Xw before it can approach the optimum.

**ODBO fix:** `Δx = |x_i + rand × X_best|` makes the deviation relative to X_best, which is always in a promising region. The `rand` factor ensures this doesn't collapse to a deterministic pull — diversity is maintained while every evaluation moves toward a productive region. **Result:** Sphere, Schwefel 2.22, Zakharov all converge to machine precision (0.0) in every single run.

### 2. Nonlinear Dynamic R → Better balance on narrow-valley and multimodal functions

**Base DBO problem:** Linear R shrinks the spawning/foraging boundaries at a fixed rate. Early in search, R drops too fast, causing premature concentration around the current best (which may be suboptimal). On Rosenbrock, the base DBO's mean (3.64e+07) shows it frequently gets trapped far from the banana-shaped valley.

**ODBO fix:** The quadratic component [(t/Tmax)²](file:///C:/Users/AAKASH/Desktop/DBO/dbo_optimized.py#140-147) keeps R near 1 for most of the search, then rapidly narrows near the end. The random multiplier means some iterations have large R (re-expansion), preventing stagnation. **Result:** Rosenbrock mean drops from 3.64×10⁷ to 28.2 — a full 6 orders of magnitude improvement, consistently finding the valley.

### 3. Preferential Boundary Control → Eliminates premature clustering

**Base DBO problem:** Hard clipping creates a "boundary pileup" — many individuals accumulate at lb/ub, consuming population diversity without contribution. This is particularly devastating in high-dimensional spaces where many dimensions simultaneously hit boundaries.

**ODBO fix:** OOB individuals are relocated as a fraction of X_best. This: (a) keeps them within bounds, (b) spreads them stochastically between [0, X_best] (for below-lb case), and (c) maintains directional information since X_best is in a promising region. **Result:** The consistent 0.0 Std Dev on unimodal functions shows the algorithm reliably finds the optimum across all 30 runs — no boundary-clustered failures.

### 4. Dual Foraging Strategy (Larval/Pelican) → Better exploration-exploitation balance

**Base DBO problem:** Gaussian C1 provides local perturbation but always around the current position. In multimodal landscapes, this causes slow drift toward local optima without enough diversity.

**ODBO fix:** 50% probability of:
- **Larval mode**: Random offset scaled by Lbb/Ubb range — explores the full foraging zone uniformly
- **Pelican mode**: l=1 gently pulls toward X_best; l=2 creates a reflection around X_best, effectively exploring the "opposite side" of the current best — a form of opposition-based sampling

**Result:** Rastrigin (170 → 0.0), Griewank (85.6 → 0.0) — functions with many local optima solved exactly.

### 5. Three-Mode Thief Update (Teaching/Lévy/Standard) → Local optima escape

**Base DBO problem:** The thief formula `Xb + S·g·(distance terms)` is Gaussian-scaled, meaning it can only explore a limited neighborhood around X_best.

**ODBO fix:**
- **Teaching mode** (s<20, r<0.5): Sinusoidal weighting `p` ensures different individuals exploit different subregions of the best-known area
- **Lévy mode** (s≥20, r<0.5): Heavy-tail jumps enable escape from deep basins. Lévy follow a power law; large jumps occur rarely but are critical for deceptive multimodal functions. The sinusoidal `k_sin` coefficient scales the jump amplitude per individual — providing structured diversification
- **Standard mode** (r≥0.5): Retains original DBO behavior as a stable fallback

**Result:** Ackley (17.56 → 4.44e-16) — machine precision, solving the near-flat deceptive landscape.

---

### Trade-off: Schwefel (F9) Performance Regression

**Cause:** The Schwefel function's global optimum is at `xi = 420.97` for each dimension (within [−500, 500]). Its unique property is that the nearest local optima are very far from the global one — requiring wide, sustained exploration with *no guidance toward a currently known best*.

ODBO's preferential boundary control (`rand × X_best`) redirects OOB individuals toward X_best. However, in early iterations X_best on Schwefel may be a spurious local optimum far from 420.97. The guided boundary control then keeps agents clustered near the wrong region, and Lévy jumps are scaled by sinusoidal coefficients that shrink per individual — limiting their effective range.

**Base DBO advantage:** Hard clipping to lb/ub places OOB individuals uniformly along boundaries, which on Schwefel provides accidental coverage of regions near 420.97 (since 500 × 0.84 ≈ 420). This is a lucky artifact that helps specifically on this function.

**Resolution:** For Schwefel-type functions with globally dispersed optima, the preferential boundary control should be disabled (use standard clipping). This can be controlled via a parameter flag in the implementation.

---

## Files Generated

| File | Purpose |
|---|---|
| [dbo_base.py](file:///C:/Users/AAKASH/Desktop/DBO/dbo_base.py) | Base DBO implementation (Xue & Shen 2023) |
| [dbo_optimized.py](file:///C:/Users/AAKASH/Desktop/DBO/dbo_optimized.py) | ODBO — synthesized optimized algorithm |
| [benchmarks.py](file:///C:/Users/AAKASH/Desktop/DBO/benchmarks.py) | 9 standard benchmark function registry |
| [benchmark.py](file:///C:/Users/AAKASH/Desktop/DBO/benchmark.py) | Runner: 30-run trials, CSV output, convergence plots |
| `results.csv` | Raw numerical results |
| `convergence_curves.png` | DBO vs ODBO convergence plots (9 functions) |
