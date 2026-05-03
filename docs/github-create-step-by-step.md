# Publicação no GitHub — passo a passo

## Dados públicos do projeto

- Nome do projeto: Drone Audit
- Repositório: drone-audit
- Criador e idealizador: Italo Schelive Correia
- Contato público: agroschelive@gmail.com
- Licença: GNU GPL v3
- Status: 0.2.0-alpha
- Escopo: ferramenta experimental para auditoria operacional de drones DJI Agras a partir de arquivos exportados, como KML e CSV.

## Criar o repositório no GitHub

1. Entre em github.com.
2. Clique em New repository.
3. Em Repository name, coloque: drone-audit.
4. Em Description, coloque: Experimental operational audit tool for DJI Agras exported files.
5. Marque Public.
6. Não marque Add a README file.
7. Não marque Add .gitignore.
8. Não escolha licença no GitHub.
9. Clique em Create repository.

## Subir pelo terminal

```bash
unzip drone-audit-public-ready-v0.2.0-alpha.zip
cd drone-audit

git init
git checkout -b main

git add .
git status

git commit -m "chore: prepare public GPLv3 alpha release"

git remote add origin https://github.com/SEU_USUARIO/drone-audit.git
git push -u origin main
```

## Conferir depois do push

1. Abra o repositório no GitHub.
2. Confirme se o README.md aparece na página inicial.
3. Confirme se a licença aparece como GPL-3.0.
4. Abra a aba Actions e veja se o CI rodou.
5. Abra Settings > Security e ative recursos de segurança disponíveis.

## Criar a primeira release

1. Vá em Releases.
2. Clique em Draft a new release.
3. Clique em Choose a tag e escreva: v0.2.0-alpha.
4. Título da release: Drone Audit v0.2.0-alpha.
5. Descrição:

```text
Initial public alpha release of Drone Audit.

This version provides a minimal, experimental workflow for DJI Agras exported files, focused on KML/CSV input, basic operational metrics and simple report generation.

This release does not provide complete DAT parsing, automatic SmartFarm integration, regulatory validation or professional technical conclusions.
```

6. Marque This is a pre-release.
7. Clique em Publish release.

## Configurações recomendadas

Ative no GitHub, quando disponível:

- Dependabot alerts
- Dependency graph
- Secret scanning
- Push protection
- Private vulnerability reporting

## Informações que não devem ser publicadas

Não subir:

- CPF
- telefone pessoal
- endereço
- arquivos reais de voo
- coordenadas reais
- dados de cliente
- prints reais do SmartFarm
- senhas, tokens ou chaves de API
- relatórios comerciais sensíveis
