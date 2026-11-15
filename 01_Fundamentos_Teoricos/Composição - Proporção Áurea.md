---
title: Composição - Proporção Áurea
part: 01_Fundamentos_Teoricos
category: Composição
status: rascunho
draft: false
tags: [composicao, proporcao-aurea, golden-ratio, phi, espiral]
aliases:
  - Proporção Áurea
  - Golden Ratio
  - Proporção Dourada
  - Seção Áurea
tem_imagem: false
images: []
effort: 2
last_tested: 2026-11-15
sources:
  - Guia Avançado de Linguagem Visual em IA.md
---
# Composição — Proporção Áurea

## Conceito Técnico

Razão matemática de aproximadamente **1:1,618** (o número φ, *phi*), encontrada
na divisão de um segmento em que a parte menor está para a maior assim como a
maior está para o todo. Aplicada à imagem, ela organiza os elementos ao longo de
uma **espiral logarítmica** que conduz o olhar do exterior até o ponto focal de
forma contínua e progressiva.

Diferente da [[Composição - Regra dos Terços|regra dos terços]], que oferece
quatro pontos de interesse fixos, a proporção áurea não oferece pontos — oferece
um **caminho**. É por isso que composições áureas parecem "corretas" sem que o
espectador consiga explicar por quê.

---

## Efeito Psicológico e Narrativo

* **Harmonia orgânica:** o padrão aparece na natureza (conchas, distribuição de
  folhas, galáxias), então o olho o lê como natural em vez de construído.
* **Fluxo contínuo:** guia a atenção num percurso curvo, sem os saltos que a
  grade de terços provoca. Bom para imagens que devem ser *percorridas*.
* **Sofisticação silenciosa:** associada à tradição clássica e ao design
  editorial de alto padrão; pode soar fria em contextos que pedem ruptura.
* **Quando evitar:** em cenas de caos, pânico ou urgência — a suavidade da
  espiral desacelera justamente onde se quer tensão.

---

## Aplicações Práticas

* **Retrato e still-life:** posicionar o olho do sujeito ou o objeto principal
  na extremidade estreita da espiral.
* **Design editorial e capas:** usar a grade φ (*phi grid*) em vez da grade de
  terços para layouts mais refinados.
* **Paisagem:** alinhar o horizonte à linha que divide o quadro na razão áurea
  em vez de dividi-lo ao meio.
* **Direção de fotografia:** composições que repetem a espiral em vários planos
  (galhos, ondas, escadas) criam profundidade sem precisar de foco seletivo.

---

## Módulos para Engenharia de Prompt

| Parâmetro | Configuração Recomendada | Efeito no Gerador de IA |
| :--- | :--- | :--- |
| **Estrutura** | `golden ratio composition` | Organiza os elementos numa espiral implícita |
| **Grade** | `phi grid alignment` | Empurra o sujeito para fora do centro exato |
| **Fluxo** | `spiral visual flow leading to the focal point` | Cria um caminho de leitura curvo |
| **Foco** | `subject placed at the golden section` | Evita centralização rígida |

### Vocabulário para Prompt
* `golden ratio composition`
* `phi grid`
* `spiral of Fibonacci`
* `divine proportion`
* `harmonic proportions`

---

## ⚙️ Prompt de Referência (Testado)

```
A weathered fisherman mending nets on a wooden dock at dawn, golden ratio
composition, spiral visual flow leading from the coiled ropes to his face,
phi grid alignment, muted teal and ochre palette, soft volumetric morning
light, shot on 85mm lens, shallow depth of field, textured and cinematic
--ar 16:9
```

## Notas de Revisão
- [ ] Comparar lado a lado com a regra dos terços usando o mesmo sujeito (Série 05 do [[MOC - Laboratorio|Laboratório]])
- [ ] Testar se `phi grid` produz resultado distinguível de `rule of thirds`
