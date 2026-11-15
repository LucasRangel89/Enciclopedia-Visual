---
title: Luz - Direção e Qualidade
part: 01_Fundamentos_Teoricos
category: Luz
status: rascunho
draft: false
tags: [luz, direcao, qualidade, dura, suave, sombra]
aliases:
  - Direção e Qualidade da Luz
  - Light Direction and Quality
  - Luz Dura e Luz Suave
tem_imagem: false
images: []
effort: 2
last_tested: 2026-11-15
sources:
  - Guia Avançado de Linguagem Visual em IA.md
---
# Luz — Direção e Qualidade

## Conceito Técnico

Duas dimensões independentes de qualquer esquema de iluminação:

- **Direção** — de onde a luz vem em relação ao eixo da câmera: *frontal*,
  *lateral* (45°), *superior* (*top light*), *inferior* e *contraluz*
  (*backlight*, 180°).
- **Qualidade** — o tamanho aparente da fonte. Fonte **grande** (relativa ao
  sujeito) produz transições suaves; fonte **pequena** produz bordas duras. É a
  razão pela qual o sol, enorme, dá luz dura (parece pequeno por estar longe) e
  um teto nublado, difuso, dá luz suave.

A direção determina **onde** as sombras caem; a qualidade determina **quão
nítidas** elas são.

---

## Efeito Psicológico e Narrativo

* **Frontal suave:** honestidade, beleza comercial, ausência de segredo. Apaga
  textura — rugas e relevos desaparecem.
* **Lateral (Rembrandt):** introspecção, caráter, pintura clássica. Revela
  textura e cria volume.
* **Superior:** autoridade, julgamento, divindade. Também produce olheiras —
  daí o desconforto.
* **Inferior:** irrealidade, terror, trauma. Nada na natureza ilumina de baixo.
* **Contraluz:** silhueta, transcendência, isolamento, revelação parcial.

---

## Aplicações Práticas

* **Retrato:** lateral a 45° com fonte grande para pele favorável; contraluz
  para cabelo e separação do fundo.
* **Produto:** top light com difusor grande para destacar forma sem sombra
  dura; lateral rasante para revelar textura.
* **Interior:** luz vinda de janela lateral, nunca de flash frontal, para dar
  profundidade ao ambiente.
* **Terror:** inferior ou lateral rasante, sempre com qualidade dura.

---

## Módulos para Engenharia de Prompt

| Parâmetro | Configuração Recomendada | Efeito no Gerador de IA |
| :--- | :--- | :--- |
| **Frontal difusa** | `soft frontal lighting, beauty dish, even illumination` | Pele lisa, sombras mínimas |
| **Lateral 45°** | `45-degree side lighting, Rembrandt triangle under the eye` | Volume, caráter, textura |
| **Superior** | `top-down lighting, overhead spotlight` | Autoridade, olheiras, mistério |
| **Inferior** | `underlighting, light from below, eerie uplight` | Inquietação, horror |
| **Contraluz** | `strong backlight, rim light, silhouette against the light` | Silhueta, halo, separação |
| **Qualidade dura** | `hard directional light, sharp shadows, small light source` | Bordas nítidas, drama |
| **Qualidade suave** | `soft diffused light, overcast, large light source` | Transições graduais, névoa |

### Vocabulário para Prompt
* `soft diffused lighting` / `hard directional light`
* `Rembrandt lighting` / `split lighting` / `butterfly lighting`
* `rim light` / `backlit silhouette`
* `golden hour light` / `blue hour light`
* `volumetric light rays`

---

## ⚙️ Prompt de Referência (Testado)

```
A middle-aged lighthouse keeper standing on a stone balcony, 45-degree side
lighting with a Rembrandt triangle under one eye, hard directional light from
a single bare bulb, deep textured shadows across weathered skin, storm clouds
behind, muted navy and slate palette, shot on 85mm lens, shallow depth of
field, cinematic and contemplative --ar 16:9
```

## Notas de Revisão
- [ ] Testar se `Rembrandt lighting` sobrevive à interpretação do gerador ou se exige descrição geométrica
- [ ] Série 03 do [[MOC - Laboratorio|Laboratório]]: mesma cena, 6 direções de luz
