#!/usr/bin/env python3
"""
Encaminha as pranchas comparativas para os MOCs que elas servem.

As pranchas em `08_Imagens_Geradas/Pranchas_Comparativas/` sao imagens de
4-5 paineis que contrastam conceitos irmaos (SOFT/HARD/BACK/UNDER,
WARM/COLD/TEAL/NOIR, EYE/TOP/LOW/DUTCH...). Cada uma encaixa naturalmente
no MOC da area, como visao geral.

Este script insere a prancha no MOC correspondente, numa secao propria,
sem sobrescrever o resto do arquivo.

Uso:
    python3 scripts/ligar_pranchas.py            # dry-run
    python3 scripts/ligar_pranchas.py --apply
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRANCHAS = ROOT / "08_Imagens_Geradas" / "Pranchas_Comparativas"

# grupo da prancha -> (caminho do MOC, nota de rodape)
MAPEAMENTO = {
    "Iluminacao": ("01_Fundamentos_Teoricos/Luz/MOC - Luz.md",
                   "Suave · Dura · Contraluz · Contra-luz de baixo"),
    "Cor_e_grading": ("02_Catalogo_Visual/Cor_e_Grading/MOC - Cor e Grading.md",
                      "Quente · Fria · Teal & Orange · Noir"),
    "Cor_paleta": ("01_Fundamentos_Teoricos/Cor/MOC - Cor.md",
                   "Quente · Fria · Noir · Pastel"),
    "Paletas_humor": ("01_Fundamentos_Teoricos/Cor/MOC - Cor.md",
                      "Ciano · Terrosa · Pastel · Escura"),
    "Cor_Paleta": ("02_Catalogo_Visual/Cor_e_Grading/MOC - Cor e Grading.md",
                   "Teal · Bleach Bypass · Day-for-Night · Matte"),
    "Camera_enquadramento": ("01_Fundamentos_Teoricos/Geometria de Cena/Angulos e Pontos de Vista/MOC - Angulos e Pontos de Vista.md",
                             "Eye-level · Plongée · Contra-plongée · Over-the-shoulder"),
    "Camera_composicao": ("01_Fundamentos_Teoricos/Óptica & Lentes/MOC - Óptica & Lentes.md",
                          "16mm · 200mm · Olho de peixe · Tilt-shift"),
    "Lentes_e_perspectiva": ("01_Fundamentos_Teoricos/Óptica & Lentes/MOC - Óptica & Lentes.md",
                             "Grande-angular · Teleobjetiva · Olho de peixe · Tilt-shift"),
    "Distancia_plano": ("01_Fundamentos_Teoricos/Geometria de Cena/MOC - Geometria de Cena.md",
                        "Plano aberto · médio · fechado · macro"),
    "Composicao": ("01_Fundamentos_Teoricos/Composicao/MOC - Composição.md",
                   "Terços · Simetria · Espaço negativo · Linhas de condução"),
    "Generos_universos": ("02_Catalogo_Visual/Generos_e_Universos/MOC - Generos_e_Universos.md",
                          "Cyberpunk · Fantasia · Horror · Liminal"),
    "Movimentos": ("02_Catalogo_Visual/Movimentos/MOC - Movimentos.md",
                   "Realismo · Impressionismo · Expressionismo · Surrealismo"),
    "Textura_materiais": ("01_Fundamentos_Teoricos/Textura e Materialidade/MOC - Textura e Materialidade.md",
                          "Metal · Vidro · Concreto · Ouro"),
    "Midias_pintura_desenho": ("02_Catalogo_Visual/Midias_e_Suportes/MOC - Midias e Suportes.md",
                               "Óleo · Aquarela · Grafite · Impressão"),
    "Gravura_impressao": ("02_Catalogo_Visual/Midias_e_Suportes/Gravura_e_Impressão/MOC - Gravura_e_Impressão.md",
                          "Xilogravura · Água-forte · Risografia · Litografia"),
    "Desenho_tinta": ("02_Catalogo_Visual/Midias_e_Suportes/Desenho/MOC - Desenho.md",
                      "Nanquim · Carvão · Marcador · Sumi-e"),
    "Digital_3D": ("02_Catalogo_Visual/Midias_e_Suportes/Midias Mistas e Digitais/MOC - Midias Mistas e Digitais.md",
                   "Render 3D · Pixel art · Low-poly · Cel shading · PBR"),
    "Fotografia_comparativa": ("02_Catalogo_Visual/Fotografia/MOC - Fotografia.md",
                               "Filme · Lomografia · Polaroid · Street"),
    "Fotos_retrato": ("02_Catalogo_Visual/Fotografia/MOC - Fotografia.md",
                      "Estúdio · Candid · Macro · Infravermelho"),
    "Midia_suporte": ("02_Catalogo_Visual/Midias_e_Suportes/MOC - Midias e Suportes.md",
                      "35mm · Lomografia · Polaroid · Street"),
    "Estilo_suporte": ("02_Catalogo_Visual/Midias_e_Suportes/MOC - Midias e Suportes.md",
                       "Estúdio · Macro · Longa exposição · Infravermelho"),
    "Atmosfera_NOIR": ("02_Catalogo_Visual/Cor_e_Grading/MOC - Cor e Grading.md",
                       "Noir · Bleach bypass · Day-for-night · Matte painting"),
    "Atmosfera_efeitos": ("02_Catalogo_Visual/Arquitetura_Cenario_e_Personagem/MOC - Arquitetura_Cenario_e_Personagem.md",
                          "Névoa · Chuva · Neve · Glitch"),
    "Efeitos_atmosfericos": ("02_Catalogo_Visual/Arquitetura_Cenario_e_Personagem/MOC - Arquitetura_Cenario_e_Personagem.md",
                             "Névoa · Chuva · Brilho · Glitch"),
    "Efeitos_pos-producao": ("02_Catalogo_Visual/Midias_e_Suportes/Artefatos_e_Imperfeicoes_Analogicas/MOC - Artefatos_e_Imperfeicoes_Analogicas.md",
                    "Brilho · Meio-tom · Scanline · Vaporwave"),
    "Dicionario_tecnico": ("01_Fundamentos_Teoricos/Óptica & Lentes/MOC - Óptica & Lentes.md",
                           "Bokeh · Grão · Vinheta · Aberração cromática"),
    "Fundamentos_tecnicos": ("01_Fundamentos_Teoricos/Densidade Visual/MOC - Densidade Visual.md",
                             "Minimalismo · Equilíbrio · Riqueza · Exagero"),
    "Artistas_estudios": ("02_Catalogo_Visual/Assinaturas_Autorais/MOC - Assinaturas_Autorais.md",
                          "Frazetta · Giger · Klimt · Hokusai"),
    "Concept_ilustracao": ("02_Catalogo_Visual/Assinaturas_Autorais/Ilustradores_e_Concept_Artists/MOC - Ilustradores_e_Concept_Artists.md",
                           "Personagem · Ambiente · Prop · Criatura"),
    "Templates": ("06_Templates/MOC - 06_Templates.md",
                  "Retrato · Sci-fi · Personagem · Objeto"),
}

SECAO = "## 🖼️ Prancha comparativa"


def grupo(nome: str, chaves: list[str]) -> str | None:
    """Prefixo mais longo do nome que exista no mapa de destinos."""
    stem = re.sub(r"\s*\(\d+\)$", "", Path(nome).stem)
    partes = stem.split("_")
    melhor = None
    for i in range(1, len(partes) + 1):
        cand = "_".join(partes[:i])
        for chave in chaves:
            if cand.lower() == chave.lower():
                melhor = chave
    return melhor


def inserir(moc: Path, arquivo: str, rodape: str) -> bool:
    texto = moc.read_text(encoding="utf-8", errors="replace")
    if f"[[{arquivo}]]" in texto:
        return False
    bloco = f"\n{SECAO}\n\n![[{arquivo}]]\n\n*{rodape}*\n"
    # insere antes da primeira secao de relacoes/rodape, ou no fim
    for marca in ("## 🔗", "## ⚙️", "## 📌"):
        i = texto.find(marca)
        if i != -1:
            texto = texto[:i] + bloco.lstrip("\n") + "\n" + texto[i:]
            moc.write_text(texto, encoding="utf-8")
            return True
    moc.write_text(texto.rstrip("\n") + "\n" + bloco, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    usadas, orfas = 0, []
    for p in sorted(PRANCHAS.glob("*")):
        if not p.is_file():
            continue
        g = grupo(p.name, list(MAPEAMENTO))
        alvo = MAPEAMENTO.get(g)
        if not alvo:
            orfas.append(p.name)
            continue
        moc = ROOT / alvo[0]
        if not moc.exists():
            print(f"  ! MOC ausente: {alvo[0]}")
            orfas.append(p.name)
            continue
        ok = inserir(moc, p.name, alvo[1])
        if ok:
            usadas += 1
            print(f"  {p.name:52s} -> {moc.name}")
        else:
            print(f"  = ja estava: {p.name} -> {moc.name}")

    print(f"\n{usadas} prancha(s) encaminhada(s), {len(orfas) } sem destino.")
    if orfas:
        print("  sem destino: " + ", ".join(orfas))
    print("APLICADO." if args.apply else "Dry-run. Use --apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
