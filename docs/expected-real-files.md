# Arquivos reais esperados para a próxima fase

## Objetivo

A próxima fase de desenvolvimento depende da coleta de arquivos reais exportados de operações com drones DJI Agras, como `.dat`, `.txt`, `.kml` e `.csv`. Esses arquivos são necessários para adaptar os parsers atuais, validar métricas operacionais e reduzir suposições feitas apenas com dados sintéticos.

## Tipos de arquivos desejados

### .DAT

Arquivos DAT podem conter informações mais ricas de voo, controladora e telemetria. Ainda assim, o parsing completo de DAT **não é garantido neste momento** e permanece fora do escopo atual.

### .TXT

Exports em TXT podem trazer telemetria legível, logs, avisos, eventos, pontos de rota, status de pulverização e outros registros operacionais úteis, dependendo da origem da exportação.

### .KML

Arquivos KML são úteis para rota, trilha, coordenadas, visualização de trajetórias e validação de distância percorrida.

### .CSV

CSV já possui suporte básico no projeto e é especialmente útil quando contém campos como timestamp, latitude, longitude, velocidade, bateria e indicadores de válvula/pulverização/bomba, além de telemetrias relacionadas.

## Informações que queremos extrair

- tempo total ligado/registrado
- tempo pulverizando
- tempo em deslocamento
- tempo em manobra
- tempo parado com drone ligado
- tempo improdutivo
- distância percorrida
- área informada ou estimada
- produtividade em ha/h
- velocidade média
- consumo/uso de calda, quando disponível
- bateria, quando disponível
- alertas e inconsistências no arquivo
- qualidade dos dados
- possíveis perdas operacionais

Nem todas as métricas serão possíveis em todos os tipos de arquivo; a disponibilidade depende dos campos realmente presentes em cada exportação.

## Cuidados com dados sensíveis

Não publique:

- dados reais de clientes
- coordenadas privadas
- nomes de propriedades
- nomes de operadores
- tokens, senhas, chaves de API
- arquivos que exponham informações comerciais ou pessoais

Sempre que possível, utilize cópias anonimizadas/sanitizadas para testes e compartilhamento.

## Como nomear arquivos de teste

Sugestões de estrutura para amostras de validação:

- `examples/real_samples/README.md`
- `examples/real_samples/t20p_sample_route.kml`
- `examples/real_samples/t20p_sample_export.csv`
- `examples/real_samples/t20p_sample_log.txt`

Não adicione arquivos privados reais ao repositório.
