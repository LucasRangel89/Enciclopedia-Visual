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

## Acervo SNAP INSTA — 47 referencias do Instagram

Pasta `SNAP INSTA/` na raiz, 47 JPEG retrato (15 MB), upload direto para `main`.
Conteudo: ilustracao fantasy e concept art, com capas de HQ no estilo pulp e anos
80, character design, environment art de escala epica, gravura em linha, posteres
Art Nouveau e duotones. Autores recorrentes nas marcas d'agua: `TSINT THEHATCA`
e `PHANDI GRAMS`.

`scripts/rotear_snapinsta.py` moveu **30 imagens** para
`08_Imagens_Geradas/Referencias_SnapInsta/`, renomeadas para o embed que a nota
ja declarava, e reescreveu o bloco `## Exemplo Visual` de 30 notas:

| Destino | Imagem | Conceito |
| :--- | :--- | :--- |
| `Gravura_e_Impressao/Agua-forte.md` | `agua_forte.jpg` | coruja em hachura densa |
| `Gravura_e_Impressao/Xilogravura.md` | `xilogravura.jpg` | collie em traco gravado |
| `Ilustradores/Gustav Klimt.md` | `klimt.jpg` | mandala ornamental sobre cidade |
| `Ilustradores/Frank Frazetta.md` | `frazetta.jpg` | rei guerreiro de armadura ornada |
| `Ilustradores/H.R. Giger.md` | `giger.jpg` | olho biomecanico ramificado |
| `Ilustradores/Akira Toriyama.md` | `toriyama.jpg` | criatura peluda de traco arredondado |
| `Ilustradores/Keith Haring.md` | `haring.jpg` | gato em circulo vermelho, linhas irradiantes |
| `Iluminacao_Avancada/Low-Key…md` | `low_key.jpg` | alquimista, luz de vela motivada |
| `Iluminacao_Avancada/Rim Light…md` | `rim_light.jpg` | contorno dourado sobre fundo negro |
| `Iluminacao_Avancada/Silhueta…md` | `silhueta.jpg` | figura de costas contra fogo |
| `Iluminacao_Avancada/Split Lighting…md` | `split_lighting.jpg` | perfil partido ao meio |
| `Cor_e_Grading/Matrix Green…md` | `matrix_green.jpg` | monocromia esverdeada na selva |
| `Cor_e_Grading/Teal and Orange.md` | `teal_orange.jpg` | cemiterio de navios ao poente |
| `Narrativa/Ambiente como Personagem.md` | `ambiente_personagem.jpg` | castelo como protagonista |
| `Narrativa/O Momento Narrativo…md` | `momento_narrativo.jpg` | instante depois da batalha |
| `Narrativa/Prop Storytelling.md` | `prop_storytelling.jpg` | espada em primeiro plano |
| `Narrativa/Staging…md` | `staging.jpg` | tres hobbits contra o troll |
| `Familias/Sonho e Incongruencia.md` | `sonho_incongruencia.jpg` | Jedi em ambiente feudal japones |
| `Fotografia/…Retrato Classico.md` | `retrato_classico.jpg` | busto frontal de estudio |
| `Generos/Fantasia.md` | `fantasia.jpg` | elfa guerreira em floresta azul |
| `Generos/Horror.md` | `horror.jpg` | figura cornuda sobre mar de lava |
| `Generos/Liminal.md` | `liminal.jpg` | torres vermelhas na nevoa |
| `Generos/Pos-Apocaliptico.md` | `pos_apocaliptico.jpg` | vilas abandonadas, ceu esverdeado |
| `Generos/Ficcao Cientifica…md` | `scifi.jpg` | samurai e wookiee armadurados |
| `Midias Mistas/Ilustracao Editorial.md` | `ilustracao_editorial.jpg` | capa de revista com retrato |
| `Midias Mistas/Concept Art.md` | `concept_art.jpg` | olho cosmico sobre piramide |
| `Concept_Art_Games_vs_Cinema…md` | `concept_games.jpg` | guerreiro de caveira gigante |
| `Onda_02/Hiper-realismo…md` | `hiper_realismo.jpg` | mascara de precisao fotografica |
| `Onda_02/Realismo Magico.md` | `realismo_magico.jpg` | hobbits e criatura rinoceronte |
| `Onda_04/Fauvismo.md` | `fauvismo.jpg` | campo de espadas em vermelho e azul |
| `Onda_07/Manga Anime.md` | `manga_anime.jpg` | capa com olhos grandes e hachura |

Duas imagens servem a duas notas cada uma (`651560555` para retrato classico e
hiper-realismo; `69eac7631b3be` para low-key) — a referencia e genuinamente apta
aos dois conceitos.

**Embeds ausentes: 189 -> 159.** 0 links quebrados, 0 ambiguos, 0 homonimos.

As **17 restantes** ficam em `SNAP INSTA/` documentadas em
`SNAP INSTA/LEIA-ME.md`. A pasta entrou em `EXCLUDE_DIRS` de `sync_content.py` e
em `ignorePatterns` de `quartz.config.yaml`, no mesmo tratamento de
`attachments/`: nada referencia essas imagens, e publica-las so pesaria o build.
