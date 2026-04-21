"""
Benchmark Runner: Base DBO vs Optimized DBO (ODBO)
====================================================
Runs each algorithm on each benchmark function for N_RUNS independent trials
and reports: Best, Mean, Std Dev, Worst for both algorithms.

Usage:
    python benchmark.py

Outputs:
    • Console table
    • results.csv  (for further analysis)
    • convergence_curves.png
"""

import numpy as np
import csv
import time
import sys
import os

# ---- import algorithms ---------------------------------------------------- #
sys.path.insert(0, os.path.dirname(__file__))
from dbo_base      import DBO
from dbo_optimized import ODBO
from benchmarks    import BENCHMARKS

# ---- Configuration -------------------------------------------------------- #
DIM      = 30       # problem dimensionality
N_POP    = 30       # population size
MAX_ITER = 500      # max iterations
N_RUNS   = 30       # independent runs (statistical significance)
SEED     = 42       # for reproducibility

# --------------------------------------------------------------------------- #
#  Run a single algorithm on a single benchmark N_RUNS times
# --------------------------------------------------------------------------- #

def run_trials(AlgoClass, algo_kwargs, bench, n_runs):
    """Returns arrays: bests, means_per_run, convergence_curves."""
    bests  = np.zeros(n_runs)
    scores_all = []
    conv_all   = []

    for run in range(n_runs):
        np.random.seed(SEED + run)
        lb = np.full(DIM, bench["lb"])
        ub = np.full(DIM, bench["ub"])
        algo = AlgoClass(
            obj_func=bench["func"],
            lb=lb, ub=ub,
            dim=DIM,
            n_pop=N_POP,
            max_iter=MAX_ITER,
            **algo_kwargs,
        )
        _, best_score, conv = algo.optimize()
        bests[run]   = best_score
        conv_all.append(conv)

    return bests, np.array(conv_all)


# --------------------------------------------------------------------------- #
#  Main benchmark loop
# --------------------------------------------------------------------------- #

