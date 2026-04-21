# statistical_analysis.py – compute mean, std, rank, and Wilcoxon tables
# Reads JSON results from results/ directory

import os
import json
import numpy as np
from scipy.stats import ranksums

RESULTS_DIR = os.path.join(os.path.dirname(__file__), "results")
TABLES_DIR = os.path.join(os.path.dirname(__file__), "tables")
os.makedirs(TABLES_DIR, exist_ok=True)

PROPOSED = "MSDBO"


def load_results(prefix):
    """Load results JSON for a suite."""
    path = os.path.join(RESULTS_DIR, f"{prefix}_results.json")
    if not os.path.exists(path):
        print(f"  Not found: {path}")
        return None
    with open(path) as f:
        return json.load(f)


def compute_tables(data, suite_name):
    """Compute mean, std, rank, and Wilcoxon tables from results dict."""
    if data is None:
        return

    funcs = list(data.keys())
    algos = list(data[funcs[0]].keys())

    # -- Mean table --
    mean_table = {}
    for fn in funcs:
        mean_table[fn] = {}
        for alg in algos:
            mean_table[fn][alg] = data[fn][alg].get("mean", float('inf'))

    # -- Std table --
    std_table = {}
    for fn in funcs:
        std_table[fn] = {}
        for alg in algos:
            std_table[fn][alg] = data[fn][alg].get("std", 0)

    # -- Rank table (per function, lower mean = better rank) --
    rank_table = {}
    for fn in funcs:
        means = [(alg, mean_table[fn].get(alg, float('inf'))) for alg in algos]
        # sort by mean (ascending for min problems)
        means.sort(key=lambda x: x[1] if x[1] is not None else float('inf'))
        rank_table[fn] = {}
        # handle ties
        prev_val, prev_rank = None, 0
        for r, (alg, val) in enumerate(means, 1):
            if val == prev_val:
                rank_table[fn][alg] = prev_rank
            else:
                rank_table[fn][alg] = r
                prev_rank = r
            prev_val = val

    # -- Wilcoxon test: proposed vs each competitor --
    wilcoxon_table = {}
    pvalue_table = {}
    for fn in funcs:
        wilcoxon_table[fn] = {}
        pvalue_table[fn] = {}
        proposed_bests = data[fn].get(PROPOSED, {}).get("bests", [])
        if not proposed_bests:
            continue
        for alg in algos:
            if alg == PROPOSED:
                wilcoxon_table[fn][alg] = "---"
                continue
            comp_bests = data[fn].get(alg, {}).get("bests", [])
            if not comp_bests or len(comp_bests) < 5:
                wilcoxon_table[fn][alg] = "N/A"
                continue
            stat, pval = ranksums(proposed_bests, comp_bests)
            pvalue_table[fn][alg] = float(pval)
            if pval < 0.05:
                # check direction: proposed better?
                if np.mean(proposed_bests) < np.mean(comp_bests):
                    wilcoxon_table[fn][alg] = "+"
                else:
                    wilcoxon_table[fn][alg] = "-"
            else:
                wilcoxon_table[fn][alg] = "="

    return {
        "mean": mean_table,
        "std": std_table,
        "rank": rank_table,
        "wilcoxon": wilcoxon_table,
        "pvalues": pvalue_table,
        "functions": funcs,
        "algorithms": algos,
    }


def format_table(table_data, value_key, suite_name, fmt=".4e"):
    """Format a table as a readable text table."""
    if table_data is None:
        return ""
    funcs = table_data["functions"]
    algos = table_data["algorithms"]
    tbl = table_data[value_key]

    header = f"{'Function':<20}" + "".join(f"{a:>14}" for a in algos)
    lines = [f"\n=== {value_key.upper()} TABLE: {suite_name} ===", header, "-"*len(header)]

    for fn in funcs:
        row = f"{fn:<20}"
        for alg in algos:
            val = tbl[fn].get(alg, "")
            if isinstance(val, (int, float)) and val is not None:
                row += f"{val:>14{fmt}}"
            else:
                row += f"{str(val):>14}"
        lines.append(row)

    # avg rank row for rank table
    if value_key == "rank":
        row = f"{'Avg Rank':<20}"
        for alg in algos:
            vals = [tbl[fn].get(alg, 0) for fn in funcs]
            avg = np.mean(vals) if vals else 0
            row += f"{avg:>14.2f}"
        lines.append("-"*len(header))
        lines.append(row)

    return "\n".join(lines)


