# BLUEPRINT — Enciclopédia Visual

> Plano de desenvolvimento do projeto: diagnóstico, arquitetura, roadmap e
> estratégia de escala.
>
> **Data:** 2026-11-15 · **Branch:** `arena/b80f92cb-enciclopedia-visual`
> **Repositório:** `LucasRangel89/Enciclopedia-Visual`

---

## Sumário

1. [Diagnóstico](#1-diagnóstico)
2. [O que estamos construindo](#2-o-que-estamos-construindo)
3. [Opções de implementação](#3-opções-de-implementação)
4. [Arquitetura recomendada](#4-arquitetura-recomendada)
5. [Roadmap](#5-roadmap)
6. [O motor de conteúdo](#6-o-motor-de-conteúdo)
7. [O problema das 495 imagens](#7-o-problema-das-495-imagens)
8. [Automação e CI](#8-automação-e-ci)
9. [Escalonamento](#9-escalonamento)
10. [Riscos e decisões em aberto](#10-riscos-e-decisões-em-aberto)

---

## 1. Diagnóstico

### 1.1 O que existe hoje

| Indicador | Valor |
| :--- | ---: |
| Arquivos Markdown | **248** |
| Notas na árvore canônica | **240** |
| Notas em pastas de staging (`Notas_*_Lote*`) | **92** → já absorvidas |
| Notas com frontmatter | 100% |
| Notas declarando `tem_imagem: true` | **126** |
| Arquivos de imagem no repositório | **0** |
| Embeds `![[...]]` sem arquivo | **495** |
| Wikilinks que não resolviam | **24** → **0** |
| Notas homônimas (quebram wikilinks) | 8 × `00_README.md` |
| Nomes de arquivo com encoding quebrado | **33** → **0** |
| Documentos-fonte soltos na raiz | **8 arquivos, 1,38 MB** |
| Áreas canônicas referenciadas mas inexistentes | **4** → **0** |

> O relatório completo e reproduzível está em
> [`docs/AUDITORIA-2026-11-15.md`](docs/AUDITORIA-2026-11-15.md).
> Regenere quando quiser com `python3 scripts/enciclopedia.py audit`.

### 1.2 O que estava quebrado — e por quê

**a) O cofre tinha duas cópias de si mesmo.**
Seis pastas `Notas_<Tema>_Lote<N>/` continham 92 notas boas, cada uma dentro de
uma duplicata do próprio nome de pasta (`Notas_X/Notas_X/02_Catalogo_Visual/...`),
fora da árvore canônica. Ou seja: o conteúdo existia, mas não era navegável, não
aparecia em nenhum MOC e não podia ser publicado. **Resolvido** pelo
`merge-lots`.

**b) Os nomes de arquivo estavam com encoding quebrado.**
33 arquivos foram gravados com os bytes UTF-8 interpretados como CP437/CP850:
`Sebasti├úo Salgado.md`, `├ôptica & Lentes/`, `Espa├ºo Negativo.md`. Em alguns
sistemas isso quebra links e busca. **Resolvido** pelo `fix-names`.

**c) Quatro módulos existiam só na imaginação.**
O Dashboard apontava para `03_Laboratorio_Visual`, `04_Engenharia_e_Receitas`,
`06_Templates` e `07_Sujeitos_Fixos` — nenhuma dessas pastas existia. **Resolvido**:
as quatro foram criadas, com MOC e conteúdo inicial.

**d) 34 notas eram cascas vazias.**
`Movimento_01` a `Movimento_34` tinham o esqueleto do template mas nenhum
conteúdo real ("Definição breve do movimento 1", "Autor / Obra 1"). Elas
**continuam** sendo o maior trabalho em aberto — ver [Roadmap](#5-roadmap).

**e) Havia três dialetos de frontmatter.**
`parte`/`categoria`, `part`/`category`, `type`/`parent` — três convenções
diferentes convivendo. **Padronizado** para uma só
(`part`, `category`, `status`, `draft`, `tags`, `aliases`, `tem_imagem`,
`images`, `effort`, `last_tested`, `sources`).

**f) A lacuna real: 495 imagens, zero arquivos.**
Este é o gargalo que mais pesa. Ver [seção 7](#7-o-problema-das-495-imagens).

### 1.3 O diagnóstico que importa

O projeto não está atrasado por falta de conteúdo. **Está atrasado porque o
trabalho manual está no lugar errado.** Você já escreveu 1,38 MB de material de
referência de altíssima qualidade — o problema é que cada átomo de conhecimento
dependia de você: criar a nota, criar a pasta, colar os embeds, acertar o
frontmatter, testar o prompt em quatro geradores, corrigir os links.

A conclusão do blueprint é uma só: **automatize tudo que não é julgamento
estético, e reserve seu tempo para o julgamento.**

---

## 2. O que estamos construindo

Uma **enciclopédia interativa**, não um blog e não uma wiki. A diferença é
estrutural:

| | Blog | Wiki | **Enciclopédia interativa** |
| :--- | :--- | :--- | :--- |
| Unidade | post datado | página | **átomo de conhecimento** |
| Ordem | cronológica | alfabética | **navegação por conceito** |
| Entrada | feed | busca | **múltiplas: área, tag, grafo, busca** |
| Saída | ler | consultar | **copiar um prompt e usar** |
| Atualização | publicar | editar | **versionar** |

Para este projeto especificamente, o produto final tem cinco propriedades:

1. **Navegação em rede.** Cada conceito liga a conceitos vizinhos. O grafo do
   Quartz não é enfeite — é a estrutura do domínio ficando visível.
2. **Busca full-text** que encontre o termo de prompt, não só o título da nota.
3. **Consistência formal.** Toda nota tem o mesmo esqueleto, então o leitor
   aprende uma vez e consulta cem.
4. **Vocabulário acionável.** O leitor sai de cada nota com termos em inglês que
   pode colar num gerador.
5. **Manutenção barata.** Publicar é commitar. Nada mais.

---

## 3. Opções de implementação

Comparadas em eixos que importam para *este* projeto (que já é Obsidian, já é
Git, e cujo valor está nos wikilinks e nos embeds de imagem).

| Critério | **Quartz v5** | MkDocs Material | Obsidian Publish | Digital Garden | Astro/Next próprio |
| :--- | :--- | :--- | :--- | :--- | :--- |
| Custo | grátis | grátis | US$ 8/mês | grátis | grátis |
| Wikilinks `[[...]]` | **nativo** | via plugin | nativo | nativo | você implementa |
| Embeds `![[img]]` | **nativo** | via plugin | nativo | nativo | você implementa |
| Grafo de conexões | **sim** | não | parcial | sim | você implementa |
| Backlinks | **sim** | não | sim | sim | você implementa |
| Busca full-text | **sim** | sim (ótima) | sim | sim | você implementa |
| Callouts `> [!tip]` | **sim** | sim | sim | sim | você implementa |
| Frontmatter/propriedades | **sim** | sim | sim | sim | você implementa |
| Deploy Git → Pages | **sim** | sim | n/a | via Netlify | sim |
| Controle do layout | médio | **alto** | nenhum | baixo | **total** |
| Curva de setup | baixa | média | **zero** | baixa | alta |
| Versionamento do site | **sim** | sim | não | sim | sim |
| Escala (1000+ notas) | boa | **ótima** | boa | média | depende |
| Multi-idioma (i18n) | **sim** | sim | não | não | sim |

### 3.1 Recomendação: **Quartz v5**

**Por quê:**

- É o único que entende o cofre *como ele é*, sem camada de conversão. Nenhum
  passo de "exportar para markdown limpo" — o que elimina uma classe inteira de
  problemas de manutenção.
- Grafo, backlinks, popovers de prévia e busca full-text vêm de fábrica. Para
  uma enciclopédia, isso não é opcional.
- O site é **gerado**: o repositório contém só o cofre e a config. O Quartz é
  clonado no CI. Atualizar o gerador é trocar uma linha.
- É grátis e o deploy no GitHub Pages é um workflow de 40 linhas.

**Ressalvas honestas:**

- MkDocs Material tem busca e navegação hierárquica melhores, e é a escolha
  certa se o projeto evoluir para *documentação técnica* em vez de enciclopédia.
  Se isso acontecer, a migração é possível porque o conteúdo continua sendo
  Markdown.
- Quartz **não** tem sistema de comentários nativo (dá para plugar giscus) nem
  controle fino de layout sem mexer em componentes.
- O Quartz v5 é recente (v5.1.0, nov/2026) e exige **Node 22+**.

### 3.2 A que renunciamos ao escolher Quartz

- **Obsidian Publish** (US$ 8/mês) seria mais simples, mas trancaria o conteúdo
  num serviço pago, sem deploy por Git e sem likeability do site. Para um
  projeto que quer escalar, é um beco.
- **Digital Garden** é uma boa opção, mas exige configurar Netlify à parte e tem
  manutenção menos ativa.
- **Astro/Next próprio** daria controle total — inclusive componentes
  interativos verdadeiros (ver [seção 9](#9-escalonamento)) — mas cobraria
  semanas de trabalho que deveriam ir para o conteúdo. Fica como **fase 4
  opcional**, não como ponto de partida.

---

## 4. Arquitetura recomendada

### 4.1 Decisão de desenho: um repositório, site gerado

A grande decisão é **onde vive o Quartz**. Há duas opções:

| | (A) Dois repositórios | (B) Um repositório, site gerado |
| :--- | :--- | :--- |
| Cofre | `Enciclopedia-Visual` | `Enciclopedia-Visual` (raiz) |
| Site | `enciclopedia-site` (fork do Quartz) | clonado no CI para `site/` |
| Versionado | cofre + site | **só o cofre** |
| Atualizar o Quartz | `git pull` no fork | mudar `QUARTZ_REF` |
| Upload pelo GitHub web | funciona | funciona |
| Complexidade | dois lugares para olhar | **um** |

**Escolhemos (B).** Motivos: você faz upload pelo navegador, e ter dois
repositórios para gerenciar nesse fluxo é atrito desnecessário. Além disso, o
site gerado nunca é editado à mão — então não há razão para versioná-lo.

```
Enciclopedia-Visual/                 ◄── o cofre Obsidian (raiz do repo)
├── 00_Dashboard/                    navegação e MOCs
├── 01_Fundamentos_Teoricos/         as 9 variáveis da imagem
├── 02_Catalogo_Visual/              repertório
├── 03_Laboratorio_Visual/           séries de exploração
├── 04_Engenharia_e_Receitas/        prompts e anti-erros
├── 05_Anexos/                       PDFs
├── 06_Templates/                    template canônico + prompt de extração
├── 07_Sujeitos_Fixos/               sujeitos recorrentes
├── attachments/                     imagens dos embeds ![[...]]
├── _fontes/                         documentos-fonte (fora do site)
├── docs/                            relatórios gerados
├── scripts/                         ferramentas Python + preview.sh
├── .github/workflows/               validate.yml + deploy.yml
├── index.md                         landing page do site
├── quartz.config.yaml               config do site (vive na raiz!)
└── README.md

site/                                ◄── GERADO, no .gitignore
├── content/                         cópia filtrada do cofre (sync_content.py)
├── quartz.config.yaml               cópia do da raiz
└── public/                          saída do build
```

### 4.2 O funil de publicação

```
  cofre (raiz)
      │
      │  scripts/sync_content.py
      │  · remove .git, .obsidian, _fontes, scripts, docs, attachments,
      │    site, Notas_*, *.pdf
      │  · mantém 00_ a 07_, index.md
      ▼
  site/content/
      │
      │  npx quartz build
      │  · parseia Markdown + frontmatter
      │  · resolve wikilinks (markdownLinkResolution: shortest)
      │  · aplica ignorePatterns de quartz.config.yaml
      │  · emite HTML + busca + grafo + sitemap + RSS
      ▼
  site/public/  ──►  GitHub Pages
```

**Regra de ouro: a lista de exclusão existe em dois lugares**
(`EXCLUDE_DIRS` no `sync_content.py` e `ignorePatterns` no `quartz.config.yaml`)
e os dois precisam dizer a mesma coisa. É a única sincronização manual do
sistema — e o script falha alto se você esquecer, porque o conteúdo indevido
simplesmente aparece no site.

### 4.3 O esquema de frontmatter

Uma convenção só, aplicada a todas as notas:

```yaml
---
title: "Cor - Saturação e Contraste"   # igual ao nome do arquivo
part: "01_Fundamentos_Teoricos"        # uma das 8 áreas canônicas
category: "Cor"                        # subárea (agrupamento no explorador)
status: rascunho                       # ideia | rascunho | revisao | publicado
draft: true                            # derivado de status; true não publica
tags: [cor, saturacao, contraste]      # 3–6, minúsculas, hifenizadas
aliases: ["Saturation and Contrast"]   # nome em inglês + sinônimos (busca)
tem_imagem: false                      # true exige que images existam
images: []                             # nomes em attachments/
effort: 2                              # 1–5: quanto trabalho falta
last_tested: "2026-11-15"              # quando o prompt foi validado
sources: ["Guia Avançado...md"]        # procedência do conteúdo
---
```

`status` é a peça central: ele alimenta o filtro de rascunhos do Quartz
(`draft: true` não é publicado), o painel de progresso e a ordenação do
explorador.

### 4.4 MOCs: o esqueleto de navegação

Um **MOC** (Map of Content) é uma nota-índice que vive dentro da pasta que
indexa. São eles que transformam 240 arquivos numa enciclopédia — sem eles, o
leitor vê uma lista de pastas.

```
MOC - Fundamentos                     (01_Fundamentos_Teoricos/)
├── MOC - Composicao
│   └── MOC - Perspectiva_e_Pontos_de_Fuga
├── MOC - Cor
├── MOC - Luz
├── MOC - Óptica & Lentes
├── MOC - Ritmo e Tempo
├── MOC - Textura e Materialidade
├── MOC - Tipografia e Linguagem Visual
├── MOC - Densidade Visual
└── MOC - Figura Humana e Expressao

MOC - Catalogo Visual                 (02_Catalogo_Visual/)
├── MOC - Movimentos
│   └── MOC - Onda_01 … Onda_07
├── MOC - Assinaturas_Autorais
├── MOC - Generos_e_Universos
├── MOC - Arquitetura_Cenario_e_Personagem
├── MOC - Narrativa_Visual_e_Storytelling
├── MOC - Musica_e_Capas_de_Album
├── MOC - Cor e Grading
├── MOC - Iluminacao_Avancada
└── MOC - Midias e Suportes
```

Cada MOC tem uma **seção de índice automático** entre marcadores, regida pelo
`scripts/moc.py`:

```markdown
<!-- inicio:indice-automatico -->
- [[Composição - Regra dos Terços]]
- [[Composição - Proporção Áurea]]
<!-- fim:indice-automatico -->
```

O script só mexe **entre** os marcadores. Tudo que você escrever fora deles —
curadoria, comentários, agrupamentos temáticos — é preservado. Essa é a regra
que permite automação sem perder autoria.

---

## 5. Roadmap

### Fase 0 — Fundação técnica ✅ *concluída nesta branch*

| Entregável | Estado |
| :--- | :--- |
| Absorver as 92 notas de staging na árvore canônica | ✅ |
| Corrigir 33 nomes com encoding quebrado | ✅ |
| Criar as 4 áreas canônicas ausentes | ✅ |
| Padronizar frontmatter (232 notas) | ✅ |
| Gerar 54 MOCs a partir da estrutura de pastas | ✅ |
| Zerar os wikilinks quebrados | ✅ |
| Mover 8 documentos-fonte para `_fontes/` | ✅ |
| Criar `index.md` (landing page) | ✅ |
| `scripts/enciclopedia.py` (audit, links, fix-names, merge-lots, normalize, new) | ✅ |
| `scripts/moc.py`, `scripts/sync_content.py`, `scripts/preview.sh` | ✅ |
| `quartz.config.yaml` com tema próprio | ✅ |
| CI: `validate.yml` + `deploy.yml` | ✅ |
| `06_Templates/` com template canônico e `PROMPT-EXTRACAO` | ✅ |
| 4 notas de fundamento escritas no padrão (Proporção Áurea, Saturação/Contraste, Luz, High/Low-key) | ✅ |
| Build local do site validado | ✅ |

**O que fazer agora:**

```bash
git checkout arena/b80f92cb-enciclopedia-visual   # já está nela
./scripts/preview.sh                              # ver o site em :4173
```

### Fase 1 — Ligar o botão (1 dia)

1. **Habilitar GitHub Pages.** Repositório → *Settings → Pages → Build and
   deployment → Source: GitHub Actions*.
2. **Ajustar `baseUrl`** em `quartz.config.yaml` para
   `lucasrangel89.github.io/enciclopedia-visual` (já está assim).
3. **Merge para `main`** e confirmar que o `deploy.yml` publicou.
4. **(Opcional) Domínio próprio.** Cloudflare Pages em vez de Pages se quiser
   URLs sem barra final — o GitHub Pages não faz redirect de trailing slash.

### Fase 2 — Fechar os fundamentos (2–3 semanas)

O objetivo é que `01_Fundamentos_Teoricos/` fique **completa e coerente**, porque
é a porta de entrada de tudo.

Ordem de ataque, por retorno:

1. **As 9 variáveis** — uma nota mestra por variável, no padrão da seção 6.
2. **Sub-variáveis** — uma nota por valor distinto (ex.: em Cor, uma por
   harmonia; em Luz, uma por esquema de iluminação).
3. **Corpo, pose e expressão** — a subpasta `Figura Humana e Expressao` já tem
   casca; falta conteúdo.
4. **Óptica & Lentes** — 5 tipos de bokeh, aberração cromática, dolly zoom.

Use o [`PROMPT-EXTRACAO`](06_Templates/PROMPT-EXTRACAO.md) apontado para as
seções correspondentes dos documentos em `_fontes/`. Cada execução do prompt
produz uma nota pronta para revisão.

**Critério de conclusão da fase:** nenhuma nota em `01_Fundamentos_Teoricos/`
com `status: rascunho`.

### Fase 3 — O catálogo (4–6 semanas)

Aqui vive o maior volume: os 34 `Movimento_NN` vazios, os gêneros, as
assinaturas autorais.

Ordem:

1. **Movimentos artísticos** — 7 ondas × 5 = 35 slugs. Renomeie
   `Movimento_01.md` para o nome real do movimento antes de escrever, para que
   os wikilinks fiquem legíveis.
2. **Gêneros e universos** — 13 já escritos; faltam ~20 (western espaguete,
   ficção científica hard, new weird, fantasia sombria…).
3. **Assinaturas autorais** — 25 escritas. O padrão já está bom; falta
   consistência no `tem_imagem`.
4. **Mídias, Cor e Grading, Iluminação Avançada, Fotografia** — pastas criadas,
   zero notas. São as de maior débito.

**Critério de conclusão:** nenhuma pasta em `02_Catalogo_Visual/` sem MOC
preenchido.

### Fase 4 — O laboratório e as receitas (contínuo)

`03_Laboratorio_Visual/` e `04_Engenharia_e_Receitas/` não são para "terminar" —
são para **alimentar**. Uma série nova por mês é um bom ritmo. O laboratório é o
que separa esta enciclopédia de um compilado: é aqui que as afirmações das notas
são testadas.

### Fase 5 — Escalar (ver [seção 9](#9-escalonamento))

---

## 6. O motor de conteúdo

Este é o coração do blueprint. A pergunta não é "como escrever 1000 notas" — é
**"como escrever 1000 notas sem que isso consuma seis meses da sua vida"**.

### 6.1 O princípio: separar redação de verificação

Um modelo de linguagem escreve uma nota no padrão em **segundos**. O que dá
trabalho é confirmar que a afirmação é verdadeira e que o prompt funciona.
Portanto:

- **Redação: automatizada.** Via [`PROMPT-EXTRACAO`](06_Templates/PROMPT-EXTRACAO.md).
- **Verificação: humana, e só ela.** Você lê o ` Conceito Técnico`, testa o
  prompt em dois geradores, e marca `status: revisao`.

Tempo estimado por nota: **3–5 minutos de revisão** contra 30–60 minutos de
redação manual. É uma redução de ordem de magnitude.

### 6.2 O pipeline

```
_fontes/<documento>.md
      │
      │  1. localizar a seção (grep por "## <título>")
      ▼
   trecho
      │
      │  2. PROMPT-EXTRACAO (LLM)  → nota no formato canônico
      ▼
   02_Catalogo_Visual/.../Nota.md
      │
      │  3. você revisa: Conceito Técnico + testa o prompt
      ▼
   status: revisao → publicado
      │
      │  4. python3 scripts/enciclopedia.py links --fail
      ▼
   git commit → push → site atualiza
```

### 6.3 Regras que mantêm a qualidade em escala

1. **Uma nota = um conceito.** Se a nota precisa de dois `##` de topo, são duas
   notas. É o que permite comparar e linkar.
2. **Sempre registre `sources:`.** Em seis meses você não vai lembrar de onde
   veio a afirmação sobre bokeh swirly.
3. **Termos de prompt em inglês e entre crases.** Sem exceção — é o que torna a
   nota pesquisável e copiável.
4. **Nunca commite sem rodar `links --fail`.** Um link quebrado no site é
   credibilidade perdida.
5. **Lotes de 5 a 10 notas por sessão.** Além disso, a revisão fica mecânica e
   a qualidade cai.
6. **Um prompt de referência por nota, testado.** Se não foi testado, marque
   `last_tested:` com a data antiga e deixe `status: rascunho`.

### 6.4 Como decidir *o que* escrever a seguir

Não escreva no escuro. O repositório já contém um roteiro:
[`_fontes/Roteiro_Exploracao_Enciclopedia_Visual.md`](_fontes/Roteiro_Exploracao_Enciclopedia_Visual.md)
lista ~200 tópicos organizados em 6 fases, cruzando as quatro fontes. Transforme
esse checklist em issues do GitHub (uma por fase) e trabalhe issue por issue —
assim o progresso é visível e reversível.

---

## 7. O problema das 495 imagens

**Situação:** 126 notas declaram `tem_imagem: true` e contêm 495 embeds
`![[arquivo.png]]`. Nenhum arquivo existe. No site, cada embed quebrado renderiza
como um bloco vazio — o que é pior que não ter imagem.

### 7.1 As três opções reais

| Opção | Custo | Qualidade | Escalabilidade |
| :--- | :--- | :--- | :--- |
| **A. Gerar as 495 imagens** | altíssimo (495 execações de prompt + revisão) | alta, mas heterogênea | ruim |
| **B. Placeholder sistemático** | baixo | honesta | ótima |
| **C. Gerar só as mais importantes** | médio | alta onde importa | boa |

### 7.2 Recomendação: B agora, C depois

**Fase B (imediata, ~1 hora):**

Escreva um script que, para cada embed sem arquivo, gere um **placeholder
descritivo** — um SVG com o nome do arquivo, o nome da nota e o gerador
esperado. O site fica honesto ("esta imagem ainda não existe") em vez de
quebrado, e o débito fica **visível e mensurável**.

```python
# esqueleto de scripts/placeholders.py
# para cada embed ![[x.png]] sem attachments/x.png:
#   gerar attachments/x.png (ou x.svg) com:
#     "harmonia_complementar_leonardo"
#     "aguardando geração — Leonardo AI"
```

**Fase C (depois):**

Priorize por tráfego e por valor didático. Uma imagem vale a pena quando a nota
depende de *comparação visual* (harmonias de cor, tipos de bokeh, esquemas de
luz, ângulos de câmera). Para conceitos abstratos ( epistemologia do prompt,
hierarquia tipográfica), o texto basta.

**Ordem de prioridade para geração:**

1. Esquemas de iluminação (a imagem é o argumento)
2. Harmonias e paletas de cor
3. Ângulos e pontos de vista
4. Tipos de bokeh e aberração cromática
5. Movimentos artísticos (uma imagem de referência por movimento)
6. Todo o resto

### 7.3 Se o volume crescer

A partir de ~500 imagens ou ~50 MB:

- **Git LFS** para os binários (`git lfs track "attachments/*.png"`), ou
- **armazenamento externo** (Cloudflare R2, Backblaze B2) com os embeds
  apontando para URLs absolutas.

Não faça isso antes: LFS adiciona complexidade de setup e o GitHub dá 1 GB de
banda/mês grátis, o que é muita imagem para um site que ainda não tem público.

---

## 8. Automação e CI

Dois workflows, já no repositório:

### `validate.yml` — a rede de segurança

Roda em todo push e PR:

1. `python3 scripts/enciclopedia.py audit` → relatório completo
2. `python3 scripts/enciclopedia.py links --strict` → **falha o build** se
   houver link que não resolve
3. Publica o relatório como artefato e como resumo do job

É isto que permite commitar com pressa: o CI pega o que você esqueceu.

### `deploy.yml` — a publicação

Roda em push para `main`:

```yaml
1. checkout (fetch-depth: 0 — o Quartz usa o histórico do Git para as datas)
2. setup Node 22
3. git clone --branch v5 jackyzha0/quartz → site/
4. npm ci
5. python3 scripts/sync_content.py --dest site/content
6. cp quartz.config.yaml site/
7. npx quartz plugin install
8. npx quartz build
9. upload-pages-artifact → deploy-pages
```

**Notas de operação:**

- O `fetch-depth: 0` é obrigatório. Sem histórico, o plugin de datas usa a data
  do filesystem e todas as notas ficam com a mesma data.
- Se adicionar plugins a `quartz.config.yaml` sem atualizar o lockfile, acrescente
  `npx quartz plugin install --from-config` depois do `install`.
- Cloudflare Pages é uma alternativa melhor se URLs com barra final importarem
  (o GitHub Pages não redireciona `foo` → `foo/`).

---

## 9. Escalonamento

Quando (e se) fizer sentido — nesta ordem:

### 9.1 Curto prazo — gratuitos e de alto retorno

| Melhoria | Esforço | Retorno |
| :--- | :--- | :--- |
| Domínio próprio + Cloudflare Pages | 1h | credibilidade, URLs limpos |
| RSS já está ligado | 0 | leitores por feed |
| `og-image` já está ligado | 0 | bons cards em redes sociais |
| Plausible Analytics (grátis, sem cookie) | 30min | saber o que as pessoas leem |
| giscus (comentários via GitHub Discussions) | 1h | correções da comunidade |
| i18n: `locale: en-US` + versão em inglês | alto | multiplicar alcance |

### 9.2 Médio prazo — interatividade de verdade

O Quartz gera HTML estático. Para interatividade real, a rota é um
**componente Astro/React** embutido, ou uma migração futura para Astro.
Candidatos, por valor:

1. **Comparador lado a lado.** Dois sliders de prompt, duas imagens, mesmo
   sujeito. É o sonho do projeto — e nada no mercado faz bem.
2. **Construtor de prompt.** Checkboxes dos módulos de engenharia que montam o
   prompt em tempo real e copiam para a área de transferência.
3. **Filtro por variável.** "Mostre só notas que falam de luz" — um facet filter
   sobre o frontmatter.
4. **Modo tablea comparativa.** Ver N conceitos da mesma categoria em colunas.

**Só faça isso depois que o conteúdo justificar.** Componente sem conteúdo é
demo vazia.

### 9.3 Longo prazo — o projeto como plataforma

- **API de consulta.** O cofre é Markdown versionado; um endpoint que devolva
  `GET /api/conceito/harmonia-complementar` em JSON torna o conteúdo
  programático.
- **Contribuição externa.** Issues templateadas ("esta nota está errada porque…")
  + PRs de correção. O conteúdo é verificável porque tem `sources:`.
- **Publicação de datasets.** Exportar o vocabulário de prompt como CSV/JSON
  público — tem valor independente do site.

---

## 10. Riscos e decisões em aberto

### 10.1 Riscos

| Risco | Probabilidade | Mitigação |
| :--- | :--- | :--- |
| Voltarmos a acumular pastas `Notas_*` | alta | `ignorePatterns` já as exclui do site; rode `merge-lots` antes de commitar |
| Embeds quebrados aparecerem no site | média | `links --fail` no CI; `tem_imagem: false` até a imagem existir |
| 34 notas-vazia poluírem a navegação | alta | `status: rascunho` + `draft: true` já as exclui da publicação |
| Homônimos quebrarem wikilinks | média | `audit` seção 5 detecta; renomeie antes de linkar |
| Encoding quebrado voltar pelo upload web | média | `fix-names --apply` após cada lote; ou use Git em vez do navegador |
| Perda de motivação no meio da Fase 3 | média | **commits pequenos e frequentes**; cada merge publica algo visível |

### 10.2 Decisões que precisam da sua resposta

1. **Domínio.** GitHub Pages grátis (`lucasrangel89.github.io/enciclopedia-visual`)
   ou domínio próprio? Se próprio, qual?
2. **Imagens.** Começar pelos placeholders (recomendado) ou já investir em gerar
   as 50 mais importantes?
3. **Idioma.** Só português, ou plano de versão em inglês desde já? Isso muda
   como você escreve os `aliases`.
4. **Nomeação dos movimentos.** `Movimento_01.md` deve virar `Renascimento.md`?
   (Recomendo sim — mas são 35 renomeações e links a ajustar.)
5. **Escopo do catálogo.** O README de `02_Catalogo_Visual/` lista 14 subpastas.
   Todas são necessárias, ou podemos cortar 3–4 e reduzir o débito?

### 10.3 O que *não* fazer

- **Não escreva notas manualmente no padrão antigo.** Use o template e o
  `enciclopedia.py new`.
- **Não commite imagens diretamente na raiz.** Elas vão em `attachments/`.
- **Não edite nada em `site/`.** É gerado; editar lá é trabalho perdido.
- **Não renomeie arquivos sem rodar `links` depois.** Um rename quebrado é pior
  que um nome feio.

---

## Apêndice A — comandos do dia a dia

```bash
# criar nota
python3 scripts/enciclopedia.py new "Harmonia Tríade" \
    --part 01_Fundamentos_Teoricos --category Cor \
    --tags cor harmonia triade

# regenerar MOCs após criar/mover notas
python3 scripts/moc.py --apply

# auditar antes de commitar
python3 scripts/enciclopedia.py audit
python3 scripts/enciclopedia.py links --fail

# ver o site
./scripts/preview.sh

# corrigir encoding após upload pelo navegador
python3 scripts/enciclopedia.py fix-names --apply

# absorver pastas de lote
python3 scripts/enciclopedia.py merge-lots --apply
```

## Apêndice B — checklist de uma nota pronta

- [ ] frontmatter completo, com `status` e `draft` coerentes
- [ ] ` Conceito Técnico` verificável e com `sources:` preenchido
- [ ] termos de prompt em inglês e entre crases
- [ ] prompt de referência testado em ≥ 2 geradores, com `--ar`
- [ ] `aliases` com o nome em inglês
- [ ] 3–6 `tags` minúsculas e hifenizadas
- [ ] wikilinks para notas vizinhas (mínimo 2)
- [ ] se `tem_imagem: true`, os arquivos existem em `attachments/`
- [ ] link de entrada a partir de algum MOC
