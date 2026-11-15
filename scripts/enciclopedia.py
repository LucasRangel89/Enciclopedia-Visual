#!/usr/bin/env python3
"""
Enciclopédia Visual — ferramenta de manutenção do cofre.

Subcomandos:
  audit        Diagnóstico completo do cofre (contagens, links quebrados, etc.)
  links        Senta links wikilink/embeds que não resolvem (exit 1 se houver)
  fix-names    Corrige nomes de arquivo com encoding quebrado (mojibake)
  merge-lots   Move as pastas Notas_*_Lote* para a árvore canônica
  normalize    Padroniza o frontmatter das notas
  new          Cria uma nota nova a partir do template canônico
  sync-sources Reconstrói o índice de fontes (documentos grandes da raiz)

Tudo é non-destructive por padrão: use --apply para escrever.
Requisitos: Python 3.9+ (somente biblioteca padrão).
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import sys
import unicodedata
from collections import Counter, defaultdict
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------- constantes

CANONICAL_AREAS = [
    "00_Dashboard",
    "01_Fundamentos_Teoricos",
    "02_Catalogo_Visual",
    "03_Laboratorio_Visual",
    "04_Engenharia_e_Receitas",
    "05_Anexos",
    "06_Templates",
    "07_Sujeitos_Fixos",
]

STAGING_PREFIX = "Notas_"

ASSET_SUFFIXES = {
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".pdf",
    ".mp4", ".webm", ".mp3", ".canvas", ".base", ".excalidraw",
}

# chaves de frontmatter aceitas -> chave canônica
FRONTMATTER_ALIASES = {
    "parte": "part",
    "categoria": "category",
    "titulo": "title",
}

STATUS_ORDER = ["ideia", "rascunho", "revisao", "publicado"]

# heurística de nota ainda não escrita
PLACEHOLDER_MARKERS = [
    "Definição breve do movimento",
    "Definição breve",
    "- item 1",
    "- item 2",
    "Autor / Obra 1",
    "Prompt com nome do artista (teste)",
    "Prompt técnico equivalente sem citar artista",
    "Definição breve do gênero",
]

WIKILINK_RE = re.compile(r"!?\[\[([^\[\]]+?)\]\]")
HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$", re.MULTILINE)


# ---------------------------------------------------------------- utilidades


def slugify(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text).strip().lower()
    return re.sub(r"[\s_]+", "-", text)


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="replace")


def split_frontmatter(text: str) -> tuple[dict, str]:
    """Parser mínimo de frontmatter YAML plana (listas inline ou em bloco)."""
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    raw = text[3:end].strip("\n")
    body = text[end + 4 :]
    data: dict = {}
    current_key = None
    for line in raw.split("\n"):
        if not line.strip():
            continue
        m = re.match(r"^(\s*)-\s+(.*)$", line)
        if m and current_key:
            item = m.group(2).strip().strip("'\"")
            if not isinstance(data.get(current_key), list):
                data[current_key] = []
            data[current_key].append(item)
            continue
        m = re.match(r"^([A-Za-z_][\w-]*)\s*:\s*(.*)$", line)
        if m:
            key, value = m.group(1), m.group(2).strip()
            current_key = key
            if value == "":
                data[key] = []
            elif value.startswith("[") and value.endswith("]"):
                inner = value[1:-1].strip()
                data[key] = [
                    v.strip().strip("'\"") for v in inner.split(",") if v.strip()
                ]
            else:
                data[key] = value.strip("'\"")
    return data, body


def dump_frontmatter(data: dict) -> str:
    lines = ["---"]
    for key, value in data.items():
        if isinstance(value, list):
            if not value:
                lines.append(f"{key}: []")
            elif all(isinstance(v, str) and re.match(r"^[\w.:/-]+$", v) for v in value):
                lines.append(f"{key}: [{', '.join(value)}]")
            else:
                lines.append(f"{key}:")
                lines.extend(f"  - {v}" for v in value)
        else:
            lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines) + "\n"


def is_staging(rel_path: str) -> bool:
    return rel_path.split("/")[0].startswith(STAGING_PREFIX)


def iter_notes(include_staging: bool = False):
    for path in sorted(ROOT.rglob("*.md")):
        rp = rel(path)
        if ".git/" in rp + "/":
            continue
        if is_staging(rp) and not include_staging:
            continue
        yield path


def repair_mojibake(name: str) -> str:
    """Reverte um nome que foi decodificado com a pagina de codigo errada.

    O upload pelo Windows/terminal gravou os bytes UTF-8 como se fossem
    CP437/CP850, produzindo caracteres como '├ó' no lugar de 'ã'.
    """
    for enc in ("cp437", "cp850", "latin-1"):
        try:
            fixed = name.encode(enc).decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
        if fixed != name and fixed.isprintable():
            return fixed
    return name


def looks_mojibake(name: str) -> bool:
    """Um nome esta quebrado se ele e reparavel por outra pagina de codigo."""
    return repair_mojibake(name) != name


# ---------------------------------------------------------------- índice


class Vault:
    def __init__(self, include_staging: bool = False):
        self.notes: list[Path] = list(iter_notes(include_staging))
        self.by_stem: dict[str, list[Path]] = defaultdict(list)
        self.by_relpath: dict[str, Path] = {}
        self.by_relpath_nomd: dict[str, Path] = {}
        self.assets: dict[str, list[Path]] = defaultdict(list)
        self._build()

    def _build(self) -> None:
        for path in self.notes:
            rp = rel(path)
            self.by_relpath[rp] = path
            self.by_relpath_nomd[rp[:-3]] = path
            self.by_stem[path.stem.lower()].append(path)
        for path in sorted(ROOT.rglob("*")):
            if not path.is_file() or path.suffix.lower() == ".md":
                continue
            if ".git/" in rel(path) + "/":
                continue
            self.assets[path.name.lower()].append(path)

    def resolve(self, target: str) -> tuple[str, list[Path]]:
        """Resolve um alvo de wikilink. Retorna (status, caminhos)."""
        target = target.strip()
        if not target:
            return "empty", []
        # caminho explícito
        if "/" in target:
            key = target[:-3] if target.lower().endswith(".md") else target
            if key in self.by_relpath_nomd:
                return "ok", [self.by_relpath_nomd[key]]
            if target in self.by_relpath:
                return "ok", [self.by_relpath[target]]
            # asset com caminho explicito (ex.: 05_Anexos/Cor/foo.png)
            if Path(target).suffix.lower() in ASSET_SUFFIXES:
                hits = self.assets.get(Path(target).name.lower(), [])
                if hits:
                    # confirma se algum bate tambem com o caminho
                    norm = target.replace("\\", "/")
                    exact = [h for h in hits if rel(h) == norm]
                    if exact:
                        return "ok", exact
                    return "path-fallback", hits
                return "missing-asset", []
            # tenta por stem no final do caminho
            stem = Path(target).stem.lower()
            cands = [p for p in self.notes if p.stem.lower() == stem]
            if cands:
                return "path-fallback", cands
            return "broken", []
        # pasta: o Quartz gera uma folder-page para cada diretório
        if (ROOT / target).is_dir():
            return "ok", [ROOT / target]
        # embed de asset
        if Path(target).suffix.lower() in ASSET_SUFFIXES:
            hits = self.assets.get(Path(target).name.lower(), [])
            return ("ok" if hits else "missing-asset"), hits
        # nome inteiro primeiro: Path().stem trunca "H.R. Giger" em "H.R"
        cands = self.by_stem.get(target.lower())
        if cands and len(cands) == 1:
            return "ok", cands
        if cands and len(cands) > 1:
            return "ambiguous", cands
        stem = Path(target).stem.lower()
        cands = self.by_stem.get(stem, [])
        if len(cands) == 1:
            return "ok", cands
        if len(cands) > 1:
            return "ambiguous", cands
        return "broken", []


FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")


def strip_code(text: str) -> str:
    """Remove blocos de codigo e codigo inline antes de procurar links."""
    text = FENCE_RE.sub(" ", text)
    return INLINE_CODE_RE.sub(" ", text)


def extract_links(text: str) -> list[tuple[str, str]]:
    """Retorna (tipo, alvo) para cada link/embed.

    Lida com duas particularidades do Obsidian:
      - alias com pipe escapado dentro de tabelas Markdown: [[A\\|B]]
      - links externos escritos em forma de wikilink: [[https://...|Texto]]
    """
    out = []
    for m in WIKILINK_RE.finditer(strip_code(text)):
        full = m.group(1).replace("\\|", "\x00")
        target = re.split("[|\x00#]", full)[0].strip()
        if not target or re.match(r"^[a-z][a-z0-9+.-]*://", target, re.IGNORECASE):
            continue
        kind = "embed" if m.group(0).startswith("!") else "link"
        out.append((kind, target))
    for m in re.finditer(r"!\[[^\]]*\]\(([^)]+)\)", text):
        t = m.group(1).strip()
        if t.startswith(("http://", "https://", "data:")):
            continue
        out.append(("md-embed", t))
    return out


# ---------------------------------------------------------------- comandos


def cmd_audit(args) -> int:
    vault = Vault(include_staging=True)
    lines: list[str] = []
    out = lines.append

    out("# Auditoria do cofre — Enciclopédia Visual")
    out("")
    out(f"Gerado em {date.today().isoformat()} por `scripts/enciclopedia.py audit`.")
    out("")

    # 1. inventário
    canonical = defaultdict(list)
    staging = defaultdict(list)
    loose = []
    for path in vault.notes:
        rp = rel(path)
        if is_staging(rp):
            staging[rp.split("/")[0]].append(path)
        elif rp.split("/")[0] in CANONICAL_AREAS:
            canonical[rp.split("/")[0]].append(path)
        else:
            loose.append(path)

    total = len(vault.notes)
    out("## 1. Inventário")
    out("")
    out("| Área | Notas |")
    out("| :--- | ---: |")
    for area in CANONICAL_AREAS:
        out(f"| `{area}` | {len(canonical.get(area, []))} |")
    out(f"| **Subtotal canônico** | **{sum(len(v) for v in canonical.values())}** |")
    for area, items in sorted(staging.items()):
        out(f"| `{area}` (staging) | {len(items)} |")
    out(f"| **Subtotal staging** | **{sum(len(v) for v in staging.values())}** |")
    out(f"| **Total** | **{total}** |")
    out("")
    if loose:
        out(f"> ⚠️ {len(loose)} nota(s) fora de qualquer área canônica (raiz do repo).")
        out("")

    # 2. áreas declaradas vs existentes
    missing_areas = [a for a in CANONICAL_AREAS if not (ROOT / a).is_dir()]
    if missing_areas:
        out("## 2. Áreas canônicas ausentes no disco")
        out("")
        for a in missing_areas:
            out(f"- `{a}/` — referenciada pelo Dashboard mas inexistente.")
        out("")

    # 3. frontmatter
    fm_missing, fm_keys, status_counter, imgs = [], Counter(), Counter(), 0
    placeholder = []
    for path in vault.notes:
        text = read_text(path)
        fm, body = split_frontmatter(text)
        if not fm:
            fm_missing.append(path)
        else:
            fm_keys.update(fm.keys())
            status_counter[fm.get("status", "(sem status)")] += 1
            if str(fm.get("tem_imagem", "")).lower() in ("true", "yes"):
                imgs += 1
        if any(marker in body for marker in PLACEHOLDER_MARKERS):
            placeholder.append(path)

    out("## 3. Frontmatter")
    out("")
    out(f"- Notas **sem** frontmatter: **{len(fm_missing)}**")
    out(f"- Notas declarando `tem_imagem: true`: **{imgs}**")
    out(f"- Notas ainda em estado de placeholder (rascunho de texto): **{len(placeholder)}**")
    out("")
    out("Chaves encontradas e sua frequência:")
    out("")
    out("| Chave | Ocorrências | Canônica? |")
    out("| :--- | ---: | :--- |")
    canonical_keys = {
        "title", "part", "category", "status", "draft", "tags", "aliases",
        "tem_imagem", "images", "effort", "last_tested", "sources", "id",
        "type", "parent", "publish",
    }
    for key, count in fm_keys.most_common():
        out(f"| `{key}` | {count} | {'sim' if key in canonical_keys else '**não**'} |")
    out("")
    out("Distribuição de `status`:")
    out("")
    out("| status | Notas |")
    out("| :--- | ---: |")
    for key, count in status_counter.most_common():
        out(f"| `{key}` | {count} |")
    out("")

    # 4. links
    broken, ambiguous, missing_assets = [], [], []
    for path in vault.notes:
        text = read_text(path)
        for kind, target in extract_links(text):
            if kind == "embed" and Path(target).suffix.lower() not in {
                ".canvas", ".base", ".excalidraw", ".pdf", ".md"
            }:
                st, hits = vault.resolve(target)
                if st == "missing-asset":
                    missing_assets.append((rel(path), target))
                elif st == "ambiguous":
                    ambiguous.append((rel(path), target, len(hits)))
                continue
            st, hits = vault.resolve(target)
            if st == "broken":
                broken.append((rel(path), target))
            elif st == "ambiguous":
                ambiguous.append((rel(path), target, len(hits)))

    out("## 4. Links e mídia")
    out("")
    out(f"- Embeds de imagem/mídia sem arquivo correspondente: **{len(missing_assets)}**")
    out(f"- Wikilinks que não resolvem: **{len(broken)}**")
    out(f"- Wikilinks ambíguos (mais de um alvo possível): **{len(ambiguous)}**")
    out("")
    if missing_assets:
        out("### Amostra de mídia ausente")
        out("")
        out("| Nota | Arquivo esperado |")
        out("| :--- | :--- |")
        for src, tgt in missing_assets[: args.sample]:
            out(f"| `{src}` | `{tgt}` |")
        if len(missing_assets) > args.sample:
            out(f"| … | _e mais {len(missing_assets) - args.sample}_ |")
        out("")
    if broken:
        out("### Links quebrados (todos)")
        out("")
        out("| Nota | Alvo |")
        out("| :--- | :--- |")
        for src, tgt in sorted(broken):
            out(f"| `{src}` | `{tgt}` |")
        out("")
    if ambiguous:
        out("### Links ambíguos (todos)")
        out("")
        out("| Nota | Alvo | Candidatos |")
        out("| :--- | :--- | ---: |")
        for src, tgt, n in sorted(ambiguous):
            out(f"| `{src}` | `{tgt}` | {n} |")
        out("")

    # 5. duplicatas de nome
    dups = {k: v for k, v in vault.by_stem.items() if len(v) > 1}
    out("## 5. Notas homônimas")
    out("")
    if not dups:
        out("Nenhuma. ✅")
    else:
        out(f"**{len(dups)}** nome(s) aparecem em mais de um arquivo — isso quebra a")
        out("resolução de wikilinks no modo `shortest` usado pelo Quartz.")
        out("")
        for stem, paths in sorted(dups.items()):
            out(f"- **{stem}**")
            for p in paths:
                out(f"  - `{rel(p)}`")
    out("")

    # 6. encoding
    mojibake = [p for p in ROOT.rglob("*") if looks_mojibake(p.name)]
    out("## 6. Nomes de arquivo com encoding quebrado")
    out("")
    out(f"**{len(mojibake)}** entrada(s). Corrija com `scripts/enciclopedia.py fix-names --apply`.")
    out("")

    # 7. staging
    out("## 7. Pastas de staging (`Notas_*_Lote*`)")
    out("")
    if not staging:
        out("Nenhuma. ✅")
    else:
        out("Essas pastas duplicam a árvore canônica e devem ser absorvidas por ela.")
        out("")
        out("| Pasta | Notas |")
        out("| :--- | ---: |")
        for area, items in sorted(staging.items()):
            out(f"| `{area}` | {len(items)} |")
        out("")
        out("Absorção: `scripts/enciclopedia.py merge-lots --apply`.")
    out("")

    # 8. documentos-fonte
    sources = [
        p for p in sorted(ROOT.glob("*.md")) + sorted(ROOT.glob("*.pdf"))
    ]
    out("## 8. Documentos-fonte na raiz")
    out("")
    if sources:
        out("| Arquivo | Tamanho |")
        out("| :--- | ---: |")
        for p in sources:
            out(f"| `{p.name}` | {p.stat().st_size / 1024:.0f} KB |")
        out("")
        out("Devem sair da raiz para `_fontes/` (ver blueprint).")
    else:
        out("Nenhum. ✅")
    out("")

    report = "\n".join(lines)
    if args.output:
        dest = ROOT / args.output
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_text(report + "\n", encoding="utf-8")
        print(f"Relatório escrito em {args.output} ({len(report)} bytes)")
    else:
        print(report)
    return 0


def cmd_links(args) -> int:
    vault = Vault(include_staging=args.staging)
    problems = []
    for path in vault.notes:
        text = read_text(path)
        for kind, target in extract_links(text):
            st, hits = vault.resolve(target)
            if st in ("broken", "missing-asset"):
                problems.append((rel(path), target, st))
            elif st == "ambiguous" and args.strict:
                problems.append((rel(path), target, f"ambíguo ({len(hits)})"))
    for src, tgt, st in problems:
        print(f"[{st}] {src} -> {tgt}")
    print(f"\nTotal: {len(problems)} problema(s).")
    return 1 if problems and args.fail else 0


def cmd_fix_names(args) -> int:
    renamed = 0
    # processa do mais fundo para a raiz, para renomear filhos antes dos pais
    entries = sorted(
        (p for p in ROOT.rglob("*") if ".git" not in p.parts and looks_mojibake(p.name)),
        key=lambda p: len(p.parts),
        reverse=True,
    )
    for path in entries:
        new_name = repair_mojibake(path.name)
        target = path.with_name(new_name)
        print(f"{'RENOMEAR' if args.apply else 'prever  '}: {path.name!r} -> {new_name!r}")
        if not args.apply:
            renamed += 1
            continue
        if target.exists():
            if path.is_dir() and target.is_dir():
                for child in sorted(path.rglob("*")):
                    dest = target / child.relative_to(path)
                    if child.is_dir():
                        dest.mkdir(parents=True, exist_ok=True)
                    else:
                        dest.parent.mkdir(parents=True, exist_ok=True)
                        shutil.move(str(child), str(dest))
                shutil.rmtree(path, ignore_errors=True)
            else:
                print(f"  ! conflito, mantido: {rel(target)} já existe")
                continue
        else:
            path.rename(target)
        renamed += 1
    print(f"\n{renamed} entrada(s). {'Aplicado.' if args.apply else 'Use --apply.'}")
    return 0


def _canonical_destination(path: Path) -> Path:
    """Descobre o destino canônico de uma nota de staging.

    A estrutura dentro do lote já carrega o caminho canônico; o que precisa
    ser removido é o prefixo do lote (e o diretório duplicado que o upload
    do GitHub cria). Ex.:

      Notas_X/Notas_X/02_Catalogo_Visual/A/B.md -> 02_Catalogo_Visual/A/B.md
      Notas_X/Fundamentos_Notas/Luz/Y.md        -> 01_Fundamentos_Teoricos/Luz/Y.md
    """
    parts = list(path.relative_to(ROOT).parts)
    lot = parts[0]
    parts = parts[1:]  # remove a pasta do lote
    # remove diretórios repetidos (Notas_X/Notas_X/...)
    while parts and parts[0] == lot:
        parts = parts[1:]
    if not parts:
        parts = [path.name]
    if parts[0].startswith("Fundamentos_Notas"):
        parts = ["01_Fundamentos_Teoricos"] + parts[1:]
    if not re.match(r"^\d{2}_", parts[0]):
        # sem prefixo numérico: cai no catálogo
        parts = ["02_Catalogo_Visual"] + parts
    parts = [repair_mojibake(part) for part in parts]
    return ROOT.joinpath(*parts)


def cmd_merge_lots(args) -> int:
    staging_dirs = [
        p for p in sorted(ROOT.iterdir())
        if p.is_dir() and p.name.startswith(STAGING_PREFIX)
    ]
    if not staging_dirs:
        print("Nenhuma pasta de staging encontrada.")
        return 0
    moved, conflicts = 0, []
    for sdir in staging_dirs:
        for path in sorted(sdir.rglob("*.md")):
            if path.name == "README.md":
                continue
            dest = _canonical_destination(path)
            if dest.exists():
                same = dest.read_bytes() == path.read_bytes()
                conflicts.append((rel(path), rel(dest), same))
                if not args.apply or not args.force:
                    continue
            dest.parent.mkdir(parents=True, exist_ok=True)
            print(f"{'MOVER' if args.apply else 'prever'}: {rel(path)} -> {rel(dest)}")
            if args.apply:
                shutil.move(str(path), str(dest))
            moved += 1
    if conflicts:
        print("\nConflitos (destino já existe):")
        for src, dst, same in conflicts:
            flag = "idêntico" if same else "**DIVERGENTE**"
            print(f"  [{flag}] {src} -> {dst}")
    if args.apply:
        for sdir in staging_dirs:
            leftovers = [p for p in sdir.rglob("*") if p.is_file()]
            if not leftovers:
                shutil.rmtree(sdir, ignore_errors=True)
                print(f"removido: {sdir.name}/")
    print(f"\n{moved} nota(s). {'Aplicado.' if args.apply else 'Use --apply.'}")
    return 0


def cmd_normalize(args) -> int:
    changed = 0
    for path in iter_notes():
        text = read_text(path)
        fm, body = split_frontmatter(text)
        if not fm:
            print(f"[sem frontmatter] {rel(path)}")
            continue
        new = {}
        for key, value in fm.items():
            new[FRONTMATTER_ALIASES.get(key, key)] = value
        status = str(new.get("status", "")).strip().strip('"').lower()
        # `draft` = "nao publicar". Rascunho de texto ainda e publicavel;
        # so `ideia` (nota sem conteudo) fica fora do site.
        if status == "ideia":
            new["draft"] = "true"
        elif status:
            new["draft"] = "false"
        new.setdefault("status", "rascunho")
        if "part" in new and not str(new["part"]).startswith('"'):
            new["part"] = f'"{new["part"]}"'
        if new != fm:
            print(f"{'AJUSTAR' if args.apply else 'prever '}: {rel(path)}")
            if args.apply:
                path.write_text(dump_frontmatter(new) + body.lstrip("\n"), encoding="utf-8")
            changed += 1
    print(f"\n{changed} nota(s). {'Aplicado.' if args.apply else 'Use --apply.'}")
    return 0


TEMPLATE = """---
title: "{title}"
part: "{part}"
category: "{category}"
status: rascunho
draft: true
tags: [{tags}]
aliases: []
tem_imagem: false
images: []
effort: 2
last_tested: "{today}"
sources: []
---

# {title}

## Conceito Técnico


## Efeito Psicológico e Narrativo


## Aplicações Práticas


## Módulos para Engenharia de Prompt

| Parâmetro | Configuração Recomendada | Efeito no Gerador de IA |
| :--- | :--- | :--- |
|  | `` |  |

### Vocabulário para Prompt
*

## Prompt de Referência (Testado)

```

```

## Notas de Revisão
-
"""


def cmd_new(args) -> int:
    area = args.part
    base = ROOT / area
    dest_dir = base / args.category if args.category else base
    dest_dir.mkdir(parents=True, exist_ok=True)
    name = args.title if args.title.endswith(".md") else f"{args.title}.md"
    dest = dest_dir / name
    if dest.exists() and not args.force:
        print(f"já existe: {rel(dest)}")
        return 1
    tags = ", ".join(slugify(t) for t in args.tags) if args.tags else ""
    dest.write_text(
        TEMPLATE.format(
            title=Path(name).stem,
            part=area,
            category=args.category or "",
            tags=tags,
            today=date.today().isoformat(),
        ),
        encoding="utf-8",
    )
    print(f"criado: {rel(dest)}")
    return 0


def cmd_sync_sources(args) -> int:
    dest = ROOT / "_fontes"
    moved = 0
    for path in sorted(list(ROOT.glob("*.md")) + list(ROOT.glob("*.pdf"))):
        if path.name in {"README.md", "BLUEPRINT.md", "index.md"}:
            continue
        target = dest / path.name
        print(f"{'MOVER' if args.apply else 'prever'}: {path.name} -> _fontes/{path.name}")
        if args.apply:
            dest.mkdir(parents=True, exist_ok=True)
            shutil.move(str(path), str(target))
        moved += 1
    print(f"\n{moved} arquivo(s). {'Aplicado.' if args.apply else 'Use --apply.'}")
    return 0


# ---------------------------------------------------------------- CLI


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("audit", help="diagnóstico completo")
    p.add_argument("--output", default="")
    p.add_argument("--sample", type=int, default=25)
    p.set_defaults(func=cmd_audit)

    p = sub.add_parser("links", help="lista links/embeds que não resolvem")
    p.add_argument("--staging", action="store_true")
    p.add_argument("--strict", action="store_true", help="conta ambíguos como erro")
    p.add_argument("--fail", action="store_true", help="exit code 1 se houver problemas")
    p.set_defaults(func=cmd_links)

    for name, fn, helptext in [
        ("fix-names", cmd_fix_names, "corrige nomes com encoding quebrado"),
        ("merge-lots", cmd_merge_lots, "absorve pastas Notas_* na árvore canônica"),
        ("normalize", cmd_normalize, "padroniza frontmatter"),
        ("sync-sources", cmd_sync_sources, "move documentos-fonte para _fontes/"),
    ]:
        p = sub.add_parser(name, help=helptext)
        p.add_argument("--apply", action="store_true")
        p.add_argument("--force", action="store_true")
        p.set_defaults(func=fn)

    p = sub.add_parser("new", help="cria nota a partir do template")
    p.add_argument("title")
    p.add_argument("--part", default="01_Fundamentos_Teoricos",
                   choices=CANONICAL_AREAS)
    p.add_argument("--category", default="")
    p.add_argument("--tags", nargs="*", default=[])
    p.add_argument("--force", action="store_true")
    p.set_defaults(func=cmd_new)

    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
