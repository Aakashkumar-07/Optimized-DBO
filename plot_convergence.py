# plot_convergence.py – convergence curve plots per benchmark suite

import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
PLOTS_DIR = os.path.join(os.path.dirname(__file__), "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

COLORS = [
    "#E74C3C", "#3498DB", "#2ECC71", "#F39C12",
    "#9B59B6", "#1ABC9C", "#E67E22", "#34495E", "#C0392B"
]


def plot_suite(prefix, suite_name, max_funcs_per_fig=6):
    """Load convergence data and plot curves."""
    npz_path = os.path.join(RESULTS_DIR, f"{prefix}_convergence.npz")
    if not os.path.exists(npz_path):
        print(f"  No convergence data: {npz_path}")
        return

    data = np.load(npz_path, allow_pickle=True)
    keys = sorted(data.files)

    # group by function
    func_algo = {}
    for key in keys:
        parts = key.split("__")
        if len(parts) != 2:
            continue
        fn, alg = parts
        if fn not in func_algo:
            func_algo[fn] = {}
        arr = data[key]
        # mean convergence across runs
        if arr.ndim == 2:
            func_algo[fn][alg] = np.mean(arr, axis=0)
        else:
            func_algo[fn][alg] = arr

    funcs = sorted(func_algo.keys())
    if not funcs:
        return

    # plot in pages of max_funcs_per_fig
    for page_start in range(0, len(funcs), max_funcs_per_fig):
        page_funcs = funcs[page_start:page_start + max_funcs_per_fig]
        n = len(page_funcs)
        ncols = min(3, n)
        nrows = (n + ncols - 1) // ncols

        fig, axes = plt.subplots(nrows, ncols, figsize=(5*ncols, 4*nrows))
        if nrows * ncols == 1:
            axes = np.array([axes])
        axes = axes.flatten()

        for ax, fn in zip(axes, page_funcs):
            algos_data = func_algo[fn]
            for i, (alg, conv) in enumerate(sorted(algos_data.items())):
                iters = np.arange(1, len(conv) + 1)
                color = COLORS[i % len(COLORS)]
                lw = 2.2 if alg == "MSDBO" else 1.2
                ls = "-" if alg == "MSDBO" else "--"
                ax.semilogy(iters, conv + 1e-300, color=color,
                           linewidth=lw, linestyle=ls, label=alg)
            ax.set_title(fn, fontsize=9, fontweight="bold")
            ax.set_xlabel("Iteration", fontsize=8)
            ax.set_ylabel("Best Fitness (log)", fontsize=8)
            ax.legend(fontsize=6, ncol=2)
            ax.grid(True, alpha=0.3)

        for ax in axes[n:]:
            ax.set_visible(False)

        fig.suptitle(f"Convergence: {suite_name}", fontsize=12, fontweight="bold")
        plt.tight_layout()

        page_idx = page_start // max_funcs_per_fig
        out_path = os.path.join(PLOTS_DIR, f"{prefix}_convergence_p{page_idx+1}.png")
        plt.savefig(out_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"  Saved: {out_path}")


def main():
    suites = [
        ("cec2014", "CEC 2014"),
        ("cec2017", "CEC 2017"),
        ("cec2020", "CEC 2020"),
        ("cec2022", "CEC 2022"),
        ("engineering", "Engineering Problems"),
    ]
    for prefix, name in suites:
        print(f"\nPlotting {name}...")
        plot_suite(prefix, name)


if __name__ == "__main__":
    main()
