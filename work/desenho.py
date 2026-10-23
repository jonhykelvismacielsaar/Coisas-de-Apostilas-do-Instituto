# -*- coding: utf-8 -*-
"""Desenho do PDF: primitivas gráficas, teclado e painéis."""

import os
import math
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, HexColor, white, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from teoria import (KEYS, MODES, CHORD_TYPES, FINGER_NAMES, build_chord,
                    build_scale, chord_symbol, chord_symbol_both,
                    chord_description, relative_major, voicing,
                    fingering_text, fingering_seq)

BASE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(BASE, 'assets')

pdfmetrics.registerFont(TTFont('Anton', os.path.join(ASSETS, 'fonts', 'Anton-Regular.ttf')))
pdfmetrics.registerFont(TTFont('ABlack', os.path.join(ASSETS, 'fonts', 'ArchivoBlack-Regular.ttf')))

W, H = 844.456726, 597.842529            # paisagem A4
RED = HexColor('#EC1C23')
DARKRED = HexColor('#8E0F14')
YELLOW = HexColor('#FFF100')
BLACK = HexColor('#000000')
INK = HexColor('#111111')
GRAY = HexColor('#7A7A7A')
LGRAY = HexColor('#BDBDBD')
KEYWHITE = HexColor('#FCFCFC')
KEYEDGE = HexColor('#8C8C8C')
PAPER = white


# ------------------------------------------------------------------ primitivas
def Y(y):
    return H - y


def text(c, x, y, s, font='Anton', size=10, color=BLACK, align='l', track=0.0):
    """y = linha de base (coordenada de cima para baixo)."""
    c.setFillColor(color)
    c.setFont(font, size)
    if track:
        c.setCharSpace(track)
    wdt = pdfmetrics.stringWidth(s, font, size) + track * max(0, len(s) - 1)
    if align == 'c':
        x -= wdt / 2.0
    elif align == 'r':
        x -= wdt
    c.drawString(x, Y(y), s)
    if track:
        c.setCharSpace(0)
    return wdt


def fit(c, x, y, s, maxw, font='Anton', size=20, color=BLACK, align='c', minsize=5):
    while size > minsize and pdfmetrics.stringWidth(s, font, size) > maxw:
        size -= 0.4
    return text(c, x, y, s, font, size, color, align)


def fitl(c, x, y, s, maxw, font='Anton', size=10, color=BLACK, minsize=4.0):
    """Texto alinhado à esquerda que encolhe até caber em maxw."""
    while size > minsize and pdfmetrics.stringWidth(s, font, size) > maxw:
        size -= 0.2
    return text(c, x, y, s, font, size, color, 'l')


def rrect(c, x, y, w, h, fill=None, stroke=None, lw=1, r=3):
    c.saveState()
    if fill is not None:
        c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
    c.roundRect(x, Y(y + h), w, h, r, stroke=1 if stroke is not None else 0,
                fill=1 if fill is not None else 0)
    c.restoreState()


def rect(c, x, y, w, h, fill=None, stroke=None, lw=1):
    c.saveState()
    if fill is not None:
        c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
    c.rect(x, Y(y + h), w, h, stroke=1 if stroke is not None else 0,
           fill=1 if fill is not None else 0)
    c.restoreState()


def line(c, x1, y1, x2, y2, color=BLACK, lw=1, dash=None):
    c.saveState()
    c.setStrokeColor(color)
    c.setLineWidth(lw)
    if dash:
        c.setDash(dash)
    c.line(x1, Y(y1), x2, Y(y2))
    c.restoreState()


def circle(c, cx, cy, r, fill=None, stroke=None, lw=1):
    c.saveState()
    if fill is not None:
        c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke)
        c.setLineWidth(lw)
    c.circle(cx, Y(cy), r, stroke=1 if stroke is not None else 0,
             fill=1 if fill is not None else 0)
    c.restoreState()


def star(c, cx, cy, r, fill=RED, stroke=None):
    pts = []
    for i in range(24):
        ang = -math.pi / 2 + i * math.pi / 12
        rr = r if i % 2 == 0 else r * 0.62
        pts.append((cx + rr * math.cos(ang), Y(cy) + rr * math.sin(ang)))
    p = c.beginPath()
    p.moveTo(*pts[0])
    for pt in pts[1:]:
        p.lineTo(*pt)
    p.close()
    c.saveState()
    c.setFillColor(fill)
    if stroke is not None:
        c.setStrokeColor(stroke)
        c.setLineWidth(1)
    c.drawPath(p, stroke=1 if stroke is not None else 0, fill=1)
    c.restoreState()


def border(c):
    rect(c, 8, 8, W - 16, H - 16, None, BLACK, 2.4)
    rect(c, 13.5, 13.5, W - 27, H - 27, None, BLACK, 0.7)


# ------------------------------------------------------------------ teclado
PC_LETTER = [0, 0, 1, 1, 2, 3, 3, 4, 4, 5, 5, 6]      # pc -> índice da branca
PC_BLACK = [False, True, False, True, False, False, True, False, True, False, True, False]
N_WHITE = 21


