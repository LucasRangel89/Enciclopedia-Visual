#!/usr/bin/env python3
"""
Roteia o acervo de "SNAP INSTA" (47 imagens de referencia baixadas do
Instagram) para as notas que esperam uma imagem.

Cada entrada de MAPA eh:
    origem (relativa a "SNAP INSTA/") -> (nome final, legenda, nota)

O nome final corresponde ao embed que a nota ja declara, so que com .jpg
(os arquivos originais sao JPEG). O script reescreve o bloco
"## Exemplo Visual" da nota e acerta o tem_imagem do frontmatter.

Uso:
    python3 scripts/rotear_snapinsta.py            # dry-run
    python3 scripts/rotear_snapinsta.py --apply
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "SNAP INSTA"
DEST = ROOT / "08_Imagens_Geradas" / "Referencias_SnapInsta"

G = "02_Catalogo_Visual"
IL = f"{G}/Assinaturas_Autorais/Ilustradores_e_Concept_Artists"
LUZ = f"{G}/Iluminacao_Avancada"
COR = f"{G}/Cor_e_Grading"
NAR = f"{G}/Narrativa_Visual_e_Storytelling"
FAM = f"{G}/Familias_de_Linguagem_Visual"
FOT = f"{G}/Fotografia"
GEN = f"{G}/Generos_e_Universos"
MID = f"{G}/Midias_e_Suportes"
MOV = f"{G}/Movimentos"
GRA = f"{MID}/Gravura_e_Impressão"
MIX = f"{MID}/Midias Mistas e Digitais"
JOG = f"{G}/Videogames_Linguagem_Visual/Concept_Art_Games_vs_Cinema"

MAPA = {
    # --- gravura em linha -------------------------------------------------
    "SnapInsta.to_654024721_17940694845157959_6300460249014702582_n.jpg": (
        "agua_forte.jpg",
        "Agua-forte: coruja em hachura densa, sombra construida por acumulo de linha.",
        f"{GRA}/Água-forte.md"),
    "SnapInsta.to_656723666_17994042251931330_4860894367331779320_n.jpg": (
        "xilogravura.jpg",
        "Xilogravura: collie em traço gravado, contorno expressivo e areas de sombra riscadas.",
        f"{GRA}/Xilogravura.md"),
    # --- assinaturas autorais ---------------------------------------------
    "snapinsta.com.br-69eac79275fb9.jpg": (
        "klimt.jpg",
        "Klimt: mandala ornamental sobre cidade, ouro, vermelho e teal em padrao hipnotico.",
        f"{IL}/Gustav Klimt.md"),
    "snapinsta.com.br-69eac88749f0f.jpg": (
        "frazetta.jpg",
        "Frazetta: rei guerreiro de armadura ornada, volume pintado e luz quente de fundo.",
        f"{IL}/Frank Frazetta.md"),
    "snapinsta.com.br-69eac798df63c.jpg": (
        "giger.jpg",
        "Giger: olho biomecanico ramificado sobre paisagem infernal, horror organico.",
        f"{IL}/H.R. Giger.md"),
    "snapinsta.com.br-69eac8b9f3c4f.jpg": (
        "toriyama.jpg",
        "Toriyama: criatura peluda de traco arredondado, expressao caricatural.",
        f"{IL}/Akira Toriyama.md"),
    "SnapInsta.to_658948115_17904760134428932_4110338220820059667_n.jpg": (
        "haring.jpg",
        "Haring: gato guerreiro em circulo vermelho, linha grafica plana e raios irradiantes.",
        f"{IL}/Keith Haring.md"),
    # --- iluminacao avancada ----------------------------------------------
    "snapinsta.com.br-69eac7631b3be.jpg": (
        "low_key.jpg",
        "Low-key: alquimista escrevendo, sombra dominante e luz de vela como fonte motivada.",
        f"{LUZ}/Low-Key Lighting (Iluminação Baixa-Chave).md"),
    "snapinsta.com.br-69eac71dd27a4.jpg": (
        "rim_light.jpg",
        "Rim light: Scorpion recortado por contorno dourado sobre fundo negro.",
        f"{LUZ}/Rim Light - Luz de Contorno.md"),
    "snapinsta.com.br-69eac7f9dfb9d.jpg": (
        "silhueta.jpg",
        "Silhueta: guerreiro de costas contra explosao de fogo, figura reduzida a forma escura.",
        f"{LUZ}/Silhueta (Silhouette Lighting).md"),
    "snapinsta.com.br-69eac88a334d4.jpg": (
        "split_lighting.jpg",
        "Split lighting: perfil do anao partido ao meio por uma divisao clara de luz e sombra.",
        f"{LUZ}/Split Lighting (Iluminação Dividida).md"),
    # --- cor e grading -----------------------------------------------------
    "snapinsta.com.br-69eac7f2e466e.jpg": (
        "matrix_green.jpg",
        "Matrix green: criaturas na selva sob monocromia esverdeada e raios de luz.",
        f"{COR}/Matrix Green (Monocromia Esverdeada).md"),
    "SnapInsta.to_671151946_18124400101617903_7394942475648697149_n.jpg": (
        "teal_orange.jpg",
        "Teal and orange: cemiterio de navios ao poente, sombras azul-frias contra ceu laranja.",
        f"{COR}/Teal and Orange.md"),
    # --- narrativa visual --------------------------------------------------
    "snapinsta.com.br-69eac75f21634.jpg": (
        "ambiente_personagem.jpg",
        "Ambiente como personagem: o castelo e a encosta funcionam como segundo protagonista.",
        f"{NAR}/Ambiente como Personagem.md"),
    "snapinsta.com.br-69eac7ff2763e.jpg": (
        "momento_narrativo.jpg",
        "Momento narrativo: o instante depois da batalha, cadaveres como consequencia visivel.",
        f"{NAR}/O Momento Narrativo (Antes-Durante-Depois).md"),
    "snapinsta.com.br-69eac8b1e8917.jpg": (
        "prop_storytelling.jpg",
        "Prop storytelling: espada em primeiro plano, a gema vermelha carrega a historia do objeto.",
        f"{NAR}/Prop Storytelling.md"),
    "snapinsta.com.br-69eac7f61dd85.jpg": (
        "staging.jpg",
        "Staging: tres hobbits enfileirados contra o troll, leitura clara de planos e olhares.",
        f"{NAR}/Staging (Posicionamento Encenado).md"),
    # --- familias de linguagem visual --------------------------------------
    "snapinsta.com.br-69eac6d5486df.jpg": (
        "sonho_incongruencia.jpg",
        "Sonho e incongruencia: Jedi e droides em ambiente feudal japones, choque de imaginarios.",
        f"{FAM}/Sonho e Incongruência.md"),
    # --- fotografia --------------------------------------------------------
    "SnapInsta.to_651560555_17940261450157959_6268589195653260928_n.jpg": (
        "retrato_classico.jpg",
        "Retrato classico: busto frontal, luz difusa de estudio, fundo neutro.",
        f"{FOT}/Fotografia de Estúdio - Retrato Clássico.md"),
    # --- generos e universos -----------------------------------------------
    "snapinsta.com.br-69eac7f87a9ce.jpg": (
        "fantasia.jpg",
        "Fantasia: elfa guerreira de armadura ornada em floresta azul, high fantasy classica.",
        f"{GEN}/Fantasia.md"),
    "snapinsta.com.br-69eac7a29d4ec.jpg": (
        "horror.jpg",
        "Horror: figura cornuda sobre tabuleiro flutuante em mar de lava, escala opressiva.",
        f"{GEN}/Horror.md"),
    "SnapInsta.to_670418516_17944555863157959_50961591370456434_n.jpg": (
        "liminal.jpg",
        "Liminal: torres vermelhas na nevoa azul, estruturas sem funcao aparente e sem pessoas.",
        f"{GEN}/Liminal.md"),
    "SnapInsta.to_670248051_17944555866157959_8693342940203772223_n.jpg": (
        "pos_apocaliptico.jpg",
        "Pos-apocaliptico: vilas abandonadas sob ceu esverdeado, figuras diminutas na estrada.",
        f"{GEN}/Pós-Apocalíptico.md"),
    "snapinsta.com.br-69eac6d814aeb.jpg": (
        "scifi.jpg",
        "Sci-fi: samurai e wookiee armadurados em arquitetura oriental, ficcao cientifica hibrida.",
        f"{GEN}/Ficção Científica (Sci-fi).md"),
    # --- midias, suportes e concept art ------------------------------------
    "snapinsta.com.br-69eac756376db.jpg": (
        "ilustracao_editorial.jpg",
        "Ilustracao editorial: capa de revista com retrato carregado e tipografia display.",
        f"{MIX}/Ilustração Editorial.md"),
    "snapinsta.com.br-69eac7a65ad05.jpg": (
        "concept_art.jpg",
        "Concept art: olho cosmico sobre piramide, figura minuscula para dar escala.",
        f"{MIX}/Concept Art.md"),
    "snapinsta.com.br-69eac75a45297.jpg": (
        "concept_games.jpg",
        "Concept art de games: guerreiro de caveira gigante ao lado da crianca, exercito ao fundo.",
        f"{JOG}/Concept Art de Games vs. Cinema.md"),
    # --- movimentos artisticos ---------------------------------------------
    "SnapInsta.to_651560555_17940261450157959_6268589195653260928_n.jpg": (
        "hiper_realismo.jpg",
        "Hiper-realismo: mascara renderizada com precisao fotografica, pele e tecido sem falha.",
        f"{MOV}/Onda_02_Realismos/Hiper-realismo e Fotorrealismo.md"),
    "snapinsta.com.br-69eac7620e026.jpg": (
        "realismo_magico.jpg",
        "Realismo magico: hobbits e criatura rinoceronte tratados como cena cotidiana.",
        f"{MOV}/Onda_02_Realismos/Realismo Mágico.md"),
    "SnapInsta.to_673128604_18124400110617903_5944543820842510965_n.jpg": (
        "fauvismo.jpg",
        "Fauvismo: campo de espadas em vermelho e azul nao-naturalistas, cor como emocao.",
        f"{MOV}/Onda_04_Vanguardas_Sec_XV/Fauvismo.md"),
    "snapinsta.com.br-69eac71f9c89e.jpg": (
        "manga_anime.jpg",
        "Manga/anime: capa com personagem de olhos grandes, linhas de velocidade e hachura.",
        f"{MOV}/Onda_07_Tradicoes_Asiaticas/Manga Anime.md"),
}


def reescrever(nota: Path, arquivo: str, legenda: str) -> bool:
    """Troca o bloco de exemplo visual da nota pela referencia do acervo."""
    if not nota.exists():
        print(f"    ! nota ausente: {nota.relative_to(ROOT)}")
        return False
    texto = nota.read_text(encoding="utf-8", errors="replace")
    if arquivo in texto:
        return False

    bloco = ("## 🖼️ Exemplo Visual\n\n"
             "### Referência — Acervo SNAP INSTA\n"
             f"![[{arquivo}]]\n"
             f"* **Legenda:** {legenda}\n")

    # secao existente: do cabecalho ate o proximo "## " ou separador "---"
    m = re.search(r"^## 🖼️ Exemplo Visual[ \t]*$", texto, re.M)
    if m:
        fim = re.search(r"^(## |---[ \t]*$)", texto[m.end():], re.M)
        corte = m.end() + (fim.start() if fim else len(texto) - m.end())
        texto = texto[:m.start()] + bloco + "\n" + texto[corte:]
    else:
        ancora = re.search(r"^(## ⚙️|## 🔗|## 📌)", texto, re.M)
        if ancora:
            texto = texto[:ancora.start()] + bloco + "\n" + texto[ancora.start():]
        else:
            texto = texto.rstrip("\n") + "\n" + bloco

    if re.search(r"^tem_imagem:\s*false", texto, re.M):
        texto = re.sub(r"^tem_imagem:\s*false", "tem_imagem: true", texto, count=1, flags=re.M)

    nota.write_text(texto, encoding="utf-8")
    return True


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    args = ap.parse_args()

    movidos = ligados = 0
    for origem, (novo, legenda, nota_rel) in MAPA.items():
        src = SRC / origem
        if not src.exists():
            print(f"  ! origem ausente: {origem}")
            continue
        dst = DEST / novo
        print(f"  {origem[:52]:<54} -> {novo}")
        if args.apply:
            DEST.mkdir(parents=True, exist_ok=True)
            if not dst.exists():
                src.rename(dst)
            movidos += 1
            if reescrever(ROOT / nota_rel, novo, legenda):
                ligados += 1

    resto = len(list(SRC.glob("*.jpg"))) if SRC.exists() else 0
    print(f"\n{movidos} movida(s), {ligados} embed(s) reescrito(s), {resto} no acervo SNAP INSTA.")
    print("APLICADO." if args.apply else "Dry-run. Use --apply.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
