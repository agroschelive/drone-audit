from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class AgrasTelemetryPoint:
    timestamp: Any = None
    latitude: float | None = None
    longitude: float | None = None
    altitude_m: float | None = None
    speed_m_s: float | None = None
    heading_deg: float | None = None
    battery_pct: float | None = None
    voltage_v: float | None = None
    current_a: float | None = None
    spray_on: bool | None = None
    valve_open: bool | None = None
    pump_on: bool | None = None
    flow_l_min: float | None = None
    volume_total_l: float | None = None
    swath_width_m: float | None = None
    area_total_ha: float | None = None
    source: str | None = None
    raw: dict[str, Any] | None = None


@dataclass(frozen=True)
class AgrasSpraySegment:
    start_time: Any
    end_time: Any
    duration_s: float
    start_index: int
    end_index: int
    volume_l: float | None
    area_ha: float | None
    distance_m: float | None
    avg_flow_l_min: float | None
    avg_speed_m_s: float | None
    avg_swath_width_m: float | None


@dataclass(frozen=True)
class AgrasBatterySegment:
    start_time: Any
    end_time: Any
    battery_start_pct: float | None
    battery_end_pct: float | None
    battery_consumed_pct: float | None
    voltage_min_v: float | None
    current_avg_a: float | None
    temperature_max_c: float | None


@dataclass(frozen=True)
class AgrasTelemetryQuality:
    has_coordinates: bool
    has_timestamps: bool
    has_battery: bool
    has_spray_signal: bool
    has_flow: bool
    has_volume: bool
    has_swath_width: bool
    has_area: bool
    has_speed: bool
    warnings: list[str] = field(default_factory=list)
