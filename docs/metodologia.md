# Metodologia mínima

O `drone-audit` deve começar simples.

## Entradas principais

1. KML de rota.
2. CSV simples, quando disponível.
3. Dados complementares opcionais em JSON.

## Saídas principais

1. Distância percorrida.
2. Tempo total, quando houver timestamp.
3. Produtividade estimada, quando houver área informada.
4. Estados operacionais estimados.
5. Relatório HTML auxiliar.

## Princípio de honestidade técnica

O projeto só deve afirmar o que consegue calcular a partir dos arquivos fornecidos.

Não afirmar:

- leitura completa de DAT;
- integração automática com plataformas externas;
- medição definitiva de aplicação real;
- conformidade regulatória;
- precisão agronômica.

## Dados complementares

Dados complementares podem melhorar o relatório, mas não são obrigatórios para gerar o relatório básico.

Exemplos:

- tempo de reabastecimento;
- tempo de troca de bateria;
- observações de campo;
- checklist operacional.

Esses dados devem ser tratados como complementares e sempre identificados como informados manualmente.
