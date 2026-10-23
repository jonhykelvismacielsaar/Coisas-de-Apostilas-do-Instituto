# -*- coding: utf-8 -*-
"""Páginas / painéis da apostila."""

import os
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics

from desenho import (W, H, RED, DARKRED, YELLOW, BLACK, INK, GRAY, LGRAY,
                     KEYWHITE, KEYEDGE, PAPER, Y, text, fit, fitl, rrect, rect,
                     line, circle, star, border, Keys, badge)
from teoria import (KEYS, MODES, CHORD_TYPES, FINGER_NAMES, build_chord,
                    build_scale, chord_symbol, chord_symbol_both,
                    chord_description, relative_major, voicing,
                    fingering_text, fingering_seq, degree_label)

ASSETS = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets')
MAO_ESQ = os.path.join(ASSETS, 'mao_esq.png')
MAO_DIR = os.path.join(ASSETS, 'mao_dir.png')

# ponta de cada dedo na foto (relativo, da esquerda para a direita)
TIPS = {5: (0.243, 0.105), 4: (0.646, 0.150), 3: (0.800, 0.150),
        2: (0.893, 0.235), 1: (0.966, 0.360)}


def panel(c, x, y, w, h, lw=2.2):
    rect(c, x, y, w, h, PAPER, BLACK, lw)


# ------------------------------------------------------------------ mão
def draw_palm(c, x, y, w, h, hand, used=None):
    used = set(used or [])
    path = MAO_ESQ if hand == 'E' else MAO_DIR
    c.drawImage(path, x, Y(y + h), width=w, height=h, mask='auto')
    for f, (fx, fy) in TIPS.items():
        px = x + (fx if hand == 'E' else 1 - fx) * w
        py = y + fy * h
        on = f in used
        r = max(5.4, w * 0.056)
        circle(c, px, py, r, (BLACK if hand == 'E' else RED) if on else white,
               BLACK if on else GRAY, 0.9)
        text(c, px, py + r * 0.37, str(f), 'Anton', r * 1.25,
             white if on else GRAY, 'c')


def hand_line(c, x, y, w, items, hand, size=7.0):
    col = BLACK if hand == 'E' else RED
    tag = 'ESQ.' if hand == 'E' else 'DIR.'
    tw = text(c, x, y, tag + ' ', 'Anton', size, col)
    txt = '   '.join('%d %s (%s)' % (it['finger'], it['note'].display,
                                     FINGER_NAMES[hand][it['finger']])
                     for it in items)
    fitl(c, x + tw, y, txt, w - tw, 'Anton', size, BLACK)


def hand_list(c, x, y, items, hand, size=10.5, gap=12.6, photo=None):
    """Lista 'dedo -> nota -> nome do dedo'.  photo=(x, w, h) desenha a mão."""
    col = BLACK if hand == 'E' else RED
    title = 'MÃO ESQUERDA' if hand == 'E' else 'MÃO DIREITA'
    text(c, x, y, title, 'Anton', size * 1.02, col)
    text(c, x, y + size * 0.85,
         'DEDO 5 = POLEGAR' if hand == 'E' else 'DEDO 1 = POLEGAR',
         'Anton', 5.7, GRAY)
    ly = y + size * 2.1
    for it in items:
        f = it['finger']
        chip = size * 1.0
        rrect(c, x, ly - chip * 0.79, chip, chip, col, None, 0, 2.4)
        text(c, x + chip / 2.0, ly - chip * 0.79 + chip * 0.71, str(f),
             'Anton', chip * 0.74, white, 'c')
        nm = it['note'].display
        text(c, x + chip + 4, ly, nm, 'Anton', size)
        text(c, x + chip + 4 + pdfmetrics.stringWidth(nm, 'Anton', size) + 4,
             ly, FINGER_NAMES[hand][f], 'Anton', size * 0.55, GRAY)
        ly += gap
    if photo:
        px, pw, ph = photo
        draw_palm(c, px, y - 4, pw, ph, hand, [it['finger'] for it in items])
    return ly


