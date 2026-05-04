from __future__ import annotations

def area_to_ha(value: float | None, unit: str | None) -> float | None:
    if value is None:
        return None
    u = (unit or "ha").lower()
    if u in {"ha", "hectare", "hectares"}:
        return value
    if u in {"acre", "acres"}:
        return value * 0.40468564224
    if u in {"m2", "sqm"}:
        return value / 10000.0
    return value

def speed_to_ms(value: float | None, unit: str | None) -> float | None:
    if value is None:
        return None
    u = (unit or "m/s").lower()
    if u in {"m/s", "ms"}:
        return value
    if u in {"km/h", "kmh"}:
        return value / 3.6
    return value
