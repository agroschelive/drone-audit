from __future__ import annotations

STATE_SPRAYING = "estimated_spraying"
STATE_MOVING = "moving"
STATE_IDLE = "idle"
STATE_UNKNOWN = "unknown"

SPRAYING_STATES = {STATE_SPRAYING, "pulverizando"}
TRANSIT_STATES = {STATE_MOVING, "deslocando", "retorno_base"}
IDLE_STATES = {STATE_IDLE, "parado", "troca_bateria", "reabastecimento"}
MANEUVER_STATES = {"manobrando"}