# ------------------------------------------------------------------ painel grande (com fotos)
def chord_panel_big(c, x, y, w, h, mode, key, ctype):
    panel(c, x, y, w, h)
    notes = build_chord(mode, key, ctype)
    lh, rh = voicing(notes, ctype)
    colw = 214

    ty = y + 25
    fit(c, x + (w - colw) / 2.0, ty,
        '%s - %s - AS DUAS MÃOS' % (mode['name'], ctype['label']),
        w - colw - 24, 'Anton', 23, BLACK, 'c')
    fit(c, x + (w - colw) / 2.0, ty + 19,
        '%s - %s' % (chord_symbol_both(mode, key, ctype),
                     chord_description(mode, key, ctype)),
        w - colw - 14, 'Anton', 14.5, BLACK, 'c')

    pad = 15
    kx = x + pad
    ky = y + 70
    kh = min(h - (ky - y) - 52, 140)
    kw = min(w - pad * 2 - colw - 12, kh * 3.7)
    kh = kw / 3.7
    kb = Keys(kx, ky, kw, kh)

    hl, deg = {}, {}
    for it in lh + rh:
        p = it['pitch']
        hl[p] = 'black' if p % 12 in (1, 3, 6, 8, 10) else 'white'
        deg[p] = (it['note'].label, it['note'].is_char)
    kb.draw(c, hl, deg)

    for hand, items, dy in (('D', rh, -11), ('E', lh, kh + 11)):
        seen = set()
        for it in items:
            cx = kb.key_center(it['pitch'])
            if cx in seen:
                continue
            seen.add(cx)
            if hand == 'D':
                line(c, cx, ky - 1.5, cx, ky - 5, LGRAY, 0.7)
            else:
                line(c, cx, ky + kh + 1.5, cx, ky + kh + 5, LGRAY, 0.7)
            badge(c, cx, ky + dy, '%s%d' % (hand, it['finger']), 15, 10, 6.8)

    # coluna das mãos (com foto)
    mx = kx + kw + 14
    px = x + w - pad - 58
    hand_list(c, mx, ky - 8, rh, 'D', 10.2, 12.2, (px, 58, 55))
    hand_list(c, mx, ky + 70, lh, 'E', 10.2, 12.2, (px, 58, 55))

    ny = ky + kh + 30
    cw = text(c, kx, ny, 'NOTAS DO ACORDE:', 'Anton', 10, RED)
    text(c, kx + cw + 5, ny, ' - '.join(n.display for n in notes), 'Anton', 10)
    fw = text(c, kx, ny + 15, 'FÓRMULA:', 'Anton', 10, RED)
    text(c, kx + fw + 5, ny + 15,
         ' - '.join(n.label for n in notes), 'Anton', 10)
    dx = kx + max(210, cw + 150)
    dw = text(c, dx, ny, 'DEDILHADO:', 'Anton', 10, RED)
    text(c, dx + dw + 5, ny,
         'ESQ. %s   |   DIR. %s' % (fingering_seq('E', lh),
                                    fingering_seq('D', rh)), 'Anton', 10)
    text(c, dx, ny + 15,
         '%s  •  %s' % (fingering_text('E', lh), fingering_text('D', rh)),
         'Anton', 6.4, GRAY)


