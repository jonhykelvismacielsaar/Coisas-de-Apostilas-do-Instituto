# Coisas de Apostilas do Instituto

## Apostilas geradas

| Arquivo | Conteúdo |
|---|---|
| `EU NAVEGAREI - TOM Am - 4 ACORDES (TECLADO).pdf` | Apostila de teclado de **Eu Navegarei** no tom de **Am**, com apenas **4 acordes** (Am → G → F → E) e as **duas mãos em 1-3-5** |

### EU NAVEGAREI — Tom Am (4 acordes)

Sequência única da música: **Am → G → F → E**

| # | Acorde | Notas | Mão esquerda | Mão direita |
|---|---|---|---|---|
| 1 | Am (Lá menor) | A - C - E | 1 - 3 - 5 | 1 - 3 - 5 |
| 2 | G (Sol maior) | G - B - D | 1 - 3 - 5 | 1 - 3 - 5 |
| 3 | F (Fá maior) | F - A - C | 1 - 3 - 5 | 1 - 3 - 5 |
| 4 | E (Mi maior) | E - G# - B | 1 - 3 - 5 | 1 - 3 - 5 |

Páginas do PDF:

1. Os 4 acordes no teclado ilustrado (teclas acesas, numeração dos dedos, E1/E3/E5 e D1/D3/D5) + legenda das mãos.
2. Onde entra cada acorde (intro, verso, refrão, final) e a cifra com a letra.
3. Notas de cada acorde e dicas de estudo.

## Como regerar o PDF

```bash
pip install --break-system-packages reportlab pymupdf
python3 scripts/gerar_apostila_eu_navegarei.py
```

O script `scripts/gerar_apostila_eu_navegarei.py` desenha tudo (teclado, dedilhado e cartões) e usa apenas `assets/mao.png` como imagem.
