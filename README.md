# Ellipse Circumference: A High-Precision Compensation Method

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)


This repository contains the official implementation and benchmark code for the paper:

**"A High-Precision and Computationally Efficient Method for Ellipse Circumference Based on a Compensation Identity"**  
*Jie Peiying (Independent Researcher)*

## Overview

The accurate and rapid computation of ellipse circumference is a classical problem in applied mathematics. This work introduces a novel compensation identity framework that achieves near-machine precision while maintaining microsecond-level execution time.

## 📄 Citation

[![DOI](https://img.shields.io/badge/DOI-10.5281/zenodo.19687794-blue)](https://doi.org/10.5281/zenodo.19687794)

If you use this method in your work, please cite:

```bibtex
@misc{Jie2026EllipseCompensation,
  author       = {Peiying Jie},
  title        = {A High-Precision and Computationally Efficient Method for Ellipse Circumference Based on a Compensation Identity},
  year         = {2026},
  doi          = {10.5281/zenodo.19687794},
  url          = {https://github.com/J-constant-math/ellipse-compensation}
}

### Key Features
- **Accuracy**: Maximum relative error < 2×10⁻⁷%
- **Speed**: ~6.4 μs per evaluation (only 3.9× slower than Ramanujan-I)
- **Comprehensive benchmarks**: Compared against Ramanujan approximations, AGM iteration, and Carlson symmetric integrals

## Repository Structure
