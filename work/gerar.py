# -*- coding: utf-8 -*-
"""Gera a apostila completa: Acordes em todos os modos com dedilhado das duas mãos."""

import os
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.lib.colors import white, HexColor

from desenho import (W, H, RED, DARKRED, YELLOW, BLACK, INK, GRAY, LGRAY,
                     KEYWHITE, KEYEDGE, PAPER, Y, text, fit, fitl, rrect, rect,
                     line, circle, star, border, Keys, badge)
from paginas import (panel, chord_panel_big, chord_panel_grid,
                     scale_panel_grid, hand_list, draw_palm)
from teoria import (KEYS, MODES, CHORD_TYPES, FINGER_NAMES, build_chord,
                    build_scale, chord_symbol, chord_symbol_both,
                    chord_description, relative_major, voicing,
                    fingering_text, fingering_seq, degree_label)

OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                   'APOSTILA TECLADO - ACORDES EM TODOS OS MODOS (DUAS MÃOS).pdf')

PER_HAND = {
    'triade': ('1-3-5', '1-3-5', 'CADA MÃO FAZ O ACORDE INTEIRO'),
    'tetrade': ('1-3-4-5', '1-2-3-5', 'CADA MÃO FAZ O ACORDE INTEIRO'),
    'nona': ('1-3-5', '1-2', 'ESQ. 1-3-5 / DIR. 7 E 9'),
    'onze': ('1-3-5', '1-2-3', 'ESQ. 1-3-5 / DIR. 7, 9 E 11'),
    'treze': ('1-3-5', '1-2-3-4', 'ESQ. 1-3-5 / DIR. 7, 9, 11 E 13'),
}


# =============================================================== páginas
def page_capa(c, sec_pages=None):
    border(c)
    rect(c, 18, 18, W - 36, H - 36, None, BLACK, 1.0)
    text(c, W / 2, 74, 'APOSTILA TECLADO', 'Anton', 62, BLACK, 'c')
    text(c, W / 2, 122, 'ACORDES EM TODOS OS MODOS', 'Anton', 42, RED, 'c')
    text(c, W / 2, 148,
         'DO JÔNIO AO LÓCRIO  •  12 TONS  •  TRÍADE, TÉTRADE, 9ª, 11ª E 13ª',
         'ABlack', 12.5, BLACK, 'c')
    text(c, W / 2, 168, 'COM O DEDILHADO EXATO DAS DUAS MÃOS', 'Anton', 17, RED, 'c')
    line(c, 60, 188, W - 60, 188, BLACK, 2.6)
    line(c, 60, 191, W - 60, 191, BLACK, 1.0)

    sp = sec_pages or {}
    rows = [('SEÇÃO 0', 'COMPARAÇÃO DOS 7 MODOS', 'TABELA GERAL + OS 7 MODOS EM CADA TOM',
             sp.get('comparacao', 5))]
    for i, m in enumerate(MODES):
        rows.append(('SEÇÃO %d' % (i + 1), 'MODO ' + m['name'], m['short'],
                     sp.get(m['key'], 0)))
    rows += [('EXTRA', 'COMO FAZER O ACORDE COM AS DUAS MÃOS',
              'POSIÇÃO DAS MÃOS E DEDO POR DEDO', 2)]

    y = 212
    for sec, nome, sub, pg in rows:
        text(c, 62, y, sec, 'Anton', 12.5, RED)
        text(c, 132, y, nome, 'Anton', 19, BLACK)
        text(c, 470, y + 1, sub, 'Anton', 8.4, HexColor('#333333'))
        text(c, W - 62, y, 'PÁG. %d' % pg if pg else '', 'Anton', 12.5, RED, 'r')
        line(c, 60, y + 9, W - 60, y + 9, LGRAY, 0.6)
        y += 30

    text(c, W / 2, y + 14,
         'AS DUAS MÃOS TOCAM JUNTAS: A ESQUERDA SEGURA A BASE E A DIREITA COMPLETA O ACORDE',
         'Anton', 10, GRAY, 'c')
    text(c, W / 2, y + 30,
         'CADA PÁGINA DE ACORDE MOSTRA O TECLADO COM O NÚMERO DO DEDO EM CIMA DE CADA NOTA',
         'Anton', 10, GRAY, 'c')


