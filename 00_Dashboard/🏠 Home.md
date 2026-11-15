---
title: 🏠 Home
part: "00_Dashboard"
category: Home
type: moc-category
status: publicado
draft: false
tags: [home, dashboard, navegacao]
aliases: [Início, Dashboard]
tem_imagem: false
images: []
effort: 1
sources: []
---
# 🏠 Central da Enciclopédia Visual

Sistema de **direção de arte** e **engenharia de prompts** para geração de imagem. Comece pelo [[index\|índice]] ou vá direto a um módulo.

---

## 📚 Módulos

| Módulo | O que é |
| :--- | :--- |
| [[MOC - Fundamentos\|🧠 Fundamentos Teóricos]] | As nove variáveis que governam qualquer imagem |
| [[MOC - Catalogo Visual\|🎨 Catálogo Visual]] | Movimentos, mídias, gêneros, assinaturas e tradições |
| [[MOC - Laboratorio\|🧪 Laboratório Visual]] | Séries de exploração com uma variável isolada |
| [[MOC - Receitas\|⚙️ Engenharia e Receitas]] | Prompts completos, templates e anti-erros |

---

## 🧠 Fundamentos — navegação por variável

[[MOC - Composição\|Composição]] · [[MOC - Cor\|Cor]] · [[MOC - Densidade Visual\|Densidade]] · [[MOC - Figura Humana e Expressao\|Figura Humana]] · [[MOC - Geometria de Cena\|Geometria de Cena]] · [[MOC - Luz\|Luz]] · [[MOC - Óptica & Lentes\|Óptica]] · [[MOC - Ritmo e Tempo\|Ritmo e Tempo]] · [[MOC - Textura e Materialidade\|Textura]] · [[MOC - Tipografia e Linguagem Visual\|Tipografia]]

## 🎨 Catálogo — navegação por repertório

[[MOC - Movimentos\|Movimentos Artísticos]] · [[MOC - Assinaturas_Autorais\|Assinaturas Autorais]] · [[MOC - Generos_e_Universos\|Gêneros e Universos]] · [[MOC - Arquitetura_Cenario_e_Personagem\|Arquitetura e Cenário]] · [[MOC - Narrativa_Visual_e_Storytelling\|Narrativa Visual]] · [[MOC - Musica_e_Capas_de_Album\|Música e Capas]]

---

## 🛠️ Manutenção

- 📖 `BLUEPRINT.md` — plano de desenvolvimento e arquitetura do projeto (arquivo do repo, nao entra no site)
- 🔍 `docs/AUDITORIA-2026-11-15.md` — diagnóstico do cofre (arquivo do repo, nao entra no site)
- 🧩 [[MOC - 06_Templates]] — templates e prompt de extração
- 🎯 [[MOC - 07_Sujeitos_Fixos]] — sujeitos recorrentes para controle de variáveis

> [!tip] Fluxo de trabalho
> Escreva no Obsidian → commite → o site se reconstrói sozinho via GitHub Actions. Antes de commitar, rode `python3 scripts/enciclopedia.py audit` para pegar links quebrados.
