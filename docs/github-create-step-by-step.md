# GitHub publishing — step by step

## Public project data

- Project name: Drone Audit
- Repository: drone-audit
- Creator and idealizer: Italo Schelive Correia
- Public contact: agroschelive@gmail.com
- License: GNU GPL v3
- Status: 0.2.1-alpha
- Scope: experimental tool for operational audit of DJI Agras exported files, such as KML and CSV.

## Create the repository on GitHub

1. Open github.com.
2. Click New repository.
3. In Repository name, enter: drone-audit.
4. In Description, enter: Experimental operational audit tool for DJI Agras exported files.
5. Select Public.
6. Do not select Add a README file.
7. Do not select Add .gitignore.
8. Do not choose a license on GitHub.
9. Click Create repository.

## Push from the terminal

```bash
unzip drone-audit-public-ready-v0.2.1-alpha-en.zip
cd drone-audit

git init
git checkout -b main

git add .
git status

git commit -m "chore: prepare public GPLv3 alpha release"

git remote add origin https://github.com/YOUR_USERNAME/drone-audit.git
git push -u origin main
```

## Check after push

1. Open the repository on GitHub.
2. Confirm that README.md appears on the home page.
3. Confirm that the license appears as GPL-3.0.
4. Open the Actions tab and check if CI ran.
5. Open Settings > Security and enable available security features.

## Create the first release

1. Go to Releases.
2. Click Draft a new release.
3. Click Choose a tag and type: v0.2.1-alpha.
4. Release title: Drone Audit v0.2.1-alpha.
5. Description:

```text
Initial public alpha release of Drone Audit.

This version provides a minimal, experimental workflow for DJI Agras exported files, focused on KML/CSV input, basic operational metrics and simple report generation.

This release does not provide complete DAT parsing, automatic SmartFarm integration, regulatory validation or professional technical conclusions.
```

6. Select This is a pre-release.
7. Click Publish release.

## Recommended settings

Enable on GitHub when available:

- Dependabot alerts
- Dependency graph
- Secret scanning
- Push protection
- Private vulnerability reporting

## Information that must not be published

Do not upload:

- personal ID numbers;
- personal phone number;
- home or business address;
- real flight files;
- real private coordinates;
- client data;
- real SmartFarm screenshots;
- passwords, tokens or API keys;
- sensitive commercial reports.
