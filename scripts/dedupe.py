#!/usr/bin/env python3
"""
Deduplicacao e absorcao do cofre.

Resolve o que o upload em lote trouxe de volta:
  - notas casca `Movimento_NN` (superadas pelas notas com nome real)
  - duplicatas `Nota (2).md` geradas pelo Obsidian ao copiar arquivos
  - variantes `Nota (expansao).md` que devem substituir a nota base
  - espelhos de nota dentro de `05_Anexos/`
  - pastas duplicadas (`Generos e Universos` vs `Generos_e_Universos`)

Uso:
    python3 scripts/dedupe.py            # dry-run, so mostra
    python3 scripts/dedupe.py --apply    # executa
    python3 scripts/dedupe.py --only X   # executa so o passo X
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

STUB_MARKERS = [
    "Definição breve do movimento",
    "Definição breve",
    "- item 1",
    "Autor / Obra 1",
    "(escreva aqui a definição técnica)",
    "(escreva aqui",
]


def is_stub(p: Path) -> bool:
    """True se a nota ainda eh um esboco sem conteudo real."""
    body = body_of(p)
    if not body.strip():
        return True
    return any(m in body for m in STUB_MARKERS)


def log(msg: str) -> None:
    print(msg)


def sha(p: Path) -> str:
    import hashlib
    return hashlib.sha256(p.read_bytes()).hexdigest()


def body_of(p: Path) -> str:
    text = p.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            return text[end + 4:].strip()
    return text.strip()


def has_new_keys(p: Path) -> bool:
    """A versao canonica usa part/category; a antiga usava parte/categoria."""
    text = p.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
    if not text.startswith("---"):
        return False
    end = text.find("\n---", 3)
    if end == -1:
        return False
    fm = text[3:end]
    if "parte:" in fm or "categoria:" in fm:
        return False
    return "part:" in fm and "category:" in fm


# ------------------------------------------------------------------ passos


def step_stubs(apply: bool) -> int:
    """Apaga as notas casca Movimento_NN, superadas pelas notas com nome real."""
    n = 0
    for p in sorted(ROOT.rglob("Movimento_[0-9][0-9].md")):
        if ".git" in p.parts:
            continue
        body = body_of(p)
        if not any(m in body for m in STUB_MARKERS):
            log(f"  ! {p.relative_to(ROOT)} tem conteudo real — mantido")
            continue
        log(f"  - casca: {p.relative_to(ROOT)}")
        if apply:
            p.unlink()
        n += 1
    log(f"  ({n} casca(s))")
    return n


def step_paren_dupes(apply: bool) -> int:
    """Apaga `Nota (2).md` quando a base existe e eh maior."""
    n = 0
    for dup in sorted(ROOT.rglob("* (2).md")):
        if ".git" in dup.parts:
            continue
        base = dup.with_name(dup.name.replace(" (2)", ""))
        if not base.exists():
            log(f"  ! {dup.relative_to(ROOT)} sem base — mantido")
            continue
        b, d = len(body_of(base)), len(body_of(dup))
        if d > b:
            log(f"  ! {dup.relative_to(ROOT)} eh MAIOR que a base — mantido")
            continue
        log(f"  - duplicata: {dup.relative_to(ROOT)} ({d}B < {b}B)")
        if apply:
            dup.unlink()
        n += 1
    log(f"  ({n} duplicata(s))")
    return n


def step_expansao(apply: bool) -> int:
    """Promove `Nota (expansao).md` sobre a nota base."""
    n = 0
    for exp in sorted(ROOT.rglob("* (expansão).md")):
        if ".git" in exp.parts:
            continue
        base = exp.with_name(exp.name.replace(" (expansão)", ""))
        e, b = len(body_of(exp)), len(body_of(base)) if base.exists() else 0
        if base.exists() and e <= b:
            log(f"  ! {exp.relative_to(ROOT)} nao eh maior — mantido")
            continue
        log(f"  ^ promover: {exp.relative_to(ROOT)} ({e}B) -> {base.name} ({b}B)")
        if apply:
            if base.exists():
                base.unlink()
            exp.rename(base)
        n += 1
    log(f"  ({n} promocao(oes))")
    return n


def deaccent(name: str) -> str:
    import unicodedata
    return "".join(
        c for c in unicodedata.normalize("NFD", name)
        if unicodedata.category(c) != "Mn"
    )


def step_acentos(apply: bool) -> int:
    """Remove a variante sem acento quando a versao acentuada existe ao lado."""
    n = kept = 0
    for pasta in sorted({q.parent for q in ROOT.rglob("*.md")}):
        if ".git" in pasta.parts:
            continue
        grupos: dict[str, list[Path]] = {}
        for q in pasta.glob("*.md"):
            grupos.setdefault(deaccent(q.stem).lower(), []).append(q)
        for chave, arquivos in grupos.items():
            if len(arquivos) < 2:
                continue
            # fica a que tem acento (titulo canonico em portugues)
            acentuados = [a for a in arquivos if deaccent(a.stem) != a.stem]
            if not acentuados:
                continue
            keeper = max(acentuados, key=lambda a: a.stat().st_size)
            for a in arquivos:
                if a == keeper:
                    continue
                if is_stub(a):
                    log(f"  - esboco: {a.relative_to(ROOT)}")
                    if apply:
                        a.unlink()
                    n += 1
                    continue
                if body_of(a) != body_of(keeper):
                    log(f"  ! corpo difere de {keeper.relative_to(ROOT)} — "
                        f"mantido: {a.name}")
                    kept += 1
                    continue
                log(f"  - sem acento: {a.relative_to(ROOT)}")
                if apply:
                    a.unlink()
                n += 1
    log(f"  ({n} removido(s), {kept} mantido(s))")
    return n


def step_mojibake(apply: bool) -> int:
    """Apaga o arquivo de nome corrompido quando a versao correta existe ao lado."""
    n = kept = 0
    for bad in sorted(ROOT.rglob("*.md")):
        if ".git" in bad.parts:
            continue
        good_name = repair(bad.name)
        if good_name == bad.name:
            continue
        good = bad.with_name(good_name)
        if not good.exists():
            continue
        if body_of(bad) != body_of(good):
            log(f"  ! corpo difere de {good.relative_to(ROOT)} — mantido")
            kept += 1
            continue
        # corpo igual: fica a versao com frontmatter canonico
        if has_new_keys(bad) and not has_new_keys(good):
            log(f"  ! {good.relative_to(ROOT)} tem frontmatter antigo — mantido")
            kept += 1
            continue
        log(f"  - nome corrompido: {bad.relative_to(ROOT)}")
        if apply:
            bad.unlink()
        n += 1
    log(f"  ({n} removido(s), {kept} mantido(s))")
    return n


def step_empty_folders(apply: bool) -> int:
    """Remove pastas que ficaram vazias."""
    n = 0
    for p in sorted(ROOT.rglob("*"), key=lambda x: -len(x.parts)):
        if ".git" in p.parts or not p.is_dir() or p == ROOT:
            continue
        try:
            if not any(p.iterdir()):
                log(f"  - pasta vazia: {p.relative_to(ROOT)}")
                if apply:
                    p.rmdir()
                n += 1
        except OSError:
            pass
    log(f"  ({n} pasta(s))")
    return n


def repair(name: str) -> str:
    """Reverte UTF-8 lido como CP437/CP850."""
    for enc in ("cp437", "cp850", "latin-1"):
        try:
            fixed = name.encode(enc).decode("utf-8")
        except (UnicodeEncodeError, UnicodeDecodeError):
            continue
        if fixed != name and fixed.isprintable():
            return fixed
    return name


def route(p: Path) -> Path:
    """Descobre o destino canonico de uma nota a partir do frontmatter."""
    text = p.read_text(encoding="utf-8", errors="replace")
    part = cat = ""
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end != -1:
            for line in text[3:end].split("\n"):
                m = re.match(r'^(parte|part)\s*:\s*"?([^"\n]+)"?', line)
                if m:
                    part = m.group(2).strip().strip('"')
                m = re.match(r'^(categoria|category)\s*:\s*"?([^"\n]+)"?', line)
                if m:
                    cat = m.group(2).strip().strip('"')
    if part.startswith("01_"):
        area = "01_Fundamentos_Teoricos"
    elif part.startswith(("03_", "04_", "05_", "06_", "07_")):
        area = part
    else:
        area = "02_Catalogo_Visual"
    base = ROOT / area
    sub = repair(cat) if cat else ""
    if sub and (base / sub).is_dir():
        return base / sub / repair(p.name)
    if sub and (base / sub.replace(" ", "_")).is_dir():
        return base / sub.replace(" ", "_") / repair(p.name)
    # sem frontmatter util: usa a subpasta de origem dentro de 05_Anexos
    parts = [repair(x) for x in p.relative_to(ROOT / "05_Anexos").parts[:-1]]
    if parts:
        cand = base
        for piece in parts:
            nxt = cand / piece
            if not nxt.is_dir():
                nxt = cand / piece.replace(" ", "_")
            if nxt.is_dir():
                cand = nxt
            else:
                break
        return cand / repair(p.name)
    return base / repair(p.name)


def step_anexos_notes(apply: bool) -> int:
    """Absorve/remove as notas espelhadas dentro de 05_Anexos/."""
    anexos = ROOT / "05_Anexos"
    if not anexos.is_dir():
        return 0
    canon: dict[str, list[Path]] = {}
    for p in ROOT.rglob("*.md"):
        if ".git" in p.parts or str(p).startswith(str(anexos)):
            continue
        canon.setdefault(repair(p.stem).lower(), []).append(p)

    removed = moved = 0
    for p in sorted(anexos.rglob("*.md")):
        if p.name.startswith("00_README"):
            continue
        size = p.stat().st_size
        hits = canon.get(repair(p.stem).lower(), [])
        if not hits and size > 0:
            dest = route(p)
            log(f"  > nova: {p.relative_to(ROOT)} -> {dest.relative_to(ROOT)}")
            if apply:
                dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(p), str(dest))
            moved += 1
            continue
        reason = "vazia" if size == 0 else (
            "identica" if any(sha(p) == sha(q) for q in hits) else "espelho"
        )
        log(f"  - {reason}: {p.relative_to(ROOT)} ({size}B)")
        if apply:
            p.unlink()
        removed += 1
    log(f"  ({removed} removida(s), {moved} movida(s))")
    return removed + moved


def health(d: Path) -> int:
    """Quanto maior, pior. Conta nomes mojibake, ausencia de MOC/README e arquivos soltos."""
    score = 0
    for f in d.rglob("*"):
        if not f.is_file():
            continue
        name = f.name
        if repair(name) != name:
            score += 2          # nome corrompido
        if name != name.strip(" ."):
            score += 2          # nome com espaco/ponto nas pontas
    if not any(f.name.startswith("MOC - ") for f in d.glob("*.md")):
        score += 1              # sem mapa do conteudo
    if not any(f.name.startswith("00_README") for f in d.glob("*.md")):
        score += 1
    return score


def step_folder_dupes(apply: bool) -> int:
    """Resolve pastas que diferem so por espaco/underscore no nome."""
    n = 0
    for parent in sorted({p.parent for p in ROOT.rglob("*") if p.is_dir()}):
        if ".git" in parent.parts:
            continue
        dirs = [p for p in parent.iterdir() if p.is_dir()]
        for pa in dirs:
            for pb in dirs:
                if pa.name >= pb.name:
                    continue
                if pa.name.replace(" ", "_") != pb.name.replace(" ", "_"):
                    continue
                ha, hb = health(pa), health(pb)
                loser, winner = (pa, pb) if ha >= hb else (pb, pa)
                log(f"  - duplicata: {loser.relative_to(ROOT)} (saude {health(loser)}) "
                    f"<- mantendo {winner.relative_to(ROOT)} (saude {health(winner)})")
                if apply:
                    for f in sorted(loser.rglob("*")):
                        if f.is_file():
                            dest = winner / f.relative_to(loser)
                            dest.parent.mkdir(parents=True, exist_ok=True)
                            if not dest.exists():
                                shutil.move(str(f), str(dest))
                    shutil.rmtree(loser, ignore_errors=True)
                n += 1
    log(f"  ({n} pasta(s))")
    return n


# Notas que dividem nome com outra. O mapa eh (caminho, nome novo).
DESAMBIGUACAO = [
    ("01_Fundamentos_Teoricos/Densidade Visual/Minimalismo.md",
     "Minimalismo (Densidade Visual)"),
    ("01_Fundamentos_Teoricos/Luz/Luz Volumétrica e Meio/Luz Volumétrica e Meio.md",
     "../Luz Volumétrica e Meio"),
]

# Links que apontam em notas que ainda nao existem, com o destino real.
DESTINOS = {
    "Rembrandt Lighting": "Iluminação Rembrandt",
    "Render 3D / PBR": "3D Render",
    "Textura e Materialidade": "Textura - Materialidade",
    "Composição": "MOC - Composição",
    "Atmosfera e Clima": "MOC - Luz",
    "Paleta de Cores": "MOC - Cor",
    "Fotografia de Paisagem": "MOC - Fotografia",
    "Escala": "MOC - Geometria de Cena",
    "Cinema de Atmosfera": "MOC - Catalogo Visual",
    "Macrofotografia": "MOC - Midias e Suportes",
}


def step_homonimos(apply: bool) -> int:
    """Renomeia notas que dividem o nome com outra."""
    n = 0
    for rel_path, novo in DESAMBIGUACAO:
        alvo = ROOT / rel_path
        if not alvo.exists():
            log(f"  ! ausente: {rel_path}")
            continue
        dest = alvo.with_name(f"{novo}.md")
        log(f"  ^ {rel_path} -> {dest.relative_to(ROOT)}")
        if apply:
            dest.parent.mkdir(parents=True, exist_ok=True)
            alvo.rename(dest)
        n += 1
    log(f"  ({n} renomeio(s))")
    return n


def step_destinos(apply: bool) -> int:
    """Reaponta links orfaos para a nota correta."""
    n = 0
    for p in sorted(ROOT.rglob("*.md")):
        if ".git" in p.parts:
            continue
        t = p.read_text(encoding="utf-8", errors="replace")
        o = t
        for velho, novo in DESTINOS.items():
            t = re.sub(rf"\[\[{re.escape(velho)}(\|[^\]]*)?\]\]",
                       lambda m, n=novo: "[[" + n + (m.group(1) or "") + "]]", t)
        if t != o:
            log(f"  ~ {p.relative_to(ROOT)}")
            if apply:
                p.write_text(t, encoding="utf-8")
            n += 1
    log(f"  ({n} arquivo(s))")
    return n


def step_fix_links(apply: bool) -> int:
    """Corrige wikilinks que apontam para alvos renomeados/removidos."""
    fixes = [
        ("[[MOC - Fundamentos Teoricos]]", "[[MOC - Fundamentos]]"),
        ("[[MOC - Fundamentos Teóricos]]", "[[MOC - Fundamentos]]"),
        ("[[Luz - High-key / Low-key]]", "[[Luz - High-key vs Low-key]]"),
    ]
    n = 0
    for p in sorted(ROOT.rglob("*.md")):
        if ".git" in p.parts:
            continue
        t = p.read_text(encoding="utf-8", errors="replace")
        o = t
        for a, b in fixes:
            t = t.replace(a, b)
        if t != o:
            log(f"  ~ links: {p.relative_to(ROOT)}")
            if apply:
                p.write_text(t, encoding="utf-8")
            n += 1
    log(f"  ({n} arquivo(s))")
    return n


STEPS = [
    ("stubs", "apagar notas casca Movimento_NN", step_stubs),
    ("dupes", "apagar duplicatas 'Nota (2)'", step_paren_dupes),
    ("mojibake", "apagar arquivos de nome corrompido", step_mojibake),
    ("acentos", "apagar variantes sem acento", step_acentos),
    ("expansao", "promover 'Nota (expansao)' sobre a base", step_expansao),
    ("anexos", "absorver espelhos de 05_Anexos", step_anexos_notes),
    ("folders", "resolver pastas duplicadas", step_folder_dupes),
    ("homonimos", "desambiguar notas de nome repetido", step_homonimos),
    ("destinos", "reapontar links orfaos", step_destinos),
    ("links", "corrigir wikilinks quebrados", step_fix_links),
    ("vazias", "remover pastas vazias", step_empty_folders),
]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--only", default="")
    args = parser.parse_args()

    for key, desc, fn in STEPS:
        if args.only and key != args.only:
            continue
        log(f"\n=== {key}: {desc} ===")
        fn(args.apply)

    log("\n" + ("APLICADO." if args.apply else "Dry-run. Use --apply."))
    return 0


if __name__ == "__main__":
    sys.exit(main())