# ------------------------------------------------------------------ painel de grade
def chord_panel_grid(c, x, y, w, h, mode, key, ctype):
    panel(c, x, y, w, h, 2.0)
    notes = build_chord(mode, key, ctype)
    lh, rh = voicing(notes, ctype)

    text(c, x + w / 2.0, y + 17,
         '%s - %s - AS DUAS MÃOS' % (mode['name'], ctype['label']),
         'Anton', 14.5, BLACK, 'c')
    fit(c, x + w / 2.0, y + 31,
        '%s - %s' % (chord_symbol_both(mode, key, ctype),
                     chord_description(mode, key, ctype)),
        w - 22, 'Anton', 9.2, BLACK, 'c')

    pad = 12
    ky = y + 52
    kw = min(w - pad * 2, (h - 52 - 78) * 3.7)
    kh = kw / 3.7
    kx = x + (w - kw) / 2.0
    kb = Keys(kx, ky, kw, kh, label_size=6.2)
    hl, deg = {}, {}
    for it in lh + rh:
        p = it['pitch']
        hl[p] = 'black' if p % 12 in (1, 3, 6, 8, 10) else 'white'
        deg[p] = (it['note'].label, it['note'].is_char)
    kb.draw(c, hl, deg)

    for hand, items, dy in (('D', rh, -9.5), ('E', lh, kh + 9.5)):
        seen = set()
        for it in items:
            cx = kb.key_center(it['pitch'])
            if cx in seen:
                continue
            seen.add(cx)
            if hand == 'D':
                line(c, cx, ky - 1.0, cx, ky - 3.8, LGRAY, 0.6)
            else:
                line(c, cx, ky + kh + 1.0, cx, ky + kh + 3.8, LGRAY, 0.6)
            badge(c, cx, ky + dy, '%s%d' % (hand, it['finger']), 13, 8.6, 6.0)

    hy = ky + kh + 24
    hand_line(c, kx, hy, w - pad * 2, rh, 'D', 7.6)
    hand_line(c, kx, hy + 13, w - pad * 2, lh, 'E', 7.6)
    text(c, kx, hy + 30, 'DIREITA %s  •  ESQUERDA %s' % (
        'COMPLETA O ACORDE' if ctype['key'] in ('nona', 'onze', 'treze')
        else 'TOCA O ACORDE INTEIRO ACIMA',
        'FAZ A BASE 1-3-5' if ctype['key'] in ('nona', 'onze', 'treze')
        else 'TOCA O ACORDE INTEIRO'), 'Anton', 6.4, GRAY)

    ny = y + h - 20
    cw = text(c, kx, ny, 'NOTAS:', 'Anton', 7.4, RED)
    text(c, kx + cw + 4, ny, ' - '.join(n.display for n in notes), 'Anton', 7.4)
    fw = text(c, kx, ny + 9.5, 'FÓRMULA:', 'Anton', 7.4, RED)
    text(c, kx + fw + 4, ny + 9.5, ' - '.join(n.label for n in notes),
         'Anton', 7.4)
    dx = x + w / 2.0 + 4
    dw = text(c, dx, ny, 'DEDOS:', 'Anton', 7.4, RED)
    text(c, dx + dw + 4, ny,
         'ESQ. %s / DIR. %s' % (fingering_seq('E', lh),
                                fingering_seq('D', rh)), 'Anton', 7.4)


# ------------------------------------------------------------------ escala (grade)
def scale_panel_grid(c, x, y, w, h, mode, key):
    panel(c, x, y, w, h, 2.0)
    scale = build_scale(mode, key)
    text(c, x + w / 2.0, y + 17, 'ESCALA - MODO %s' % mode['name'],
         'Anton', 14.5, BLACK, 'c')
    fit(c, x + w / 2.0, y + 31,
        '%s - MESMAS NOTAS DE %s' % (key['name'], relative_major(mode, key)),
        w - 22, 'Anton', 9.2, BLACK, 'c')
    pad = 12
    ky = y + 52
    kw = min(w - pad * 2, (h - 52 - 82) * 3.7)
    kh = kw / 3.7
    kx = x + (w - kw) / 2.0
    kb = Keys(kx, ky, kw, kh, label_size=6.2)
    hl, deg = {}, {}
    for n in scale:
        p = n.pitch
        hl[p] = 'black' if p % 12 in (1, 3, 6, 8, 10) else 'white'
        deg[p] = (n.label, n.is_char)
    kb.draw(c, hl, deg)

    yy = ky + kh + 24
    text(c, kx, yy, 'NOTAS DA ESCALA', 'Anton', 8.6, RED)
    text(c, kx + 88, yy, ' - '.join(n.display for n in scale), 'Anton', 9.4)
    text(c, kx, yy + 13, 'FÓRMULA', 'Anton', 8.6, RED)
    text(c, kx + 88, yy + 13, ' - '.join(n.label for n in scale), 'Anton', 9.4)
    text(c, kx, yy + 27, 'NOTA CARACTERÍSTICA', 'Anton', 8.6, RED)
    tw = text(c, kx + 88, yy + 27, mode['char_text'], 'Anton', 9.4)
    circle(c, kx + 90 + tw + 6, yy + 24.5, 5.4, YELLOW, BLACK, 0.9)


def scale_strip(c, x, y, w, h, mode, key):
    """Faixa compacta de escala (usada nas páginas de tom)."""
    scale = build_scale(mode, key)
    cw = text(c, x, y + 10, 'ESCALA', 'Anton', 9, RED)
    text(c, x + cw + 5, y + 10,
         ' '.join('%s (%s)' % (n.display, n.label) for n in scale),
         'Anton', 9, BLACK)
