# Roadmap de Issues

Backlog proposto organizado por horizonte de entrega.

## Curto Prazo (0–3 meses)

- **Validar parser CSV com arquivos originais**  
  Receber arquivos CSV originais, rodar parser, validar métricas e documentar resultados.  
  **Labels:** `parser`, `tests`, `data-validation`

- **Validar parser KML com arquivos originais**  
  Rodar parser KML, verificar mapa no relatório HTML e comparar métricas.  
  **Labels:** `parser`, `report`, `data-validation`

- **Criar modelo central FlightData**  
  Definir classe FlightData para padronizar entrada de dados e cálculos de métricas.  
  **Labels:** `infra`, `parser`

- **Expandir testes automatizados**  
  Criar testes pytest com arquivos originais e aumentar cobertura.  
  **Labels:** `tests`, `infra`

- **Documentar compatibilidade inicial**  
  Atualizar README com formatos suportados e exemplos anonimizados.  
  **Labels:** `documentation`

## Médio Prazo (3–9 meses)

- **Implementar parser DAT**  
  Mapear estrutura dos arquivos DAT, implementar parser inicial e documentar diferenças entre versões.  
  **Labels:** `parser`, `data-validation`, `documentation`

- **Gerar relatórios HTML/PDF avançados**  
  Criar relatórios com mapas, métricas detalhadas e exportação em PDF.  
  **Labels:** `report`, `infra`

- **Estrutura de API ou biblioteca**  
  Criar API ou pacote Python para uso externo.  
  **Labels:** `infra`, `integration`

- **Configurar pipeline CI/CD**  
  Automatizar testes e validação de contribuições com GitHub Actions.  
  **Labels:** `infra`, `tests`

- **Início de comunidade ativa**  
  Divulgar projeto, abrir issues públicas e exemplos anonimizados.  
  **Labels:** `community`, `documentation`

## Longo Prazo (9–18 meses)

- **Integração com plataformas agrícolas**  
  Conectar com SmartFarm, FieldView e outras plataformas para ingestão de dados.  
  **Labels:** `integration`, `community`

- **Dashboards interativos**  
  Criar dashboards web para múltiplos voos, com banco de dados central.  
  **Labels:** `report`, `infra`, `visualization`

- **Análises avançadas**  
  Implementar cálculos de eficiência de pulverização, consumo energético e manutenção preventiva.  
  **Labels:** `analysis`, `infra`

- **Suporte a múltiplos fabricantes**  
  Expandir parsers para além da DJI, cobrindo outros drones agrícolas.  
  **Labels:** `parser`, `integration`

- **Serviço web escalável**  
  Transformar pipeline em serviço web capaz de processar centenas de voos em lote.  
  **Labels:** `infra`, `scalability`

- **Consolidação da comunidade open-source**  
  Atrair colaboradores ativos, organizar contribuições e manter governança.  
  **Labels:** `community`
