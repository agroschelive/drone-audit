from __future__ import annotations

from dataclasses import dataclass


LANDING_LOGIN = "landing_login"
OPERATIONS_CENTER = "operations_center"
CREATE_OS = "create_os"
OPERATION_DETAIL = "operation_detail"
GATE = "gate"
EXECUTION = "execution"
ARO = "aro"
DOSSIER = "dossier"

WORKFLOW_SEQUENCE = [
    LANDING_LOGIN,
    OPERATIONS_CENTER,
    CREATE_OS,
    OPERATION_DETAIL,
    GATE,
    EXECUTION,
    ARO,
    DOSSIER,
]

WORKFLOW_TRANSITIONS: dict[str, set[str]] = {
    LANDING_LOGIN: {OPERATIONS_CENTER},
    OPERATIONS_CENTER: {CREATE_OS},
    CREATE_OS: {OPERATION_DETAIL},
    OPERATION_DETAIL: {GATE},
    GATE: {EXECUTION},
    EXECUTION: {ARO},
    ARO: {DOSSIER},
    DOSSIER: set(),
}


@dataclass(frozen=True)
class WorkflowValidation:
    is_valid: bool
    current_stage: str | None
    expected_next: list[str]
    visited_stages: list[str]
    errors: list[str]


def validate_workflow_path(stages: list[str]) -> WorkflowValidation:
    if not stages:
        return WorkflowValidation(
            is_valid=False,
            current_stage=None,
            expected_next=[LANDING_LOGIN],
            visited_stages=[],
            errors=["workflow_empty"],
        )

    normalized = [s.strip().lower() for s in stages if s and s.strip()]
    errors: list[str] = []

    if not normalized:
        return WorkflowValidation(
            is_valid=False,
            current_stage=None,
            expected_next=[LANDING_LOGIN],
            visited_stages=[],
            errors=["workflow_empty"],
        )

    if normalized[0] != LANDING_LOGIN:
        errors.append("workflow_must_start_at_landing_login")

    for idx, stage in enumerate(normalized):
        if stage not in WORKFLOW_TRANSITIONS:
            errors.append(f"workflow_unknown_stage:{stage}")
            continue
        if idx == 0:
            continue
        previous = normalized[idx - 1]
        allowed = WORKFLOW_TRANSITIONS.get(previous, set())
        if stage not in allowed:
            errors.append(f"workflow_invalid_transition:{previous}->{stage}")

    current = normalized[-1]
    expected_next = sorted(WORKFLOW_TRANSITIONS.get(current, set())) if current in WORKFLOW_TRANSITIONS else []

    return WorkflowValidation(
        is_valid=not errors,
        current_stage=current,
        expected_next=expected_next,
        visited_stages=normalized,
        errors=errors,
    )


def workflow_progress(stages: list[str]) -> float:
    result = validate_workflow_path(stages)
    if not result.visited_stages:
        return 0.0

    reached = 0
    for stage in WORKFLOW_SEQUENCE:
        if stage in result.visited_stages:
            reached += 1
        else:
            break

    return reached / len(WORKFLOW_SEQUENCE)
