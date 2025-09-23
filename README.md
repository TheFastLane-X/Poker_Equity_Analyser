# Poker Equity Analyser

![Development Status](https://img.shields.io/badge/status-active%20development-yellow)
![Python](https://img.shields.io/badge/python-3.10+-blue)
![License](https://img.shields.io/badge/license-MIT-green)


A Texas Hold'em equity calculator using Monte Carlo simulation to determine mathematically optimal poker decisions.

## Overview

This project implements a poker decision engine that calculates hand equity (win probability) against opponent ranges and compares it to pot odds for profitable decision-making. Built with Python, it achieves sub-second evaluation of complex multi-player scenarios.

## Features

- **Hand Evaluation**: Complete poker hand ranking system supporting all standard hands
- **Monte Carlo Simulation**: Statistical analysis using 100K+ iterations for accurate equity calculation
- **Pot Odds Analysis**: Real-time EV calculations and break-even point determination
- **Opponent Modelling**: Range-based analysis for unknown opponent holdings


## Development Progress
### Core Implementation

- ✅ Card and Deck classes 
- ✅ Hand evaluator
- ✅ Monte Carlo engine
- Pot odds calculator

### Future Development

- GTO solver
- CFR implementation
- ML integration 

## Project Structure
```
poker-equity-analyser/
├── src/
│   ├── __init__.py          # Makes src a Python package
│   ├── poker_engine.py      # Core poker components
│   ├── hand_evaluator.py    # Hand ranking algorithms
│   ├── monte_carlo.py       # Simulation engine
│   └── strategy.py          # GTO calculations
├── tests/
│   └── test_*.py           # Unit tests
├── examples/
│   └── demo.ipynb          # Usage examples
└── requirements.txt
```