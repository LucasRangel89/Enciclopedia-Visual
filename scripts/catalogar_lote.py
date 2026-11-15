#!/usr/bin/env python3
"""
Cataloga o lote de imagens de nome opaco em attachments/.

Cada entrada de MAPA eh:
    origem (relativa a attachments/) -> (destino, rotulo, tipo, alvo)

O destino fica em 08_Imagens_Geradas/, que entra no build; attachments/
fica de fora. O alvo eh a nota ou MOC que recebe o embed.

Uso:
    python3 scripts/catalogar_lote.py            # dry-run
    python3 scripts/catalogar_lote.py --apply
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ATT = ROOT / "attachments"
GER = ROOT / "08_Imagens_Geradas"
PRANCHAS = GER / "Pranchas_Comparativas"

MAPA = {
    "NOVAS/ChatGPT Image 28 de abr. de 2026, 19_18_19.png": (
        "Iluminacao_DURA_SOFT_BACK_DIFFUSED.png",
        "Luz dura · Luz suave · Contraluz · Luz difundida de estudio",
        "plate", "01_Fundamentos_Teoricos/Luz/MOC - Luz.md"),
    "NOVAS/ChatGPT Image 28 de abr. de 2026, 19_18_21.png": (
        "Cor_saturacao_ALTA_DESSATURADA_PASTEL_DUOTONE.png",
        "Alta saturacao · Dessaturada · Pastel · Duotone (ciano + vermelho quente)",
        "plate", "01_Fundamentos_Teoricos/Cor/MOC - Cor.md"),
    "NOVAS/ChatGPT Image 28 de abr. de 2026, 19_18_24.png": (
        "Cor_paleta_QUENTE_FRIA_MONOCROMATICA_COMPLEMENTAR.png",
        "Paleta quente · Paleta fria · Monocromatica · Contraste complementar",
        "plate", "01_Fundamentos_Teoricos/Cor/MOC - Cor.md"),
    "NOVAS/ChatGPT Image 28 de abr. de 2026, 19_18_26.png": (
        "Generos_CYBERPUNK_SOLARPUNK_STEAMPUNK_BIOPUNK.png",
        "Cyberpunk · Solarpunk · Steampunk · Biopunk",
        "plate", "02_Catalogo_Visual/Generos_e_Universos/MOC - Generos_e_Universos.md"),
    "NOVAS/ChatGPT Image 28 de abr. de 2026, 19_18_29.png": (
        "Generos_fantasia_ALTA_ESCURA_URBANA_LIMINAL.png",
        "High fantasy · Dark fantasy · Urban fantasy · Liminal space",
        "plate", "02_Catalogo_Visual/Generos_e_Universos/MOC - Generos_e_Universos.md"),
    "NOVAS/ChatGPT Image 28 de abr. de 2026, 19_21_26 (1).png": (
        "Cineastas_ANDERSON_BURTON_VILLENEUVE_GHIBLI.png",
        "Wes Anderson · Tim Burton · Denis Villeneuve · Studio Ghibli (anos 90)",
        "plate",
        "02_Catalogo_Visual/Assinaturas_Autorais/Cineastas_e_Estudios/MOC - Cineastas_e_Estudios.md"),
    "NOVAS/Gemini_Generated_Image_1ipv461ipv461ipv.png": (
        "ukiyo_e.png", "Ukiyo-e — referencia de movimento",
        "single", "02_Catalogo_Visual/Movimentos/Onda_07_Tradicoes_Asiaticas/Ukiyo-e.md"),
    "NOVAS/Gemini_Generated_Image_s4sgk6s4sgk6s4sg.png": (
        "romantismo.png", "Romantismo — referencia de movimento",
        "single", "02_Catalogo_Visual/Movimentos/Onda_01_Pre_Moderna/Romantismo.md"),
    "NOVAS/Gemini_Generated_Image_6r111f6r111f6r11.png": (
        "pop_art.png", "Pop Art — referencia de movimento",
        "single", "02_Catalogo_Visual/Movimentos/Onda_06_Pop_Conceito_e_Rua/Pop Art.md"),
    "NOVAS/Gemini_Generated_Image_sxow33sxow33sxow.png": (
        "minimalismo_densidade.png", "Minimalismo como densidade visual",
        "single", "01_Fundamentos_Teoricos/Densidade Visual/Minimalismo (Densidade Visual).md"),
}


def inserir(alvo: Path, arquivo: str, rotulo: str) -> bool:
    if not alvo.exists():
        print(f"    ! alvo ausente: {alvo.relative_to(ROOT)}")
        return False
    texto = alvo.read_text(encoding="utf-8", errors="replace")
    if f"[[{arquivo}]]" in texto:
        return False
    bloco = f"## Exemplo Visual\n\n![[{arquivo}]]\n\n*{rotulo}*\n"
    for marca in ("## Relacoes", "## Prompt", "## Referencia", "## Exemplo"):
        i = texto.find(marca)
        if i != -1:
            texto = texto[:i] + bloco + "\n" + texto[i:]
            alvo.write_text(texto, encoding="utf-8")
            return True
    alvo.write_text(texto.rstrip("\n") + "\n" + bloco, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    movidos = ligados = 0
    for origem, (novo, rotulo, tipo, alvo_rel) in MAPA.items():
        src = ATT / origem
        dst = PRANCHAS / novo if tipo == "plate" else GER / novo
        if not src.exists():
            print(f"  ! origem ausente: {origem}")
            continue
        print(f"  {origem}")
        print(f"      -> {dst.relative_to(ROOT)}")
        print(f"      -> {alvo_rel}")
        if args.apply:
            dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.exists():
                src.rename(dst)
            movidos += 1
            if inserir(ROOT / alvo_rel, novo, rotulo):
                ligados += 1

    print(f"\n{movidos} movido(s), {ligados} embed(s) inserido(s).")
    print("APLICADO." if args.apply else "Dry-run. Use --apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
