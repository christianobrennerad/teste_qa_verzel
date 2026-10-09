# Regras para a automação e seus relatórios

- Use Playwright com TypeScript. Os arquivos `.spec.ts` executam os cenários; os BDD em `../Testes Manuais/features/` são a referência.
- Para os relatórios, siga a estrutura e a linguagem de [AGENTS.md dos testes manuais](<../Testes Manuais/AGENTS.md>): resultado, data real em America/Fortaleza, ambiente, objetivo, BDD completo, tabela de esperado/encontrado, falhas, evidências e limites da avaliação.
- Salve relatórios aprovados em `reports/sucesso/<nome>.md` e os reprovados em `reports/falhas/<nome>.md`, nesta pasta de automação. Evidências ficam em `reports/<resultado>/evidencias/<nome>/<execucao>/`.
- Preserve os relatórios manuais como referência. Não substitua as execuções deles por resultados automatizados sem pedido do usuário.
- Quando um cenário tiver exemplos aprovados e reprovados, mantenha a execução completa na pasta de falhas e identifique cada exemplo. Não classifique um bloqueio de execução como defeito da loja.
- Registre requisições, respostas, horários e comparações. Em testes de interface, salve capturas da tela e os valores exibidos. Nunca grave credenciais. Mantenha a verificação TLS ativa.
- Preserve as evidências das execuções anteriores. Registre e corrija falhas da automação antes de concluir uma falha do produto, mantendo o diagnóstico original.
- Atualize `reports/README.md` e os índices de sucesso e falhas; confira os links. Arquive HTML, saída do runner e versões em `reports/execucoes/<execucao>/`.
- Execute `npm run typecheck` quando modificar os testes. Verifique o resultado real do runner: aprovado, falhou, pulado ou bloqueado.
- Commit e push dependem do pedido do usuário na conversa.
