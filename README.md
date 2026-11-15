# Enciclopédia Visual

> Um atlas interativo de **linguagem visual** — fundamentos, repertório e
> vocabulário de prompt para direção de arte, fotografia, ilustração e geração
> de imagem por IA.

Este repositório é **a fonte da verdade**. Ele é ao mesmo tempo:

1. um **cofre Obsidian** — onde o conteúdo é escrito;
2. um **site estático** — gerado a partir do cofre e publicado no GitHub Pages;
3. um **projeto de software** — com scripts de manutenção e integração contínua.

---

## Início rápido

```bash
# 1. validar o cofre (links, frontmatter, mídia ausente)
python3 scripts/enciclopedia.py audit

# 2. ver o site localmente (requer Node 22+)
./scripts/preview.sh          # sincroniza, builda e serve em http://localhost:4173

# 3. (opcional) preview apenas do conteúdo, sem rebuild completo
python3 scripts/sync_content.py --dest /tmp/preview-content --dry-run
```

Documentação completa em **[BLUEPRINT.md](BLUEPRINT.md)**.

---

## Estrutura

```
├── 00_Dashboard/          Home, MOCs e mapas de navegação
├── 01_Fundamentos_Teoricos/   As 9 variáveis da imagem
├── 02_Catalogo_Visual/        Movimentos, mídias, gêneros, assinaturas
├── 03_Laboratorio_Visual/     Séries de exploração controlada
├── 04_Engenharia_e_Receitas/  Prompts completos e anti-erros
├── 05_Anexos/                 PDFs e material de referência
├── 06_Templates/              Template canônico + prompt de extração
├── 07_Sujeitos_Fixos/         Sujeitos recorrentes para controle de variáveis
├── attachments/               Imagens referenciadas pelos embeds ![[...]]
├── _fontes/                   Documentos-fonte de onde o conteúdo é extraído
├── scripts/                   Ferramentas de manutenção (Python 3.9+)
├── docs/                      Relatórios gerados (auditoria)
├── quartz.config.yaml         Configuração do site (vive na raiz, copiada p/ site/)
└── .github/workflows/         CI: validação e deploy
```

---

## Os scripts

| Comando | O que faz |
| :--- | :--- |
| `python3 scripts/enciclopedia.py audit` | Diagnóstico completo: contagens, links quebrados, mídia ausente, homônimos, encoding |
| `python3 scripts/enciclopedia.py links --fail` | Só os problemas de link; útil no CI |
| `python3 scripts/enciclopedia.py new "<Título>" --part 01_Fundamentos_Teoricos --category Cor` | Cria nota a partir do template canônico |
| `python3 scripts/moc.py --apply` | Gera/atualiza os MOCs a partir da estrutura de pastas |
| `python3 scripts/enciclopedia.py fix-names --apply` | Corrige nomes de arquivo com encoding quebrado |
| `python3 scripts/enciclopedia.py merge-lots --apply` | Absorve pastas `Notas_*` na árvore canônica |
| `python3 scripts/enciclopedia.py sync-sources --apply` | Move documentos-fonte para `_fontes/` |
| `python3 scripts/sync_content.py` | Copia o cofre para `site/content/` |
| `./scripts/preview.sh` | Sobe o site local |

Todos os comandos destrutivos são **dry-run por padrão** — só agem com `--apply`.

---

## Fluxo de trabalho

```
escreve no Obsidian
      │
      ▼
python3 scripts/enciclopedia.py audit      ◄── pega link quebrado antes do push
      │
      ▼
git commit + push
      │
      ├──► .github/workflows/validate.yml  ◄── auditoria e checagem de links
      └──► .github/workflows/deploy.yml    ◄── build Quartz + GitHub Pages
```

---

## Stack

| Camada | Tecnologia |
| :--- | :--- |
| Autoria | Obsidian (Markdown + wikilinks) |
| Versionamento | Git / GitHub |
| Site | [Quartz v5](https://quartz.jzhao.xyz/) (Node 22+) |
| Hospedagem | GitHub Pages |
| Manutenção | Python 3.9+ (somente biblioteca padrão) |
| CI | GitHub Actions |
