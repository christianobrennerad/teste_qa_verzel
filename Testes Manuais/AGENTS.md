# Regras para relatórios de QA

Ao criar ou atualizar relatórios de teste neste repositório, siga este padrão solicitado pelo usuário. Use `reports/sucesso/produto-p001.md` como referência de estrutura e os critérios abaixo para manter linguagem simples.

## Público e linguagem

- Escreva em português para uma pessoa de Produto, com frases claras e curtas.
- Destaque primeiro o resultado e seu significado para o comportamento testado.
- Evite termos técnicos no resumo. Quando necessários no BDD ou nas evidências, explique brevemente API, status HTTP e JSON.
- Apresente valores monetários como `R$ 59,90` nas tabelas para leitura humana; preserve os valores originais no BDD e nas evidências.

## Estrutura obrigatória do Markdown

1. Título: `Relatório de teste — <comportamento>`.
2. Resultado (`Aprovado`, `Falhou`, `Bloqueado` ou `Não executado`) com explicação curta.
3. Data e hora reais da execução em America/Fortaleza, ambiente/loja e referência à documentação e ao arquivo `.feature` quando disponíveis.
4. `O que foi testado`: objetivo e escopo em linguagem de negócio.
5. `Cenário BDD`: bloco `gherkin` com o cenário completo, incluindo passos, exemplos/tabelas e contexto necessário, fiel ao comportamento testado.
6. `Resultados da conferência`: tabela com `Verificação | Esperado | Encontrado | Resultado`. Adicione tabela por produto ou caso quando necessário para a leitura.
7. `Falhas encontradas`: divergências e impacto observado; se não houver falhas, informe isso explicitamente. Se houver bloqueio, descreva-o sem afirmar que há defeito no produto.
8. `Comprovantes do teste`: links relativos para as evidências e, para consultas de API, comando reproduzível usado na execução. Mantenha os detalhes técnicos nesta seção.
9. `Limite desta avaliação`: o que não foi testado e a quais execução e escopo o resultado se aplica.

## Evidências e integridade

- Para resultado `Aprovado`, salve o relatório em `reports/sucesso/<nome>.md` e as evidências em `reports/sucesso/evidencias/<nome>/<execucao>/`.
- Para resultado `Falhou`, salve o relatório em `reports/falhas/<nome>.md` e as evidências em `reports/falhas/evidencias/<nome>/<execucao>/`.
- Organize pelo resultado final e pelo escopo registrado, não pelo status HTTP isoladamente. Uma resposta de erro prevista em um teste negativo pode ser aprovada. Quando o cenário ou esquema do cenário falhar, mantenha seus exemplos aprovados e reprovados juntos no relatório de falhas, com os resultados individuais identificados.
- Não classifique testes `Bloqueado` ou `Não executado` como sucesso ou falha funcional. Mantenha esses resultados explícitos e fora das duas categorias até haver execução conclusiva.
- Atualize `reports/README.md` e os índices de `reports/sucesso/` e `reports/falhas/` ao adicionar ou reorganizar relatórios. Confira links para evidências, cenários BDD e outros relatórios.
- Para testes de API, preserve resposta HTTP completa, corpo recebido, erros da ferramenta e validação detalhada com horário, comando, status e comparação dos valores. Nunca salve credenciais ou dados pessoais sensíveis.
- Registre o status final da aplicação; a conexão bem-sucedida com um proxy não comprova sucesso da aplicação.
- Só marque como aprovado o que foi executado e verificado. Diferencie falha funcional, impedimento de execução e teste não executado.
- Ao revisar apenas a redação de um relatório, mantenha a data, o resultado e as evidências da execução original. Não apresente a edição como um novo teste.
- Não altere evidências ou critérios esperados para fazer um teste passar. Preserve evidências históricas ao repetir testes, usando uma pasta distinta por execução.
- Ao mover evidências, preserve o conteúdo de todos os arquivos. Scripts arquivados podem conter caminhos antigos: copie e adapte um script de trabalho para novas execuções, sem editar o original histórico.
- Mantenha os nomes existentes dos relatórios ao editar e confira links e formatação antes de concluir.
- Commit e push devem respeitar a autorização do usuário na conversa; criar um relatório não implica publicar automaticamente.
