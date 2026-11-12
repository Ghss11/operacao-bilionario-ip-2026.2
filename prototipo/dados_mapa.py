# dados_mapa.py
# DADOS do mapa da mansão (sem nenhuma lógica e sem importar pygame).
#
# Todas as medidas estão em pixels da IMAGEM ORIGINAL (1600 x 1160).
# Para descobrir uma posição nova: rode o protótipo, aperte F1 e
# clique no mapa. O terminal mostra a coordenada já convertida para a imagem original.
#
# Cada retângulo é uma tupla (x, y, largura, altura).

IMAGEM = "mapa_mansao.jpg"
TAMANHO_ORIGINAL = (1600, 1160)

# Onde a espiã começa: no hall, perto da porta de entrada
INICIO_JOGADOR = (820, 950)

# ---------- PAREDES (e móveis grandes que bloqueiam a passagem) ----------
PAREDES = [
    # Bordas externas da casa
    (0, 0, 1600, 25),        # topo
    (0, 0, 40, 1160),        # esquerda
    (1560, 0, 40, 1160),     # direita
    (0, 1000, 800, 160),     # fachada de baixo (lado esquerdo da porta)
    (840, 1000, 760, 160),   # fachada de baixo (lado direito da porta)
    (800, 1040, 40, 120),    # a porta em si (por enquanto ela não deixa sair)

    # Sala de música (cima, à esquerda)
    (40, 25, 480, 175),      # parede do fundo + estantes
    (520, 0, 40, 400),       # parede entre a sala e o hall (a passagem fica embaixo)
    (40, 440, 320, 30),      # parede de baixo, à esquerda da passagem
    (440, 440, 120, 30),     # parede de baixo, à direita da passagem

    # Biblioteca (baixo, à esquerda)
    (520, 470, 40, 530),     # parede entre a biblioteca e o hall
    (40, 470, 320, 160),     # parede do fundo
    (440, 470, 80, 140),     # parede do fundo (depois da passagem)
    (120, 740, 120, 75),     # estantes
    (280, 740, 240, 75),
    (120, 860, 120, 80),
    (280, 860, 240, 80),

    # Hall (centro)
    (560, 25, 200, 140),     # nicho da esquerda (armários)
    (760, 25, 120, 455),     # escadaria (por enquanto não sobe)
    (880, 25, 160, 140),     # nicho da direita (armários)
    (1040, 0, 40, 270),      # parede direita do hall, parte de cima
    (1040, 520, 40, 480),    # parede direita do hall, parte de baixo

    # Cozinha (cima, à direita)
    (1080, 25, 480, 155),    # parede do fundo + fogão e armários
    (1040, 240, 160, 30),    # parede de baixo, antes da passagem
    (1282, 240, 280, 30),    # parede de baixo, depois da passagem

    # Despensa (meio, à direita)
    (1040, 270, 160, 170),   # estante e relógio
    (1282, 270, 280, 150),   # prateleiras de comida
    (1080, 520, 160, 30),    # parede de baixo, antes da passagem
    (1320, 520, 240, 30),    # parede de baixo, depois da passagem

    # Sala de jantar (baixo, à direita)
    (1080, 550, 160, 150),   # parede do fundo + armários
    (1320, 550, 240, 150),
    (1160, 780, 320, 125),   # mesa com cadeiras
]

# ---------- SALAS (usadas para o "teto" e para mostrar onde a espiã está) ----------
# tem_teto = False: a sala nunca é coberta (o hall fica sempre visível)
SALAS = [
    {"nome": "Sala de musica", "rect": (25, 20, 495, 420),   "tem_teto": True},
    {"nome": "Biblioteca",     "rect": (25, 440, 495, 565),  "tem_teto": True},
    {"nome": "Hall",           "rect": (520, 20, 520, 985),  "tem_teto": False},
    {"nome": "Cozinha",        "rect": (1040, 20, 535, 235), "tem_teto": True},
    {"nome": "Despensa",       "rect": (1040, 255, 535, 280), "tem_teto": True},
    {"nome": "Sala de jantar", "rect": (1040, 535, 535, 470), "tem_teto": True},
]

# ---------- COLETÁVEIS ----------
# (tipo, x, y). O tipo precisa ser "caderneta", "pendrive" ou "gpu".
COLETAVEIS = [
    ("caderneta", 110, 300),
    ("pendrive", 470, 380),
    ("caderneta", 400, 690),
    ("pendrive", 70, 960),
    ("gpu", 260, 840),
    ("caderneta", 620, 600),
    ("pendrive", 990, 880),
    ("gpu", 1520, 215),
    ("caderneta", 1420, 470),
    ("gpu", 1120, 950),
    ("pendrive", 1520, 750),
]
