"""Run and save real pytest/coverage output; invoke with the Python used for tests."""

import json
import os
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parent
REPORTS = ROOT / "reports"
REPORTS.mkdir(exist_ok=True)


def run_stage(name, test_file, branch=False):
    env = os.environ.copy()
    env.update(COVERAGE_FILE=str(ROOT / f".coverage.{name}"), PYTEST_DISABLE_PLUGIN_AUTOLOAD="1", NO_COLOR="1")
    command = ["run", "--source=mobile_data_plan"]
    if branch:
        command.append("--branch")
    command += ["-m", "pytest", "-q", test_file]
    transcript = []
    for args in [command, ["report", "-m"], ["json", "-o", f"reports/{name}.json"]]:
        display = "python -m coverage " + " ".join(args)
        result = subprocess.run([sys.executable, "-m", "coverage", *args], cwd=ROOT, env=env, text=True, capture_output=True)
        output = result.stdout + result.stderr
        transcript += [f"> {display}", output.rstrip(), ""]
        if result.returncode:
            raise RuntimeError(f"{display}\n{output}")
    text = "\n".join(transcript)
    (REPORTS / f"{name}.txt").write_text(text, encoding="utf-8")
    report = json.loads((REPORTS / f"{name}.json").read_text())
    # Retain reproducible metrics without disclosing the local system path.
    report["meta"].pop("cwd", None)
    (REPORTS / f"{name}.json").write_text(json.dumps(report, indent=2) + "\n")
    totals = report["totals"]
    print(name, json.dumps(totals))
    print(text)
    return totals


results = {
    "initial_line": run_stage("initial_line", "test_mobile_data_plan.py"),
    "initial_branch": run_stage("initial_branch", "test_mobile_data_plan.py", branch=True),
    "code_coverage": run_stage("code_coverage", "CodeCoverageTest_mobile_data_plan.py"),
    "branch_coverage": run_stage("branch_coverage", "BranchCoverageTest_mobile_data_plan.py", branch=True),
}
for stage in ["code_coverage", "branch_coverage"]:
    assert results[stage]["percent_covered"] >= 90
assert results["branch_coverage"]["missing_branches"] == 0
assert results["branch_coverage"]["missing_lines"] == 0
(REPORTS / "summary.json").write_text(json.dumps(results, indent=2) + "\n")
