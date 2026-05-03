# Final GitHub checklist

## Before the first commit

```bash
PYTHONPATH=src pytest -q

git grep -nE "(password|passwd|secret|token|api_key|apikey|client|customer|cpf|cnpj|farm|property|lat|lon)"
```

Review any result manually. Expected occurrences should only appear in guidance files such as `README.md`, `NOTICE.md`, `SECURITY.md`, `CONTRIBUTING.md`, `.env.example` or `.gitignore`.

## GitHub security

After creating the repository, enable:

- Dependabot alerts;
- Dependency graph;
- Secret scanning;
- Push protection;
- Private vulnerability reporting.

## Public release

Publish as a pre-release:

- Tag: `v0.2.1-alpha`
- Title: `Drone Audit v0.2.1-alpha`
