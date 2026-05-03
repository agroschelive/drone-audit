# drone-audit

Projeto open source, mínimo e experimental para análise auxiliar de arquivos exportados de operações com drones agrícolas DJI Agras.

O objetivo inicial é transformar arquivos simples, como KML e CSV, em um relatório básico com rota, distância, tempo, produtividade estimada e observações operacionais.

## Status

Versão: `0.2.0-alpha`

Este projeto ainda está em desenvolvimento. Os resultados devem ser conferidos antes de qualquer uso técnico, comercial, operacional ou regulatório.

## O que funciona nesta versão

- Leitura básica de KML, incluindo `LineString` e `gx:Track`.
- Leitura básica de CSV com aliases comuns de colunas.
- Cálculo de distância percorrida.
- Cálculo de tempo total, quando houver timestamps.
- Cálculo de produtividade estimada, quando houver área informada.
- Classificação simples de estados operacionais quando houver velocidade e indicador de válvula/pulverização.
- Entrada opcional de dados complementares de campo em JSON.
- Geração de relatório HTML simples com mapa.
- Testes automatizados básicos.

## O que esta versão não garante

- Leitura completa de arquivos DAT.
- Integração automática com SmartFarm.
- Compatibilidade com todos os formatos exportados pela DJI.
- Identificação automática definitiva de pulverização real.
- Diagnóstico técnico completo da aeronave.
- Precisão operacional, agronômica, regulatória ou legal.
- Conformidade com fabricante, ANAC, MAPA, legislação local ou normas operacionais.

## Uso correto

O `drone-audit` é uma ferramenta auxiliar. Ele não substitui interpretação profissional, relatório técnico assinado, inspeção em campo, validação agronômica, análise regulatória ou decisão do responsável técnico.

Decisões técnicas continuam sob responsabilidade do operador, engenheiro, agrônomo, consultor, empresa operadora ou responsável técnico competente.

Leia também: [`DISCLAIMER.md`](DISCLAIMER.md).

## Entradas esperadas

- `.kml` com rota da operação.
- `.csv` com dados tabulares, quando disponível.
- `.json` opcional com dados complementares fictícios ou reais previamente autorizados.

Nunca publique dados reais de clientes, coordenadas privadas, arquivos de voo identificáveis, nomes de propriedades, tokens, senhas ou chaves de API.

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows PowerShell
pip install -r requirements.txt
```

## Executar com KML

```bash
PYTHONPATH=src python -m drone_audit.cli \
  --kml examples/sample_route.kml \
  --area-ha 12.5 \
  --output reports/relatorio_kml.html
```

## Executar com CSV

```bash
PYTHONPATH=src python -m drone_audit.cli \
  --csv examples/sample_flight.csv \
  --area-ha 12.5 \
  --output reports/relatorio_csv.html
```

## Executar com dados complementares

```bash
PYTHONPATH=src python -m drone_audit.cli \
  --csv examples/sample_flight.csv \
  --field-data examples/sample_field_data.json \
  --area-ha 12.5 \
  --output reports/relatorio_enriquecido.html
```

## Rodar testes

```bash
PYTHONPATH=src pytest -q
```

## Autor

Projeto criado e idealizado por **Italo Schelive Correia**.

Contato público: agroschelive@gmail.com

## Licença

Este projeto é distribuído sob a **GNU General Public License v3.0 only**.

Isso significa que o código pode ser usado, estudado, modificado e redistribuído conforme os termos da GPLv3. Redistribuições e versões modificadas devem respeitar a mesma licença e manter os avisos aplicáveis.

Consulte [`LICENSE`](LICENSE), [`NOTICE.md`](NOTICE.md) e [`AUTHORS.md`](AUTHORS.md).

Para publicação no GitHub, consulte [`docs/github-create-step-by-step.md`](docs/github-create-step-by-step.md).

## Aviso de marca

DJI e Agras são marcas de seus respectivos titulares. Este projeto não é afiliado, patrocinado ou endossado pela DJI. O uso dos nomes é apenas descritivo para indicar compatibilidade técnica com arquivos exportados por plataformas relacionadas.
