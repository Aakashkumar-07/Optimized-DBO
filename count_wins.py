import json
import os
import numpy as np

files = {
    "CEC-2014": "results/cec2014_results.json",
    "CEC-2017": "results/cec2017_results.json",
    "Engineering": "results/engineering_results.json"
}

overall_wins = 0
overall_total = 0

print(f"{'Suite':<15} | {'Total Funcs':<12} | {'MSDBO Wins':<12} | {'Win %':<8}")
print("-" * 55)

for suite, path in files.items():
    if not os.path.exists(path):
        continue
    with open(path, 'r') as f:
        data = json.load(f)
    
    wins = 0
    total = len(data)
    
    for func, algos in data.items():
        # Get all means for this function
        means = {name: d['mean'] for name, d in algos.items() if d['mean'] is not None}
        if not means:
            continue
            
        # Find the algorithm with the minimum mean
        best_algo = min(means, key=means.get)
        
        if best_algo == "MSDBO":
            wins += 1
            
    overall_wins += wins
    overall_total += total
    win_pct = (wins / total) * 100 if total > 0 else 0
    print(f"{suite:<15} | {total:<12} | {wins:<12} | {win_pct:>6.1f}%")

print("-" * 55)
win_pct_all = (overall_wins / overall_total) * 100 if overall_total > 0 else 0
print(f"{'OVERALL':<15} | {overall_total:<12} | {overall_wins:<12} | {win_pct_all:>6.1f}%")
