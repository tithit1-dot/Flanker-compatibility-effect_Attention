"""Quick independent check of the planned trial distribution; does not require PsychoPy."""
from collections import Counter
import csv
from pathlib import Path

HERE = Path(__file__).resolve().parent
SPEC = HERE / "condition_specification.csv"
N_EXPERIMENTAL_TRIALS = 120

with SPEC.open(newline="", encoding="utf-8") as f:
    specs = list(csv.DictReader(f))
assert len(specs) == 4, f"Expected 4 stimulus definitions, found {len(specs)}"
assert {r["condition"] for r in specs} == {"congruent", "incongruent"}
assert {r["target"] for r in specs} == {"H", "S"}
assert all(len(r["stimulus"]) == 5 for r in specs)
assert N_EXPERIMENTAL_TRIALS % 4 == 0
per_cell = N_EXPERIMENTAL_TRIALS // 4
counts = Counter((r["condition"], r["target"]) for r in specs for _ in range(per_cell))
assert len(counts) == 4 and all(n == 30 for n in counts.values())
print("PASS: four stimulus definitions; 120 experimental trials planned")
print("PASS: 60 congruent, 60 incongruent; 30 in each condition × target cell")
