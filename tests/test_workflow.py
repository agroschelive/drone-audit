from drone_audit.workflow import (
    ARO,
    CREATE_OS,
    DOSSIER,
    EXECUTION,
    GATE,
    LANDING_LOGIN,
    OPERATION_DETAIL,
    OPERATIONS_CENTER,
    validate_workflow_path,
    workflow_progress,
)


def test_validate_workflow_happy_path():
    stages = [
        LANDING_LOGIN,
        OPERATIONS_CENTER,
        CREATE_OS,
        OPERATION_DETAIL,
        GATE,
        EXECUTION,
        ARO,
        DOSSIER,
    ]
    result = validate_workflow_path(stages)

    assert result.is_valid is True
    assert result.current_stage == DOSSIER
    assert result.expected_next == []
    assert result.errors == []


def test_validate_workflow_rejects_jump():
    stages = [LANDING_LOGIN, OPERATIONS_CENTER, OPERATION_DETAIL]
    result = validate_workflow_path(stages)

    assert result.is_valid is False
    assert "workflow_invalid_transition:operations_center->operation_detail" in result.errors


def test_workflow_progress_partial():
    stages = [LANDING_LOGIN, OPERATIONS_CENTER, CREATE_OS]
    assert workflow_progress(stages) == 3 / 8
