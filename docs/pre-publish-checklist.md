# Checklist antes de publicar

Antes do primeiro push público:

- [ ] Confirmar que `agroschelive@gmail.com` é o contato público correto para segurança e comunicação do projeto.
- [ ] Rodar `PYTHONPATH=src pytest -q`.
- [ ] Conferir `git status`.
- [ ] Rodar busca por segredos.
- [ ] Confirmar que exemplos são fictícios.
- [ ] Confirmar que nenhum arquivo real de voo foi incluído.
- [ ] Confirmar que nenhum PDF, relatório, proposta ou dado comercial foi incluído.
- [ ] Confirmar que `.env` não existe no commit.
- [ ] Confirmar que não há histórico Git anterior com dados sensíveis.
- [ ] Habilitar Secret Scanning e Push Protection no GitHub.
