---
title: Template - Nota Atômica
part: "06_Templates"
category: Template
type: template
status: publicado
draft: false
tags: [template, nota-atomica, padrao]
aliases:
  - Nota Atômica
  - Template de Nota
tem_imagem: false
images: []
effort: 1
sources: []
---
# Template — Nota Atômica

Este é o esqueleto canônico de toda nota da enciclopédia. **Não invente seções novas**: a uniformidade é o que permite comparar conceitos e alimentar o site.

Copie o bloco abaixo (ou rode `python3 scripts/enciclopedia.py new "<Título>" --part <área> --category <subárea>`).

```markdown
---
title: "<Título da nota>"
part: "<00_Dashboard|01_Fundamentos_Teoricos|02_Catalogo_Visual|...>"
category: "<subárea>"
status: rascunho
draft: true
tags: [<3 a 6 tags, minúsculas, hifenizadas>]
aliases: ["<Nome em inglês>", "<Sinônimo em português>"]
tem_imagem: false
images: []
effort: 2
last_tested: "<AAAA-MM-DD>"
sources: ["<documento-fonte de onde veio>"]
---

# <Título>

## Conceito Técnico
<Definição em 2 a 5 frases. O que é, como funciona, qual a origem do termo.>

---

## Efeito Psicológico e Narrativo
* **<Efeito 1>:** <como o espectador lê>
* **<Efeito 2>:** <que emoção ou sentido produz>
* **<Efeito 3>:** <quando usar e quando evitar>

---

## Aplicações Práticas
* **<Mídia/campo 1>:** <exemplo concreto>
* **<Mídia/campo 2>:** <exemplo concreto>

---

## Módulos para Engenharia de Prompt

| Parâmetro | Configuração Recomendada | Efeito no Gerador de IA |
| :--- | :--- | :--- |
| **<Parâmetro>** | `termo em inglês, entre crases` | <o que muda na imagem> |

### Vocabulário para Prompt
* `termo-um`
* `termo-dois`
* `termo-tres`

---

## 🖼️ Galeria de Exemplos Visuais (Multi-gerador)

### 1. ChatGPT (DALL-E 3)
![[<slug>_dalle3.png]]
* **Legenda:** <o que observar nesta imagem>

### 2. Gemini (Google Imagen)
![[<slug>_imagen.png]]
* **Legenda:** <...>

### 3. Leonardo AI
![[<slug>_leonardo.png]]
* **Legenda:** <...>

---

## ⚙️ Prompt de Referência (Testado)

```
<prompt completo, em inglês, com proporção no final>
```

## Notas de Revisão
- <data: o que testar ainda>
```

---

## Regras do frontmatter

| Chave | Valores | Observação |
| :--- | :--- | :--- |
| `title` | texto | Igual ao nome do arquivo, sem `.md` |
| `part` | uma das 8 áreas canônicas | Define em qual módulo do site a nota aparece |
| `category` | texto | Subárea; vira o agrupamento no explorador |
| `status` | `ideia` `rascunho` `revisao` `publicado` | Só `publicado` entra na vitrine |
| `draft` | `true`/`false` | Derivado de `status`; `true` não é publicado |
| `tags` | lista | 3 a 6, minúsculas e hifenizadas |
| `aliases` | lista | Nome em inglês + sinônimos; alimenta a busca |
| `tem_imagem` | `true`/`false` | `true` exige que os arquivos de `images` existam |
| `images` | lista | Nomes dos arquivos em `attachments/` |
| `effort` | 1–5 | Quanto trabalho ainda falta |
| `last_tested` | data | Quando o prompt foi validado pela última vez |
| `sources` | lista | De qual documento-fonte o conteúdo veio |

> [!warning] Imagens
> Um embed `![[arquivo.png]]` só funciona se o arquivo existir em `attachments/`.
> Enquanto não existir, deixe `tem_imagem: false` e remova a seção de galeria —
> um embed quebrado aparece como bloco vazio no site.
