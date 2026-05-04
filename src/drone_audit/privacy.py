from __future__ import annotations

import unicodedata
from datetime import datetime, timedelta, timezone

import pandas as pd

SENSITIVE_EXACT_NAMES = {
    "client",
    "cliente",
    "customer",
    "farm",
    "fazenda",
    "property",
    "propriedade",
    "owner",
    "proprietario",
    "operator",
    "operador",
    "pilot",
    "piloto",
    "user",
    "usuario",
    "email",
    "phone",
    "telefone",
    "cpf",
    "cnpj",
    "serial",
    "drone_serial",
    "aircraft_serial",
    "sn",
    "token",
    "password",
    "senha",
    "api_key",
    "secret_key",
    "access_key",
    "private_key",
    "public_key",
    "credential_key",
    "token_key",
    "location_name",
    "nome_local",
    "field_name",
    "talhao",
    "boundary",
}
LOCATION_NAMES = {
    "latitude",
    "lat",
    "gps_lat",
    "longitude",
    "lon",
    "lng",
    "gps_lon",
    "gps_latitude",
    "gps_longitude",
    "latitude_deg",
    "longitude_deg",
    "lat_deg",
    "lon_deg",
    "lng_deg",
    "flight_lat",
    "flight_lon",
    "flight_lng",
    "aircraft_lat",
    "aircraft_lon",
    "aircraft_lng",
}
TIMESTAMP_NAMES = {
    "timestamp",
    "time",
    "datetime",
    "record_time",
    "date_time",
    "gps_time",
    "flight_time",
    "recorded_at",
    "created_at",
    "updated_at",
    "started_at",
    "ended_at",
    "date",
    "data",
    "hora",
    "data_hora",
}
RELATIVE_DURATION_NAMES = {
    "time_s",
    "elapsed_s",
    "elapsed_time_s",
    "duration_s",
    "spray_time_s",
    "moving_time_s",
    "idle_time_s",
}


def _normalize_parts(name: str) -> list[str]:
    text = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode("ascii").lower()
    parts = pd.Series([text]).str.split(r"[^a-z0-9]+", regex=True).iloc[0]
    return [part for part in parts if part]


def _normalized_name(name: str) -> str:
    return "_".join(_normalize_parts(name))


def _is_sensitive_column(name: str) -> bool:
    normalized = _normalized_name(name)
    parts = _normalize_parts(name)
    if normalized in LOCATION_NAMES:
        return True
    if normalized in SENSITIVE_EXACT_NAMES:
        return True
    if "key" in parts:
        return True
    return any(part in SENSITIVE_EXACT_NAMES for part in parts)


def _is_coordinate_column(name: str) -> bool:
    normalized = _normalized_name(name)
    if normalized in LOCATION_NAMES:
        return True

    parts = _normalize_parts(name)
    return any(part in {"latitude", "longitude", "lat", "lon", "lng"} for part in parts)


def _timestamp_columns(columns: list[str]) -> list[str]:
    selected: list[str] = []
    for col in columns:
        normalized = _normalized_name(col)
        if normalized in RELATIVE_DURATION_NAMES:
            continue
        if normalized in TIMESTAMP_NAMES:
            selected.append(col)
    return selected


def sanitize_csv_dataframe(
    df: pd.DataFrame,
    *,
    remove_coordinates: bool = True,
    fake_coordinates: bool = False,
    normalize_timestamps: bool = True,
) -> pd.DataFrame:
    sanitized = df.copy(deep=True)
    sensitive_cols: list[str] = []
    coordinate_cols: list[str] = []

    for col in sanitized.columns:
        if _is_coordinate_column(col):
            coordinate_cols.append(col)
            continue
        if _is_sensitive_column(col):
            sensitive_cols.append(col)

    keep_cols = [c for c in sanitized.columns if c not in sensitive_cols]
    sanitized = sanitized.loc[:, keep_cols]

    if fake_coordinates:
        sanitized = sanitized.drop(columns=[c for c in coordinate_cols if c in sanitized.columns], errors="ignore")
        sanitized["latitude"] = [-23.0 + (idx * 0.00001) for idx in range(len(sanitized))]
        sanitized["longitude"] = [-51.0 + (idx * 0.00001) for idx in range(len(sanitized))]
    elif remove_coordinates:
        sanitized = sanitized.drop(columns=[c for c in coordinate_cols if c in sanitized.columns], errors="ignore")

    if normalize_timestamps:
        base = datetime(2026, 1, 1, tzinfo=timezone.utc)  # noqa: UP017
        for col in _timestamp_columns(list(sanitized.columns)):
            parsed = pd.to_datetime(sanitized[col], errors="coerce", utc=True)
            valid = parsed.dropna()
            if valid.empty:
                deltas = [timedelta(seconds=i) for i in range(len(sanitized))]
            else:
                min_ts = valid.min()
                deltas = []
                for idx in range(len(sanitized)):
                    value = parsed.iloc[idx]
                    if pd.isna(value):
                        deltas.append(timedelta(seconds=idx))
                    else:
                        seconds = int((value - min_ts).total_seconds())
                        deltas.append(timedelta(seconds=max(seconds, 0)))

            sanitized[col] = [(base + delta).strftime("%Y-%m-%dT%H:%M:%SZ") for delta in deltas]

    return sanitized
