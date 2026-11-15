#!/usr/bin/env python3
"""
Reescreve os MOCs de cada Onda para apontar nos movimentos que existem de
fato, em vez dos 34 placeholders `Movimento_NN`.

Cada Onda tem 5 slots (Movimento_01..35) mas o roteiro-fonte lista uma
quantidade diferente de movimentos por onda, e 30 movimentos ja tem nota.
Este script casa os dois: usa a ordem do roteiro para preencher os slots e
lista como "faltando" o que nao tem nota.

Uso:
    python3 scripts/mapear_movimentos.py          # dry-run
    python3 scripts/mapear_movimentos.py --apply
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MOV = ROOT / "02_Catalogo_Visual" / "Movimentos"

# A pasta real de cada onda tem um sufixo descritivo.
PASTAS = {
    "Onda_01": "Onda_01_Pre_Moderna",
    "Onda_02": "Onda_02_Realismos",
    "Onda_03": "Onda_03_Luz_e_Cor",
    "Onda_04": "Onda_04_Vanguardas_Sec_XV",
    "Onda_05": "Onda_05_Design_e_Utopia_Industrial",
    "Onda_06": "Onda_06_Pop_Conceito_e_Rua",
    "Onda_07": "Onda_07_Tradicoes_Asiaticas",
}

# Ordem canonica do roteiro-fonte, por onda. Cada entrada e
# (titulo do movimento, nome do arquivo .md ou None se ainda nao existe).
ONDAS: dict[str, list[tuple[str, str | None]]] = {
    "Onda_01": [
        ("Renascimento", "Renascimento.md"),
        ("Barroco", "Barroco.md"),
        ("Rococó", "Rococó.md"),
        ("Romantismo", "Romantismo.md"),
    ],
    "Onda_02": [
        ("Realismo Clássico", "Realismo Clássico.md"),
        ("Hiper-realismo / Fotorrealismo", "Hiper-realismo e Fotorrealismo.md"),
        ("Realismo Mágico", "Realismo Mágico.md"),
    ],
    "Onda_03": [
        ("Impressionismo", "Impressionismo.md"),
        ("Pontilhismo", "Pontilhismo.md"),
        ("Pós-Impressionismo", "Pós-Impressionismo.md"),
    ],
    "Onda_04": [
        ("Expressionismo", "Expressionismo.md"),
        ("Expressionismo Abstrato", "Expressionismo Abstrato.md"),
        ("Fauvismo", "Fauvismo.md"),
        ("Cubismo", "Cubismo.md"),
        ("Futurismo", "Futurismo.md"),
        ("Dadaísmo", "Dadaismo.md"),
        ("Surrealismo", "Surrealismo.md"),
    ],
    "Onda_05": [
        ("Art Nouveau", "Art Nouveau.md"),
        ("Art Déco", "Art Deco.md"),
        ("Bauhaus", "Bauhaus.md"),
        ("Construtivismo Soviético", "Construtivismo Soviético.md"),
        ("Op Art", "Op Art.md"),
    ],
    "Onda_06": [
        ("Pop Art", "Pop Art.md"),
        ("Minimalismo", "Minimalismo.md"),
        ("Art Brut / Outsider Art", "Art Brut.md"),
        ("Arte Conceitual", "Arte Conceitual.md"),
        ("Street Art / Graffiti", "Street Art Graffiti.md"),
    ],
    "Onda_07": [
        ("Ukiyo-e", "Ukiyo-e.md"),
        ("Sumi-e", "Sumi-e.md"),
        ("Mangá / Anime", "Manga Anime.md"),
    ],
}


def unificar(onda: str) -> Path | None:
    """Move o MOC da pasta-slot `Onda_NN` para a pasta descritiva."""
    slot = MOV / onda
    real = MOV / PASTAS[onda]
    if not slot.is_dir():
        return real
    for f in slot.rglob("*"):
        if not f.is_file():
            continue
        dest = real / f.name
        if dest.exists():
            f.unlink()
            continue
        real.mkdir(parents=True, exist_ok=True)
        f.rename(dest)
    return real


def render(onda: str, itens: list[tuple[str, str | None]], sub: Path) -> str:
    tem, falta = [], []
    for titulo, arq in itens:
        alvo = sub / arq if arq else None
        if alvo and alvo.exists():
            stem = alvo.stem
            tem.append(f"- [[{stem}|{titulo}]]" if titulo != stem else f"- [[{stem}]]")
        else:
            falta.append(f"- [ ] {titulo}")
    linhas = ["## Movimentos nesta onda", *tem]
    if falta:
        linhas += ["", "## Ainda sem nota", *falta]
    return "\n".join(linhas) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    total_tem = total_falta = 0
    for onda, itens in ONDAS.items():
        sub = MOV / PASTAS[onda]
        if not sub.is_dir():
            print(f"  ! pasta ausente: {sub.relative_to(ROOT)}")
            continue
        sub = unificar(onda)
        moc = sub / f"MOC - {onda}.md"
        if not moc.exists():
            print(f"  ! MOC ausente em {sub.relative_to(ROOT)}")
            continue
        bloco = render(onda, itens, sub)
        n_tem = sum(1 for t, a in itens if a and (sub / a).exists())
        n_falta = len(itens) - n_tem
        total_tem += n_tem
        total_falta += n_falta
        print(f"\n=== {onda} ({n_tem} com nota, {n_falta} sem) ===")
        print(bloco.rstrip())

        if args.apply:
            txt = moc.read_text(encoding="utf-8")
            txt = re.sub(
                r"^part:.*$",
                f"part: 02_Catalogo_Visual/Movimentos/{PASTAS[onda]}",
                txt, count=1, flags=re.M,
            )
            novo = re.sub(
                r"## Movimentos nesta onda.*\Z",
                bloco,
                txt,
                flags=re.S,
            )
            moc.write_text(novo, encoding="utf-8")

    print(f"\nTOTAL: {total_tem} movimentos com nota, {total_falta} sem nota.")
    print("APLICADO." if args.apply else "Dry-run. Use --apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