def page_legenda(c):
    border(c)
    text(c, W / 2, 40, 'COMO LER ESTA APOSTILA', 'Anton', 34, BLACK, 'c')
    line(c, 150, 52, W - 150, 52, BLACK, 2)

    # bloco 1 - símbolos
    x, y = 40, 76
    text(c, x, y, 'O QUE CADA SÍMBOLO QUER DIZER', 'Anton', 14, RED)
    items = [
        (('c', True), 'GRAU DA ESCALA (1 A 13) — 8 = OITAVA, 9 = 2ª, 11 = 4ª E 13 = 6ª UMA OITAVA ACIMA'),
        (('c', False), 'TECLA VERMELHA = NOTA QUE FORMA O ACORDE'),
        (('y', True), 'CÍRCULO AMARELO = NOTA CARACTERÍSTICA DO MODO'),
        (('b', 'E1'), 'E1 A E5 = MÃO ESQUERDA (E DE ESQUERDA) — DEDO 1 = MÍNIMO ... 5 = POLEGAR'),
        (('b', 'D1'), 'D1 A D5 = MÃO DIREITA (D DE DIREITA) — DEDO 1 = POLEGAR ... 5 = MÍNIMO'),
    ]
    yy = y + 20
    for kind, label in items:
        if kind[0] in ('c', 'y'):
            circle(c, x + 7, yy - 3, 6.4, YELLOW if kind[0] == 'y' else white, BLACK, 1)
            text(c, x + 7, yy - 1, '1', 'Anton', 7.6, BLACK, 'c')
        else:
            badge(c, x + 12, yy - 3, kind[1], 22, 11, 7.4)
        text(c, x + 32, yy, label, 'Anton', 8.4, BLACK)
        yy += 16

    # bloco 2 - numeração das mãos
    y2 = yy + 18
    text(c, x, y2, 'A NUMERAÇÃO DOS DEDOS É A MESMA EM TODA A APOSTILA', 'Anton', 14, RED)
    text(c, x, y2 + 15,
         'NA MÃO ESQUERDA O DEDO 1 É O MAIS GRAVE (MÍNIMO) E O 5 É O POLEGAR. '
         'NA MÃO DIREITA O DEDO 1 É O POLEGAR E O 5 É O MAIS AGUDO (MÍNIMO).',
         'Anton', 8.2, HexColor('#333333'))
    text(c, x, y2 + 26,
         'ASSIM, O DEDO 1 FICA SEMPRE NA NOTA MAIS GRAVE DA MÃO E O DEDO 5 NA NOTA MAIS AGUDA.',
         'Anton', 8.2, HexColor('#333333'))

    draw_palm(c, x + 10, y2 + 36, 120, 113, 'E', [1, 3, 5])
    text(c, x + 10, y2 + 162, 'MÃO ESQUERDA', 'Anton', 11, BLACK)
    text(c, x + 10, y2 + 172, '1 MÍNIMO  2 ANELAR  3 MÉDIO  4 INDICADOR  5 POLEGAR',
         'Anton', 6.4, GRAY)
    draw_palm(c, x + 190, y2 + 36, 120, 113, 'D', [1, 2])
    text(c, x + 190, y2 + 162, 'MÃO DIREITA', 'Anton', 11, RED)
    text(c, x + 190, y2 + 172, '1 POLEGAR  2 INDICADOR  3 MÉDIO  4 ANELAR  5 MÍNIMO',
         'Anton', 6.4, GRAY)

    # bloco 3 - dedilhado padrão
    bx = 380
    by = 76
    text(c, bx, by, 'DEDILHADO PADRÃO DE CADA ACORDE', 'Anton', 14, RED)
    hdr = ['ACORDE', 'MÃO ESQUERDA', 'MÃO DIREITA', 'O QUE CADA MÃO TOCA']
    xs = [bx, bx + 108, bx + 200, bx + 296]
    rect(c, bx - 6, by + 10, W - 34 - bx, 17, BLACK, None)
    for xx, hh in zip(xs, hdr):
        text(c, xx, by + 22, hh, 'Anton', 8, white)
    yy = by + 44
    rows = [
        ('TRÍADE', 'DEDOS 1 - 3 - 5', 'DEDOS 1 - 3 - 5', 'A DIREITA TOCA O MESMO ACORDE 1 OITAVA ACIMA'),
        ('TÉTRADE', 'DEDOS 1 - 3 - 4 - 5', 'DEDOS 1 - 2 - 3 - 5', 'A DIREITA TOCA O MESMO ACORDE 1 OITAVA ACIMA'),
        ('COM 9ª', 'DEDOS 1 - 3 - 5', 'DEDOS 1 - 2', 'ESQ. 1-3-5 / DIR. 7ª E 9ª'),
        ('COM 11ª', 'DEDOS 1 - 3 - 5', 'DEDOS 1 - 2 - 3', 'ESQ. 1-3-5 / DIR. 7ª, 9ª E 11ª'),
        ('COM 13ª', 'DEDOS 1 - 3 - 5', 'DEDOS 1 - 2 - 3 - 4', 'ESQ. 1-3-5 / DIR. 7ª, 9ª, 11ª E 13ª'),
    ]
    for i, r in enumerate(rows):
        if i % 2 == 0:
            rect(c, bx - 6, yy - 10, W - 34 - bx, 18, HexColor('#F2F2F2'), None)
        text(c, xs[0], yy, r[0], 'Anton', 11, BLACK)
        text(c, xs[1], yy, r[1], 'Anton', 9, BLACK)
        text(c, xs[2], yy, r[2], 'Anton', 9, RED)
        text(c, xs[3], yy, r[3], 'Anton', 7.2, HexColor('#333333'))
        line(c, bx - 6, yy + 7, W - 40, yy + 7, LGRAY, 0.5)
        yy += 18

    text(c, bx, yy + 20, 'MÃO ESQUERDA FAZ A BASE (1 - 3 - 5) E A DIREITA COMPLETA O ACORDE',
         'Anton', 9.4, BLACK)
    text(c, bx, yy + 34,
         'NAS TRÍADES E TÉTRADES AS DUAS MÃOS TOCAM O ACORDE INTEIRO, A DIREITA UMA OITAVA ACIMA.',
         'Anton', 7.4, HexColor('#333333'))
    text(c, bx, yy + 46,
         'EXEMPLO EM DÓ: ESQUERDA C - E - G (DEDOS 1-3-5) E DIREITA C - E - G UMA OITAVA ACIMA.',
         'Anton', 7.4, HexColor('#333333'))


