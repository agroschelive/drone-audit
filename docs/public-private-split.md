# Separação entre público e privado

## Repositório público

Manter público:

- núcleo do código;
- parser KML/CSV básico;
- métricas genéricas;
- relatório simples;
- documentação de uso;
- exemplos fictícios;
- testes.

## Repositório ou ambiente privado

Manter privado:

- dados reais de voo;
- coordenadas privadas;
- nomes de clientes;
- relatórios comerciais;
- conectores com credenciais;
- configurações de clientes;
- templates internos;
- heurísticas comerciais não publicáveis.

## Regra prática

Se o dado identifica alguém, algum cliente, uma propriedade, uma operação real ou uma vantagem comercial sensível, não deve ir para o repositório público.
