# Checklist final para GitHub

## Antes do primeiro commit

```bash
PYTHONPATH=src pytest -q

git grep -nE "(password|passwd|secret|token|api[_-]?key|senha|chave)"
git status
```

Revise manualmente qualquer resultado. As ocorrências esperadas devem estar apenas em arquivos de orientação, como `README.md`, `NOTICE.md`, `SECURITY.md`, `CONTRIBUTING.md`, `.env.example` ou `.gitignore`.

## Segurança no GitHub

Depois de criar o repositório, ative:

- Secret Scanning;
- Push Protection;
- Dependabot alerts;
- Dependency Graph;
- Private Vulnerability Reporting.

## Primeiro commit sugerido

```text
chore: prepare public GPLv3 alpha release
```
