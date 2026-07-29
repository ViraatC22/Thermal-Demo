# ThermalDemo Completion Plan

Updated: 2026-07-29

## Milestone 0 — Repository and environment recovery

### TD-001 — Audit repository safety and runtime

* Reason: establish a safe baseline and distinguish code defects from
  environment failures.
* Files: repository metadata, `requirements.txt`, all source and documentation.
* Dependencies: none.
* Acceptance: clean pre-automation tree, valid `main` tracking branch, dependency
  imports pass, and evidence is recorded in `PROJECT_AUDIT.md`.
* Verification: `git status --short`; dependency import; `gh auth status`.
* Status: COMPLETED
* Commit: `4c492bb`

## Milestone 1 — Correct second-law simulation

### TD-002 — Prevent equilibrium overshoot and false success

* Reason: aggressive controls previously produced non-physical temperature
  crossing and slow controls could report equilibrium without reaching it.
* Files: `app.py`, `thermodynamics.py`.
* Dependencies: TD-001.
* Acceptance: temperatures never cross equilibrium, thermal energy is
  conserved, entropy does not decrease, and the UI reports the actual terminal
  state.
* Verification: `python3 -m unittest discover -s tests -v`.
* Status: COMPLETED
* Commit: `4c492bb`

### TD-003 — Add calculation regression coverage

* Reason: the original physical model had no automated safety net.
* Files: `tests/test_thermodynamics.py`.
* Dependencies: TD-002.
* Acceptance: all materials converge at the slowest mass setting and the
  extreme Gold case cannot overshoot.
* Verification: `python3 -m unittest discover -s tests -v`.
* Status: COMPLETED
* Commit: `4c492bb`

## Milestone 2 — Documentation and handoff

### TD-004 — Document the recovered operating model

* Reason: setup, architecture, verification, privacy, and limitations must match
  the code.
* Files: `README.md`, `docs/PROJECT_AUDIT.md`,
  `docs/COMPLETION_PLAN.md`, `docs/FINAL_STATUS.md`.
* Dependencies: TD-002, TD-003.
* Acceptance: every documented command has been exercised and limitations are
  explicit.
* Verification: manual document-to-command comparison.
* Status: COMPLETED
* Commit: `4c492bb` plus the final handoff documentation commit.

### TD-005 — Push the tested milestone

* Reason: keep the GitHub remote synchronized with the verified local state.
* Files: Git metadata only.
* Dependencies: TD-004 and valid GitHub authentication.
* Acceptance: `origin/main` contains the final local commit.
* Verification: `git status -sb`; `git log origin/main..main --oneline`.
* Status: BLOCKED
* Blocker: `gh auth status` reports an invalid token for `ViraatC22`. Run
  `gh auth login -h github.com`, then `git push origin main`.
