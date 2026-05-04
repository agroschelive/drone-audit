from __future__ import annotations

def diagnose_operational(metrics: dict, data_quality_warnings: list[str] | None = None) -> list[dict]:
    w=data_quality_warnings or []; op=metrics.get("operational", {}); out=[]
    eff=op.get("eficiencia_operacional_pct") or 0
    if eff < 50: out.append({"code":"baixa_eficiencia_operacional","severity":"warning","message":"Eficiência operacional baixa.","evidence":{"eficiencia":eff}})
    taxa=op.get("taxa_real_l_ha")
    if taxa is not None and (taxa<5 or taxa>40): out.append({"code":"taxa_real_fora_do_planejado","severity":"warning","message":"Taxa real fora do planejado.","evidence":{"taxa_real_l_ha":taxa}})
    if not out: out.append({"code":"operacao_eficiente","severity":"info","message":"Operação eficiente para os dados disponíveis.","evidence":{"eficiencia":eff}})
    return out
