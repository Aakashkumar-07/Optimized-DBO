import os
import sys
import json
import importlib
import traceback
import warnings
import logging
warnings.filterwarnings("ignore")
logging.getLogger("mealpy").setLevel(logging.WARNING)

import numpy as np
from joblib import Parallel, delayed
from mealpy import FloatVar

from config import POP_SIZE, MAX_ITER, N_RUNS, DIM, COMPETITORS
from alcdbo import MSDBO
from engineering_problems import ENGINEERING_PROBLEMS

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
os.makedirs(RESULTS_DIR, exist_ok=True)


# ── helper: import competitors from mealpy ──

def get_competitor(name):
    """Dynamically import a mealpy optimizer class."""
    pkg, mod, cls = COMPETITORS[name]
    if mod is None:
        # local module (e.g. dbo_mealpy)
        module = importlib.import_module(pkg)
        return getattr(module, cls)
    module = importlib.import_module(f"{pkg}")
    parent = getattr(module, mod)
    return getattr(parent, cls)


# ── CEC benchmark suite loader ──

def load_cec_functions(suite, dim=30):
    """Load CEC functions via opfunu. Returns list of (name, problem_dict)."""
    import opfunu
    funcs = []

    if suite == "cec2014":
        for fid in range(1, 31):
            fname = f"F{fid}2014"
            try:
                f = getattr(opfunu.cec_based, fname)(ndim=dim)
                prob = {
                    "obj_func": f.evaluate,
                    "bounds": FloatVar(lb=tuple(f.lb), ub=tuple(f.ub)),
                    "minmax": "min",
                }
                funcs.append((f"CEC2014_F{fid}", prob))
            except Exception as e:
                print(f"  skip {fname}: {e}")

    elif suite == "cec2017":
        for fid in range(1, 31):
            fname = f"F{fid}2017"
            try:
                f = getattr(opfunu.cec_based, fname)(ndim=dim)
                prob = {
                    "obj_func": f.evaluate,
                    "bounds": FloatVar(lb=tuple(f.lb), ub=tuple(f.ub)),
                    "minmax": "min",
                }
                funcs.append((f"CEC2017_F{fid}", prob))
            except Exception as e:
                print(f"  skip {fname}: {e}")

    elif suite == "cec2020":
        for fid in range(1, 11):
            fname = f"F{fid}2020"
            try:
                f = getattr(opfunu.cec_based, fname)(ndim=dim)
                prob = {
                    "obj_func": f.evaluate,
                    "bounds": FloatVar(lb=tuple(f.lb), ub=tuple(f.ub)),
                    "minmax": "min",
                }
                funcs.append((f"CEC2020_F{fid}", prob))
            except Exception as e:
                print(f"  skip {fname}: {e}")

    elif suite == "cec2022":
        for fid in range(1, 13):
            fname = f"F{fid}2022"
            try:
                f = getattr(opfunu.cec_based, fname)(ndim=dim)
                prob = {
                    "obj_func": f.evaluate,
                    "bounds": FloatVar(lb=tuple(f.lb), ub=tuple(f.ub)),
                    "minmax": "min",
                }
                funcs.append((f"CEC2022_F{fid}", prob))
            except Exception as e:
                print(f"  skip {fname}: {e}")

    return funcs


# ── single run ──

def single_run(algo_cls, problem_dict, run_id, algo_kwargs=None):
    """Execute one independent run. Returns best fitness and convergence."""
    if algo_kwargs is None:
        algo_kwargs = {}
    np.random.seed(42 + run_id)

    model = algo_cls(epoch=MAX_ITER, pop_size=POP_SIZE, **algo_kwargs)
    model.solve(problem_dict, seed=42+run_id)

    best_fit = model.g_best.target.fitness
    if model.history.list_global_best_fit:
        if isinstance(model.history.list_global_best_fit[0], (list, tuple)):
            conv = [entry[0] for entry in model.history.list_global_best_fit]
        else:
            conv = list(model.history.list_global_best_fit)
    else:
        conv = []
    return best_fit, conv


# ── run all 50 trials for one (algorithm, function) pair ──

def run_all_trials(algo_name, algo_cls, problem_dict, algo_kwargs=None):
    """Run N_RUNS independent trials, return array of best values + convergences."""
    results = Parallel(n_jobs=4, verbose=0)(
        delayed(single_run)(algo_cls, problem_dict, r, algo_kwargs)
        for r in range(N_RUNS)
    )
    bests = np.array([r[0] for r in results])
    convs = [r[1] for r in results]
    return bests, convs


# ── main entry ──