def page_indice(c, sec_pages):
    border(c)
    text(c, W / 2, 52, 'ÍNDICE', 'Anton', 40, BLACK, 'c')
    line(c, 120, 66, W - 120, 66, BLACK, 2)
    text(c, W / 2, 86, 'TODAS AS SEÇÕES, TODOS OS TONS, TODOS OS ACORDES COM AS DUAS MÃOS',
         'Anton', 10, GRAY, 'c')

    col_x = [66, 420]
    rows = [('SEÇÃO 0 - COMPARAÇÃO DOS 7 MODOS', 'TABELA GERAL E OS 7 MODOS NOS 12 TONS',
             sec_pages['comparacao'])]
    for i, m in enumerate(MODES):
        rows.append(('SEÇÃO %d - MODO %s' % (i + 1, m['name']),
                     '%s  •  TABELA + 12 TONS COM DEDILHADO' % m['short'],
                     sec_pages[m['key']]))
    per_col = (len(rows) + 1) // 2
    for i, (a, b, pg) in enumerate(rows):
        cx = col_x[0] if i < per_col else col_x[1]
        yy = 118 + (i % per_col) * 42
        text(c, cx, yy, a, 'Anton', 12.6, BLACK)
        text(c, cx, yy + 11, b, 'Anton', 6.8, HexColor('#444444'))
        text(c, cx + 320, yy, 'PÁG. %d' % pg, 'Anton', 12.6, RED, 'r')
        line(c, cx, yy + 16, cx + 320, yy + 16, LGRAY, 0.6)

    text(c, 66, 118 + per_col * 42 + 16,
         'DENTRO DE CADA SEÇÃO: PÁGINA A = TRÍADE E TÉTRADE  •  PÁGINA B = 9ª, 11ª E 13ª + ESCALA',
         'Anton', 9, RED)
    text(c, 66, 118 + per_col * 42 + 28,
         'TODAS AS PÁGINAS MOSTRAM O DEDO EXATO DE CADA MÃO (E1-E5 / D1-D5) SOBRE A NOTA.',
         'Anton', 8.2, HexColor('#333333'))