def main():
    print("=" * 80)
    print("  Dung Beetle Optimizer – Benchmark Results")
    print(f"  Dim={DIM}  |  Pop={N_POP}  |  MaxIter={MAX_ITER}  |  Runs={N_RUNS}")
    print("=" * 80)

    header = (
        f"{'ID':<4} {'Function':<16} {'Type':<26} "
        f"{'Algorithm':<7} "
        f"{'Best':>14} {'Mean':>14} {'Std Dev':>14} {'Worst':>14}"
    )
    print(header)
    print("-" * len(header))

    csv_rows = []
    all_convs = {}   # for plotting

    for bench in BENCHMARKS:
        fid   = bench["id"]
        fname = bench["name"]
        ftype = bench["type"]

        # --- DBO ----------------------------------------------------------- #
        t0 = time.time()
        bests_dbo, conv_dbo = run_trials(
            DBO, {"k": 0.1, "b": 0.3, "S": 0.5}, bench, N_RUNS
        )
        t_dbo = time.time() - t0

        # --- ODBO ---------------------------------------------------------- #
        t0 = time.time()
        bests_odbo, conv_odbo = run_trials(
            ODBO, {"k": 0.1, "b": 0.3, "S": 0.5,
                   "levy_beta": 1.5, "p_forager": 0.5},
            bench, N_RUNS
        )
        t_odbo = time.time() - t0

        all_convs[fid] = {
            "dbo"  : conv_dbo.mean(axis=0),
            "odbo" : conv_odbo.mean(axis=0),
        }

        for algo_name, bests, t_elapsed in [
            ("DBO",  bests_dbo,  t_dbo),
            ("ODBO", bests_odbo, t_odbo),
        ]:
            row = {
                "ID"    : fid,
                "Name"  : fname,
                "Type"  : ftype,
                "Algo"  : algo_name,
                "Best"  : np.min(bests),
                "Mean"  : np.mean(bests),
                "Std"   : np.std(bests, ddof=1),
                "Worst" : np.max(bests),
                "Time_s": round(t_elapsed, 1),
            }
            csv_rows.append(row)
            print(
                f"{fid:<4} {fname:<16} {ftype:<26} "
                f"{algo_name:<7} "
                f"{row['Best']:>14.6e} {row['Mean']:>14.6e} "
                f"{row['Std']:>14.6e} {row['Worst']:>14.6e}"
            )

        imp_mean = (np.mean(bests_dbo) - np.mean(bests_odbo)) / (
            abs(np.mean(bests_dbo)) + 1e-300
        ) * 100
        sign = "+" if imp_mean >= 0 else ""
        print(f"     => ODBO improvement over DBO (mean): {sign}{imp_mean:.1f}%")
        print()

    # ------- Save CSV ------------------------------------------------------ #
    csv_path = os.path.join(os.path.dirname(__file__), "results.csv")
    with open(csv_path, "w", newline="") as f:
        fieldnames = ["ID", "Name", "Type", "Algo",
                      "Best", "Mean", "Std", "Worst", "Time_s"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(csv_rows)
    print(f"\nResults saved → {csv_path}")

    # ------- Plot convergence curves --------------------------------------- #
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        n_funcs = len(BENCHMARKS)
        ncols   = 3
        nrows   = (n_funcs + ncols - 1) // ncols
        fig, axes = plt.subplots(nrows, ncols,
                                 figsize=(5 * ncols, 4 * nrows))
        axes = axes.flatten()

        for ax, bench in zip(axes, BENCHMARKS):
            fid = bench["id"]
            dbo_curve  = all_convs[fid]["dbo"]
            odbo_curve = all_convs[fid]["odbo"]
            iters = np.arange(1, MAX_ITER + 1)

            ax.semilogy(iters, dbo_curve + 1e-300,
                        color="#E05A5A", linewidth=1.8,
                        label="DBO",  linestyle="--")
            ax.semilogy(iters, odbo_curve + 1e-300,
                        color="#3A9EDB", linewidth=1.8,
                        label="ODBO", linestyle="-")

            ax.set_title(f"{fid}: {bench['name']}", fontsize=10, fontweight="bold")
            ax.set_xlabel("Iteration", fontsize=8)
            ax.set_ylabel("Best Fitness (log)", fontsize=8)
            ax.legend(fontsize=8)
            ax.grid(True, alpha=0.3)

        # Hide unused axes
        for ax in axes[n_funcs:]:
            ax.set_visible(False)

        fig.suptitle(
            "Convergence: DBO vs ODBO\n"
            f"(Dim={DIM}, Pop={N_POP}, MaxIter={MAX_ITER}, {N_RUNS} runs avg)",
            fontsize=13, fontweight="bold", y=1.01
        )
        plt.tight_layout()
        img_path = os.path.join(os.path.dirname(__file__), "convergence_curves.png")
        plt.savefig(img_path, dpi=150, bbox_inches="tight")
        print(f"Convergence plots saved → {img_path}")
    except ImportError:
        print("matplotlib not available – skipping convergence plots.")

    # ------- Final summary table ------------------------------------------- #
    print("\n" + "=" * 80)
    print("  SUMMARY  –  Mean fitness values (lower is better)")
    print("=" * 80)
    print(f"{'ID':<4} {'Function':<16} {'DBO Mean':>16} {'ODBO Mean':>16} {'Improvement':>12}")
    print("-" * 68)
    i = 0
    while i < len(csv_rows):
        r_dbo  = csv_rows[i]
        r_odbo = csv_rows[i + 1]
        dbo_m  = r_dbo["Mean"]
        odbo_m = r_odbo["Mean"]
        pct    = (dbo_m - odbo_m) / (abs(dbo_m) + 1e-300) * 100
        pct_str = f"{pct:+.1f}%"
        print(
            f"{r_dbo['ID']:<4} {r_dbo['Name']:<16} "
            f"{dbo_m:>16.6e} {odbo_m:>16.6e} {pct_str:>12}"
        )
        i += 2
    print("=" * 80)


if __name__ == "__main__":
    main()
