# -*- coding: utf-8 -*-
"""Teoria musical usada na apostila: tons, modos, acordes e dedilhado."""

LETTERS = ['C', 'D', 'E', 'F', 'G', 'A', 'B']
NATURAL_PC = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}

# 12 tons: nome principal (bemol quando existe) + nome enarmônico
KEYS = [
    dict(pc=0,  name='C',  alt=None,   pt='DÓ',   pt_alt=None),
    dict(pc=1,  name='Db', alt='C#',   pt='RÉ BEMOL', pt_alt='DÓ SUSTENIDO'),
    dict(pc=2,  name='D',  alt=None,   pt='RÉ',   pt_alt=None),
    dict(pc=3,  name='Eb', alt='D#',   pt='MÍ BEMOL', pt_alt='RÉ SUSTENIDO'),
    dict(pc=4,  name='E',  alt=None,   pt='MÍ',   pt_alt=None),
    dict(pc=5,  name='F',  alt=None,   pt='FÁ',   pt_alt=None),
    dict(pc=6,  name='Gb', alt='F#',   pt='SOL BEMOL', pt_alt='FÁ SUSTENIDO'),
    dict(pc=7,  name='G',  alt=None,   pt='SOL',  pt_alt=None),
    dict(pc=8,  name='Ab', alt='G#',   pt='LÁ BEMOL', pt_alt='SOL SUSTENIDO'),
    dict(pc=9,  name='A',  alt=None,   pt='LÁ',   pt_alt=None),
    dict(pc=10, name='Bb', alt='A#',   pt='SÍ BEMOL', pt_alt='LÁ SUSTENIDO'),
    dict(pc=11, name='B',  alt=None,   pt='SÍ',   pt_alt=None),
]

SHARP_NAMES = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
FLAT_NAMES = ['C', 'Db', 'D', 'Eb', 'E', 'F', 'Gb', 'G', 'Ab', 'A', 'Bb', 'B']

# intervalos (semitons) de cada modo
MODES = [
    dict(key='jonio', num=1, name='JÔNIO', short='MAIOR NATURAL',
         desc='É A PRÓPRIA ESCALA MAIOR NATURAL',
         intervals=[0, 2, 4, 5, 7, 9, 11],
         char=[3, 6], char_text='4 E 7',
         symbols=['', '7M', '7M(9)', '7M(9/11)', '7M(9/11/13)'],
         quality='MAIOR'),
    dict(key='dorico', num=2, name='DÓRICO', short='MENOR COM 6ª MAIOR',
         desc='MENOR COM 6ª MAIOR',
         intervals=[0, 2, 3, 5, 7, 9, 10],
         char=[5], char_text='6',
         symbols=['m', 'm7', 'm7(9)', 'm7(9/11)', 'm7(9/11/13)'],
         quality='MENOR'),
    dict(key='frigio', num=3, name='FRÍGIO', short='MENOR COM 2ª MENOR (b2)',
         desc='MENOR COM 2ª MENOR (b2)',
         intervals=[0, 1, 3, 5, 7, 8, 10],
         char=[1], char_text='b2',
         symbols=['m', 'm7', 'm7(b9)', 'm7(b9/11)', 'm7(b9/11/b13)'],
         quality='MENOR'),
    dict(key='lidio', num=4, name='LÍDIO', short='MAIOR COM 4ª AUMENTADA (#4)',
         desc='MAIOR COM 4ª AUMENTADA (#4)',
         intervals=[0, 2, 4, 6, 7, 9, 11],
         char=[3], char_text='#4',
         symbols=['', '7M', '7M(9)', '7M(9/#11)', '7M(9/#11/13)'],
         quality='MAIOR'),
    dict(key='mixolidio', num=5, name='MIXOLÍDIO', short='MAIOR COM 7ª MENOR (b7)',
         desc='MAIOR COM 7ª MENOR (b7)',
         intervals=[0, 2, 4, 5, 7, 9, 10],
         char=[6], char_text='b7',
         symbols=['', '7', '7(9)', '7(9/11)', '7(9/11/13)'],
         quality='MAIOR'),
    dict(key='eolio', num=6, name='EÓLIO', short='É A ESCALA MENOR NATURAL (6ª MENOR)',
         desc='É A ESCALA MENOR NATURAL (6ª MENOR)',
         intervals=[0, 2, 3, 5, 7, 8, 10],
         char=[5], char_text='b6',
         symbols=['m', 'm7', 'm7(9)', 'm7(9/11)', 'm7(9/11/b13)'],
         quality='MENOR'),
    dict(key='locrio', num=7, name='LÓCRIO', short='MENOR COM 2ª MENOR E 5ª DIMINUTA (b2 E b5)',
         desc='MENOR COM 2ª MENOR E 5ª DIMINUTA (b2 E b5)',
         intervals=[0, 1, 3, 5, 6, 8, 10],
         char=[1, 4], char_text='b2 E b5',
         symbols=['°', 'm7(b5)', 'm7(b5/b9)', 'm7(b5/b9/11)', 'm7(b5/b9/11/b13)'],
         quality='DIMINUTO'),
]

