# Quality gates

Minimum quality gates before merging pull requests:

- Scope must be small and explicit.
- Existing behavior must be preserved unless the PR explicitly states otherwise.
- New behavior must have tests.
- Privacy-sensitive behavior must have regression tests.
- Documentation must be updated when behavior or workflow changes.
- Real files must not be committed.
- DAT/TXT parsing must not be introduced without locally validated files, tests and documentation.
- `ruff check src tests` must pass.
- `pytest -q` must pass.
- Coverage should be attempted when available.
