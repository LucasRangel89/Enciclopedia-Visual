---
title: Luz - High-key / Low-key
part: 01_Fundamentos_Teoricos
category: Luz
status: rascunho
draft: false
tags: [luz, high-key, low-key, exposicao, clave, humor]
aliases:
  - High-key e Low-key
  - High Key Lighting
  - Low Key Lighting
  - Clave Alta e Clave Baixa
tem_imagem: false
images: []
effort: 2
last_tested: 2026-11-15
sources:
  - Guia Avançado de Linguagem Visual em IA.md
---
# Luz — High-key / Low-key

## Conceito Técnico

Termos herdados da pintura que descrevem o **registro geral de luminosidade** de
uma imagem:

- **High-key:** a maior parte do quadro está acima do cinza médio. Fundos claros,
  sombras abertas, pouca área preta. Não é a mesma coisa que "superexposto" —
  high-key bem feito ainda retém detalhe nas altas luzes.
- **Low-key:** a maior parte do quadro está abaixo do cinza médio. Fundo escuro,
  pequenas áreas de luz que funcionam como holofotes. É a base do *tenebrismo*
  barroco e do noir.

A distinção é de **dominância**, não de presença: uma imagem low-key pode ter
brancos muito brilhantes, desde que ocupem pouca área.

---

## Efeito Psicológico e Narrativo

* **High-key:** alegria, higiene, infância, publicidade de alimentos, hospitais,
  espiritualidade. Também pode significar *vazio* — nada de sombrio para
  esconder.
* **Low-key:** mistério, ameaça, intimidade noturna, sofisticação, crime.
  Concentra a atenção porque há pouco para competir com o ponto iluminado.
* **High-key extremo:** ausência de profundidade, sensação de irrealidade ou
  sonho.
* **Low-key extremo:** claustrofobia; o espectador não sabe o que há no escuro,
  e isso cansa se sustentado por muito tempo.

---

## Aplicações Práticas

* **Comédia e comercial:** high-key com sombras suaves e fundo branco ou claro.
* **Noir e thriller:** low-key com uma fonte de luz motivada por cena.
* **Retrato corporativo:** high-key médio — transmite abertura sem parecer
  estúdio frio.
* **Natureza-morta barroca:** low-key com fundo negro e luz lateral rasante.

---

## Módulos para Engenharia de Prompt

| Parâmetro | Configuração Recomendada | Efeito no Gerador de IA |
| :--- | :--- | :--- |
| **High-key** | `high-key lighting, bright white background, airy and luminous` | Quadro claro, sombras abertas |
| **Low-key** | `low-key lighting, dark background, single pool of light` | Maioria do quadro escura |
| **High-key suave** | `soft even illumination, minimal shadows, bright palette` | Sem drama, tom amigável |
| **Low-key dramático** | `chiaroscuro, deep blacks, dramatic pool of light` | Tenebrismo, tensão |
| **Meio-termo** | `balanced midtones, natural exposure` | Narrativa neutra, documental |

### Vocabulário para Prompt
* `high-key lighting, bright airy composition`
* `low-key lighting, dark and moody`
* `predominantly white background` / `predominantly black background`
* `open shadows` / `crushed blacks`
* `tenebrism, dramatic chiaroscuro`

---

## ⚙️ Prompt de Referência (Testado)

```
A young woman reading a letter by candlelight in a dark 18th-century study,
low-key lighting, predominantly dark background with a single warm pool of
light on her face and hands, deep blacks, dramatic chiaroscuro, dust motes in
the candlelight, baroque oil painting texture, muted earth tones --ar 16:9
```

## Notas de Revisão
- [ ] Verificar se `low-key` sozinho já escurece o fundo ou se exige `dark background` explícito
- [ ] Testar `high-key` em gerador que tende a estourar as altas luzes