MODES_BY_KEY = {m['key']: m for m in MODES}

# tipos de acorde: nome, quantos graus, índices de grau usados
CHORD_TYPES = [
    dict(key='triade', label='TRÍADE',   degrees=[0, 2, 4],              name='TRÍADE'),
    dict(key='tetrade', label='TÉTRADE', degrees=[0, 2, 4, 6],           name='TÉTRADE'),
    dict(key='nona',    label='COM 9ª',  degrees=[0, 2, 4, 6, 1],        name='COM 9ª'),
    dict(key='onze',    label='COM 11ª', degrees=[0, 2, 4, 6, 1, 3],     name='COM 11ª'),
    dict(key='treze',   label='COM 13ª', degrees=[0, 2, 4, 6, 1, 3, 5],  name='COM 13ª'),
]

# rótulo de grau que aparece no acorde (1,3,5,7,9,11,13)
CHORD_DEGREE_LABEL = {0: '1', 2: '3', 4: '5', 6: '7', 1: '9', 3: '11', 5: '13'}

MAJOR_REF = [0, 2, 4, 5, 7, 9, 11]


def spell(tonic_name, deg_index, pc_target):
    """Escreve a nota do grau deg_index (0-6) usando a letra certa da escala."""
    li = LETTERS.index(tonic_name[0])
    letter = LETTERS[(li + deg_index) % 7]
    natural = NATURAL_PC[letter]
    acc = (pc_target - natural) % 12
    if acc > 6:
        acc -= 12
    if acc == 0:
        return letter
    if acc > 0:
        return letter + '#' * acc
    return letter + 'b' * (-acc)


def degree_label(mode, deg_index):
    """Rótulo do grau (1, b2, b3, 4, #4, 5, b6, 6, b7, 7...)."""
    iv = mode['intervals'][deg_index]
    ref = MAJOR_REF[deg_index]
    if iv == ref:
        return str(deg_index + 1)
    if iv < ref:
        return 'b' * (ref - iv) + str(deg_index + 1)
    return '#' * (iv - ref) + str(deg_index + 1)


def chord_degree_label(mode, deg_index):
    """Rótulo do grau dentro do acorde (1, 3, 5, 7, 9, b9, 11, #11, 13, b13)."""
    base = degree_label(mode, deg_index)
    num = CHORD_DEGREE_LABEL[deg_index]
    prefix = base[:-1]
    return prefix + num


def note_name(tonic_name, deg_index, pc):
    """Nome da nota já escrito + alias enarmônico quando fizer sentido."""
    name = spell(tonic_name, deg_index, pc)
    if name in (FLAT_NAMES[pc], SHARP_NAMES[pc]):
        alias = SHARP_NAMES[pc] if name == FLAT_NAMES[pc] else FLAT_NAMES[pc]
    elif FLAT_NAMES[pc] == SHARP_NAMES[pc]:
        alias = FLAT_NAMES[pc]
    else:
        alias = FLAT_NAMES[pc] if 'b' in name else SHARP_NAMES[pc]
    if alias == name:
        alias = None
    return name, alias


