#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera a apostila "EU NAVEGAREI - TOM: Am" no mesmo estilo visual da apostila
"VITORIA NO DESERTO" (teclado ilustrado, dedilhado 1-3-5 nas duas maos).

4 acordes apenas:  Am  ->  G  ->  F  ->  E
Mao esquerda: 1 - 3 - 5   |   Mao direita: 1 - 3 - 5

Uso:
    python3 scripts/gerar_apostila_eu_navegarei.py
"""

import os

from reportlab.lib.colors import Color, black, white
from reportlab.lib.pagesizes import landscape, A4
from reportlab.lib.utils import ImageReader
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAIDA = os.path.join(BASE, "EU NAVEGAREI - TOM Am - 4 ACORDES (TECLADO).pdf")
IMG_MAO = os.path.join(BASE, "assets", "mao.png")

VERMELHO = Color(0.90, 0.09, 0.15)
CINZA_LINHA = Color(0.35, 0.35, 0.35)
CINZA_CLARO = Color(0.93, 0.93, 0.93)

# ---------------------------------------------------------------- fontes
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
pdfmetrics.registerFont(TTFont("DejaVu", os.path.join(FONT_DIR, "DejaVuSans.ttf")))
pdfmetrics.registerFont(TTFont("DejaVu-Bold", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf")))
BOLD = "DejaVu-Bold"
REG = "DejaVu"

# ---------------------------------------------------------------- teclado
# 21 teclas brancas: 3 oitavas  C D E F G A B
NOTAS = ["C", "D", "E", "F", "G", "A", "B"]
SUSTENIDOS = {0: "C#", 1: "D#", 3: "F#", 4: "G#", 5: "A#"}   # preta depois da branca i
N_BRANCAS = 21


def nome_branca(i):
    return NOTAS[i % 7]


class Acorde:
    """pos_*: lista de (branca, rotulo, ativo) ou ('b', branca, rotulo, ativo)."""

    def __init__(self, numero, cifra, nome_pt, pos_esq, pos_dir, notas_esq, notas_dir):
        self.numero = numero
        self.cifra = cifra
        self.nome_pt = nome_pt
        self.pos_esq = pos_esq
        self.pos_dir = pos_dir
        self.notas_esq = notas_esq
        self.notas_dir = notas_dir

    @property
    def titulo(self):
        return f"{self.numero}º ACORDE: {self.cifra} - {self.nome_pt}"


ACORDES = [
    Acorde(
        1, "Am", "LÁ MENOR",
        [(5, "1", True), (6, "2", False), (7, "b3", True), (8, "4", False), (9, "5", True)],
        [(12, "1", True), (13, "2", False), (14, "b3", True), (15, "4", False), (16, "5", True)],
        "A - C - E", "A - C - E",
    ),
    Acorde(
        2, "G", "SOL MAIOR",
        [(4, "1", True), (5, "2", False), (6, "3", True), (7, "4", False), (8, "5", True)],
        [(11, "1", True), (12, "2", False), (13, "3", True), (14, "4", False), (15, "5", True)],
        "G - B - D", "G - B - D",
    ),
    Acorde(
        3, "F", "FÁ MAIOR",
        [(3, "1", True), (4, "2", False), (5, "3", True), ("b", 5, "4", False), (7, "5", True)],
        [(10, "1", True), (11, "2", False), (12, "3", True), ("b", 12, "4", False), (14, "5", True)],
        "F - A - C", "F - A - C",
    ),
    Acorde(
        4, "E", "MI MAIOR",
        [(2, "1", True), ("b", 3, "2", False), ("b", 4, "3", True), (5, "4", False), (6, "5", True)],
        [(9, "1", True), ("b", 10, "2", False), ("b", 11, "3", True), (12, "4", False), (13, "5", True)],
        "E - G# - B", "E - G# - B",
    ),
]


# ---------------------------------------------------------------- helpers
def texto_central(c, x, y, txt, font, size, cor=black):
    c.setFont(font, size)
    c.setFillColor(cor)
    c.drawCentredString(x, y, txt)


def pill(c, cx, cy, txt, cheia):
    """Marcador E1/E3... (cheia, preta) ou D1/D3... (vazada)."""
    c.setFont(BOLD, 6.5)
    w = pdfmetrics.stringWidth(txt, BOLD, 6.5) + 10
    h = 11
    x, y = cx - w / 2, cy - h / 2
    c.setLineWidth(1)
    if cheia:
        c.setFillColor(black)
        c.setStrokeColor(black)
        c.roundRect(x, y, w, h, 3, stroke=1, fill=1)
        cor = white
    else:
        c.setFillColor(white)
        c.setStrokeColor(black)
        c.roundRect(x, y, w, h, 3, stroke=1, fill=1)
        cor = black
    c.setFillColor(cor)
    c.drawCentredString(cx, cy - 2.4, txt)


def circulo_dedo(c, cx, cy, rotulo, ativo):
    r = 8.0
    c.setLineWidth(1.1)
    if ativo:
        c.setFillColor(white)
        c.setStrokeColor(VERMELHO)
        c.circle(cx, cy, r, stroke=1, fill=1)
        cor_txt = VERMELHO
    else:
        c.setFillColor(black)
        c.setStrokeColor(black)
        c.circle(cx, cy, r, stroke=1, fill=1)
        cor_txt = white
    size = 7.6 if len(rotulo) > 1 else 8.4
    c.setFont(BOLD, size)
    c.setFillColor(cor_txt)
    c.drawCentredString(cx, cy - 2.9, rotulo)


def desenhar_teclado(c, x, y_base, acorde):
    ww = 366 / N_BRANCAS
    alt_branca = 88.0
    alt_preta = 38.0
    lar_preta = ww * 0.62
    y_topo = y_base + alt_branca
    y_preto_base = y_topo - alt_preta

    brancas_ativas = set()
    pretas_ativas = {}
    for pos in acorde.pos_esq + acorde.pos_dir:
        if pos[0] == "b":
            pretas_ativas[pos[1]] = True
        elif pos[2]:
            brancas_ativas.add(pos[0])

    # teclas brancas
    for i in range(N_BRANCAS):
        x0 = x + i * ww
        c.setFillColor(VERMELHO if i in brancas_ativas else white)
        c.setStrokeColor(CINZA_LINHA)
        c.setLineWidth(0.7)
        c.rect(x0, y_base, ww, alt_branca, stroke=1, fill=1)

    # nomes das brancas
    for i in range(N_BRANCAS):
        cor = white if i in brancas_ativas else Color(0.25, 0.25, 0.25)
        c.setFont(BOLD, 7)
        c.setFillColor(cor)
        c.drawCentredString(x + i * ww + ww / 2, y_base + 8, nome_branca(i))

    # teclas pretas
    for oitava in range(3):
        for i in (0, 1, 3, 4, 5):
            idx = oitava * 7 + i
            bx = x + idx * ww + ww - lar_preta / 2
            ativa = pretas_ativas.get(idx, False)
            c.setFillColor(VERMELHO if ativa else black)
            c.setStrokeColor(black if not ativa else VERMELHO)
            c.setLineWidth(0.7)
            c.rect(bx, y_preto_base, lar_preta, alt_preta, stroke=1, fill=1)
            # etiqueta da nota
            c.setFont(BOLD, 5.6)
            c.setFillColor(white)
            c.drawCentredString(bx + lar_preta / 2, y_topo - 9, SUSTENIDOS[i])
            # tracinho
            c.setStrokeColor(white)
            c.setLineWidth(1)
            c.line(bx + lar_preta / 2 - 3.4, y_preto_base + 8,
                   bx + lar_preta / 2 + 3.4, y_preto_base + 8)

    # dedilhado
    y_dedos = y_preto_base - 13
    for pos in acorde.pos_esq + acorde.pos_dir:
        if pos[0] == "b":
            _, branca, rotulo, ativo = pos
            cx = x + branca * ww + ww
            cy = y_preto_base + 12
            c.setFillColor(white)
            c.setStrokeColor(VERMELHO if ativo else black)
            c.setLineWidth(1)
            c.circle(cx, cy, 7.2, stroke=1, fill=1)
            size = 7.4 if len(rotulo) > 1 else 8.0
            c.setFont(BOLD, size)
            c.setFillColor(VERMELHO if ativo else black)
            c.drawCentredString(cx, cy - 2.7, rotulo)
        else:
            branca, rotulo, ativo = pos
            circulo_dedo(c, x + branca * ww + ww / 2, y_dedos, rotulo, ativo)

    # marcadores E / D
    y_marca = y_base - 11
    for pos in acorde.pos_esq:
        if pos[0] == "b":
            _, branca, rotulo, ativo = pos
            if ativo:
                pill(c, x + branca * ww + ww, y_marca, "E" + rotulo, True)
        elif pos[2]:
            pill(c, x + pos[0] * ww + ww / 2, y_marca, "E" + pos[1], True)
    for pos in acorde.pos_dir:
        if pos[0] == "b":
            _, branca, rotulo, ativo = pos
            if ativo:
                pill(c, x + branca * ww + ww, y_marca, "D" + rotulo, False)
        elif pos[2]:
            pill(c, x + pos[0] * ww + ww / 2, y_marca, "D" + pos[1], False)


def card_acorde(c, x, y, w, h, acorde):
    c.setLineWidth(3)
    c.setStrokeColor(black)
    c.setFillColor(white)
    c.rect(x, y, w, h, stroke=1, fill=1)

    c.setFont(BOLD, 16.5)
    c.setFillColor(black)
    largura = pdfmetrics.stringWidth(acorde.titulo, BOLD, 16.5)
    size = min(16.5, 16.5 * (w - 34) / max(largura, 1))
    c.setFont(BOLD, size)
    c.drawString(x + 17, y + h - 24, acorde.titulo)

    sub = "AS DUAS MÃOS JUNTAS   •   MÃO ESQUERDA: 1 - 3 - 5   •   MÃO DIREITA: 1 - 3 - 5"
    tam = 7.0
    while pdfmetrics.stringWidth(sub, BOLD, tam) > w - 34 and tam > 5:
        tam -= 0.2
    c.setFont(BOLD, tam)
    c.setFillColor(VERMELHO)
    c.drawString(x + 17, y + h - 37, sub)

    desenhar_teclado(c, x + 18, y + 52, acorde)

    # rodapé: notas
    yy = y + 16
    c.setFont(BOLD, 8.4)
    c.setFillColor(VERMELHO)
    c.drawString(x + 18, yy, "MÃO ESQUERDA:")
    x1 = x + 18 + pdfmetrics.stringWidth("MÃO ESQUERDA:", BOLD, 8.4) + 4
    c.setFillColor(black)
    c.drawString(x1, yy, acorde.notas_esq)
    x2 = x1 + pdfmetrics.stringWidth(acorde.notas_esq, BOLD, 8.4) + 22
    c.setFillColor(VERMELHO)
    c.drawString(x2, yy, "MÃO DIREITA:")
    x3 = x2 + pdfmetrics.stringWidth("MÃO DIREITA:", BOLD, 8.4) + 4
    c.setFillColor(black)
    c.drawString(x3, yy, acorde.notas_dir)


def cabecalho(c, subtitulo):
    texto_central(c, 421, 574,
                  "EU NAVEGAREI   •   TOM: Am   •   " + subtitulo,
                  BOLD, 12.5)
    c.setLineWidth(2)
    c.setStrokeColor(black)
    c.line(12, 566, 830, 566)


def rodape_maos(c, y, h):
    """Faixa inferior com as fotos das mãos e a legenda dos dedos."""
    c.setLineWidth(3)
    c.setStrokeColor(black)
    c.setFillColor(white)
    c.rect(12, y, 818, h, stroke=1, fill=1)

    # mão esquerda (espelhada) e mão direita
    img = ImageReader(IMG_MAO)
    larg_img = 92
    alt_img = larg_img * 290 / 307

    c.saveState()
    c.translate(30 + larg_img, y + 16)
    c.scale(-1, 1)
    c.drawImage(img, 0, 0, width=larg_img, height=alt_img, mask="auto")
    c.restoreState()

    c.drawImage(img, 818 + 12 - 30 - larg_img, y + 16,
                width=larg_img, height=alt_img, mask="auto")

    cx = 421
    texto_central(c, cx, y + h - 20, "COMO TOCAR: AS DUAS MÃOS FAZEM 1 - 3 - 5", BOLD, 12)
    texto_central(c, cx, y + h - 37,
                  "Cada acorde é formado pela 1ª, 3ª e 5ª nota (tônica, terça e quinta).",
                  REG, 8.6, Color(0.28, 0.28, 0.28))

    linhas = [
        ("MÃO ESQUERDA:", "dedo 1 (mínimo)  -  dedo 3 (médio)  -  dedo 5 (polegar)"),
        ("MÃO DIREITA:", "dedo 1 (polegar)  -  dedo 3 (médio)  -  dedo 5 (mínimo)"),
    ]
    yy = y + h - 58
    for titulo, corpo in linhas:
        c.setFont(BOLD, 9.2)
        c.setFillColor(VERMELHO)
        c.drawString(150, yy, titulo)
        c.setFont(REG, 9.2)
        c.setFillColor(black)
        c.drawString(150 + pdfmetrics.stringWidth(titulo, BOLD, 9.2) + 6, yy, corpo)
        yy -= 16

    c.setFont(BOLD, 8.8)
    c.setFillColor(black)
    c.drawString(150, yy, "Toque as duas mãos ao mesmo tempo, devagar, e só troque de acorde quando a troca sair limpa.")
    c.setFont(BOLD, 8.8)
    c.setFillColor(VERMELHO)
    c.drawString(150, yy - 15, "ORDEM:  Am  →  G  →  F  →  E")


# ---------------------------------------------------------------- páginas
def pagina_1(c):
    cabecalho(c, "4 ACORDES: Am → G → F → E   •   MÃO ESQUERDA 1-3-5 / MÃO DIREITA 1-3-5")

    w = (842 - 2 * 12 - 14) / 2
    h = 185
    card_acorde(c, 12, 350, w, h, ACORDES[0])
    card_acorde(c, 12 + w + 14, 350, w, h, ACORDES[1])
    card_acorde(c, 12, 152, w, h, ACORDES[2])
    card_acorde(c, 12 + w + 14, 152, w, h, ACORDES[3])
    rodape_maos(c, 10, 130)
    c.showPage()


def cartao(c, x, y, w, h):
    c.setLineWidth(3)
    c.setStrokeColor(black)
    c.setFillColor(white)
    c.rect(x, y, w, h, stroke=1, fill=1)


def linha_separadora(c, x1, x2, y):
    c.setStrokeColor(Color(0.84, 0.84, 0.84))
    c.setLineWidth(0.7)
    c.line(x1, y, x2, y)


def secao_cifra(c, x, y, rotulo, linhas, largura):
    """Escreve 'rotulo' + pares acorde/letra. Retorna o y final."""
    c.setFont(BOLD, 9.5)
    c.setFillColor(VERMELHO)
    c.drawString(x, y, rotulo)
    y -= 14
    for segs in linhas:
        xx = x + 14
        posicoes = []
        for cifra, letra in segs:
            posicoes.append((xx, cifra))
            xx += pdfmetrics.stringWidth(letra, REG, 9.3)
        for px, cifra in posicoes:
            c.setFont(BOLD, 8.8)
            c.setFillColor(VERMELHO)
            c.drawString(px, y, cifra)
        y -= 12
        xx = x + 14
        c.setFont(REG, 9.3)
        c.setFillColor(black)
        for cifra, letra in segs:
            c.drawString(xx, y, letra)
            xx += pdfmetrics.stringWidth(letra, REG, 9.3)
        y -= 15
    return y - 8


def pagina_2(c):
    cabecalho(c, "ONDE ENTRA CADA ACORDE   •   CIFRA COM A LETRA")

    # --- ordem dos acordes ------------------------------------
    x, y, w, h = 12, 420, 818, 138
    cartao(c, x, y, w, h)
    texto_central(c, 421, y + h - 27, "ONDE ENTRA CADA ACORDE", BOLD, 16.5)

    linhas = [
        ("INTRO", "Am  →  G  →  F  →  E"),
        ("VERSO", "Am  →  G  →  F  →  E    (repete 2x)"),
        ("REFRÃO", "Am  →  G  →  F  →  E    (repete 2x)"),
        ("VERSO 2", "Am  →  G  →  F  →  E"),
        ("FINAL", "Am  →  G  →  F  →  E  →  Am"),
    ]
    yy = y + h - 47
    for titulo, seq in linhas:
        c.setFont(BOLD, 10.5)
        c.setFillColor(VERMELHO)
        c.drawString(34, yy, titulo)
        c.setFillColor(black)
        c.drawString(180, yy, seq)
        linha_separadora(c, 34, 808, yy - 5)
        yy -= 18.5

    # --- cifra -------------------------------------------------
    x, y, w, h = 12, 20, 818, 388
    cartao(c, x, y, w, h)
    texto_central(c, 421, y + h - 25, "EU NAVEGAREI   •   CIFRA EM Am  (4 ACORDES)", BOLD, 14)

    col_esq = 34
    col_dir = 448

    yy = y + h - 52
    yy = secao_cifra(c, col_esq, yy, "VERSO", [
        [("Am", "Eu navegarei no oceano do "), ("G", "Espírito")],
        [("F", "E ali adorarei ao Deus do meu "), ("E", "amor")],
        [("Am", "Eu navegarei no oceano do "), ("G", "Espírito")],
        [("F", "E ali adorarei ao Deus do meu "), ("E", "amor")],
    ], 400)

    secao_cifra(c, col_esq, yy, "REFRÃO", [
        [("Am", "Espírito, Espírito, que desce como "), ("G", "fogo")],
        [("F", "Vem como em pentecostes e enche-me de "), ("E", "novo")],
        [("Am", "Espírito, Espírito, que desce como "), ("G", "fogo")],
        [("F", "Vem como em pentecostes e enche-me de "), ("E", "novo")],
    ], 400)

    yy = y + h - 52
    yy = secao_cifra(c, col_dir, yy, "VERSO 2", [
        [("Am", "Eu adorarei ao Deus da minha "), ("G", "vida")],
        [("F", "Que me compreendeu sem nenhuma "), ("E", "explicação")],
    ], 380)

    yy = secao_cifra(c, col_dir, yy, "FINAL", [
        [("Am", "Finaliza em Am (segura 4 tempos e volta ao início)")],
    ], 380)

    # caixa de lembrete na coluna da direita
    bx, by, bw, bh = col_dir, y + 34, 376, 104
    c.setLineWidth(2.2)
    c.setStrokeColor(VERMELHO)
    c.setFillColor(Color(1, 0.96, 0.96))
    c.rect(bx, by, bw, bh, stroke=1, fill=1)
    c.setFont(BOLD, 10.5)
    c.setFillColor(VERMELHO)
    c.drawString(bx + 14, by + bh - 22, "LEMBRETE")
    textos = [
        "As duas mãos fazem 1 - 3 - 5.",
        "A troca de acorde cai sempre no 1º tempo.",
        "Se a troca travar, repita o compasso devagar.",
    ]
    ty = by + bh - 40
    for t in textos:
        c.setFont(REG, 9.2)
        c.setFillColor(black)
        c.drawString(bx + 14, ty, "•  " + t)
        ty -= 16

    c.showPage()


def pagina_3(c):
    cabecalho(c, "AS NOTAS DE CADA ACORDE   •   DICAS DE ESTUDO")

    w = (842 - 24 - 14) / 2

    # --- notas de cada acorde ---------------------------------
    x, y, w1, h = 12, 372, w, 176
    cartao(c, x, y, w1, h)
    c.setFont(BOLD, 14)
    c.setFillColor(black)
    c.drawString(x + 18, y + h - 26, "AS NOTAS DE CADA ACORDE")
    dados = [
        ("Am", "LÁ MENOR", "A - C - E"),
        ("G", "SOL MAIOR", "G - B - D"),
        ("F", "FÁ MAIOR", "F - A - C"),
        ("E", "MI MAIOR", "E - G# - B"),
    ]
    yy = y + h - 52
    for i, (cifra, nome, notas) in enumerate(dados, start=1):
        c.setFont(BOLD, 10.5)
        c.setFillColor(VERMELHO)
        c.drawString(x + 18, yy, f"{i}º")
        c.setFillColor(black)
        c.drawString(x + 52, yy, f"{cifra}  ({nome})")
        c.setFont(BOLD, 10.5)
        c.setFillColor(VERMELHO)
        c.drawRightString(x + w1 - 20, yy, notas)
        yy -= 24

    # --- por que esses 4 acordes -------------------------------
    x, y, w2, h = 12 + w + 14, 372, w, 176
    cartao(c, x, y, w2, h)
    c.setFont(BOLD, 14)
    c.setFillColor(black)
    c.drawString(x + 18, y + h - 26, "POR QUE ESSES 4 ACORDES")
    itens = [
        "É a sequência mais usada em Am.",
        "Cada acorde usa só 3 notas por mão.",
        "Am e E são o “lar” da música.",
        "Dá para tocar a canção quase inteira.",
    ]
    yy = y + h - 52
    for t in itens:
        c.setFont(BOLD, 10)
        c.setFillColor(VERMELHO)
        c.drawString(x + 18, yy, "•")
        c.setFont(REG, 10)
        c.setFillColor(black)
        c.drawString(x + 30, yy, t)
        yy -= 24

    # --- dicas -------------------------------------------------
    x, y, w3, h3 = 12, 20, 818, 334
    cartao(c, x, y, w3, h3)
    c.setFont(BOLD, 15)
    c.setFillColor(black)
    c.drawString(x + 20, y + h3 - 28, "DICAS PARA TOCAR SEM ERRAR")

    dicas = [
        "Mão esquerda na região grave e mão direita uma oitava acima, as duas em 1 - 3 - 5.",
        "Estude um acorde por vez: 4 tempos em cada um, contando em voz alta (1, 2, 3, 4).",
        "Junte dois de cada vez: Am → G (10x), depois G → F, depois F → E.",
        "Só então faça o ciclo completo: Am → G → F → E, devagar e no mesmo tempo.",
        "A troca de acorde cai no tempo forte (1º tempo do compasso).",
        "Cante a letra junto: é o que mostra a hora exata de cada troca.",
    ]
    yy = y + h3 - 58
    for i, t in enumerate(dicas, start=1):
        c.setFont(BOLD, 10.5)
        c.setFillColor(VERMELHO)
        c.drawString(x + 22, yy, f"{i}.")
        c.setFont(REG, 10.5)
        c.setFillColor(black)
        c.drawString(x + 44, yy, t)
        yy -= 32

    c.setLineWidth(2)
    c.setStrokeColor(VERMELHO)
    c.setFillColor(Color(1, 0.96, 0.96))
    c.rect(x + 20, y + 34, w3 - 40, 48, stroke=1, fill=1)
    c.setFont(BOLD, 12)
    c.setFillColor(VERMELHO)
    c.drawString(x + 38, y + 60, "LEMBRETE:")
    c.setFillColor(black)
    c.drawString(x + 140, y + 60, "Am  →  G  →  F  →  E")
    c.setFont(REG, 9)
    c.setFillColor(Color(0.3, 0.3, 0.3))
    c.drawString(x + 38, y + 44, "Mão esquerda 1 - 3 - 5   •   Mão direita 1 - 3 - 5   •   as duas mãos juntas")

    c.showPage()


def main():
    c = canvas.Canvas(SAIDA, pagesize=landscape(A4))
    c.setTitle("Eu Navegarei - Tom Am - 4 acordes")
    c.setAuthor("Apostila de Teclado")
    pagina_1(c)
    pagina_2(c)
    pagina_3(c)
    c.save()
    print("Gerado:", SAIDA)


if __name__ == "__main__":
    main()