def page_tabela_geral(c):
    border(c)
    text(c, W / 2, 34, 'OS 7 MODOS - TABELA DE COMPARAÇÃO (EXEMPLO EM DÓ)', 'Anton', 20, BLACK, 'c')
    x0, y0 = 24, 50
    widths = [66, 34, 118, 56, 62, 62, 66, 78, 118]
    headers = ['MODO', 'GRAU', 'FÓRMULA', 'TRÍADE', 'TÉTRADE', 'COM 9ª', 'COM 11ª',
               'COM 13ª', 'CARACTERÍSTICA']
    total = sum(widths)
    rect(c, x0, y0, total, 16, BLACK, None)
    xx = x0
    for w_, h_ in zip(widths, headers):
        text(c, xx + 5, y0 + 11, h_, 'Anton', 8, white)
        xx += w_
    yy = y0 + 16
    rh = 21
    key = KEYS[0]
    for i, m in enumerate(MODES):
        if i % 2 == 0:
            rect(c, x0, yy, total, rh, HexColor('#F4F4F4'), None)
        line(c, x0, yy + rh, x0 + total, yy + rh, LGRAY, 0.6)
        text(c, x0 + 5, yy + 14, m['name'], 'Anton', 10.5, BLACK)
        text(c, x0 + widths[0] + 5, yy + 14, '%dº' % m['num'], 'Anton', 9.5, RED)
        f = ' '.join(degree_label(m, d) for d in range(7))
        text(c, x0 + widths[0] + widths[1] + 5, yy + 14, f, 'Anton', 8.4, BLACK)
        cx = x0 + widths[0] + widths[1] + widths[2]
        for ctype in CHORD_TYPES:
            sym = chord_symbol(m, key, ctype)
            text(c, cx + 4, yy + 14, sym, 'Anton', 8.0, RED)
            cx += widths[3 + [ct['key'] for ct in CHORD_TYPES].index(ctype['key'])]
        fitl(c, x0 + total - widths[8] + 5, yy + 14, m['desc'], widths[8] - 10,
             'Anton', 6.8, HexColor('#222222'))
        yy += rh
    rect(c, x0, y0, total, yy - y0, None, BLACK, 1.4)
    xx = x0
    for w_ in widths[:-1]:
        xx += w_
        line(c, xx, y0, xx, yy, LGRAY, 0.5)

    # segunda metade: como fazer com as duas mãos
    y2 = yy + 14
    text(c, W / 2, y2 + 12,
         'COMO TOCAR CADA UM DESSES ACORDES COM AS DUAS MÃOS', 'Anton', 15, RED, 'c')
    boxes = [
        ('TRÍADE', 'ESQ. 1 - 3 - 5', 'DIR. 1 - 3 - 5', 'AS DUAS MÃOS TOCAM O ACORDE COMPLETO'),
        ('TÉTRADE', 'ESQ. 1 - 3 - 4 - 5', 'DIR. 1 - 2 - 3 - 5', 'AS DUAS MÃOS TOCAM O ACORDE COMPLETO'),
        ('COM 9ª', 'ESQ. 1 - 3 - 5', 'DIR. 1 - 2', 'DIREITA ACRESCENTA 7ª E 9ª'),
        ('COM 11ª', 'ESQ. 1 - 3 - 5', 'DIR. 1 - 2 - 3', 'DIREITA ACRESCENTA 7ª, 9ª E 11ª'),
        ('COM 13ª', 'ESQ. 1 - 3 - 5', 'DIR. 1 - 2 - 3 - 4', 'DIREITA ACRESCENTA 7ª, 9ª, 11ª E 13ª'),
    ]
    bw = (W - 52) / 5.0
    for i, (a, b, d, e) in enumerate(boxes):
        bx = 26 + i * bw
        rect(c, bx + 2, y2 + 24, bw - 4, 62, None, BLACK, 1.2)
        text(c, bx + bw / 2, y2 + 42, a, 'Anton', 12, RED, 'c')
        text(c, bx + bw / 2, y2 + 56, b, 'Anton', 9, BLACK, 'c')
        text(c, bx + bw / 2, y2 + 68, d, 'Anton', 9, BLACK, 'c')
        fit(c, bx + bw / 2, y2 + 79, e, bw - 16, 'Anton', 6.2, GRAY, 'c')


