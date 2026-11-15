# Inventário de imagens — Enciclopédia Visual

Gerado em 2026-11-15 a partir de `scripts/enciclopedia.py audit`.

## Números

| | |
| :--- | ---: |
| Notas no cofre | 404 |
| Notas com imagem embutida ausente | 238 |
| Total de imagens ausentes | 913 |
| Notas sem nenhuma imagem faltando | 166 |

O build **passa** com todas elas ausentes: o Quartz emitiu 4047 arquivos
a partir de 392 notas sem nenhum erro. A dívida é visual, não estrutural.

## Por prioridade (a ordem que você aprovou)

| Prioridade | Notas | Imagens |
| :--- | ---: | ---: |
| 1. Esquemas de iluminação | 8 | 32 |
| 2. Harmonia e paletas de cor | 15 | 48 |
| 3. Ângulos e pontos de vista | 4 | 16 |
| 4. Bokeh, lentes e aberrações | 11 | 44 |
| 5. Movimentos artísticos | 25 | 96 |
| 6. Todo o resto | 175 | 677 |
| **Total** | **238** | **913** |

## Por gerador esperado

Cada nota pede 4 imagens, uma por gerador, pelo sufixo do nome do arquivo:

| Gerador | Imagens |
| :--- | ---: |
| `raphael` | 239 |
| `dalle3` | 237 |
| `leonardo` | 222 |
| `imagen` | 215 |

## Notas que mais precisam de imagem

| Faltam | Nota |
| ---: | :--- |
| 4 | `01_Fundamentos_Teoricos/Figura Humana e Expressao/Abordagens_do_Nu_na_Arte/Nudez Artística Clássica.md` |
| 4 | `01_Fundamentos_Teoricos/Figura Humana e Expressao/Abordagens_do_Nu_na_Arte/Nudez Documental.md` |
| 4 | `01_Fundamentos_Teoricos/Figura Humana e Expressao/Expressao_Facial_e_Emocao/Alegria.md` |
| 4 | `01_Fundamentos_Teoricos/Figura Humana e Expressao/Expressao_Facial_e_Emocao/Surpresa.md` |
| 4 | `01_Fundamentos_Teoricos/Figura Humana e Expressao/Expressao_Facial_e_Emocao/Tristeza.md` |
| 4 | `01_Fundamentos_Teoricos/Geometria de Cena/Angulos e Pontos de Vista/Dutch Angle (Câmera Inclinada).md` |
| 4 | `01_Fundamentos_Teoricos/Geometria de Cena/Angulos e Pontos de Vista/Ângulo Contra-Plongée.md` |
| 4 | `01_Fundamentos_Teoricos/Geometria de Cena/Angulos e Pontos de Vista/Ângulo Eye-Level.md` |
| 4 | `01_Fundamentos_Teoricos/Geometria de Cena/Angulos e Pontos de Vista/Ângulo Plongée (Câmera Alta).md` |
| 4 | `01_Fundamentos_Teoricos/Geometria de Cena/Distancia Focal e Efeito Psicologico/Grande-Angular e Efeito Psicológico.md` |
| 4 | `01_Fundamentos_Teoricos/Geometria de Cena/Distancia Focal e Efeito Psicologico/Teleobjetiva e Efeito Psicológico.md` |
| 4 | `01_Fundamentos_Teoricos/Geometria de Cena/Movimentos de Camera Implicitos/Movimento Implícito — Dolly.md` |
| 4 | `01_Fundamentos_Teoricos/Geometria de Cena/Movimentos de Camera Implicitos/Movimento Implícito — Pan.md` |
| 4 | `01_Fundamentos_Teoricos/Geometria de Cena/Movimentos de Camera Implicitos/Movimento Implícito — Tilt.md` |
| 4 | `01_Fundamentos_Teoricos/Geometria de Cena/Profundidade de Campo e Abertura/Profundidade de Campo Profunda.md` |
| 4 | `01_Fundamentos_Teoricos/Geometria de Cena/Profundidade de Campo e Abertura/Profundidade de Campo Rasa.md` |
| 4 | `01_Fundamentos_Teoricos/Geometria de Cena/Regras de Composicao e Subversao/Enquadramento (Frame Dentro do Frame).md` |
| 4 | `01_Fundamentos_Teoricos/Geometria de Cena/Regras de Composicao e Subversao/Espaço Negativo.md` |
| 4 | `01_Fundamentos_Teoricos/Geometria de Cena/Regras de Composicao e Subversao/Proporção Áurea e Padrão Espiral.md` |
| 4 | `01_Fundamentos_Teoricos/Geometria de Cena/Regras de Composicao e Subversao/Simetria como Princípio Compositivo.md` |
| 4 | `01_Fundamentos_Teoricos/Geometria de Cena/Regras de Composicao e Subversao/Subversão Deliberada da Composição.md` |
| 4 | `01_Fundamentos_Teoricos/Ritmo e Tempo/Congelamento de Movimento (Freeze).md` |
| 4 | `01_Fundamentos_Teoricos/Ritmo e Tempo/Longa Exposição e Motion Blur.md` |
| 4 | `01_Fundamentos_Teoricos/Textura e Materialidade/Grão e Ruído Visual (Grain, Dust, Scratches).md` |
| 4 | `01_Fundamentos_Teoricos/Textura e Materialidade/Superfícies Artificiais.md` |

## O que já existe no cofre

297 imagens em `05_Anexos/` e 230 em `attachments/`. Nenhuma delas resolve
os 913 embeds: as de `05_Anexos/` seguem o padrão `<Artista>_<Gerador>.jpg`
(ex. `Frazetta_Leonardo.jpg`), enquanto os embeds pedem
`<conceito>_<gerador>.png` (ex. `harmonia_complementar_raphael.png`).
São acervos paralelos — as de `05_Anexos/` cobrem **assinaturas autorais**,
os embeds cobrem **fundamentos técnicos**.

## Recomendação de execução

1. **Placeholders primeiro.** Rodar `generate_image` para as 238 notas é
   inviável nesta sessão; em vez disso, marcar a dívida no frontmatter
   (`falta: [raphael, dalle3]`) para que o painel mostre o buraco.
2. **Depois, as ~50 de maior valor**, na ordem da tabela de prioridade:
   32 de iluminação + 48 de cor + 60 de ângulos já são 140 imagens.
   Dentro de cada nota, gerar **1** imagem (não 4) e apontar os outros
   três embeds para ela.
3. **Bokeh e movimento:** 0 imagens em bucket próprio porque essas notas
   estão em `Óptica & Lentes` e `Geometria de Cena` — verificar antes de
   priorizar.