class Note(object):
    """Uma nota do acorde/escala posicionada no teclado."""

    def __init__(self, pitch, deg_index, label, mode, key):
        self.pitch = pitch              # semitons a partir da tônica no registro 0
        self.deg_index = deg_index
        self.label = label              # 1, b3, 5, 7, 9...
        self.is_char = deg_index in mode['char']
        pc = (key['pc'] + pitch) % 12
        self.name, self.alias = note_name(key['name'], deg_index, pc)
        self.pc = pc
        self.octave = pitch // 12       # 0,1,2 (registro do diagrama)

    @property
    def display(self):
        return self.name

    @property
    def keyboard_name(self):
        if self.alias:
            return '%s(%s)' % (self.name, self.alias)
        return self.name


def build_chord(mode, key, ctype):
    """Constrói as notas do acorde (sempre empilhadas a partir da tônica)."""
    scale = []
    for i, iv in enumerate(mode['intervals']):
        scale.append(iv)
    notes = []
    for di in ctype['degrees']:
        base = scale[di]
        if di in (0, 2, 4, 6):
            pitch = base
        else:  # extensões uma oitava acima
            pitch = base + 12
        notes.append(Note(pitch, di, chord_degree_label(mode, di), mode, key))
    return notes


def build_scale(mode, key):
    return [Note(iv, i, degree_label(mode, i), mode, key)
            for i, iv in enumerate(mode['intervals'])]


def chord_symbol(mode, key, ctype, alt=False):
    name = key['alt'] if alt and key['alt'] else key['name']
    idx = [c['key'] for c in CHORD_TYPES].index(ctype['key'])
    return name + mode['symbols'][idx]


def chord_symbol_both(mode, key, ctype):
    s = chord_symbol(mode, key, ctype)
    if key['alt']:
        return s + ' / ' + chord_symbol(mode, key, ctype, alt=True)
    return s


# ---------------------------------------------------------------- dedilhado
# A numeração é a mesma da apostila: na mão esquerda 1 = mínimo ... 5 = polegar;
# na mão direita 1 = polegar ... 5 = mínimo.  Nos dois casos o dedo 1 é o mais
# grave da mão e o 5 o mais agudo, então os números sobem junto com as notas.
FINGER_NAMES = {
    'E': {1: 'MÍNIMO', 2: 'ANELAR', 3: 'MÉDIO', 4: 'INDICADOR', 5: 'POLEGAR'},
    'D': {1: 'POLEGAR', 2: 'INDICADOR', 3: 'MÉDIO', 4: 'ANELAR', 5: 'MÍNIMO'},
}


def voicing(notes, ctype):
    """Divide as notas entre as duas mãos e devolve (mão esquerda, mão direita).

    Cada item: dict(note=Note, finger=int, hand='E'/'D', octave=int)
    TRÍADE e TÉTRADE: cada mão faz o acorde completo (a direita uma oitava acima).
    9ª/11ª/13ª: a esquerda faz 1-3-5 e a direita completa 7-9(-11-13).
    """
    k = ctype['key']
    if k == 'triade':
        lh_oct, lh_fing = 0, [1, 3, 5]
        rh_oct, rh_fing = 12, [1, 3, 5]
        lh_notes, rh_notes = notes, notes
    elif k == 'tetrade':
        lh_oct, lh_fing = 0, [1, 3, 4, 5]
        rh_oct, rh_fing = 12, [1, 2, 3, 5]
        lh_notes, rh_notes = notes, notes
    elif k == 'nona':
        lh_oct, lh_fing = 0, [1, 3, 5]
        rh_oct, rh_fing = 0, [1, 2]
        lh_notes, rh_notes = notes[:3], notes[3:]
    elif k == 'onze':
        lh_oct, lh_fing = 0, [1, 3, 5]
        rh_oct, rh_fing = 0, [1, 2, 3]
        lh_notes, rh_notes = notes[:3], notes[3:]
    else:
        lh_oct, lh_fing = 0, [1, 3, 5]
        rh_oct, rh_fing = 0, [1, 2, 3, 4]
        lh_notes, rh_notes = notes[:3], notes[3:]

    lh = []
    for n, f in zip(lh_notes, lh_fing):
        lh.append(dict(note=n, finger=f, hand='E', pitch=n.pitch + lh_oct))
    rh = []
    for n, f in zip(rh_notes, rh_fing):
        rh.append(dict(note=n, finger=f, hand='D', pitch=n.pitch + rh_oct))
    return lh, rh