# ------------------------------------------------------- comparação por tom
def comp_panel_extra(c, x, y, w, h, key):
    panel(c, x, y, w, h, 2.0)
    text(c, x + w / 2.0, y + 26, 'COMO TOCAR COM AS DUAS MÃOS', 'Anton', 15, RED, 'c')
    text(c, x + w / 2.0, y + 42,
         'A MÃO ESQUERDA FAZ A BASE E A DIREITA COMPLETA O ACORDE',
         'Anton', 8.4, HexColor('#333333'), 'c')
    rows = [
        ('TRÍADE', 'ESQ. 1-3-5', 'DIR. 1-3-5'),
        ('TÉTRADE', 'ESQ. 1-3-4-5', 'DIR. 1-2-3-5'),
        ('COM 9ª', 'ESQ. 1-3-5', 'DIR. 1-2'),
        ('COM 11ª', 'ESQ. 1-3-5', 'DIR. 1-2-3'),
        ('COM 13ª', 'ESQ. 1-3-5', 'DIR. 1-2-3-4'),
    ]
    yy = y + 62
    rect(c, x + 14, yy - 11, w - 28, 15, BLACK, None)
    text(c, x + 22, yy, 'ACORDE', 'Anton', 7.4, white)
    text(c, x + 120, yy, 'MÃO ESQUERDA', 'Anton', 7.4, white)
    text(c, x + 236, yy, 'MÃO DIREITA', 'Anton', 7.4, white)
    yy += 16
    for i, (a, b, d) in enumerate(rows):
        if i % 2 == 0:
            rect(c, x + 14, yy - 9, w - 28, 14, HexColor('#F2F2F2'), None)
        text(c, x + 22, yy, a, 'Anton', 9.4, BLACK)
        text(c, x + 120, yy, b, 'Anton', 8.6, BLACK)
        text(c, x + 236, yy, d, 'Anton', 8.6, RED)
        yy += 14
    yy += 8
    for l1, l2 in [
        ('NA MÃO ESQUERDA: 1 MÍNIMO, 2 ANELAR, 3 MÉDIO, 4 INDICADOR, 5 POLEGAR.',
         'NA MÃO DIREITA: 1 POLEGAR, 2 INDICADOR, 3 MÉDIO, 4 ANELAR, 5 MÍNIMO.'),
        ('NAS TRÍADES E TÉTRADES A DIREITA TOCA O MESMO ACORDE UMA OITAVA ACIMA.',
         'NAS EXTENSÕES A ESQUERDA SEGURA 1-3-5 E A DIREITA ENTRA COM 7, 9, 11 E 13.'),
        ('O SELO E1-E5 OU D1-D5 FICA SEMPRE EM CIMA DA NOTA QUE AQUELE DEDO TOCA.',
         'EXEMPLO EM %s: MÃO ESQUERDA %s COM OS DEDOS 1-3-5.'
         % (key['name'], ' - '.join(
             n.display for n in build_chord(MODES[0], key, CHORD_TYPES[0])))),
    ]:
        text(c, x + 22, yy, l1, 'Anton', 7.0, HexColor('#333333'))
        text(c, x + 22, yy + 9, l2, 'Anton', 7.0, HexColor('#333333'))
        yy += 22


