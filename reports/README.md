# Relatórios de QA

Os 33 relatórios existentes estão separados pelo resultado final registrado em cada teste:

| Resultado | Quantidade de relatórios | Onde consultar |
| --- | --- | --- |
| Aprovado | 24 | [Testes com sucesso](sucesso/README.md) |
| Falhou | 9 | [Testes que falharam](falhas/README.md) |

Cada pasta reúne os relatórios em Markdown e as evidências correspondentes:

```text
reports/
├── README.md
├── sucesso/
│   ├── README.md
│   ├── produto-p001.md
│   └── evidencias/
│       └── produto-p001/
└── falhas/
    ├── README.md
    ├── pedido-resumo-calculo.md
    └── evidencias/
        └── pedido-resumo-calculo/
```

## Como os resultados foram separados

- **Sucesso:** o relatório registra Aprovado para o cenário e o escopo avaliados. As limitações e observações adicionais continuam descritas no documento.
- **Falhas:** o relatório registra Falhou. Quando há exemplos aprovados e reprovados na mesma execução, o relatório completo e todas as suas evidências ficam aqui. As tabelas continuam identificando o resultado de cada exemplo.
- Uma resposta de erro esperada, como recusar quantidade zero, representa sucesso quando atende ao cenário.

As datas, o BDD, as comparações e os resultados originais foram mantidos. Esta reorganização não representa uma nova execução. Os 1.096 arquivos de evidências foram movidos sem alteração de conteúdo, incluindo os registros de tentativas anteriores.

## Próximos relatórios

Use o padrão de [AGENTS.md](../AGENTS.md). Salve o relatório em `sucesso/<nome>.md` ou `falhas/<nome>.md`, conforme o resultado. Guarde seus comprovantes em `evidencias/<nome>/<execucao>/` dentro da mesma pasta e mantenha os links relativos.

Atualize os índices e as quantidades ao adicionar relatórios. Um teste bloqueado ou não executado deve permanecer identificado com esse resultado, sem ser apresentado como sucesso ou falha funcional.

## Reutilizar os scripts das evidências

Os scripts e comandos arquivados foram preservados como registros das execuções originais. Alguns ainda contêm caminhos da estrutura anterior. Para uma nova execução, copie o script para um arquivo de trabalho e ajuste a pasta de saída para a estrutura atual, usando uma pasta de execução nova. Preserve o script original e os comprovantes históricos.

Os relatórios automáticos do Playwright são consultados separadamente, conforme o [guia de automação](../tests/README.md).
