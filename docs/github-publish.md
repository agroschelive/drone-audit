# GitHub publishing

## Create the repository

Create an empty repository named `drone-audit` on GitHub.

Do not select automatic README, license or `.gitignore` options because these files already exist in the package.

## Commands

```bash
cd drone-audit

git init
git checkout -b main

git add .
git status

git commit -m "chore: prepare public GPLv3 alpha release"

git remote add origin https://github.com/YOUR_USERNAME/drone-audit.git
git push -u origin main
```

## After push

Enable on GitHub when available:

- Secret Scanning;
- Push Protection;
- Dependabot alerts;
- Dependency Graph;
- Private Vulnerability Reporting.
