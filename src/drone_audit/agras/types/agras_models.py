from __future__ import annotations
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

@dataclass
class AgrasRawSmartFarmRow:
    source_row: int
    values: dict[str, Any]

@dataclass
class AgrasImport:
    fonte: str
    arquivo_nome: str | None = None
    arquivo_tipo: str | None = None
    arquivo_hash: str | None = None
    status: str = "pendente"
    total_linhas: int | None = None
    linhas_validas: int | None = None
    linhas_com_erro: int | None = None
    metadados: dict[str, Any] = field(default_factory=dict)

@dataclass
class AgrasFlight:
    inicio: datetime | None = None
    fim: datetime | None = None
    modelo_agras: str | None = None
    area_aplicada_ha: float | None = None
    volume_aplicado_l: float | None = None
    distancia_m: float | None = None
    bateria_inicial_pct: float | None = None
    bateria_final_pct: float | None = None
    operador: str | None = None

@dataclass
class AgrasTelemetryPoint:
    latitude: float
    longitude: float
    sequencia: int
    altitude_m: float | None = None
    timestamp: datetime | None = None
    velocidade_ms: float | None = None
    spray_ligado: bool | None = None
    volume_acumulado_l: float | None = None
    area_acumulada_ha: float | None = None
    fonte: str = "smartfarm_kml"

@dataclass
class AgrasOperationalEvent:
    tipo_evento: str
    inicio: datetime | None
    fim: datetime | None
    confianca: float = 0.5
    observacao: str | None = None

@dataclass
class AgrasFlightMetrics:
    tempo_total_segundos: float | None = None
    tempo_pulverizando_segundos: float | None = None
    tempo_manobrando_segundos: float | None = None
    tempo_deslocando_segundos: float | None = None
    tempo_parado_segundos: float | None = None
    eficiencia_operacional_pct: float | None = None
    produtividade_real_ha_h: float | None = None

@dataclass
class AgrasDiagnostic:
    codigo: str
    mensagem: str
    severidade: str = "info"

@dataclass
class AgrasOperation:
    tipo_operacao: str = "pulverizacao"
    data_inicio: datetime | None = None
    data_fim: datetime | None = None

@dataclass
class AgrasNormalizedResult:
    importacao: AgrasImport
    operacoes: list[AgrasOperation]
    voos: list[AgrasFlight]
    pontos: list[AgrasTelemetryPoint]
    avisos: list[str]

@dataclass
class AgrasImportPreview:
    valid_rows: list[AgrasRawSmartFarmRow]
    invalid_rows: list[dict[str, Any]]
    warnings: list[str]
