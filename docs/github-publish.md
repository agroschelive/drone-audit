# Publicação no GitHub

## Criar repositório

Crie um repositório vazio chamado `drone-audit` no GitHub.

Não marque opções automáticas de README, licença ou `.gitignore`, pois estes arquivos já existem no pacote.

## Comandos

```bash
cd drone-audit

git init
git checkout -b main

git add .
git status

git commit -m "chore: prepare public GPLv3 alpha release"

git remote add origin https://github.com/SEU_USUARIO/drone-audit.git
git push -u origin main
```

## Depois do push

Ative no GitHub:

- Secret Scanning;
- Push Protection;
- Dependabot alerts;
- Dependency Graph;
- Private Vulnerability Reporting.