def format_markdown_table(table_data, suite_name):
    """Format combined Mean/Std/Rank table in markdown for the report."""
    if table_data is None:
        return ""
    funcs = table_data["functions"]
    algos = table_data["algorithms"]
    mean_tbl = table_data["mean"]
    std_tbl = table_data["std"]
    rank_tbl = table_data["rank"]

    lines = [f"### {suite_name} Results\n"]
    # Header
    header = "| Function |" + "|".join(f" {a} |" for a in algos)
    lines.append(header)
    sep = "|---|" + "|".join(["---|" for _ in algos])
    lines.append(sep)
    lines.append("| | " + " | ".join(["Mean / Std / Rank" for _ in algos]) + " |")
    lines.append(sep)

    for fn in funcs:
        row = f"| {fn} |"
        for alg in algos:
            m = mean_tbl[fn].get(alg, float('inf'))
            s = std_tbl[fn].get(alg, 0)
            r = rank_tbl[fn].get(alg, 0)
            cell = f" {m:.2e} / {s:.2e} / **{r}** |"
            row += cell
        lines.append(row)

    # Avg rank
    row = "| **Avg Rank** |"
    for alg in algos:
        vals = [rank_tbl[fn].get(alg, 0) for fn in funcs]
        avg = np.mean(vals)
        row += f" **{avg:.2f}** |"
    lines.append(row)

    return "\n".join(lines)


def format_wilcoxon_detail(table_data, suite_name):
    """Detailed Wilcoxon table with p-values."""
    if table_data is None:
        return ""
    algos = table_data["algorithms"]
    funcs = table_data["functions"]
    tbl = table_data["wilcoxon"]
    pvals = table_data.get("pvalues", {})

    lines = [f"### Wilcoxon Rank-Sum Test: {suite_name}\n"]
    comps = [a for a in algos if a != PROPOSED]
    header = "| Function |" + "|".join(f" {a} |" for a in comps)
    lines.append(header)
    sep = "|---|" + "|".join(["---|" for _ in comps])
    lines.append(sep)

    for fn in funcs:
        row = f"| {fn} |"
        for alg in comps:
            sig = tbl.get(fn, {}).get(alg, "N/A")
            pv = pvals.get(fn, {}).get(alg, None)
            if pv is not None:
                row += f" {sig} (p={pv:.4f}) |"
            else:
                row += f" {sig} |"
        lines.append(row)

    return "\n".join(lines)


def format_wilcoxon_summary(table_data, suite_name):
    """Summary: W/T/L counts for proposed vs each competitor."""
    if table_data is None:
        return ""
    algos = table_data["algorithms"]
    funcs = table_data["functions"]
    tbl = table_data["wilcoxon"]

    lines = [f"\n=== WILCOXON SUMMARY: {suite_name} ({PROPOSED} vs competitors) ==="]
    header = f"{'Competitor':<14}  {'Win(+)':>6}  {'Tie(=)':>6}  {'Loss(-)':>7}"
    lines.append(header)
    lines.append("-"*40)

    for alg in algos:
        if alg == PROPOSED:
            continue
        w = sum(1 for fn in funcs if tbl.get(fn, {}).get(alg) == "+")
        t = sum(1 for fn in funcs if tbl.get(fn, {}).get(alg) == "=")
        l = sum(1 for fn in funcs if tbl.get(fn, {}).get(alg) == "-")
        lines.append(f"{alg:<14}  {w:>6}  {t:>6}  {l:>7}")

    return "\n".join(lines)


def save_tables(suite_name, prefix, table_data):
    """Save all tables to files."""
    if table_data is None:
        return

    for key in ["mean", "std", "rank"]:
        fmt = ".4e" if key != "rank" else ".0f"
        text = format_table(table_data, key, suite_name, fmt)
        path = os.path.join(TABLES_DIR, f"{prefix}_{key}_table.txt")
        with open(path, "w") as f:
            f.write(text)
        print(text)

    wtext = format_wilcoxon_summary(table_data, suite_name)
    path = os.path.join(TABLES_DIR, f"{prefix}_wilcoxon_table.txt")
    with open(path, "w") as f:
        f.write(wtext)
    print(wtext)


def run_analysis():
    """Run statistical analysis on all saved results."""
    suites = [
        ("CEC 2014", "cec2014"),
        ("CEC 2017", "cec2017"),
        ("Engineering", "engineering"),
    ]
    all_tables = {}
    for name, prefix in suites:
        data = load_results(prefix)
        if data:
            tables = compute_tables(data, name)
            save_tables(name, prefix, tables)
            all_tables[name] = tables

            # Also save markdown versions
            md_path = os.path.join(TABLES_DIR, f"{prefix}_results_table.md")
            with open(md_path, "w") as f:
                f.write(format_markdown_table(tables, name))

            wd_path = os.path.join(TABLES_DIR, f"{prefix}_wilcoxon_detail.md")
            with open(wd_path, "w") as f:
                f.write(format_wilcoxon_detail(tables, name))

    return all_tables


if __name__ == "__main__":
    run_analysis()
