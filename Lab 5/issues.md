# Lab 5 - Identified Issues and Fixes

Student: **Akshay V Gudur (PES1UG24CS047)**

Line numbers refer to the assigned script, preserved in
[`original/ticket_booking_system.py`](original/ticket_booking_system.py).
Bandit severities are the tool's actual labels. Priority for quality findings
is a review judgment: Pylint and Flake8 do not use Bandit's severity scheme.

| Issue | Type / tool | Line(s) | Description | Fix Approach |
|---|---|---|---|---|
| 1. Weak ticket hash | Security - **High**, Bandit B324 | 47 | MD5 is unsuitable for security-sensitive hashing. | Use SHA-256 over UTF-8 encoded ticket codes. Digests change from 32 to 64 hexadecimal characters. |
| 2. Shell invocation | Security - **High**, Bandit B605 | 58 | The filename is concatenated into a shell command solely to display a status message. | Remove the shell and print the filename as data. Test export to a path containing spaces and `&`. |
| 3. Unrestricted promotion evaluation | Security - **Medium**, Bandit B307; Pylint W0123 | 41-43 | `eval` treats promotions as Python code rather than validated data. | Accept only `base_price * factor`, with decimal factor 0-1. Use `re.fullmatch`, cap input at 64 characters, multiply directly, and round to two decimals. The supplied discount still returns 16.00. |
| 4. Shared default history | Correctness - medium priority, Pylint W0102 | 15, 19 | The default list is created once, so unrelated reservations share hidden history. | Default to `None` and create a list per call. Continue updating explicitly supplied history lists. |
| 5. Hidden cancellation errors | Error handling - Bandit **Low** B110; Pylint W0702; Flake8 E722 | 24-27 | Bare `except` with `pass` hides all errors, including programming errors. | Catch only `KeyError` and return `False` for unknown seats; return `True` for success. Other exceptions propagate. |
| 6. Predictable PIN source | Security - **Low**, Bandit B311 | 51 | `random.randint` is not intended for security-sensitive identifiers. | Use `secrets.randbelow(9000) + 1000`, retaining the inclusive 1000-9999 range. Test both boundaries and the secure generator call. |
| 7. Hard-coded token printed | Security - manual review, no direct Bandit finding | 70, 79 | A literal box-office token is embedded and printed, although no operation uses it. | Remove the token and its print statement. The demo needs no external credentials. |
| 8. Import-time execution | Design - manual review | 82 | Import runs the demo, mutates seats, prints output, and creates a chart. | Add a `__main__` guard. Test imports for no output or generated files. |
| 9. Unmanaged output file | Resource handling, Pylint R1732 and W1514 | 55-57 | Exceptions before `close()` can leave the file open; encoding depends on the platform. | Use a context manager and explicit UTF-8 encoding. |
| 10. Naming and documentation | Maintainability, Pylint C0103 and C0116 | 15, 23, 30, 40, 46, 50, 54, 61, 69 | `reserveSeat` is not snake_case and functions lack documented contracts. | Rename it `reserve_seat`, update the demo call, and document every function. |
| 11. Shadowing and unused loop variable | Maintainability, Pylint W0621 and W0612 | 61, 63 | The summary argument shadows the global map; the loop variable `seat` is unused. | Rename the argument `seats` and count sold entries using `seats.values()`. |
| 12. Redundant status branching | Simplification, Pylint R1703 and R1705 | 34-37 | An `if`/`else` indirectly returns a boolean expression. | After handling unknown seats, return `not theater_seats[seat_id]["is_sold"]`. |
| 13. Unused code and old string formatting | Pylint W0611, W0612, C0209; Flake8 F401 and F841 | 6, 19, 31, 41 | `math` and `booking_fee` are unused; history uses old formatting. Tools cannot see the implicit use of `base_price` inside `eval`. | Remove unused code, use an f-string, and reference `base_price` directly in safe arithmetic. |
| 14. Singleton comparison | Style, Pylint C0121; Flake8 E711 | 32 | `None` is compared using `==`. | Use `is None` in the missing-seat check. |
| 15. Line length and final newline | Style, Pylint C0304; Flake8 E501 and W292 | 19, 82 | A line exceeds 79 columns and the file lacks a final newline. | Wrap long lines and end the source with a newline; also wrap the new validation error message. |

## Verification

| Check | Before | After |
|---|---|---|
| Pylint | 5.37/10; 25 messages; exit 28 | **10.00/10; no messages; exit 0** |
| Bandit | 5 findings: 2 High, 1 Medium, 2 Low; exit 1 | **0 findings; exit 0** |
| Flake8 | 7 findings; exit 1 | **0 findings; exit 0** |
| Regression tests | No suite in assigned repository | **15 passed** |

Final analysis targets the cleaned script, excluding the intentionally preserved
original. No rules, scoring settings, `# noqa`, or `# nosec` suppressions were
used. Pylint's `--persistent=no` only avoids machine-local score caching.

The promotion contract deliberately excludes arbitrary Python expressions.
SHA-256 is a digest, not a ticket signature. A deployed authentication service
would need controls such as rate limiting beyond this four-digit PIN demo.
