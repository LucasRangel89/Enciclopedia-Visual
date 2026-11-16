#!/usr/bin/env python3
"""
Copia o cofre para dentro de `site/content/`, aplicando a lista de exclusão.

Uso:
    python3 scripts/sync_content.py                  # sincroniza
    python3 scripts/sync_content.py --dest /tmp/x    # destino alternativo
    python3 scripts/sync_content.py --dry-run        # só mostra o que faria

A lista de exclusão espelha `ignorePatterns` do `quartz.config.yaml`.
Se mudar um, mude o outro.
"""

from __future__ import annotations

import argparse
import fnmatch
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# nomes de diretório excluídos em qualquer nível da árvore
EXCLUDE_DIRS = {
    ".git", ".obsidian", ".github", "node_modules", "site", "public",
    "_fontes", "scripts", "docs", "attachments", "SNAP INSTA", ".quartz", ".arena",
    "__pycache__", ".pytest_cache", ".mypy_cache", ".ruff_cache",
}

# padrões excluídos só no primeiro nível (pastas de staging, builds, etc.)
EXCLUDE_TOP_GLOBS = ("Notas_*",)

# extensões que nunca vão para o site
EXCLUDE_SUFFIXES = {".pdf", ".pyc", ".py"}

# arquivos da raiz que não são conteúdo
EXCLUDE_ROOT_FILES = {"quartz.config.yaml", "README.md", "BLUEPRINT.md"}


def excluded(rel: Path) -> bool:
    parts = rel.parts
    if any(p in EXCLUDE_DIRS for p in parts):
        return True
    if parts and any(fnmatch.fnmatch(parts[0], pat) for pat in EXCLUDE_TOP_GLOBS):
        return True
    if len(parts) == 1 and parts[0] in EXCLUDE_ROOT_FILES:
        return True
    if rel.suffix.lower() in EXCLUDE_SUFFIXES:
        return True
    return False


def sync(dest: Path, dry_run: bool = False) -> tuple[int, int]:
    copied = skipped = 0
    if not dry_run:
        if dest.exists():
            shutil.rmtree(dest)
        dest.mkdir(parents=True)
    for path in sorted(ROOT.rglob("*")):
        rel = path.relative_to(ROOT)
        if excluded(rel):
            skipped += 1
            continue
        target = dest / rel
        if path.is_dir():
            if not dry_run:
                target.mkdir(parents=True, exist_ok=True)
            continue
        if dry_run:
            copied += 1
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(path, target)
        copied += 1
    return copied, skipped


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dest", default=str(ROOT / "site" / "content"))
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    copied, skipped = sync(Path(args.dest), args.dry_run)
    print(f"{'[dry-run] ' if args.dry_run else ''}"
          f"{copied} arquivo(s) copiados, {skipped} ignorado(s) -> {args.dest}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
