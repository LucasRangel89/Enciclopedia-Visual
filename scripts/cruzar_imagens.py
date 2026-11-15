#!/usr/bin/env python3
"""
Cruza o acervo de imagens com as notas do cofre.

Responde tres perguntas:
  1. quais notas tem imagem disponivel (e qual)
  2. quais imagens nao tem nota (candidatas a nota nova)
  3. quais notas nao tem imagem (candidatas a geracao)

Uso:
    python3 scripts/cruzar_imagens.py              # relatorio
    python3 scripts/cruzar_imagens.py --apply      # reescreve os embeds
"""

from __future__ import annotations

import argparse
import re
import sys
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

GERADORES = (
    "bing", "chatgpt", "gemini", "krea", "leonardo", "manus", "raphael",
    "reve", "dalle3", "dalle", "imagen",
)
SUFIXOS = {".png", ".jpg", ".jpeg", ".webp", ".gif"}

# stem da nota -> conceito de imagem, quando os nomes divergem
ALIAS = {
    "canone_classico_greco_romano": "greco_romana",
    "estilizacao_expressiva_do_corpo": "estilizacao_expressiva",
    "pose_editorial": "pose_editorial",
    "pose_de_acao": "pose_acao",
    "pose_de_retrato": "pose_retrato",
    "postura_aberta": "postura_aberta",
    "postura_fechada": "postura_fechada",
    "medo": "medo",
    "nojo": "nojo",
    "raiva": "raiva",
    "congelamento_de_movimento_freeze": "freeze",
    "longa_exposicao_e_motion_blur": "longa_exposicao",
    "a24": "a24",
    "os_gemeos": "gemeos",
    "technicolor_saturado": "technicolor_saturado",
    "bleach_bypass": "bleach_bypass",
    "luz_suave_difusa": "luz_suave_difusa",
    "luz_suave_difusa": "luz_difusa",
    "iluminacao_rembrandt": "rembrandt",
    "profundidade_de_campo_profunda": "profunda",
    "profundidade_de_campo_rasa": "rasa",
    "movimento_implicito_dolly": "dolly",
    "movimento_implicito_pan": "pan",
    "movimento_implicito_tilt": "tilt",
    "efeito_hitchcock_dolly_zoom_em_imagem_estatica": "dolly_zoom",
    "regra_aurea": "aurea",
    "enquadramento": "enquadramento",
    "espaco_negativo": "espaco_negativo",
    "simetria": "simetria",
    "subversao_deliberada": "subversao_deliberada",
    "linhas_guia": "linhas_guias",
    "pesos_visuais": "pesos_visuais",
    "regra_dos_tercos": "regra_dos_tercos",
    "1_ponto": "um_ponto",
    "2_pontos": "dois_pontos",
    "3_pontos": "tres_pontos",
    "perspectiva_atmosferica": "perspectiva_atmosferica",
    "cor_fria": "cor_fria",
    "cor_quente": "cor_quente",
    "harmonia_analoga": "harmonia_analoga",
    "harmonia_complementar": "harmonia_complementar",
    "harmonia_monocromatica": "harmonia_monocromatica",
    "harmonia_triade": "harmonia_triade",
    "maximalismo": "maximalismo",
    "minimalismo_densidade_visual": "minimalismo",
    "cultura_de_massa_e_consumo": "massa_consumo",
    "art_nouveau": "art_nouveau",
    "art_deco": "art_deco",
    "art_brut": "art_brut",
    "arte_conceitual": "arte_conceitual",
    "impressionismo": "impressionismo",
    "pop_art": "pop_art",
    "surrealismo": "surrealismo",
    "fotocopia": "fotocopia",
    "videoteipe_vhs": "vhs",
    "aquarela": "aquarela",
    "fotografia_analogica_35mm": "foto_analog_35mm",
    "pintura_a_oleo": "pintura_a_oleo",
    "pixel_art": "pixel_art",
    "superficies_artificiais": "artificial",
    "superficies_organicas": "organicas",
    "grao_e_ruido_visual_grain_dust_scratches": "grao_ruido",
    "aberracao_cromatica": "aberracoes",
    "bokeh_circular_suave": "bokeh_circular_suave",
    "bokeh_nervoso_hardado": "bokeh_nervoso",
    "bokeh_oval_anamorfico": "bokeh_oval",
    "bokeh_poligonal": "bokeh_poligonal",
    "bokeh_swirly_lente_helios_44_2": "bokeh_swirly",
    "alex_ross": "alex_ross",
    "ashley_wood": "ashley_wood",
    "frank_frazetta": "frazzetta",
    "simon_stalenhag": "stalenhag",
    "genndy_tartakovsky": "tartakovsky",
    "michael_whelan": "whelan",
    "pintura_shanshui": "shanshui",
    "polaroid_instantaneo": "polaroid",
    "luz_volumetrica_e_meio": "luz_volumetrica",
    "luz_dura": "luz_dura",
    "luz_de_vela": "luz_de_vela",
    "contraluz": "contraluz",
    "golden_hour": "golden_hour",
    "underlight": "underlight",
    "iluminacao_rembrandt": "rembrandt_exemplo",
}


def norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s)
    s = "".join(c for c in s if unicodedata.category(c) != "Mn")
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")


def sem_gerador(stem: str) -> str:
    partes = stem.split("_")
    while len(partes) > 1 and partes[-1].lower() in GERADORES:
        partes.pop()
    return "_".join(partes)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    # ---- indice de notas
    notas: dict[str, Path] = {}
    for p in ROOT.rglob("*.md"):
        if ".git" in p.parts:
            continue
        notas.setdefault(norm(p.stem), p)

    # ---- indice de imagens: conceito -> [arquivos]
    conceitos: dict[str, list[Path]] = {}
    for p in sorted(ROOT.rglob("*")):
        if not p.is_file() or ".git" in p.parts or p.suffix.lower() not in SUFIXOS:
            continue
        chave = norm(sem_gerador(p.stem))
        if chave:
            conceitos.setdefault(chave, []).append(p)

    # ---- cruzamento, escopado nas notas que precisam de imagem
    sys.path.insert(0, str(ROOT / "scripts"))
    from enciclopedia import Vault, extract_links

    vault = Vault(include_staging=False)
    precisam = []
    for q in vault.notes:
        embeds = [t for k, t in extract_links(q.read_text(encoding="utf-8", errors="replace"))
                  if k == "embed"]
        faltando = [t for t in embeds if vault.resolve(t)[0] == "missing-asset"]
        if faltando or not embeds:
            precisam.append((q, faltando[0] if faltando else None))

    com_imagem, sem_imagem = [], []
    usadas = set()
    for q, alvo in precisam:
        chave = norm(q.stem)
        conceito = ALIAS.get(chave, chave)
        cands = conceitos.get(conceito)
        if cands:
            com_imagem.append((q, cands))
            usadas.update(str(c) for c in cands)
        else:
            sem_imagem.append((q, alvo))

    img_sem_nota = [
        (chave, cands) for chave, cands in sorted(conceitos.items())
        if not any(str(c) in usadas for c in cands)
    ]

    print("=== RESUMO ===")
    print(f"  notas que precisam de imagem : {len(precisam)}")
    print(f"    com imagem disponivel      : {len(com_imagem)}")
    print(f"    sem imagem disponivel      : {len(sem_imagem)}")
    print(f"  imagens sem nota             : {len(img_sem_nota)} "
          f"({sum(len(c) for _, c in img_sem_nota)} arquivos)")
    print(f"  conceitos de imagem no cofre : {len(conceitos)}")

    print("\n=== IMAGENS SEM NOTA (candidatas a nota nova) ===")
    for chave, cands in img_sem_nota:
        pasta = cands[0].parent.relative_to(ROOT).as_posix()
        print(f"  {chave:38s} {len(cands):2d}  [{pasta}]")

    from collections import Counter
    por_area = Counter(q.relative_to(ROOT).parts[0] for q, _ in sem_imagem)
    print("\n=== NOTAS SEM IMAGEM DISPONIVEL, por area ===")
    for area, n in por_area.most_common():
        print(f"  {area:26s} {n}")

    if args.apply:
        n = 0
        for q, cands in com_imagem:
            melhor = sorted(
                cands,
                key=lambda c: (0 if c.suffix.lower() == ".png" else 1, c.name),
            )[0]
            texto = q.read_text(encoding="utf-8", errors="replace")
            if f"[[{melhor.name}]]" in texto:
                continue
            novo = re.sub(
                r"!\[\[[^\]|#]+(?:\|[^\]]*)?\]\]",
                f"![[{melhor.name}]]",
                texto,
                count=1,
            )
            if novo != texto:
                q.write_text(novo, encoding="utf-8")
                n += 1
        print(f"\n{n} embed(s) reescrito(s).")

    return 0


if __name__ == "__main__":
    sys.exit(main())
