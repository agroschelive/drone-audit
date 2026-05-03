# Desenvolvimento do drone-audit

## Instalação para desenvolvimento

```bash
pip install -e ".[dev]"
```

## Rodar testes

```bash
pytest -q
```

## Rodar lint

```bash
ruff check src tests
```

## Rodar cobertura

```bash
pytest -q --cov=drone_audit --cov-report=term-missing
```

## Rodar modo diagnóstico

```bash
PYTHONPATH=src python -m drone_audit.cli --csv examples/sample_flight.csv --area-ha 12.5 --output reports/report_csv.html --diagnose
```

## Como preparar um PR

1. Crie uma branch a partir da `main`.
2. Implemente mudanças pequenas, conservadoras e com testes.
3. Rode lint, testes e cobertura antes de abrir o PR.
4. Descreva claramente motivação, escopo e limitações.

## Regra de dados

Nunca commitar dados reais de clientes, propriedades privadas ou arquivos sensíveis de voo.
