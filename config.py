# config.py – central parameters for all experiments
# FE budget: POP_SIZE * MAX_ITER = 30 * 2000 = 60,000

POP_SIZE  = 30
MAX_ITER  = 2000    # epochs
N_RUNS    = 50      # independent runs per function
DIM       = 30      # dimensionality for CEC suites

# competitor algorithms (mealpy class paths)
# STRICTLY NATURE-INSPIRED COMPETITORS (2021-2026)
COMPETITORS = {
    "DBO":     ("dbo_mealpy", None,  "OriginalDBO"),      # Dung Beetle Optimizer (2023)
    "AO":      ("mealpy", "AO",      "OriginalAO"),       # Aquila Optimizer (2021)
    "MGO":     ("mealpy", "MGO",     "OriginalMGO"),      # Mountain Gazelle Optimizer (2022)
    "FFO":     ("mealpy", "FFO",     "OriginalFFO"),      # Fennec Fox Optimization (2022)
    "AVOA":    ("mealpy", "AVOA",    "OriginalAVOA"),     # African Vultures Optimization (2021)
    "NGO":     ("mealpy", "NGO",     "OriginalNGO"),      # Northern Goshawk Optimization (2022)
    "ZOA":     ("mealpy", "ZOA",     "OriginalZOA"),      # Zebra Optimization Algorithm (2022)
    "CoatiOA": ("mealpy", "CoatiOA", "OriginalCoatiOA"),  # Coati Optimization Algorithm (2022)
}

# penalty coefficient for constrained problems
PENALTY_COEFF = 1e6
