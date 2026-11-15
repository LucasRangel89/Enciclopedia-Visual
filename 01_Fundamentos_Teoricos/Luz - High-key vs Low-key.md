---
title: Luz - High-key vs Low-key
part: 01_Fundamentos_Teoricos
category: Luz
status: rascunho
draft: false
tags: [luz, high-key, low-key, contraste, exposicao, claro-escuro]
aliases:
  - High-key
  - Low-key
  - Chiaroscuro de exposição
tem_imagem: true
images: []
effort: 2
last_tested: 2026-11-15
sources:
  - Guia Avançado de Linguagem Visual em IA.md
---

# Luz — High-key vs Low-key

## 📖 Definição e Lógica

Os dois extremos do **espectro tonal** de uma imagem. Não são esquemas de
iluminação (isso é [[Luz - Direção e Qualidade]]), mas a *distribuição* dos
tons entre o branco e o preto — quanta informação vive em cada faixa.

**High-key** concentra a imagem na parte clara da curva: fundo branco ou
quase branco, sombras abertas, pouco ou nenhum preto puro. Baixo contraste,
sombras suaves. Evoca higiene, leveza, inocência, publicidade, estúdio,
sonho, espiritualidade. Historicamente associado à fotografia de moda e ao
Renascimento florentino.

**Low-key** concentra a imagem na parte escura: fundo preto ou muito
escuro, luz incidindo sobre uma fração pequena do quadro. Alto contraste,
negros profundos. Evoca drama, mistério, solidão, ameaça, cinema noir.
Tecnicamente é o que se chama de *low-key lighting*.

O meio-termo — tons amplamente distribuídos — é a **exposição normal**,
que a maioria das fotografias documentais usa.

## 🎨 Aplicação Prática

| | High-key | Low-key |
| :--- | :--- | :--- |
| Fundo | claro, pouco abaixo do sujeito | escuro, vários pontos abaixo |
| Razão de contraste | 2:1 a 4:1 | 8:1 a 32:1 ou mais |
| Sombras | abertas, detalhe visível | fechadas, silhueta |
| Número de luzes | principal + preenchimento forte | principal + quase nenhum preenchimento |
| Exposição | a favor das altas luzes | a favor das sombras, sacrificando o resto |

Para gerar high-key em IA, o pedido precisa de *"high-key lighting, white
background, soft shadows, bright exposure"*. Para low-key:
*"low-key lighting, black background, single hard source, deep shadows"*.
Sem o termo explícito, o modelo tende a devolver exposição média.

## 🔗 Relações

- [[Luz - Direção e Qualidade]] — a direção da fonte, independente do registro tonal
- [[Cor - Saturação e Contraste]] — o contraste de cor, distinto do contraste tonal
- [[High-Key Lighting (Iluminação Alta-Chave)]] — o esquema de retrato
- [[Low-Key Lighting (Iluminação Baixa-Chave)]] — o esquema de retrato
- [[MOC - Luz]]
