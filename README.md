# INF201 – Deliverable 4

Group submission by Eirik Nysveen ([Enysv1n](https://github.com/Enysv1n)) and Torjus Westhagen-Fladset ([Sommerogsol123](https://github.com/Sommerogsol123)).

## Contents

| File | Description |
|------|-------------|
| `temperature.py` | Task 1: `Temperature` class supporting Celsius, Fahrenheit and Kelvin, with conversions, string representations and cross-unit comparisons |
| `test_temperature.py` | Task 1: pytest test suite for `Temperature` |
| `fraction.py` | Task 2: `Fraction` class with comparisons, arithmetic and string representations |
| `test_fraction.py` | Task 2: pytest test suite for `Fraction` |
| `deliverable_4.ipynb` | Notebook with explanations, examples and test output for both tasks |
| `requirements.txt` | Packages in the virtual environment |

Task 1 was written by Eirik and Task 2 by Torjus.

## Setup

Requires Python 3.13.

```bash
git clone https://github.com/Enysv1n/INF201-deliverable4.git
cd INF201-deliverable4
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Running the tests

```bash
pytest -v
```

This runs both `test_temperature.py` and `test_fraction.py`.
