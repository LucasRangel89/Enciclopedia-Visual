---
title: "attachments"
part: "05_Anexos"
category: "Midia"
status: publicado
draft: false
tags: [midia, imagens, anexos]
aliases: ["Anexos", "Imagens"]
tem_imagem: false
images: []
effort: 1
sources: []
---

# attachments/

Pasta das imagens referenciadas pelos embeds `![[arquivo.png]]` das notas.

## Convenção de nomes

```
<slug-da-nota>_<gerador>.<ext>
```

Exemplos:

| Arquivo | Nota | Gerador |
| :--- | :--- | :--- |
| `harmonia_complementar_dalle3.png` | Cor/Harmonia Complementar | DALL-E 3 |
| `harmonia_complementar_imagen.png` | Cor/Harmonia Complementar | Gemini Imagen |
| `harmonia_complementar_leonardo.png` | Cor/Harmonia Complementar | Leonardo AI |
| `harmonia_complementar_raphael.png` | Cor/Harmonia Complementar | Raphael AI |

Regras:

- minúsculas, sem acentos, sem espaços — use `_`;
- um sufixo por gerador, sempre o mesmo conjunto: `dalle3`, `imagen`,
  `leonardo`, `raphael`;
- a nota lista os mesmos nomes em `images:` no frontmatter.

## Estado atual

Rode `python3 scripts/enciclopedia.py audit` e veja a seção **4. Links e mídia**
para a lista de embeds sem arquivo. É a maior lacuna do projeto.

## Estratégia de armazenamento

Enquanto houver poucas dezenas de imagens, versionar aqui é suficiente. A partir
de ~500 arquivos ou ~50 MB, migre para **Git LFS** ou para um bucket externo —
ver a seção "Imagens" do [BLUEPRINT](../BLUEPRINT.md).