def page_comparacao(c, key, part, total_parts=2):
    border(c)
    nome = key['name'] if not key['alt'] else '%s / %s' % (key['name'], key['alt'])
    pt = key['pt'] if not key['pt_alt'] else '%s / %s' % (key['pt'], key['pt_alt'])
    fit(c, W / 2, 30, 'COMPARAÇÃO DOS 7 MODOS - %s (%s)' % (nome, pt),
        W - 70, 'Anton', 20, BLACK, 'c')
    text(c, W / 2, 42, 'OS 7 MODOS EM %s  •  TÉTRADE DE CADA UM COM O DEDO EXATO DAS DUAS MÃOS'
         % nome, 'Anton', 8, GRAY, 'c')
    modes = MODES[:4] if part == 1 else MODES[4:]
    pw = (W - 44) / 2.0
    ph = (H - 74) / 2.0
    for i, m in enumerate(modes):
        cx = 16 + (i % 2) * (pw + 6)
        cy = 48 + (i // 2) * (ph + 4)
        chord_panel_grid(c, cx, cy, pw, ph, m, key, CHORD_TYPES[1])
    if part == 2:
        chord_panel_grid(c, 16 + pw + 6, 48 + (ph + 4), pw, ph,
                         MODES[6], key, CHORD_TYPES[1])
        comp_panel_extra(c, 16, 48 + (ph + 4), pw, ph, key)
    text(c, W / 2, H - 10,
         'E = MÃO ESQUERDA  •  D = MÃO DIREITA  •  O NÚMERO É O DEDO QUE TOCA AQUELA NOTA',
         'Anton', 6.4, GRAY, 'c')


# ------------------------------------------------------- tabelas por modo
def page_escalas(c, mode):
    border(c)
    text(c, W / 2, 34, 'ESCALAS - MODO %s' % mode['name'], 'Anton', 22, BLACK, 'c')
    text(c, W / 2, 50, '%s  •  AS 7 NOTAS DO MODO NOS 12 TONS' % mode['desc'],
         'Anton', 9, GRAY, 'c')
    x0, y0 = 26, 64
    widths = [74] + [84] * 7 + [74]
    total = sum(widths)
    rect(c, x0, y0, total, 18, BLACK, None)
    heads = ['TOM'] + ['%dº GRAU' % (i + 1) for i in range(7)] + ['CARACTERÍSTICA']
    xx = x0
    for w_, h_ in zip(widths, heads):
        fit(c, xx + w_ / 2.0, y0 + 12.4, h_, w_ - 5, 'Anton', 8.2, white, 'c')
        xx += w_
    yy = y0 + 18
    rh = 33.5
    for i, key in enumerate(KEYS):
        if i % 2 == 0:
            rect(c, x0, yy, total, rh, HexColor('#F4F4F4'), None)
        line(c, x0, yy + rh, x0 + total, yy + rh, LGRAY, 0.6)
        nome = key['name'] if not key['alt'] else '%s/%s' % (key['name'], key['alt'])
        text(c, x0 + widths[0] / 2.0, yy + 16, nome, 'Anton', 13, BLACK, 'c')
        text(c, x0 + widths[0] / 2.0, yy + 27, key['pt'], 'Anton', 5.6, GRAY, 'c')
        scale = build_scale(mode, key)
        xx = x0 + widths[0]
        for n in scale:
            if n.is_char:
                star(c, xx + widths[1] / 2.0, yy + rh / 2.0 + 3, 12, YELLOW)
            text(c, xx + widths[1] / 2.0, yy + 16, n.display, 'Anton', 12.5,
                 BLACK, 'c')
            text(c, xx + widths[1] / 2.0, yy + 27, n.label, 'Anton', 7.4, RED, 'c')
            xx += widths[1]
        text(c, x0 + total - widths[8] / 2.0, yy + 21, mode['char_text'],
             'Anton', 9, RED, 'c')
        yy += rh
    rect(c, x0, y0, total, yy - y0, None, BLACK, 1.4)
    xx = x0
    for w_ in widths[:-1]:
        xx += w_
        line(c, xx, y0, xx, yy, LGRAY, 0.5)
    text(c, W / 2, yy + 14,
         'ESTRELA AMARELA = NOTA CARACTERÍSTICA DO MODO (%s)  •  b = MEIO TOM ABAIXO  •  # = MEIO TOM ACIMA'
         % mode['char_text'], 'Anton', 7.6, HexColor('#333333'), 'c')
    text(c, W / 2, yy + 26,
         'NAS PÁGINAS SEGUINTES CADA TOM TEM OS ACORDES DESENHADOS NO TECLADO COM O DEDO EXATO DAS DUAS MÃOS',
         'Anton', 7.2, GRAY, 'c')


def page_acordes(c, mode):
    border(c)
    text(c, W / 2, 34, 'ACORDES - MODO %s' % mode['name'], 'Anton', 22, BLACK, 'c')
    text(c, W / 2, 50, 'TRÍADE, TÉTRADE, 9ª, 11ª E 13ª NOS 12 TONS  •  SEMPRE COM AS DUAS MÃOS',
         'Anton', 9, GRAY, 'c')
    x0, y0 = 24, 64
    widths = [52, 82, 40, 86, 40, 86, 40, 86, 40, 90, 40, 96]
    total = sum(widths)
    heads = ['TOM', 'TRÍADE', 'DEDOS', 'TÉTRADE', 'DEDOS', 'COM 9ª', 'DEDOS',
             'COM 11ª', 'DEDOS', 'COM 13ª', 'DEDOS', 'MESMAS NOTAS DE']
    rect(c, x0, y0, total, 18, BLACK, None)
    xx = x0
    for w_, h_ in zip(widths, heads):
        fit(c, xx + w_ / 2.0, y0 + 12.4, h_, w_ - 5, 'Anton', 8.2, white, 'c')
        xx += w_
    yy = y0 + 18
    rh = 33.5
    for i, key in enumerate(KEYS):
        if i % 2 == 0:
            rect(c, x0, yy, total, rh, HexColor('#F4F4F4'), None)
        line(c, x0, yy + rh, x0 + total, yy + rh, LGRAY, 0.6)
        nome = key['name'] if not key['alt'] else '%s/%s' % (key['name'], key['alt'])
        text(c, x0 + widths[0] / 2.0, yy + 16, nome, 'Anton', 13, BLACK, 'c')
        text(c, x0 + widths[0] / 2.0, yy + 27, key['pt'], 'Anton', 5.6, GRAY, 'c')
        xx = x0 + widths[0]
        for j, ctype in enumerate(CHORD_TYPES):
            sym = chord_symbol(mode, key, ctype)
            notes = build_chord(mode, key, ctype)
            lh, rh_ = voicing(notes, ctype)
            text(c, xx + 4, yy + 14, sym, 'Anton', 9.6, RED)
            text(c, xx + 4, yy + 26, ' - '.join(n.display for n in notes),
                 'Anton', 6.5, BLACK)
            xx += widths[1 + j * 2]
            text(c, xx + 3, yy + 14, 'E' + fingering_seq('E', lh), 'Anton', 6.4,
                 HexColor('#333333'))
            text(c, xx + 3, yy + 25, 'D' + fingering_seq('D', rh_), 'Anton', 6.4, RED)
            xx += widths[2 + j * 2]
        text(c, x0 + total - widths[11] + 5, yy + 15,
             relative_major(mode, key).replace(' MAIOR', ''), 'Anton', 10, RED)
        text(c, x0 + total - widths[11] + 5, yy + 26,
             'MODO %s' % mode['name'], 'Anton', 6.2, HexColor('#333333'))
        yy += rh
    rect(c, x0, y0, total, yy - y0, None, BLACK, 1.4)
    text(c, W / 2, yy + 14,
         'E = MÃO ESQUERDA (1 MÍNIMO ... 5 POLEGAR)  •  D = MÃO DIREITA (1 POLEGAR ... 5 MÍNIMO)  •  '
         'A DIREITA TOCA O ACORDE UMA OITAVA ACIMA DA ESQUERDA',
         'Anton', 7.4, HexColor('#333333'), 'c')
    text(c, W / 2, yy + 26,
         'AS PÁGINAS SEGUINTES MOSTRAM CADA ACORDE DESENHADO NO TECLADO, NOTA POR NOTA, COM O DEDO MARCADO',
         'Anton', 7.2, GRAY, 'c')


# ------------------------------------------------------- seção (capa)
def page_secao(c, mode, sec_num, first_page):
    border(c)
    text(c, W / 2, 96, 'SEÇÃO %d' % sec_num, 'Anton', 24, RED, 'c')
    fit(c, W / 2, 156, 'MODO %s' % mode['name'], W - 120, 'Anton', 60, BLACK, 'c')
    text(c, W / 2, 186, '%dº GRAU DA ESCALA MAIOR  •  %s' % (mode['num'], mode['desc']),
         'ABlack', 11.5, BLACK, 'c')

    # estrelas dos graus
    cw = 74
    x = W / 2 - cw * 3
    key = KEYS[0]
    scale = build_scale(mode, key)
    for i, n in enumerate(scale):
        star(c, x + i * cw, 232, 24, YELLOW if n.is_char else RED)
        text(c, x + i * cw, 238, n.label, 'Anton', 18, BLACK, 'c')
        text(c, x + i * cw, 262, n.display, 'Anton', 13, BLACK, 'c')
    text(c, W / 2, 278, '(EXEMPLO EM DÓ)', 'Anton', 8, GRAY, 'c')

    kb = Keys(190, 300, 464, 125)
    hl, deg = {}, {}
    for n in scale:
        hl[n.pitch] = 'black' if n.pitch % 12 in (1, 3, 6, 8, 10) else 'white'
        deg[n.pitch] = (n.label, n.is_char)
    kb.draw(c, hl, deg)

    # mini tabela dos 5 acordes
    y = 448
    bw = (W - 80) / 5.0
    for i, ctype in enumerate(CHORD_TYPES):
        bx = 40 + i * bw
        rect(c, bx, y, bw - 6, 92, None, BLACK, 1.4)
        text(c, bx + (bw - 6) / 2.0, y + 15, ctype['label'], 'Anton', 10,
             HexColor('#333333'), 'c')
        fit(c, bx + (bw - 6) / 2.0, y + 40,
            chord_symbol(mode, key, ctype), bw - 18, 'Anton', 20, RED, 'c')
        notas = build_chord(mode, key, ctype)
        fit(c, bx + (bw - 6) / 2.0, y + 54,
            ' - '.join(n.label for n in notas), bw - 16, 'Anton', 8.6, BLACK, 'c')
        lh, rh = voicing(notas, ctype)
        text(c, bx + (bw - 6) / 2.0, y + 68,
             'ESQ. %s' % fingering_seq('E', lh), 'Anton', 8.6, BLACK, 'c')
        text(c, bx + (bw - 6) / 2.0, y + 80,
             'DIR. %s' % fingering_seq('D', rh), 'Anton', 8.6, RED, 'c')

    text(c, W / 2, y + 104,
         'NAS PRÓXIMAS %d PÁGINAS: TABELA DOS 12 TONS  •  2 PÁGINAS POR TOM COM O DEDILHADO DAS DUAS MÃOS'
         % 26, 'Anton', 8.4, GRAY, 'c')


# ------------------------------------------------------- páginas de tom
def page_tom_a(c, mode, key, sec_num):
    border(c)
    fit(c, W / 2, 29, 'SEÇÃO %d - %s - %s (%s)' % (sec_num, mode['name'],
                                                  key['name'] if not key['alt']
                                                  else '%s / %s' % (key['name'], key['alt']),
                                                  key['pt'] if not key['pt_alt']
                                                  else '%s / %s' % (key['pt'], key['pt_alt'])),
        W - 40, 'Anton', 13, GRAY, 'c')
    chord_panel_big(c, 14, 34, W - 28, 262, mode, key, CHORD_TYPES[0])
    chord_panel_big(c, 14, 304, W - 28, 262, mode, key, CHORD_TYPES[1])
    text(c, W / 2, H - 16,
         'TRÍADE E TÉTRADE  •  CADA MÃO TOCA O ACORDE INTEIRO, A DIREITA UMA OITAVA ACIMA  •  '
         'OS SELOS E1-E5 / D1-D5 MOSTRAM O DEDO EXATO', 'Anton', 6.2, GRAY, 'c')


def page_tom_b(c, mode, key, sec_num):
    border(c)
    fit(c, W / 2, 29, 'SEÇÃO %d - %s - %s (%s)' % (sec_num, mode['name'],
                                                  key['name'] if not key['alt']
                                                  else '%s / %s' % (key['name'], key['alt']),
                                                  key['pt'] if not key['pt_alt']
                                                  else '%s / %s' % (key['pt'], key['pt_alt'])),
        W - 40, 'Anton', 13, GRAY, 'c')
    pw = (W - 44) / 2.0
    ph = (H - 62) / 2.0
    chord_panel_grid(c, 16, 36, pw, ph - 4, mode, key, CHORD_TYPES[2])
    chord_panel_grid(c, 16 + pw + 8, 36, pw, ph - 4, mode, key, CHORD_TYPES[3])
    chord_panel_grid(c, 16, 36 + ph, pw, ph - 4, mode, key, CHORD_TYPES[4])
    scale_panel_grid(c, 16 + pw + 8, 36 + ph, pw, ph - 4, mode, key)
    text(c, W / 2, H - 16,
         '9ª, 11ª E 13ª COM AS DUAS MÃOS  •  A ESQUERDA FAZ 1-3-5 E A DIREITA COMPLETA O ACORDE',
         'Anton', 6.2, GRAY, 'c')


# =============================================================== montagem
def montar():
    spec = []
    spec.append(('capa', None))
    spec.append(('legenda', None))
    spec.append(('indice', None))
    spec.append(('tabela', None))
    for key in KEYS:
        spec.append(('comp1', key))
        spec.append(('comp2', key))
    sec_pages = {'comparacao': 5}
    pg = len(spec) + 1
    for i, m in enumerate(MODES):
        sec_pages[m['key']] = pg
        spec.append(('secao', (m, i + 1)))
        spec.append(('escalas', m))
        spec.append(('acordes', m))
        for key in KEYS:
            spec.append(('tomA', (m, key, i + 1)))
            spec.append(('tomB', (m, key, i + 1)))
        pg = len(spec) + 1

    c = canvas.Canvas(OUT, pagesize=(W, H))
    c.setTitle('Apostila Teclado - Acordes em todos os modos (Jônio ao Lócrio) - '
               'dedilhado das duas mãos')
    c.setAuthor('Apostila Teclado')
    c.setSubject('Acordes nos 7 modos com o dedilhado das duas mãos')

    for kind, data in spec:
        if kind == 'capa':
            page_capa(c, sec_pages)
        elif kind == 'legenda':
            page_legenda(c)
        elif kind == 'indice':
            page_indice(c, sec_pages)
        elif kind == 'tabela':
            page_tabela_geral(c)
        elif kind == 'comp1':
            page_comparacao(c, data, 1)
        elif kind == 'comp2':
            page_comparacao(c, data, 2)
        elif kind == 'secao':
            page_secao(c, data[0], data[1], 0)
        elif kind == 'escalas':
            page_escalas(c, data)
        elif kind == 'acordes':
            page_acordes(c, data)
        elif kind == 'tomA':
            page_tom_a(c, *data)
        elif kind == 'tomB':
            page_tom_b(c, *data)
        c.showPage()
    c.save()
    print('páginas:', len(spec))
    print(OUT)


if __name__ == '__main__':
    montar()
