# Catálogo de imagens — Enciclopédia Visual

Gerado em 2026-11-15. Cruzamento completo entre o acervo de imagens e as notas.

## Números

| | Arquivos | Usados por notas |
| :--- | ---: | ---: |
| `05_Anexos/` — `<Conceito>_<Gerador>` | 297 | 0 |
| `08_Imagens_Geradas/Pranchas_Comparativas/` — pranchas | 55 | 0 |
| `08_Imagens_Geradas/` — avulsas geradas | 65 | 0 |
| `attachments/NOVAS/` — exports crus | 118 | 0 |
| `attachments/parte2/` — exports crus | 37 | 0 |
| `attachments/ultimos/` — exports crus | 20 | 0 |
| **Total** | **592** | **0** |

## O que foi feito nesta rodada

**1. `attachments/parte1/` → `08_Imagens_Geradas/Pranchas_Comparativas/`**

55 arquivos movidos. Estava na pasta que o build **exclui**, então nenhum
chegava ao site. Agora todos chegam.

**2. 46 pranchas ligadas a 21 MOCs**

São imagens de 4–5 painéis que contrastam conceitos irmãos:

| Prancha | MOC que serve |
| :--- | :--- |
| `Iluminacao_SOFT_HARD_BACK_UNDER` | MOC - Luz |
| `Cor_e_grading_WARM_COLD_TEAL_NOIR` | MOC - Cor e Grading |
| `Camera_enquadramento_EYE_TOP_LOW_OTS` | MOC - Angulos e Pontos de Vista |
| `Generos_universos_CYBER_FANTASY_HORROR_LIMINAL` | MOC - Generos_e_Universos |
| `Movimentos_REAL_IMP_EXP_SUR` | MOC - Movimentos |
| `Textura_materiais_*` | MOC - Textura e Materialidade |
| `Composicao_THIRD_SYM_NEG_LEAD` | MOC - Composição |
| `Gravura_impressao_WOODCUT_ETCH_RISO_LITHO` | MOC - Gravura_e_Impressão |
| …e mais 13 | |

**3. 59 notas ganharam imagem que já existia**

`scripts/cruzar_imagens.py` casa o nome canônico da nota com o nome do
arquivo em `05_Anexos/`, com uma tabela de alias para os casos em que
os nomes divergem (`Greco_Romana` → *Cânone Clássico Greco Romano*).

**Embeds ausentes: 250 → 191.**

## O que ainda não tem casa

**`05_Anexos/` — 275 imagens órfãs.** Nomeadas `<Conceito>_<Gerador>`,
cobrindo ~68 conceitos. A maioria deveria estar em notas, mas as notas
usam outros nomes. A tabela de alias em `cruzar_imagens.py` cobre 83
casos; falta cobrir o resto.

**`attachments/` — 177 exports crus.** Nomes opacos
(`ChatGPT Image 30 de abr. de 2026, 19_47_38.png`). Amostragem mostra que
**também são pranchas de 4 painéis** — movimentos artísticos, famílias
tipográficas — além de imagens avulsas. Só dá para categorizar vendo uma
a uma; são 153 arquivos.

## Contradição a resolver

`attachments/LEIA-ME.md` documenta `attachments/` como o lar das imagens,
com a convenção `<slug>_<gerador>.<ext>`. Mas `sync_content.py` e
`quartz.config.yaml` **excluem** `attachments/` do build. Resultado:
nenhuma imagem seguindo a convenção oficial chega ao site.

Duas saídas:

1. **Tirar `attachments/` da exclusão** — respeita o LEIA-ME, mas publica
   também os 177 exports crus (~500 MB de imagem morta no site).
2. **Manter a exclusão e usar `08_Imagens_Geradas/`** — o site só recebe
   imagem curada. Exige atualizar o LEIA-ME para documentar as duas pastas.

A opção 2 é o que está aplicado agora.

O próprio LEIA-ME já prevê o problema de escala: *"a partir de ~500
arquivos ou ~50 MB, migre para Git LFS"*. O cofre está em **537 imagens
e 1,3 GB**.

## Lote 2 — exports crus de `attachments/NOVAS/` (10 imagens)

Os arquivos `ChatGPT Image ...` sao **pranchas de 4 paineis com rotulo em
ingles**; os `Gemini_Generated_Image_...` sao **imagens avulsas de
referencia por movimento**. `scripts/catalogar_lote.py` move cada uma para
`08_Imagens_Geradas/` com nome significativo e insere o embed no alvo.

| Arquivo original | Novo nome | Tipo | Destino |
| :--- | :--- | :--- | :--- |
| `ChatGPT Image 28 abr 19_18_19` | `Iluminacao_DURA_SOFT_BACK_DIFFUSED` | prancha | MOC - Luz |
| `ChatGPT Image 28 abr 19_18_21` | `Cor_saturacao_ALTA_DESSATURADA_PASTEL_DUOTONE` | prancha | MOC - Cor |
| `ChatGPT Image 28 abr 19_18_24` | `Cor_paleta_QUENTE_FRIA_MONOCROMATICA_COMPLEMENTAR` | prancha | MOC - Cor |
| `ChatGPT Image 28 abr 19_18_26` | `Generos_CYBERPUNK_SOLARPUNK_STEAMPUNK_BIOPUNK` | prancha | MOC - Generos |
| `ChatGPT Image 28 abr 19_18_29` | `Generos_fantasia_ALTA_ESCURA_URBANA_LIMINAL` | prancha | MOC - Generos |
| `ChatGPT Image 28 abr 19_21_26 (1)` | `Cineastas_ANDERSON_BURTON_VILLENEUVE_GHIBLI` | prancha | MOC - Cineastas |
| `Gemini ... 1ipv46...` | `ukiyo_e.png` | avulsa | Ukiyo-e |
| `Gemini ... s4sgk6...` | `romantismo.png` | avulsa | Romantismo |
| `Gemini ... 6r111f...` | `pop_art.png` | avulsa | Pop Art |
| `Gemini ... sxow33...` | `minimalismo_densidade.png` | avulsa | Minimalismo (Densidade Visual) |

Faltam **108** em `NOVAS/`, **37** em `parte2/` e **20** em `ultimos/`.
