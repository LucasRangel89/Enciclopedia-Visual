---
title: PROMPT-EXTRACAO
part: "06_Templates"
category: Template
type: template
status: publicado
draft: false
tags: [template, prompt, extracao, ia, automacao]
aliases:
  - Prompt de Extração
  - Extrator de Notas
tem_imagem: false
images: []
effort: 2
sources: []
---
# PROMPT-EXTRACAO — de documento-fonte a nota atômica

Este é o acelerador do projeto. Em vez de escrever cada nota à mão, você aponta
um modelo de linguagem para uma seção de um dos **documentos-fonte** e ele devolve
a nota no formato canônico.

---

## O prompt

Copie tudo que está dentro do bloco abaixo e substitua apenas os dois marcadores
entre `< >`.

```
Você é um especialista em linguagem visual, direção de arte e engenharia de
prompts para geradores de imagem. Vou te entregar um trecho de um documento de
referência. Sua tarefa é extrair dele UMA nota atômica no formato abaixo.

REGRAS ABSOLUTAS:
1. Não invente informações que não estejam no trecho ou que não sejam
   conhecimento artístico consolidado e verificável.
2. Todo termo de prompt deve estar em inglês e entre crases.
3. A nota deve ter entre 250 e 600 palavras no corpo.
4. Use exatamente as seções do template, na ordem, sem pular nenhuma.
5. Não use emoji.
6. Termine sempre com um prompt de referência completo, em inglês, terminando
   em --ar 16:9.
7. Devolva APENAS o markdown da nota, sem comentários sobre o que você fez.

TRECHO FONTE:
"""
<COLE AQUI O TRECHO DO DOCUMENTO-FONTE>
"""

TÍTULO DA NOTA: <TÍTULO EXATO, EM PORTUGUÊS>
CATEGORIA: <SUBÁREA>
TAGS: <3 a 6 tags minúsculas hifenizadas>

FORMATO DE SAÍDA (preencha integralmente):

---
title: "<TÍTULO>"
part: "<ÁREA>"
category: "<CATEGORIA>"
status: rascunho
draft: true
tags: [<TAGS>]
aliases: ["<Nome em inglês>", "<sinônimo>"]
tem_imagem: false
images: []
effort: 2
last_tested: "<DATA DE HOJE>"
sources: ["<NOME DO ARQUIVO FONTE>"]
---

# <TÍTULO>

## Conceito Técnico
<2 a 5 frases: definição, funcionamento, origem do termo>

---

## Efeito Psicológico e Narrativo
* **<efeito>:** <leitura do espectador>
* **<efeito>:** <emoção ou sentido>
* **<efeito>:** <quando usar / quando evitar>

---

## Aplicações Práticas
* **<campo>:** <exemplo concreto>
* **<campo>:** <exemplo concreto>

---

## Módulos para Engenharia de Prompt

| Parâmetro | Configuração Recomendada | Efeito no Gerador de IA |
| :--- | :--- | :--- |
| **<parâmetro>** | `termo em inglês` | <efeito> |

### Vocabulário para Prompt
* `termo-um`
* `termo-dois`
* `termo-tres`

---

## ⚙️ Prompt de Referência (Testado)

```
<prompt completo em inglês, --ar 16:9 no final>
```
```

---

## Variantes úteis

### Extrair várias notas de uma vez

> Substitua a seção `TRECHO FONTE` por várias seções separadas por `===` e
> acrescente: *"Extraia uma nota para cada seção separada por `===`, mantendo a
> ordem. Separe as notas com uma linha contendo apenas `---NOTA---`."*

### Expandir uma nota existente

> *"Aqui está uma nota já escrita. Reescreva-a mantendo o formato, mas
> enriquecendo as seções de Efeito Psicológico e Módulos para Engenharia de
> Prompt com base neste trecho adicional. Não remova nada do que já existe."*

### Gerar apenas o vocabulário de prompt

> *"Dada a nota abaixo, devolva uma tabela com 8 a 12 termos de prompt em inglês
> que a descrevam sem citar nomes de artistas. Para cada termo, diga qual
> efeito ele produz no gerador."*

### Auditoria de uma nota

> *"Leia a nota abaixo contra o template canônico. Aponte: seções faltando,
> termos de prompt que não estão em inglês, aliases ausentes, tags fora do
> padrão, e prompts sem proporção. Devolva uma lista de correções objetivas."*

---

## Como usar em escala sem perder qualidade

1. **Uma nota por execução.** Lotes de 5 a 10 no máximo por conversa.
2. **Sempre revise o ` Conceito Técnico`.** É a seção que o modelo mais erra por
   generalização.
3. **Teste o prompt de referência** em pelo menos dois geradores antes de marcar
   `status: revisao`. Anote o resultado em `last_tested`.
4. **Registre a procedência** em `sources:` — em seis meses você vai precisar
   saber de onde veio cada afirmação.
5. **Nunca commite sem rodar** `python3 scripts/enciclopedia.py links --fail`.

> [!tip] O gargalo não é escrever, é verificar
> O modelo escreve em segundos; o que dá trabalho é confirmar que a afirmação é
> verdadeira e que o prompt funciona. Reserve seu tempo para isso — é o que
> separa uma enciclopédia de um compilado de textos plausíveis.
