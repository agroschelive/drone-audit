from __future__ import annotations
from drone_audit.agras.types.agras_models import *
from drone_audit.agras.utils.agras_units import area_to_ha
from drone_audit.agras.utils.agras_hash import sha256_text

MODELOS=["T10","T16","T20","T20P","T25","T30","T40","T50","T70","T100"]

def _detect_model(text: str | None) -> str:
    t=(text or '').upper()
    for m in MODELOS:
        if m in t: return m
    return 'desconhecido'

def normalize_agras_flights(rows: list[AgrasRawSmartFarmRow], source_name: str) -> AgrasNormalizedResult:
    voos=[]; avisos=[]
    for r in rows:
        area = r.values.get('area_ha') or r.values.get('area')
        flight=AgrasFlight(modelo_agras=_detect_model(str(r.values.get('model') or r.values.get('drone') or '')), area_aplicada_ha=area_to_ha(float(area), 'ha') if area not in (None,'') else None, volume_aplicado_l=float(r.values['volume']) if r.values.get('volume') not in (None,'') else None, operador=r.values.get('operador') or r.values.get('pilot'))
        voos.append(flight)
    imp=AgrasImport(fonte='smartfarm', arquivo_nome=source_name, arquivo_hash=sha256_text(source_name+str(len(rows))), total_linhas=len(rows), linhas_validas=len(voos), linhas_com_erro=0)
    return AgrasNormalizedResult(importacao=imp, operacoes=[AgrasOperation()], voos=voos, pontos=[], avisos=avisos)
