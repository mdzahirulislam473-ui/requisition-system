# Requisition System Prototype

BACT7501 Software Development Fundamentals, Assessment 2.

A Python prototype of a staff requisition system built with object-oriented design. Staff submit requisitions, the system auto-approves small ones, and a manager responds to the rest. It also tracks statistics.

## Business rules

| Requisition total | What happens |
|---|---|
| Less than $500 | Approved automatically, approval reference created |
| $500 or more | Pending until a manager responds |
| Manager response | Pending can become Approved, Not approved, or stay Pending |

Approval reference number = Staff ID + last 3 digits of the Requisition ID (for example `FN19` + `10001` gives `FN19001`).

## Files

| File | Purpose |
|---|---|
| `requisition.py` | The `Requisition` class (all the logic) |
| `main.py` | Interactive terminal menu (you type all the input) |
| `demo.py` | Fixed test run with 5 requisitions covering each scenario |
| `test_requisition.py` | Automated unit tests (11 tests) |
| `sample_output.txt` | Output of `demo.py` |

## Class design

`Requisition`

- Shared class data: `_next_id` (unique ID counter), `_all_requisitions` (every object created)
- `__init__`: date, staff ID, staff name, requisition ID, items, total, status, approval reference
- `add_requisition(items)`: takes a list of `(item, cost)` and returns the total
- `requisition_details()`: calculates the total
- `approve_requisition()`: auto decision based on the total
- `respond_requisition(decision)`: manager response to a pending requisition
- `display_requisition()` / `display_requisitions()`: print one or all requisitions
- `requisition_statistics()`: prints and returns counts by status

## How to run

Requires Python 3.8 or later. No extra packages.

```bash
python main.py                  # interactive menu (type your own input)
python demo.py                  # fixed 5-requisition test run
python -m unittest -v           # run the tests
```

## Design principles used

- **Encapsulation**: each requisition keeps its own data and only changes status through its methods.
- **Single responsibility**: each method does one job (capture, compute, decide, respond, display, report).
- **Modularity**: logic in `requisition.py`, demo in `main.py`, tests in `test_requisition.py`.
- **DRY**: status names and the $500 limit are defined once as constants.
- **Defensive programming**: invalid costs, empty lists, bad dates and invalid decisions raise clear errors.
