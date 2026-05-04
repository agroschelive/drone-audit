# Support matrix

Supported formats in this alpha stage are limited and should be treated as auxiliary inputs only.

Real files must remain local only. Public examples must be synthetic or safely sanitized.

| Format | Status | Notes |
|---|---|---|
| CSV | Basic supported | Core tabular ingestion path for metrics/report when required columns exist. |
| KML | Supported for route/map | Useful for route context; may not contain detailed telemetry. |
| JSON complementar | Supported (auxiliary) | Optional context data for reports; not primary telemetry. |
| XLSX | Experimental | Parser exists, but requires broader real-world validation. |
| TXT tabular legível | Experimental/limited | Only normalized tabular TXT scenarios; quality depends on structure. |
| TXT bruto DJI | Not implemented | Raw DJI TXT logs are not supported in current version. |
| DAT | Not implemented | No DAT parser implemented in this repository. |
| BAT | Not implemented | Outside current alpha scope. |

Clarifications:
- DAT is not implemented.
- Raw DJI TXT is not implemented.
- Support means auxiliary processing only, not definitive diagnosis.

- TXT/log exports: not implemented in this version.
