# Apostila Teclado — Acordes em todos os modos (com o dedilhado das duas mãos)

Esta pasta contém a apostila em PDF:

**`APOSTILA TECLADO - ACORDES EM TODOS OS MODOS (DUAS MÃOS).pdf`** — 217 páginas, A4 paisagem.

É a mesma apostila original (Acordes em todos os modos — do Jônio ao Lócrio), com o **mesmo layout**,
mas agora **mostrando como montar cada acorde com as duas mãos, com o dedo exato em cima de cada nota**.

## O que mudou em relação à versão original

| Item | Antes | Agora |
|---|---|---|
| Tríade e tétrade | Uma mão por vez (página da esquerda e da direita) | **As duas mãos na mesma página**, uma oitava de distância, com o dedilhado das duas |
| 9ª, 11ª e 13ª | Já eram com as duas mãos, mas só mostravam o número do dedo solto | Teclado + **selos E1-E5 / D1-D5 sobre cada nota** + lista "dedo → nota → nome do dedo" + foto da mão |
| Fotos das mãos | Só na legenda | Em **toda página de acorde**, com os dedos usados destacados |
| Tabelas | Só os cifrados | Tabelas com **dedilhado (ESQ./DIR.) de cada acorde** em todos os 12 tons |
| Página nova | — | "Como ler esta apostila", índice e quadro **"o que cada mão faz"** em cada tom |

## Dedilhado usado (padrão da apostila, aplicado em todos os 12 tons)

Numeração igual à do material original: **mão esquerda 1 = mínimo … 5 = polegar**;
**mão direita 1 = polegar … 5 = mínimo** (nos dois casos o dedo 1 é a nota mais grave da mão).

| Acorde | Mão esquerda | Mão direita | O que cada mão toca |
|---|---|---|---|
| Tríade | 1 - 3 - 5 | 1 - 3 - 5 | a direita toca o mesmo acorde 1 oitava acima |
| Tétrade | 1 - 3 - 4 - 5 | 1 - 2 - 3 - 5 | a direita toca o mesmo acorde 1 oitava acima |
| Com 9ª | 1 - 3 - 5 | 1 - 2 | esquerda 1-3-5 / direita 7ª e 9ª |
| Com 11ª | 1 - 3 - 5 | 1 - 2 - 3 | esquerda 1-3-5 / direita 7ª, 9ª e 11ª |
| Com 13ª | 1 - 3 - 5 | 1 - 2 - 3 - 4 | esquerda 1-3-5 / direita 7ª, 9ª, 11ª e 13ª |

## Estrutura (217 páginas)

1. Capa
2. Como ler esta apostila (símbolos, numeração dos dedos, dedilhado padrão)
3. Índice
4. Tabela geral dos 7 modos + quadro "como tocar com as duas mãos"
5. **Seção 0** — comparação dos 7 modos nos 12 tons (2 páginas por tom)
6. **Seções 1 a 7** — um modo por seção (Jônio, Dórico, Frígio, Lídio, Mixolídio, Eólio, Lócrio):
   - capa da seção
   - tabela das escalas nos 12 tons (nota característica destacada)
   - tabela dos acordes nos 12 tons com o dedilhado de cada mão
   - **2 páginas por tom**: tríade + tétrade (com as duas mãos) e 9ª + 11ª + 13ª + escala

## Como regerar o PDF

```bash
pip install reportlab pymupdf
python3 work/gerar.py
```

Arquivos do gerador (pasta `work/`):

- `teoria.py` — tons, modos, grafia das notas, montagem dos acordes e regra de dedilhado (voicing)
- `desenho.py` — cores, fontes (Anton / Archivo Black), teclado vetorial, selos e molduras
- `paginas.py` — painéis de acorde (grande), painéis de grade, escala e mapa das mãos
- `gerar.py` — monta as 217 páginas na ordem final
- `assets/` — fontes e a foto da mão já recortada (`mao_esq.png` / `mao_dir.png`)

O PDF é vetorial e pesquisável (texto real), então imprime em qualquer tamanho sem perder qualidade.
