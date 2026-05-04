# Security and privacy policy

## Sensitive data

Drone operation files may contain sensitive information, including:

- latitude and longitude;
- property or farm names;
- client names;
- operator names;
- drone serial numbers;
- timestamps;
- routes;
- field boundaries;
- commercial operation details;
- tokens, API keys, passwords, or internal identifiers.

## What must never be committed

The following must never be committed to this public repository:

- raw `.DAT` files;
- raw `.TXT` logs;
- raw `.CSV` exports;
- raw `.KML` routes;
- real coordinates;
- identifiable flight routes;
- client/operator/property names;
- drone serial numbers;
- tokens, passwords, or API keys.

## Public examples

Public examples must be either synthetic or safely sanitized.

Removing names is not enough. Real latitude/longitude must not be published. Shifted coordinates can still reveal route shape and should not be treated as fully anonymous. The safest default is to remove coordinates entirely or use fully synthetic coordinates.

## Reporting security issues

Please report potential security or privacy issues privately to: `agroschelive@gmail.com`.
