# Lights Out Solver

## Overview
This is a Python-based solver for the "Lights Out" puzzle using both **backtracking** and **brute force** algorithms. The goal of the puzzle is to turn off all lights on an \( n \times n \) grid, where toggling a light also toggles its adjacent lights (up, down, left, and right).

## Features
- Solves the Lights Out puzzle for 3x3 grid size
- Implements **backtracking** to efficiently find a solution.
- Provides a **brute force** method for comparison.
- Outputs the sequence of moves required to solve the puzzle.

## Requirements
Ensure you have Python installed (Python 3.6+ recommended).


## Algorithms Used
### 1. Backtracking
- Uses recursion to explore different move sequences.
- Backtracks when an invalid state is reached.
- Optimized to reduce redundant checks.

### 2. Brute Force
- Tries all possible move combinations.
- Guarantees finding a solution but is computationally expensive for larger grids.