def fingering_text(hand, items):
    return '  '.join('%d %s = %s' % (it['finger'], FINGER_NAMES[hand][it['finger']],
                                     it['note'].display) for it in items)


def fingering_seq(hand, items):
    return '-'.join(str(it['finger']) for it in items)


# ---------------------------------------------------------------- descrições
def chord_description(mode, key, ctype):
    k = ctype['key']
    pt = key['pt']
    alt = key['pt_alt']
    base = pt if not alt else pt + ' / ' + alt
    mk = mode['key']
    if k == 'triade':
        q = {'MAIOR': 'MAIOR', 'MENOR': 'MENOR', 'DIMINUTO': 'DIMINUTO'}[mode['quality']]
        return '%s %s' % (base, q)
    if k == 'tetrade':
        if mk in ('jonio', 'lidio'):
            return '%s COM SÉTIMA MAIOR' % base
        if mk == 'mixolidio':
            return '%s COM SÉTIMA' % base
        if mk == 'locrio':
            return '%s MENOR COM 5ª BEMOL E 7ª' % base
        return '%s MENOR COM SÉTIMA' % base
    if k == 'nona':
        if mk in ('jonio', 'lidio'):
            return '%s COM SÉTIMA MAIOR E NONA' % base
        if mk == 'mixolidio':
            return '%s COM SÉTIMA E NONA' % base
        if mk == 'locrio':
            return '%s MENOR COM 5ª BEMOL, 7ª E NONA MENOR' % base
        if mk == 'frigio':
            return '%s MENOR COM SÉTIMA E NONA MENOR' % base
        return '%s MENOR COM SÉTIMA E NONA' % base
    if k == 'onze':
        if mk == 'jonio':
            return '%s COM 7ª MAIOR, NONA E 11ª' % base
        if mk == 'lidio':
            return '%s COM 7ª MAIOR, NONA E 11ª AUMENTADA' % base
        if mk == 'mixolidio':
            return '%s COM 7ª, NONA E 11ª' % base
        if mk == 'locrio':
            return '%s MENOR COM 5ª BEMOL, 7ª, NONA MENOR E 11ª' % base
        if mk == 'frigio':
            return '%s MENOR COM 7ª, NONA MENOR E 11ª' % base
        return '%s MENOR COM 7ª, NONA E 11ª' % base
    # 13ª
    if mk == 'jonio':
        return '%s COM 7ª MAIOR, NONA, 11ª E 13ª' % base
    if mk == 'lidio':
        return '%s COM 7ª MAIOR, NONA, 11ª AUMENTADA E 13ª' % base
    if mk == 'mixolidio':
        return '%s COM 7ª, NONA, 11ª E 13ª' % base
    if mk == 'locrio':
        return '%s MENOR COM 5ª BEMOL E 13ª MENOR' % base
    if mk in ('eolio', 'frigio'):
        return '%s MENOR COM 7ª, NONA, 11ª E 13ª MENOR' % base
    return '%s MENOR COM 7ª, NONA, 11ª E 13ª' % base


def relative_major(mode, key):
    """'MESMAS NOTAS DE' — a escala maior que contém o modo."""
    # o modo começa no grau (num) da escala maior; a tônica maior está (num-1)
    # graus abaixo na escala maior -> subir (8 - num) graus na escala maior
    major_pc = (key['pc'] - mode['intervals'][mode['num'] - 1]) % 12
    name = FLAT_NAMES[major_pc]
    alt = SHARP_NAMES[major_pc] if SHARP_NAMES[major_pc] != name else None
    if alt:
        return '%s / %s MAIOR' % (name, alt)
    return '%s MAIOR' % name
