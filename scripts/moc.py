#!/usr/bin/env python3
"""
Gera/atualiza os MOCs (Mapas de Conteúdo) a partir da estrutura de pastas.

Um MOC é uma nota-índice chamada `MOC - <Pasta>.md` dentro da pasta que indexa.
Este script:
  - cria MOCs ausentes para pastas que contêm notas;
  - reescreve a seção "Índice automático" dos MOCs existentes;
  - NUNCA apaga conteúdo escrito pelo autor (só mexe entre os marcadores).

Uso:
    python3 scripts/moc.py --check     # só mostra o que faria
    python3 scripts/moc.py --apply     # escreve
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

BEGIN = "<!-- inicio:indice-automatico -->"
END = "<!-- fim:indice-automatico -->"

SKIP_DIRS = {
    ".git", ".obsidian", ".github", "node_modules", "site", "public",
    "_fontes", "scripts", "docs", "attachments", "__pycache__",
}

SKIP_TOP_GLOBS = ("Notas_*",)

# nome do MOC raiz de cada área canônica
AREA_MOC = {
    "00_Dashboard": "MOC - 00_Dashboard",
    "01_Fundamentos_Teoricos": "MOC - Fundamentos",
    "02_Catalogo_Visual": "MOC - Catalogo Visual",
    "03_Laboratorio_Visual": "MOC - Laboratorio",
    "04_Engenharia_e_Receitas": "MOC - Receitas",
}

FRONTMATTER = """---
title: "MOC - {name}"
part: "{part}"
category: "MOC"
type: moc-category
parent: "[[MOC - {parent}]]"
status: revisao
draft: false
tags: [moc, {slug}]
aliases: ["{name}", "MOC - {name}"]
tem_imagem: false
images: []
effort: 1
sources: []
---

# MOC — {name}

{blurb}

{BEGIN}
{items}
{END}
"""


def slugify(text: str) -> str:
    import unicodedata
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[\s_]+", "-", text)


def iter_content_dirs():
    for path in sorted(ROOT.iterdir()):
        if not path.is_dir() or path.name in SKIP_DIRS:
            continue
        if any(re.match(p.replace("*", ".*"), path.name) for p in SKIP_TOP_GLOBS):
            continue
        yield path


# pai explícito dos MOCs de nível superior (a pasta-mãe é a raiz do cofre)
ROOT_PARENT = {
    "MOC - 00_Dashboard": "index",
    "MOC - Catalogo Visual": "index",
    "MOC - Fundamentos": "index",
    "MOC - Laboratorio": "index",
    "MOC - Receitas": "index",
}


def moc_parent(folder: Path) -> str:
    """Nome do MOC pai desta pasta."""
    own = f"MOC - {folder.name}"
    if own in ROOT_PARENT:
        return ROOT_PARENT[own]
    parent = folder.parent
    if parent.relative_to(ROOT).as_posix() == ".":
        return ""
    if parent.name in AREA_MOC:
        return AREA_MOC[parent.name]
    return f"MOC - {parent.name}"


def notes_in(folder: Path) -> list[Path]:
    return sorted(
        p for p in folder.rglob("*.md")
        if p.name != "00_README.md" and not p.name.startswith("MOC - ")
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    created = updated = 0
    for area in iter_content_dirs():
        for folder in sorted([area] + [p for p in area.rglob("*") if p.is_dir()]):
            if any(part in SKIP_DIRS for part in folder.relative_to(ROOT).parts):
                continue
            if folder.name.startswith("Onda_"):
                continue
            notes = notes_in(folder)
            items = "\n".join(f"- [[{p.stem}]]" for p in notes)
            if not notes:
                continue
            existing = [
                q for q in folder.glob("MOC - *.md")
            ]
            if existing:
                # já existe MOC (com nome ligeiramente diferente) — só atualiza
                moc_path = existing[0]
                text = moc_path.read_text(encoding="utf-8")
                if BEGIN in text and END in text:
                    new = re.sub(
                        re.escape(BEGIN) + r".*?" + re.escape(END),
                        f"{BEGIN}\n{items}\n{END}",
                        text,
                        flags=re.DOTALL,
                    )
                    if new != text:
                        print(f"ATUALIZAR: {moc_path.relative_to(ROOT)}")
                        if args.apply:
                            moc_path.write_text(new, encoding="utf-8")
                        updated += 1
                continue
            name = folder.name
            moc_path = folder / f"MOC - {name}.md"
            if moc_path.exists():
                text = moc_path.read_text(encoding="utf-8")
                if BEGIN in text and END in text:
                    new = re.sub(
                        re.escape(BEGIN) + r".*?" + re.escape(END),
                        f"{BEGIN}\n{items}\n{END}",
                        text,
                        flags=re.DOTALL,
                    )
                else:
                    new = text.rstrip("\n") + f"\n\n{BEGIN}\n{items}\n{END}\n"
                if new != text:
                    print(f"ATUALIZAR: {moc_path.relative_to(ROOT)}")
                    if args.apply:
                        moc_path.write_text(new, encoding="utf-8")
                    updated += 1
            else:
                print(f"CRIAR:    {moc_path.relative_to(ROOT)}")
                if args.apply:
                    part = folder.relative_to(ROOT).parent.as_posix()
                    parent = moc_parent(folder)
                    blurb = (
                        f"Índice das notas em `{folder.relative_to(ROOT).as_posix()}`. "
                        "Edite a seção entre os marcadores para acrescentar curadoria "
                        "manual — o índice automático vive entre eles."
                    )
                    moc_path.write_text(
                        FRONTMATTER.format(
                            name=name, part=part, parent=parent,
                            slug=slugify(name), blurb=blurb,
                            BEGIN=BEGIN, END=END, items=items,
                        ),
                        encoding="utf-8",
                    )
                created += 1

    # corrige o parent dos MOCs existentes
    fixed = 0
    for folder in sorted([p for p in ROOT.rglob("*") if p.is_dir()]):
        if any(part in SKIP_DIRS for part in folder.relative_to(ROOT).parts):
            continue
        for moc_path in folder.glob("MOC - *.md"):
            text = moc_path.read_text(encoding="utf-8")
            want = moc_parent(folder)
            m = re.search(r'^parent: "\[\[(.+?)\]\]"', text, re.MULTILINE)
            if m and m.group(1) != want:
                new = text.replace(m.group(0), f'parent: "[[{want}]]"')
                print(f"PARENT:   {moc_path.relative_to(ROOT)} "
                      f"({m.group(1)} -> {want})")
                if args.apply:
                    moc_path.write_text(new, encoding="utf-8")
                fixed += 1
            elif not m and want:
                print(f"PARENT+:  {moc_path.relative_to(ROOT)} -> {want}")
                if args.apply:
                    moc_path.write_text(
                        text.replace("status:", f'parent: "[[{want}]]"\nstatus:', 1),
                        encoding="utf-8",
                    )
                fixed += 1

    print(f"\n{created} MOC(s) criado(s), {updated} atualizado(s), "
          f"{fixed} parent(s) corrigido(s). "
          f"{'Aplicado.' if args.apply else 'Use --apply.'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