def run_suite(suite_name, functions, output_prefix):
    """Run all algorithms on all functions in a suite."""
    all_results = {}

    algo_list = [("MSDBO", MSDBO, {})]
    for name, (pkg, mod, cls) in COMPETITORS.items():
        algo_cls = get_competitor(name)
        algo_list.append((name, algo_cls, {}))

    print(f"\n{'='*60}")
    print(f"  Suite: {suite_name} | {len(functions)} functions | {len(algo_list)} algorithms")
    print(f"  FE budget: {POP_SIZE}x{MAX_ITER}={POP_SIZE*MAX_ITER} | Runs: {N_RUNS}")
    print(f"{'='*60}")

    for func_name, prob in functions:
        print(f"\n  Function: {func_name}")
        all_results[func_name] = {}

        for algo_name, algo_cls, kwargs in algo_list:
            print(f"    {algo_name:12s} ... ", end="", flush=True)
            try:
                bests, convs = run_all_trials(algo_name, algo_cls, prob, kwargs)
                mean_v = np.mean(bests)
                std_v = np.std(bests, ddof=1)
                print(f"mean={mean_v:.4e}  std={std_v:.4e}")
                all_results[func_name][algo_name] = {
                    "bests": bests.tolist(),
                    "mean": float(mean_v),
                    "std": float(std_v),
                    "convergence": convs,
                }
            except Exception as e:
                print(f"FAILED: {e}")
                traceback.print_exc()
                all_results[func_name][algo_name] = {
                    "bests": [], "mean": None, "std": None, "convergence": [],
                    "error": str(e)
                }

        # --- checkpointing: save after each function ---
        out_path = os.path.join(RESULTS_DIR, f"{output_prefix}_results.json")
        save_data = {}
        for fn, algos in all_results.items():
            save_data[fn] = {}
            for aname, data in algos.items():
                save_data[fn][aname] = {
                    "bests": data["bests"],
                    "mean": data["mean"],
                    "std": data["std"],
                    "error": data.get("error", None)
                }
        with open(out_path, "w") as f:
            json.dump(save_data, f, indent=2)

        conv_path = os.path.join(RESULTS_DIR, f"{output_prefix}_convergence.npz")
        conv_data = {}
        for fn, algos in all_results.items():
            for aname, data in algos.items():
                if data["convergence"]:
                    conv_data[f"{fn}__{aname}"] = np.array(data["convergence"])
        if conv_data:
            np.savez_compressed(conv_path, **conv_data)
        
    print(f"\n  Final results saved -> {out_path} and {conv_path}")

    return all_results


def verify_fe_count():
    """Quick check: pop_size * max_iter = 60000."""
    fe = POP_SIZE * MAX_ITER
    assert fe == 60000, f"FE mismatch: {fe} != 60000"
    print(f"FE check passed: {POP_SIZE} x {MAX_ITER} = {fe}")


def smoke_test():
    """Quick test: 2 runs on sphere function."""
    global N_RUNS
    orig = N_RUNS
    import config
    config.N_RUNS = 2
    from config import N_RUNS as nr

    print("=== SMOKE TEST (2 runs, Sphere) ===")
    prob = {
        "obj_func": lambda x: np.sum(np.array(x)**2),
        "bounds": FloatVar(lb=(-100.0,)*10, ub=(100.0,)*10),
        "minmax": "min",
    }

    model = MSDBO(epoch=100, pop_size=30)
    model.solve(prob, seed=42)
    print(f"  MSDBO best fitness: {model.g_best.target.fitness:.6e}")

    from mealpy.swarm_based.NGO import OriginalNGO
    model2 = OriginalNGO(epoch=100, pop_size=30)
    model2.solve(prob, seed=42)
    print(f"  NGO   best fitness: {model2.g_best.target.fitness:.6e}")
    print("=== SMOKE TEST PASSED ===")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--smoke-test":
        verify_fe_count()
        smoke_test()
        sys.exit(0)

    if len(sys.argv) > 1 and sys.argv[1] == "--verify":
        verify_fe_count()
        sys.exit(0)

    # determine mode
    global N_RUNS
    mode = "full"
    if "--validation" in sys.argv:
        mode = "validation"
    elif "--partial" in sys.argv:
        mode = "partial"

    # load suites
    cec_2014 = load_cec_functions("cec2014", DIM)
    cec_2017 = load_cec_functions("cec2017", DIM)
    cec_2020 = load_cec_functions("cec2020", DIM)
    cec_2022 = load_cec_functions("cec2022", DIM)
    eng_funcs = [(p["name"], p) for p in ENGINEERING_PROBLEMS]

    if mode == "validation":
        print("=== VALIDATION MODE (2 Funcs, 5 Runs) ===")
        N_RUNS = 5
        import config; config.N_RUNS = 5
        suites = [
            ("Validation CEC", cec_2014[:1], "val_cec"),
            ("Validation Eng", eng_funcs[:1], "val_eng")
        ]
    elif mode == "partial":
        print("=== PARTIAL MODE (5 Funcs, 10 Runs) ===")
        N_RUNS = 10
        import config; config.N_RUNS = 10
        suites = [
            ("Partial CEC", cec_2014[:3] + cec_2020[:2], "partial_cec")
        ]
    else:
        print("=== FULL BENCHMARK MODE (All Funcs, 50 Runs) ===")
        suites = [
            ("CEC 2014", cec_2014, "cec2014"),
            ("CEC 2017", cec_2017, "cec2017"),
            ("CEC 2020", cec_2020, "cec2020"),
            ("CEC 2022", cec_2022, "cec2022"),
            ("Engineering Problems", eng_funcs, "engineering")
        ]
        
    for suite_name, funcs, prefix in suites:
        if funcs:
            run_suite(suite_name, funcs, prefix)

    print("\n\nAll benchmarks completed!")
