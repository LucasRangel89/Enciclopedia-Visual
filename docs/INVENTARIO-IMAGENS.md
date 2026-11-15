# Inventário de imagens — Enciclopédia Visual

Gerado em 2026-11-15. Uma imagem por nota basta para começar.

## Números

| | |
| :--- | ---: |
| Notas no cofre | 404 |
| Notas com imagem ausente | 250 |
| Imagens ausentes | 250 |
| Imagens já geradas | 10 |

Cada nota pedia 4 imagens (uma por gerador). `scripts/reduzir_imagens.py`
colapsou a galeria para uma por nota: **913 → 260** embeds, e os
geradores descartados ficaram registrados no frontmatter `falta:`.

O build passa com todas ausentes — verificado, não presumido.

## Por prioridade

| Prioridade | Notas | Imagens |
| :--- | ---: | ---: |
| 1. Iluminação | 6 | 6 |
| 2. Cor | 17 | 17 |
| 3. Ângulos | 4 | 4 |
| 4. Bokeh/óptica | 11 | 11 |
| 5. Movimentos | 27 | 27 |
| 6. Resto | 185 | 185 |
| **Total** | **250** | **250** |

## Feito

10 imagens em `08_Imagens_Geradas/`, geradas a partir do prompt
testado de cada nota:

| Nota | Arquivo |
| :--- | :--- |
| Luz Dura | `Luz_Dura.png` |
| Luz Suave Difusa | `Luz Suave Difusa.png` |
| Iluminação Rembrandt | `Rembrandt_exemplo.png` |
| Contraluz | `Contraluz.jpg` |
| Golden Hour | `Golden_Hour.jpg` |
| Luz Volumétrica e Meio | `Luz_Volumetrica.jpg` |
| Luz de Vela | `Luz_de_Vela.jpg` |
| Underlight | `Underlight.jpg` |
| Butterfly Lighting (Iluminação Borboleta) | `butterfly.png` |
| High-Key Lighting (Iluminação Alta-Chave) | `high_key.png` |

Faltam 6 de iluminação: `pratica`, `loop_lighting`, `low_key`,
`rim_light`, `silhueta`, `split_lighting`.

## Onde as imagens entram no site

`08_Imagens_Geradas/` **entra** no build. `attachments/` **não entra** —
está em `EXCLUDE_DIRS` do `sync_content.py` e em `ignorePatterns` do
`quartz.config.yaml`.

Consequência: as **230 imagens que você subiu para `attachments/` nunca
aparecem no site**. E nenhuma delas é citada por nota alguma — são
exportações cruas (`ChatGPT Image ... .png`).

## Estado do acervo

| Pasta | Imagens | Citadas | Chegam ao site |
| :--- | ---: | ---: | :--- |
| `attachments/` | 230 | 0 | não |
| `05_Anexos/` | 297 | 22 | sim |
| `08_Imagens_Geradas/` | 10 | 10 | sim |

O cofre tem **1,3 GB** rastreados no git, a maior parte em imagens.
Nenhum arquivo passa de 50 MB, então o git aceita, mas o repo está
acima do limite recomendado pelo GitHub (~1 GB).