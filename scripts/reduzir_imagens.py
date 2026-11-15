#!/usr/bin/env python3
"""
Colapsa a galeria multi-gerador de cada nota para UMA imagem.

Cada nota pedia 4 imagens (uma por gerador). O usuario decidiu que uma
basta para comecar, entao este script:

  1. acha a secao "Galeria de Exemplos Visuais" da nota
  2. mantem so o primeiro bloco de gerador
  3. reescreve o embed para um nome canonico, sem sufixo de gerador
  4. registra os geradores descartados no frontmatter `falta:`

Assim a divida continua mensuravel (o audit mostra o que falta) mas o
trabalho de geracao cai para 1 imagem por nota.

Uso:
    python3 scripts/reduzir_imagens.py            # dry-run
    python3 scripts/reduzir_imagens.py --apply
    python3 scripts/reduzir_imagens.py --only 01_Fundamentos_Teoricos/Luz
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

GERADORES = (
    "dalle3", "dalle", "imagen", "leonardo", "raphael", "gemini",
    "chatgpt", "krea", "manus", "bing", "reve",
)

GALERIA_RE = re.compile(r"^##\s*.*(?:Galeria|Exemplos Visuais|Exemplo Visual)", re.I)
SECAO_RE = re.compile(r"^##\s+(?!\d+\.)")
BLOCO_A_RE = re.compile(r"^###\s+\d+\.\s*")
BLOCO_B_RE = re.compile(r"^>\s*\*\*\d+\.\s*")
EMBED_RE = re.compile(r"!\[\[([^\]|#]+)(?:\|[^\]]*)?\]\]")
LEGENDA_RE = re.compile(r"^\s*[>*\s]*(?:\*\*)?Legenda", re.I)


def split_frontmatter(text: str) -> tuple[str, str, str]:
    """Retorna (frontmatter, corpo, separador final)."""
    if not text.startswith("---"):
        return "", text, ""
    end = text.find("\n---", 3)
    if end == -1:
        return "", text, ""
    return text[3:end + 1], text[end + 4:], text[:end + 4]


def canonico(nome: str) -> str:
    """`plongee_dalle3.png` -> `plongee.png`; `Luz_Dura_ChatGPT.png` -> `Luz_Dura.png`"""
    stem, _, ext = nome.rpartition(".")
    if not ext or not stem:
        return nome
    partes = stem.split("_")
    while len(partes) > 1 and partes[-1].lower() in GERADORES:
        partes.pop()
    return "_".join(partes) + "." + ext


def gerador_de(nome: str) -> str:
    stem = nome.rpartition(".")[0]
    partes = stem.split("_")
    return partes[-1] if partes and partes[-1].lower() in GERADORES else "?"


def reduzir(texto: str) -> tuple[str, list[str], str | None]:
    """Colapsa a galeria. Retorna (texto novo, geradores descartados, canonico)."""
    fm, corpo, _ = split_frontmatter(texto)
    linhas = corpo.split("\n")

    ini = next((i for i, l in enumerate(linhas) if GALERIA_RE.match(l)), None)
    if ini is None:
        return texto, [], None

    fim = len(linhas)
    for i in range(ini + 1, len(linhas)):
        if SECAO_RE.match(linhas[i]):
            fim = i
            break

    bloco = linhas[ini:fim]

    # cabecalhos de gerador dentro do bloco
    idx = [
        i for i, l in enumerate(bloco)
        if BLOCO_A_RE.match(l) or BLOCO_B_RE.match(l)
    ]
    if not idx:
        return texto, [], None

    # bloco do primeiro gerador
    gen1 = bloco[idx[0]: idx[1] if len(idx) > 1 else len(bloco)]
    while gen1 and gen1[-1].strip() == "":
        gen1.pop()

    # geradores descartados (blocos 2..N)
    descartados = []
    for k in range(1, len(idx)):
        pedaco = bloco[idx[k]: idx[k + 1] if k + 1 < len(idx) else len(bloco)]
        for m in EMBED_RE.finditer("\n".join(pedaco)):
            descartados.append(gerador_de(m.group(1)))

    # embed do primeiro bloco -> nome canonico
    m = EMBED_RE.search("\n".join(gen1))
    if not m:
        return texto, [], None
    alvo = canonico(m.group(1))

    gen1 = [
        EMBED_RE.sub(f"![[{alvo}]]", l, count=1) if EMBED_RE.search(l) else l
        for l in gen1
    ]

    # preserva o separador final (--- ) se existir
    cauda = []
    if bloco and bloco[-1].strip() == "":
        k = len(bloco) - 1
        while k >= 0 and bloco[k].strip() == "":
            k -= 1
        if k >= 0 and bloco[k].strip() == "---":
            cauda = ["", "---"]

    linhas[ini:fim] = ["## 🖼️ Exemplo Visual", "", *gen1, *cauda]
    return fm + "\n".join(linhas), descartados, alvo


def atualiza_falta(fm: str, novos: list[str]) -> str:
    """Acrescenta geradores ao `falta:` sem duplicar."""
    if not novos:
        return fm
    m = re.search(r"^falta:\s*\[(.*?)\]\s*$", fm, re.MULTILINE)
    atuais = [x.strip() for x in m.group(1).split(",") if x.strip()] if m else []
    for g in novos:
        if g not in atuais:
            atuais.append(g)
    linha = f"falta: [{', '.join(atuais)}]"
    if m:
        return fm[:m.start()] + linha + fm[m.end():]
    # insere antes do fim do frontmatter
    return fm.rstrip("\n") + "\n" + linha + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--only", default="")
    args = ap.parse_args()

    total_notas = total_desc = 0
    for path in sorted(ROOT.rglob("*.md")):
        if ".git" in path.parts:
            continue
        rel = path.relative_to(ROOT).as_posix()
        if args.only and not rel.startswith(args.only):
            continue
        if rel.startswith("06_Templates/"):
            continue  # template: o <slug> eh placeholder, nao nota real
        texto = path.read_text(encoding="utf-8", errors="replace")
        novo, descartados, alvo = reduzir(texto)
        if not descartados and alvo is None:
            continue
        novo = atualiza_falta(novo, descartados)
        if novo == texto:
            continue
        total_notas += 1
        total_desc += len(descartados)
        print(f"  {rel}")
        print(f"      -> {alvo}   (descartados: {', '.join(descartados) or '—'})")
        if args.apply:
            path.write_text(novo, encoding="utf-8")

    print(f"\n{total_notas} nota(s) reduzida(s), {total_desc} embed(s) descartado(s).")
    print("APLICADO." if args.apply else "Dry-run. Use --apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
