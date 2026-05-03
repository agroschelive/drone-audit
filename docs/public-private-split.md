# Public and private separation

## Public repository

Keep public:

- core code;
- basic KML/CSV parser;
- generic metrics;
- simple report;
- usage documentation;
- fictitious examples;
- tests.

## Private repository or private environment

Keep private:

- real flight data;
- private coordinates;
- client names;
- commercial reports;
- credential-based connectors;
- client-specific configurations;
- internal templates;
- non-public commercial heuristics.

## Practical rule

If data identifies a person, client, property, real operation or sensitive commercial advantage, it must not be committed to the public repository.
