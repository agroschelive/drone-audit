# Arquitetura do drone-audit

## Objetivo da arquitetura

A arquitetura do `drone-audit` deve permanecer simples, testável e modular enquanto o projeto evolui para suportar arquivos reais do ecossistema DJI Agras.

## Fluxo atual

entrada (.csv/.kml/.json) -> parser -> dataframe normalizado -> pipeline -> métricas -> relatório HTML / JSON diagnóstico

## Contrato dos parsers

Cada parser deve evoluir para retornar:
- dataframe normalizado para o schema do projeto
- warnings
- source type

Suporte a arquivos `.dat` e `.txt` deve ser implementado somente quando arquivos reais estiverem disponíveis para validação.

## Schema normalizado

Colunas esperadas:
- timestamp
- latitude
- longitude
- altitude_m
- speed_m_s
- valve_open
- battery_pct
- source
- state

Nem todo arquivo terá todas as colunas em todas as situações.

## Métricas

Métricas atuais:
- distance_m
- time_s
- area_ha
- productivity_ha_h
- state_durations_s

A interpretação técnica continua auxiliar e experimental.

## Próximos passos arquiteturais

- parser registry
- operational state machine
- real TXT parser
- real DAT research/parser
- richer data quality report
- anonymization/sanitization tool for real files
- comparison between productive and non-productive time
