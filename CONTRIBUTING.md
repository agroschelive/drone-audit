# Contributing

Contributions are welcome if they keep the project simple, honest and technically verifiable.

## Scope

Accepted contributions should improve:

- KML parsing;
- CSV parsing;
- basic metrics;
- simple reports;
- tests;
- documentation;
- data safety;
- reproducibility.

Avoid contributions that promise unsupported features, such as complete DAT parsing, automatic SmartFarm integration or definitive application-quality diagnosis, unless they include real validation and clear limitations.

## Data safety

Do not submit real client data, real coordinates, identifiable flight logs, personal data, tokens, passwords, API keys or confidential commercial information.

Use only fictitious or fully anonymized data.

## Pull request checklist

Before opening a pull request:

- run `PYTHONPATH=src pytest -q`;
- verify that no secret or sensitive data was added;
- update documentation if behavior changes;
- keep the change small and focused;
- explain limitations clearly.

## License agreement

By contributing, you agree that your contribution will be distributed under the GNU General Public License v3.0 only.
