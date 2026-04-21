"""
Ellipse Perimeter Comparison
Compensation correction method (Peiying 2026) vs. classical approximations,
AGM, and Carlson symmetric elliptic integrals.

Paper: "A High-Precision and Computationally Efficient Method for 
Ellipse Circumference Based on a Compensation Identity"
Author: Jie Peiying
Preprint: https://github.com/J-constant-math/ellipse-compensation

If you use this code, please cite the paper.
"""

import numpy as np
from scipy.special import ellipe, elliprf, elliprd
from math import pi, sqrt
import csv

# ============================================================================
# Helper: exact circumference (reference ground truth)
# ============================================================================
def exact_circumference(a, b):
    """Exact circumference using scipy's complete elliptic integral E(e)."""
    e_sq = 1.0 - (b / a) ** 2
    return 4.0 * a * ellipe(e_sq)

# ============================================================================
# Classical approximations
# ============================================================================
def ramanujan1(a, b):
    """Ramanujan's first approximation."""
    return pi * (3*(a+b) - sqrt((3*a + b)*(a + 3*b)))

def ramanujan2(a, b):
    """Ramanujan's second approximation."""
    h = (a - b) / (a + b)
    h2 = h * h
    term = 3 * h2 / (10 + sqrt(4 - 3 * h2))
    return pi * (a + b) * (1 + term)

# ============================================================================
# Proposed method (Compensation Identity)
# Coefficients from the paper (Eq. 10)
# ============================================================================
COEFFS = [
    -9.07604402e-5,   # c0
     9.79063904e-3,   # c1
     7.81267746e-2,   # c2
    -1.13436626e-1,   # c3
     1.66437786e-1,   # c4
    -7.16493748e-2    # c5
]

def compensation_correction(a, b):
    """Peiying's compensation identity method."""
    h = (a - b) / (a + b)
    C_ram = ramanujan1(a, b)
    J0 = (2 * pi * (a - b) - C_ram) / 2.0

    # Evaluate polynomial P(h) = sum c_k * h^{2k+3}
    h2 = h * h
    h_pow = h * h2           # h^3
    P = 0.0
    for c in COEFFS:
        P += c * h_pow
        h_pow *= h2           # increase exponent by 2
    J_corr = J0 - P
    return 2 * pi * (a - b) - 2 * J_corr

# ============================================================================
# AGM method (Arithmetic-Geometric Mean)
# ============================================================================
def agm_circumference(a, b):
    """Compute ellipse circumference via Arithmetic-Geometric Mean (AGM)."""
    a0, b0 = a, b
    s = 0.0
    n = 1
    while True:
        a1 = 0.5 * (a0 + b0)
        b1 = sqrt(a0 * b0)
        c1 = 0.5 * (a0 - b0)
        s += n * c1**2
        a0, b0 = a1, b1
        n *= 2
        if abs(c1) < 1e-15 * a0:
            break
    return pi * (a**2 - s) / a0

# ============================================================================
# Carlson symmetric integrals (via scipy)
# ============================================================================
def carlson_circumference(a, b):
    """Circumference using Carlson's RF and RD (via scipy)."""
    e_sq = 1.0 - (b / a) ** 2
    rf = elliprf(0.0, 1.0 - e_sq, 1.0)
    rd = elliprd(0.0, 1.0 - e_sq, 1.0)
    E = rf - (e_sq / 3.0) * rd
    return 4.0 * a * E

# ============================================================================
# Main comparison and CSV export
# ============================================================================
def run_comparison():
    """Run full comparison and save results to CSV."""
    a = 10.0
    b_values = [9, 8, 7, 6, 5, 4, 3, 2, 1]
    
    methods = {
        "Ramanujan-I": ramanujan1,
        "Ramanujan-II": ramanujan2,
        "Proposed": compensation_correction,
        "AGM": agm_circumference,
        "Carlson": carlson_circumference
    }
    
    results = []
    
    for b in b_values:
        e = sqrt(1 - (b / a)**2)
        exact = exact_circumference(a, b)
        row = {"b": b, "eccentricity": e, "exact": exact}
        
        for name, func in methods.items():
            approx = func(a, b)
            rel_err = abs((approx - exact) / exact) * 100.0
            row[name] = approx
            row[f"{name}_error_%"] = rel_err
        
        results.append(row)
    
    return results

def save_results_to_csv(results, filename="comparison_results.csv"):
    """Save comparison results to CSV file."""
    if not results:
        return
    
    fieldnames = list(results[0].keys())
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)
    print(f"Results saved to {filename}")

def print_summary_table(results):
    """Print a formatted summary table."""
    print("\n" + "="*80)
    print("Ellipse Circumference Comparison (a=10)")
    print("="*80)
    print(f"{'b':>4} {'e':>10} {'Ram-I err%':>14} {'Ram-II err%':>14} "
          f"{'Proposed err%':>14} {'AGM err%':>14} {'Carlson err%':>14}")
    print("-"*80)
    
    for row in results:
        print(f"{row['b']:4d} {row['eccentricity']:10.6f} "
              f"{row['Ramanujan-I_error_%']:14.6e} "
              f"{row['Ramanujan-II_error_%']:14.6e} "
              f"{row['Proposed_error_%']:14.6e} "
              f"{row['AGM_error_%']:14.6e} "
              f"{row['Carlson_error_%']:14.6e}")

if __name__ == "__main__":
    results = run_comparison()
    print_summary_table(results)
    save_results_to_csv(results, "comparison_results.csv")
    print("\nDone.")
