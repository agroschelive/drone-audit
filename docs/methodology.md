# Minimal methodology

`drone-audit` should start simple.

## Main inputs

1. Route KML.
2. Simple CSV, when available.
3. Optional complementary data in JSON.

## Main outputs

1. Traveled distance.
2. Total time, when timestamps are available.
3. Estimated productivity, when an area value is provided.
4. Estimated operational states.
5. Auxiliary HTML report.

## Technical honesty principle

The project should only state what it can calculate from the provided files.

Do not claim:

- complete DAT parsing;
- automatic integration with external platforms;
- definitive measurement of real application/spraying;
- regulatory compliance;
- agronomic accuracy.

## Complementary data

Complementary data can improve the report, but it is not required to generate the basic report.

Examples:

- refill time;
- battery change time;
- field observations;
- operational checklist.

These data must be treated as complementary and always identified as manually provided.
