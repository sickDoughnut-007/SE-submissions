# Lab 5 - Reflection

Student: **Akshay V Gudur (PES1UG24CS047)**

**Handout gap:** The supplied three-page
`Lab_5_Static_Code_Analysis_Student_handout.pdf` requests reflection answers but
does not contain the questions. The assigned README refers to four questions.
These four prompts cover the stated learning outcomes; they are not quoted
questions from the PDF. If the instructor supplies a separate question sheet,
the answers should be mapped to it before final assessment.

## 1. What did each static analysis tool contribute?

Pylint identified quality and correctness risks, including the mutable default
history, broad exception handling, unused variables, and unmanaged files.
Flake8 identified style and cleanup problems such as line length, the `None`
comparison, and unused imports. Bandit identified security patterns: `eval`,
MD5, a non-cryptographic PIN generator, shell execution, and silently ignored
exceptions. Some findings overlapped, but the tools supplied complementary
reasons to improve the code.

## 2. How were issues prioritized and fixed?

The two High and one Medium Bandit findings were addressed first. Shell
execution was removed, SHA-256 replaced MD5, and promotion evaluation was
replaced with a narrowly validated discount format. The remaining Bandit
findings were also fixed. Next, the history default became `None`, cancellation
handled only its expected error, resources were managed explicitly, and the
functions were documented. Finally, the remaining Flake8 findings were removed.
Three separate commits make these stages reviewable.

## 3. How were fixes verified, and what did the tools miss?

The baseline reports recorded Pylint 5.37/10, five Bandit findings, and seven
Flake8 findings. Final reports show Pylint 10.00/10 and zero findings in the
other tools. Intermediate reports preserve the improvement at each stage.
Fifteen tests verify reservations, unavailable seats, history isolation,
cancellation, discount validation and rounding, SHA-256 output, secure PIN
boundaries, chart export, summaries, and safe imports. Running the demo
confirmed B1 is available, its discounted price is 16.0, and the sold count
is 1. Manual review also identified import side effects and the printed
hard-coded token, which the original reports did not directly flag.

## 4. How does static analysis improve maintainability, and what are its limits?

Static analysis exposes recurring issues before they reach users and gives
reviewers a repeatable process. Clear names, documented contracts, explicit
encoding, and narrow exception handling make later changes easier to understand.
Baseline and final reports plus focused commits show what changed and why.
However, a perfect score does not prove correctness or production security.
Tools cannot decide every business rule, verify every runtime input, or judge
whether a four-digit PIN is adequate for deployment. Behavioral tests and
human review remain necessary, particularly when a security fix narrows an
input contract such as promotion syntax.
