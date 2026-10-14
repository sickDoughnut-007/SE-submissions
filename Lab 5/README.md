# Lab 5 - Static Code Analysis: Ticket Booking System

**Student:** Akshay V Gudur

**SRN:** PES1UG24CS047

Completed analysis and cleanup of the assigned movie-theater ticket booking
script, following the supplied Lab 5 handout.

- [Assigned repository](https://github.com/SETAPESU26/L5_45_ticket_booking_system)
- [Personal fork](https://github.com/sickDoughnut-007/L5_45_ticket_booking_system)
- [SE submission](https://github.com/sickDoughnut-007/SE-submissions/tree/main/Lab%205)
- Original source revision: `e4bd01ed94b2e512cd339b0df7e8bac0624c8cc7`

## Results

| Tool | Before | After | Handout target |
|---|---|---|---|
| Pylint | 5.37/10 | **10.00/10** | Above 9.5 |
| Bandit | 5 findings (2 High, 1 Medium, 2 Low) | **0 findings** | Resolve every finding |
| Flake8 | 7 findings | **0 findings** | Resolve every formatting issue |
| Regression tests | None supplied | **15 passed** | Verify behavior after changes |

No analysis rules were disabled. Final checks target the cleaned script,
excluding the intentionally preserved original. Empty Flake8 reports mean
there were no violations; `analysis_runs.json` records each tool's exit code.

## Deliverables

- [`ticket_booking_system.py`](ticket_booking_system.py): cleaned script.
- [`issues.md`](issues.md): 15 issue categories, original line numbers, tool
  codes, priorities, and fixes.
- [`reflection.md`](reflection.md): four answers with a note about the
  reflection questions missing from the supplied handout.
- [`reports/before/`](reports/before/): original reports and demo output.
- [`reports/after/`](reports/after/): final reports, demo output, and test transcript.
- [`reports/after_bandit/`](reports/after_bandit/) and
  [`reports/after_pylint/`](reports/after_pylint/): intermediate verification.
- [`original/ticket_booking_system.py`](original/ticket_booking_system.py):
  unchanged assigned source for comparison.
- [`tests/test_ticket_booking_system.py`](tests/test_ticket_booking_system.py):
  behavioral and security regression tests.
- [`requirements.txt`](requirements.txt) and [`tool_versions.txt`](tool_versions.txt):
  analysis tool pins and full installed dependency versions.
- [`submission_manifest.json`](submission_manifest.json): provenance and validation.

## Three tool-focused commits

1. `fix(bandit): secure promotions, ticket identifiers, PINs and chart export`
   captures the original and baseline, resolves all five Bandit findings,
   and removes the unused printed token.
2. `fix(pylint): isolate history, manage resources and clarify booking logic`
   fixes history, names, documentation, resources, summaries, and import
   behavior; adds regression tests. Pylint reaches 9.62/10.
3. `fix(flake8): finish style cleanup and document verified Lab 5 results`
   removes the unused import, corrects the singleton comparison, wraps long
   lines, and includes final reports, documentation, and test evidence.

The SE submission mirrors these stages under `Lab 5` in three corresponding
commits. Previous lab folders are preserved.

## Reproduce the checks

Tested with Python 3.12. Run from this directory:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python ticket_booking_system.py
python -m unittest discover -s tests -v
python -m pylint --persistent=no ticket_booking_system.py
python -m bandit -r ticket_booking_system.py
python -m flake8 ticket_booking_system.py
```

On Linux/macOS, activate using `source .venv/bin/activate`. To save new reports,
redirect each tool's stdout to its corresponding report file. Baseline checks
can target `original/ticket_booking_system.py`; diagnostic paths will then
differ from the initial root-level reports.

The demo runs without interactive input and writes `seating_chart.txt` in the
current directory. PINs vary. It reserves A1, cancels A2, reports B1 available,
computes a discounted premium price of 16.0, exports the chart, and reports one
sold seat.

## Behavior changes and source discrepancies

The reservation function is now `reserve_seat`. Cancellation returns a success
boolean and only handles unknown-seat errors. Promotions accept
`base_price * factor`, with decimal factor 0-1, instead of arbitrary Python.
SHA-256 digests are 64 hex characters. Importing no longer runs the demo.
Pricing tiers, booking flow, the four-digit PIN range, and chart contents remain.

The assigned README mentions an input prompt, but the supplied script has no
`input()` call. The supplied three-page PDF also omits the reflection questions
mentioned by the README. These gaps are documented rather than presented as
steps or exact questions that were supplied.
