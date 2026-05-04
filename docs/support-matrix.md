# Support matrix

Supported formats in this alpha stage are limited and should be treated as auxiliary inputs only.

Supported does **not** mean definitive aircraft, operation, or spraying diagnosis.

Real files must remain local only. Public examples must be synthetic or safely sanitized. No public sample may contain real coordinates, identifiable routes, names, serials, tokens, or real timestamps.

| Format | Current status | Current use | Limitations | Privacy notes |
|---|---|---|---|---|
| CSV | Basic supported input | Telemetry ingestion for normalization, metrics, and reports when expected columns are present | Behavior depends on available columns and aliases; missing columns reduce output depth | Treat coordinates, timestamps, identifiers, and operator/client fields as sensitive |
| KML | Basic route parsing supported | Route extraction from `LineString` and `gx:Track` for map/report context | Not a definitive operational diagnosis source; route quality depends on export fidelity | Real route shapes and coordinates must stay local and out of public commits |
| JSON field data | Optional complementary field data | Adds optional non-telemetry context to reports | Not required for pipeline execution; quality depends on source consistency | Keep any identifiers or location-sensitive fields private |
| DAT | Not implemented | Future research only after locally validated real files, tests, and documentation | No parser implemented in this repository | DAT files must remain local and must not be uploaded publicly |
| TXT/log exports | Not implemented | Future evaluation only after locally validated real files, tests, and documentation | No parser implemented in this repository | TXT/log exports must remain local and must not be uploaded publicly |

- TXT tabular (exportado/convertido): suporte experimental com normalização e métricas de aplicação.
- DAT bruto DJI/Agras: não suportado nesta versão (stub amigável).
- BAT: não suportado.

