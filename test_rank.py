import numpy as np
import warnings
from opfunu.cec_based.cec2014 import F12014, F42014, F232014
from mealpy import FloatVar

# Import all 9 algorithms
from dbo_mealpy import OriginalDBO
from alcdbo import MSDBO
from mealpy.swarm_based.AO import OriginalAO
from mealpy.math_based.AVOA import OriginalAVOA
from mealpy.human_based.MGO import OriginalMGO
from mealpy.swarm_based.NGO import OriginalNGO
from mealpy.swarm_based.ZOA import OriginalZOA
from mealpy.swarm_based.CoatiOA import OriginalCoatiOA
from mealpy.swarm_based.FFO import OriginalFFO

warnings.filterwarnings("ignore")

funcs = [
    ("F1 (Unimodal)", F12014(ndim=10)),
    ("F4 (Multimodal)", F42014(ndim=10)),
    ("F23 (Composition)", F232014(ndim=10))
]

algorithms = {
    "MSDBO": MSDBO,
    "DBO": OriginalDBO,
    "AO": OriginalAO,
    "MGO": OriginalMGO,
    "FFO": OriginalFFO,
    "AVOA": OriginalAVOA,
    "NGO": OriginalNGO,
    "ZOA": OriginalZOA,
    "CoatiOA": OriginalCoatiOA
}

# Run tests
results = {}
for fname, f in funcs:
    results[fname] = {}
    prob = {
        "obj_func": f.evaluate,
        "bounds": FloatVar(lb=f.lb, ub=f.ub),
        "minmax": "min",
        "verbose": False,
        "log_to": "None",
    }
    
    for alg_name, AlgClass in algorithms.items():
        try:
            model = AlgClass(epoch=200, pop_size=30)
            model.solve(prob, seed=42)
            results[fname][alg_name] = model.g_best.target.fitness
        except Exception as e:
            results[fname][alg_name] = float('inf')

# Print Results & Ranks
print("\n=== QUICK BENCHMARK TEST (200 Epochs, 30 Pop, 10-D) ===")
for fname in results:
    print(f"\nFunction: {fname}")
    print(f"{'Rank':<5} | {'Algorithm':<10} | {'Best Fitness':<15}")
    print("-" * 35)
    
    # Sort algorithms by best fitness
    sorted_algs = sorted(results[fname].items(), key=lambda x: x[1])
    
    for rank, (alg_name, fitness) in enumerate(sorted_algs, 1):
        # highlight MSDBO and DBO
        if alg_name == "MSDBO":
            alg_name = "**MSDBO**"
        elif alg_name == "DBO":
            alg_name = "*DBO*"
            
        print(f"{rank:<5} | {alg_name:<10} | {fitness:<15.4e}")
