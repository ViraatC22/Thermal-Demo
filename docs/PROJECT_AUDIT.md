# ThermalDemo Project Audit

Audit date: 2026-07-29

## 1. Project purpose

ThermalDemo is a Streamlit teaching application that visualizes an ideal-gas
isobaric expansion and heat exchange between two identical blocks. The
repository's README, procedure, explanation, controls, and chart labels all
support this classroom-demonstration scope.

## 2. Existing architecture

The original application was a single 600-line `app.py` containing Streamlit
layout, Matplotlib drawings, Plotly charts, animation loops, and both physical
models. Documentation is split between the README and three classroom guides.
There is no database, network integration, authentication, or secret-bearing
configuration.

The recovery separates the second-law calculation boundary into
`thermodynamics.py`. The Streamlit interface remains in `app.py`, preserving the
original product and technology choices.

## 3. Current functionality

* Interactive first-law piston animation with heat, work, and internal-energy
  metrics.
* Interactive second-law block animation with material, temperature, and mass
  controls.
* Temperature and entropy charts.
* In-session experiment logs.
* Local Streamlit startup with the documented dependency set.

## 4. Broken functionality

The second-law explicit integration was unstable. With Gold, a 0.1 kg mass, and
a 200 °C/0 °C initial pair, one step requested an 837.2 K change for each block
despite a 200 K gap. The temperatures crossed, the `while (hot > cold)` guard
stopped the loop, and the interface incorrectly reported equilibrium.

Slow combinations could also hit the 500-step limit with a large temperature
gap remaining, after which the interface forced the progress display to 100%
and reported success.

Both defects are addressed by a bounded, energy-conserving calculation step, a
larger defensive iteration budget, and terminal status based on the actual
remaining gap.

## 5. Missing functionality

No repository evidence supports additional product features. Persistent
experiment storage and export would be optional enhancements, not completion
requirements.

## 6. Build and runtime problems

The dependency imports and Streamlit server start successfully in the current
environment. Python emitted invalid-escape warnings for LaTeX strings; those
strings are now raw literals. Dependency versions remain broadly specified in
`requirements.txt`, so future dependency drift is possible.

## 7. Dependency problems

All five declared packages import successfully. There was no project-specific
virtual environment or lockfile in the repository. The README now recommends a
virtual environment. Pinning a fully tested lock set is deferred because the
repository does not identify a deployment runtime or package-locking policy.

## 8. Security concerns

No credentials, external API clients, uploads, shell execution, or persistent
personal data were found. The app injects only repository-authored static HTML
through Streamlit. No project secret was found in the tracked working tree
scan.

## 9. Testing gaps

The repository originally had no automated tests. Regression coverage now
checks:

* stability under the most aggressive UI controls;
* conservation of total thermal energy;
* convergence for every material at the largest mass;
* positive total entropy; and
* rejection of non-physical inputs.

The visual interaction remains a manual browser smoke test.

## 10. Documentation gaps

The original README omitted verification, architecture, status, limitations,
privacy, and virtual-environment guidance. These sections are now present.

## 11. Deployment gaps

The repository has no explicit hosting manifest or CI workflow. It can run on
any Python host that supports Streamlit. Automated deployment is not inferred
from repository evidence.

## 12. Accessibility and usability gaps

The interface has descriptive text and native Streamlit controls. The custom
visualizations rely partly on color, though numeric labels and chart legends
provide redundant information. Full keyboard and screen-reader testing has not
been automated.

## 13. Completion definition

The recovered scope is complete when the app starts, both physical models
retain their intended behavior, extreme control combinations cannot produce
false equilibrium, energy and entropy invariants have regression coverage, and
the setup and verification commands match the repository.

## 14. Prioritized implementation plan

1. Stabilize the thermal-exchange calculation and report the true terminal
   state.
2. Add automated invariant and regression tests.
3. Synchronize setup, architecture, limitations, and verification docs.
4. Perform syntax, test, and local startup checks.
5. Commit and push the verified milestone.

## 15. Known blockers and assumptions

The GitHub CLI reports that the saved `ViraatC22` token is invalid, so pushing a
new local commit is externally blocked until `gh auth login -h github.com` is
completed. Local development and verification are unaffected.

The material `conductivity` values are treated as display-oriented coefficients,
consistent with the original source comments, rather than SI-calibrated thermal
conductivity.