def pc_white_index(pc):
    return PC_LETTER[pc]


class Keys(object):
    """Teclado de 3 oitavas (C..B, 21 teclas brancas) desenhado em vetor."""

    def __init__(self, x, y, w, h, label_size=None):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.wk = w / float(N_WHITE)
        self.bw = self.wk * 0.60
        self.bh = h * 0.62
        self.lab = label_size or max(5.0, min(9.0, self.wk * 0.52))

    # posição horizontal -------------------------------------------------
    def white_x(self, idx):
        return self.x + idx * self.wk

    def key_center(self, pitch):
        oct_, pc = divmod(pitch, 12)
        if PC_BLACK[pc]:
            before = pc - 1
            return self.x + (oct_ * 7 + PC_LETTER[before] + 1) * self.wk
        return self.x + (oct_ * 7 + PC_LETTER[pc] + 0.5) * self.wk

    def key_rect(self, pitch):
        """(x, y, w, h) da tecla, em coordenadas de cima para baixo."""
        oct_, pc = divmod(pitch, 12)
        if PC_BLACK[pc]:
            cx = self.key_center(pitch)
            return (cx - self.bw / 2.0, self.y, self.bw, self.bh)
        idx = oct_ * 7 + PC_LETTER[pc]
        return (self.x + idx * self.wk, self.y, self.wk, self.h)

    # desenho ------------------------------------------------------------
    def draw(self, c, highlights=None, degrees=None, show_labels=True):
        """highlights: {pitch: 'red'} ; degrees: {pitch: (label, is_char)}"""
        highlights = highlights or {}
        degrees = degrees or {}
        # teclas brancas
        for i in range(N_WHITE):
            x = self.white_x(i)
            red = False
            for pitch, mode in highlights.items():
                if mode == 'white' and self._white_index(pitch) == i:
                    red = True
            rect(c, x, self.y, self.wk, self.h, RED if red else KEYWHITE,
                 KEYEDGE, 0.55)
            # brilho superior
            rect(c, x + 0.6, self.y + 0.6, self.wk - 1.2, self.h * 0.02,
                 HexColor('#FFFFFF') if not red else RED, None)
        # teclas pretas
        for oct_ in range(3):
            for pc in (1, 3, 6, 8, 10):
                x = self.x + (oct_ * 7 + PC_LETTER[pc - 1] + 1) * self.wk - self.bw / 2.0
                red = False
                for pitch, mode in highlights.items():
                    if mode == 'black' and pitch == oct_ * 12 + pc:
                        red = True
                rect(c, x, self.y, self.bw, self.bh, DARKRED if red else INK)

        # rótulos
        if show_labels:
            for i in range(N_WHITE):
                letter = 'CDEFGAB'[i % 7]
                text(c, self.white_x(i) + self.wk / 2.0,
                     self.y + self.h - self.lab * 0.55, letter, 'Helvetica',
                     self.lab, HexColor('#3D3D3D'), 'c')
            for oct_ in range(3):
                for pc in (1, 3, 6, 8, 10):
                    nm = {1: 'C#', 3: 'D#', 6: 'F#', 8: 'G#', 10: 'A#'}[pc]
                    cx = self.x + (oct_ * 7 + PC_LETTER[pc - 1] + 1) * self.wk
                    text(c, cx, self.y + self.lab * 1.10, nm, 'Helvetica',
                         max(4.0, self.lab * 0.70), HexColor('#E8E8E8'), 'c')
        # graus
        for pitch, (lab, is_char) in degrees.items():
            oct_, pc = divmod(pitch, 12)
            cx = self.key_center(pitch)
            if PC_BLACK[pc]:
                r = min(self.bw * 0.72, self.wk * 0.41, 8.0)
                cy = self.y + self.bh * 0.56
            else:
                r = min(self.wk * 0.41, 8.4)
                cy = self.y + self.h * 0.55
            fs = r * 1.18
            circle(c, cx, cy, r, YELLOW if is_char else white,
                   BLACK, 0.9)
            text(c, cx, cy + fs * 0.36, lab, 'Anton', fs, BLACK, 'c')

    def _white_index(self, pitch):
        oct_, pc = divmod(pitch, 12)
        if PC_BLACK[pc]:
            return -1
        return oct_ * 7 + PC_LETTER[pc]


# ------------------------------------------------------------------ selos
def badge(c, cx, cy, label, w=16, h=11, fs=7.4):
    """Selo preto com o dedo (E1...D5). cy = centro vertical."""
    rrect(c, cx - w / 2.0, cy - h / 2.0, w, h, BLACK, None, 0, 3)
    text(c, cx, cy + fs * 0.36, label, 'Anton', fs, white, 'c')


def hand_chip(c, x, y, hand, finger, size=13):
    fill = BLACK if hand == 'E' else RED
    rrect(c, x, y, size, size, fill, None, 0, 3)
    text(c, x + size / 2.0, y + size * 0.70, str(finger), 'Anton',
         size * 0.72, white, 'c')
