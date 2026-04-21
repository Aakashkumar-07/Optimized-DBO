import numpy as np
import warnings
from opfunu.cec_based.cec2014 import F12014, F42014, F232014
from mealpy import FloatVar
from dbo_mealpy import OriginalDBO
from alcdbo import MSDBO

warnings.filterwarnings("ignore")

funcs = [
    ("Unimodal (F1)", F12014(ndim=10)),
    ("Multimodal (F4)", F42014(ndim=10)),
    ("Composition (F23)", F232014(ndim=10))
]

print(f"{'Function':<20} | {'DBO Best':<15} | {'MSDBO Best':<15}")
print("-" * 56)

for name, f in funcs:
    prob = {
        "obj_func": f.evaluate,
        "bounds": FloatVar(lb=f.lb, ub=f.ub),
        "minmax": "min",
        "verbose": False,
        "log_to": "None",
    }
    
    # Run DBO
    dbo = OriginalDBO(epoch=200, pop_size=30)
    dbo.solve(prob, seed=42)
    dbo_best = dbo.g_best.target.fitness
    
    # Run MSDBO
    msdbo = MSDBO(epoch=200, pop_size=30)
    msdbo.solve(prob, seed=42)
    msdbo_best = msdbo.g_best.target.fitness
    
    print(f"{name:<20} | {dbo_best:<15.4e} | {msdbo_best:<15.4e}")

