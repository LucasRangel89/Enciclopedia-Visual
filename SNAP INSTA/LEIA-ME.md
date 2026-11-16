# SNAP INSTA — acervo de referência (não publicado)

47 imagens de referência baixadas do Instagram, todas **retrato** (4:5, 3:4 ou 5:6),
total de **15 MB**. Duas origens de nome:

- `SnapInsta.to_<id>_<id>_<id>_n.jpg` — 11 arquivos
- `snapinsta.com.br-<hash>.jpg` — 36 arquivos

O conteúdo é um corpo coerente de **ilustração fantasy e concept art**, com marcas
d'água de dois autores recorrentes (`TSINT THEHATCA` e `PHANDI GRAMS`). Predominam:

- **capas de revista/HQ** no estilo pulp e anos 80 (Loremasters, Mortal Kombat,
  Thundercats, Tartarugas Ninja)
- **character design** de guerreiros, anões, elfos e criaturas
- **environment art** com escala épica e figura minúscula
- **gravura em linha** (hachura densa, água-forte e xilogravura)
- **pôsteres Art Nouveau** com moldura ornamental
- **duotones** e monocromias (azul/amarelo, vermelho/preto, dourado)

## O que já foi usado

`scripts/rotear_snapinsta.py` moveu **30 imagens** para
`08_Imagens_Geradas/Referencias_SnapInsta/`, renomeadas para o embed que a nota
já declarava (`agua_forte.jpg`, `liminal.jpg`, `fantasia.jpg`, …) e reescreveu o
bloco `## 🖼️ Exemplo Visual` de 30 notas. Embeds ausentes: **189 → 159**.

## O que sobrou aqui (17 imagens)

São referências de qualidade, mas sem nota correspondente no cofre. Ficam neste
diretório como reserva técnica.

| Arquivo | Conteúdo |
| :--- | :--- |
| `SnapInsta.to_651275556…` | Duotone azul/amarelo, homem entrando em arcada na floresta |
| `SnapInsta.to_661842984…` | Duotone vermelho/preto, raposa ronin com katana |
| `snapinsta.com.br-69eac6d1c488d` | Samurai com capacete estilizado, armadura ornamentada |
| `SnapInsta.to_673868026…` | Cena densa estilo Tartarugas Ninja, moldura de tijolo |
| `snapinsta.com.br-69eac8de15bce` | Pôster "SANSA" no trono, moldura Art Nouveau |
| `snapinsta.com.br-69eac8da3600d` | "SANSA" em duotone vermelho e preto |
| `snapinsta.com.br-69eac802b8727` | Goblin chifrudo com lobo branco e castelo ao fundo |
| `snapinsta.com.br-69eac888d923c` | Anão guerreiro, luz dourada de contorno |
| `snapinsta.com.br-69eac88617db3` | Rei de barba branca, armadura e manto |
| `snapinsta.com.br-69eac88ea2977` | Armadura branca e dourada contra céu azul saturado |
| `snapinsta.com.br-69eac88d8b5f0` | Anão com escudo redondo entre nuvens |
| `snapinsta.com.br-69eac7719cdd4` | Capa "Blood Mage Ascendant", maga de sangue élfica |
| `snapinsta.com.br-69eac8b8ea2d3` | Capa "Wilykit & Wilykat", estilo Thundercats |
| `snapinsta.com.br-69eac718ae55b` | Capa "Mortal Kombat", Sub-Zero com coluna vertebral |
| `snapinsta.com.br-69eac72245cef` | Capa "Mortal Kombat", Raiden com relâmpagos |
| `snapinsta.com.br-69eac8b7a4386` | Rei de armadura azul sob relâmpagos |
| `snapinsta.com.br-69eac91126c85` | Pôster "Brynden / The Blackfish", tocha em caverna |

## Por que esta pasta não entra no site

A pasta está em `EXCLUDE_DIRS` de `scripts/sync_content.py` e em `ignorePatterns`
de `quartz.config.yaml`, no mesmo tratamento dado a `attachments/`: são 15 MB de
binário que nenhuma nota referencia, e publicá-los só pesaria o build. As 30
imagens que passaram a ser usadas foram movidas para `08_Imagens_Geradas/`, que
é visível para o build.
