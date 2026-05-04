from __future__ import annotations

from drone_audit.agras.types.agras_models import (
    AgrasFlight,
    AgrasImport,
    AgrasNormalizedResult,
    AgrasOperation,
    AgrasRawSmartFarmRow,
)
from drone_audit.agras.utils.agras_hash import sha256_text
from drone_audit.agras.utils.agras_units import area_to_ha

MODELOS = ["T10", "T16", "T20", "T20P", "T25", "T30", "T40", "T50", "T70", "T100"]


def _detect_model(text: str | None) -> str:
    value = (text or "").upper()
    for model in MODELOS:
        if model in value:
            return model
    return "desconhecido"


def normalize_agras_flights(rows: list[AgrasRawSmartFarmRow], source_name: str) -> AgrasNormalizedResult:
    voos: list[AgrasFlight] = []
    avisos: list[str] = []

    for row in rows:
        area = row.values.get("area_ha") or row.values.get("area")
        area_ha = area_to_ha(float(area), "ha") if area not in (None, "") else None
        volume = row.values.get("volume")
        volume_l = float(volume) if volume not in (None, "") else None

        voos.append(
            AgrasFlight(
                modelo_agras=_detect_model(str(row.values.get("model") or row.values.get("drone") or "")),
                area_aplicada_ha=area_ha,
                volume_aplicado_l=volume_l,
                operador=row.values.get("operador") or row.values.get("pilot"),
            )
        )

    importacao = AgrasImport(
        fonte="smartfarm",
        arquivo_nome=source_name,
        arquivo_hash=sha256_text(f"{source_name}:{len(rows)}"),
        total_linhas=len(rows),
        linhas_validas=len(voos),
        linhas_com_erro=0,
    )

    return AgrasNormalizedResult(
        importacao=importacao,
        operacoes=[AgrasOperation()],
        voos=voos,
        pontos=[],
        avisos=avisos,
    )
