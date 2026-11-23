# dados_mapa_tecnologica.py
# DADOS da mansão "Super tecnológica" (sem nenhuma lógica e sem importar pygame).
#
# Mesmo formato do dados_mapa.py: todas as medidas estão em pixels da
# IMAGEM ORIGINAL (1600 x 1160). Cada retângulo é uma tupla (x, y, largura, altura).
#
# Salas (mesma planta da mansão original, com outro tema):
#   Sala do Telão (Mita)  -> era a sala de música
#   Servidores            -> era a biblioteca
#   Hall                  -> igual, mas com o ELEVADOR no lugar da escadaria
#   Escritório            -> era a cozinha (10 monitores na parede do fundo)
#   Mitaverso             -> era a despensa
#   Octógono              -> era a sala de jantar

IMAGEM = "mapa_mansao_tecnologica.jpg"
# Mesmo mapa, só que com a porta do elevador fechada (usada enquanto o elevador sobe)
IMAGEM_ELEVADOR_FECHADO = "mapa_mansao_tecnologica_elevador_fechado.jpg"
TAMANHO_ORIGINAL = (1600, 1160)

# Onde a espiã começa: no hall, perto da porta de entrada
INICIO_JOGADOR = (820, 950)

# ---------- ELEVADOR ----------
# "rect": área onde o jogador encosta para usar o elevador (fica logo abaixo da
#         porta aberta desenhada na parede do fundo do hall).
# "sobe_para": andar de destino (este mapa é o andar 1, então sobe para o 2).
# "mapa_destino": nome do arquivo de dados do andar de destino (sem o .py).
# A porta fica sempre aberta; ao encostar, o jogo troca para IMAGEM_ELEVADOR_FECHADO
# (não existe animação) e o elevador leva o jogador para o andar de cima.
ELEVADOR = {
    "rect": (785, 190, 70, 55),
    "sobe_para": 2,
    "mapa_destino": "dados_mapa_tecnologica_andar2",
}

# ---------- PAREDES (e móveis grandes que bloqueiam a passagem) ----------
PAREDES = [
    # Bordas externas da casa
    (0, 0, 1600, 25),        # topo
    (0, 0, 40, 1160),        # esquerda
    (1560, 0, 40, 1160),     # direita
    (0, 1000, 800, 160),     # fachada de baixo (lado esquerdo da porta)
    (840, 1000, 760, 160),   # fachada de baixo (lado direito da porta)
    (800, 1040, 40, 120),    # a porta em si (por enquanto ela não deixa sair)

    # Sala do Telão (cima, à esquerda)
    (40, 25, 480, 175),      # parede do fundo com o telão da Mita
    (520, 0, 40, 400),       # parede entre a sala e o hall (a passagem fica embaixo)
    (40, 440, 320, 30),      # parede de baixo, à esquerda da passagem
    (440, 440, 120, 30),     # parede de baixo, à direita da passagem

    # Sala dos Servidores (baixo, à esquerda)
    (520, 470, 40, 530),     # parede entre a sala e o hall
    (40, 470, 320, 160),     # parede do fundo (racks)
    (440, 470, 80, 140),     # parede do fundo (depois da passagem)
    # racks em 2 fileiras com corredores largos (passagem mínima de 70 px):
    # esquerda 70 | entre os racks 140 | direita 70 | entre as fileiras 80
    (110, 710, 100, 64),     # fileira de cima, esquerda
    (350, 710, 100, 64),     # fileira de cima, direita
    (110, 854, 100, 64),     # fileira de baixo, esquerda
    (350, 854, 100, 64),     # fileira de baixo, direita

    # Hall (centro)
    (560, 25, 200, 140),     # nicho da esquerda
    (760, 25, 120, 165),     # parede do fundo com a porta do elevador (o resto da escadaria agora é chão livre)
    (880, 25, 160, 140),     # nicho da direita
    (1040, 0, 40, 270),      # parede direita do hall, parte de cima
    (1040, 520, 40, 480),    # parede direita do hall, parte de baixo

    # Escritório (cima, à direita) - 10 monitores na parede do fundo
    (1080, 25, 480, 155),    # parede do fundo + mesas com os 10 monitores
    (1040, 240, 160, 30),    # parede de baixo, antes da passagem
    (1282, 240, 280, 30),    # parede de baixo, depois da passagem

    # Sala do Mitaverso (meio, à direita)
    (1040, 270, 160, 170),   # globo holográfico
    (1282, 270, 280, 150),   # telão do metaverso
    (1080, 520, 160, 30),    # parede de baixo, antes da passagem
    (1320, 520, 240, 30),    # parede de baixo, depois da passagem

    # Octógono (baixo, à direita)
    (1080, 550, 160, 150),   # parede do fundo
    (1320, 550, 240, 150),
    (1160, 780, 320, 125),   # o octógono (arena)
]

# ---------- SALAS (usadas para o "teto" e para mostrar onde a espiã está) ----------
# tem_teto = False: a sala nunca é coberta (o hall fica sempre visível)
SALAS = [
    {"nome": "Sala do Telao",  "rect": (25, 20, 495, 420),   "tem_teto": True},
    {"nome": "Servidores",     "rect": (25, 440, 495, 565),  "tem_teto": True},
    {"nome": "Hall",           "rect": (520, 20, 520, 985),  "tem_teto": False},
    {"nome": "Escritorio",     "rect": (1040, 20, 535, 235), "tem_teto": True},
    {"nome": "Mitaverso",      "rect": (1040, 255, 535, 280), "tem_teto": True},
    {"nome": "Octogono",       "rect": (1040, 535, 535, 470), "tem_teto": True},
]

# ---------- COLETÁVEIS ----------
# (tipo, x, y). O tipo precisa ser "caderneta", "pendrive" ou "gpu".
# Mesmas posições do mapa original (todas continuam em área livre).
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
