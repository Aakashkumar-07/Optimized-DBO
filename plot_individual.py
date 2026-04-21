# plot_individual.py – Generate individual convergence plots per function
import os, numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
PLOTS_DIR = os.path.join(os.path.dirname(__file__), "plots")
os.makedirs(PLOTS_DIR, exist_ok=True)

COLORS = {
    "MSDBO": "#E74C3C", "DBO": "#3498DB", "AO": "#2ECC71", "MGO": "#F39C12",
    "FFO": "#9B59B6", "AVOA": "#1ABC9C", "NGO": "#E67E22", "ZOA": "#34495E", "CoatiOA": "#C0392B"
}

def plot_individual(prefix, suite_name):
    npz_path = os.path.join(RESULTS_DIR, f"{prefix}_convergence.npz")
    if not os.path.exists(npz_path):
        return
    data = np.load(npz_path, allow_pickle=True)
    func_algo = {}
    for key in sorted(data.files):
        parts = key.split("__")
        if len(parts) != 2: continue
        fn, alg = parts
        if fn not in func_algo: func_algo[fn] = {}
        arr = data[key]
        func_algo[fn][alg] = np.mean(arr, axis=0) if arr.ndim == 2 else arr

    for fn in sorted(func_algo.keys()):
        fig, ax = plt.subplots(figsize=(8, 5))
        for alg, conv in sorted(func_algo[fn].items()):
            iters = np.arange(1, len(conv) + 1)
            lw = 2.5 if alg == "MSDBO" else (2.0 if alg == "DBO" else 1.2)
            ls = "-" if alg == "MSDBO" else ("--" if alg == "DBO" else "-.")
            ax.semilogy(iters, conv + 1e-300, color=COLORS.get(alg, "#666"),
                       linewidth=lw, linestyle=ls, label=alg)
        ax.set_title(f"Convergence Curve — {fn}", fontsize=13, fontweight="bold")
        ax.set_xlabel("Iteration", fontsize=11)
        ax.set_ylabel("Best Fitness (log scale)", fontsize=11)
        ax.legend(fontsize=8, ncol=3, loc="upper right")
        ax.grid(True, alpha=0.3)
        plt.tight_layout()
        safe_fn = fn.replace("/", "_").replace(" ", "_")
        out = os.path.join(PLOTS_DIR, f"{safe_fn}_convergence.png")
        plt.savefig(out, dpi=120, bbox_inches="tight")
        plt.close(fig)
    print(f"  {suite_name}: {len(func_algo)} individual plots saved")

if __name__ == "__main__":
    plot_individual("cec2014", "CEC-2014")
    plot_individual("cec2017", "CEC-2017")
    plot_individual("engineering", "Engineering")
    print("Done!")
