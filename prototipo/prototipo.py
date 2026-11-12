# prototipo.py
# PROTÓTIPO do mapa da mansão: serve só para o grupo sentir como o jogo fica
# e quanto código cada ideia custa. NÃO é o código final do projeto.
#
# Para rodar (dentro desta pasta):  python prototipo.py
#
# Controles:
#   WASD / setas  -> mover a espiã
#   TAB           -> alterna "mapa aberto" <-> "salas com teto"
#   F1            -> modo depuração (mostra paredes e salas; clique mostra a coordenada)
#   ESC           -> sair
#
# Cada bloco abaixo (Jogador, Coletavel, Sala, Inventario, HUD) vira um arquivo
# separado no projeto de verdade, seguindo a arquitetura que já combinamos.

import os
import pygame

import dados_mapa as dados

# ---------------- Configurações (no projeto real ficam no config.py) ----------------
LARGURA, ALTURA = 960, 640
FPS = 60
ESCALA = 0.5          # a imagem tem 1600x1160; com 0.5 ela vira 800x580 e cabe na janela
LARGURA_MAPA = 800    # à direita do mapa sobra uma coluna de 160 px para o HUD
ALTURA_MAPA = 580     # embaixo sobra uma faixa de 60 px para mensagens

PASTA = os.path.dirname(os.path.abspath(__file__))   # pasta onde este arquivo está


def escalar(x, y, largura, altura):
    """Converte um retângulo da imagem ORIGINAL para o tamanho da TELA."""
    return pygame.Rect(round(x * ESCALA), round(y * ESCALA),
                       round(largura * ESCALA), round(altura * ESCALA))


# ===================================================================================
# JOGADOR
# ===================================================================================
class Jogador(pygame.sprite.Sprite):
    VELOCIDADE = 150   # pixels por segundo

    def __init__(self, x, y):
        super().__init__()
        # Desenho provisório: um círculo rosa (depois vira o sprite da espiã)
        self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (235, 80, 170), (6, 6), 6)
        pygame.draw.circle(self.image, (255, 255, 255), (6, 6), 6, 2)
        self.rect = self.image.get_rect(center=(x, y))

    def mover(self, dt, teclas, paredes):
        # 1) Descobre a direção a partir das teclas apertadas
        dx = 0
        dy = 0
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            dx = -1
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            dx = 1
        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            dy = -1
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            dy = 1

        passo = self.VELOCIDADE * dt
        if dx != 0 and dy != 0:
            passo = passo * 0.7071   # na diagonal não pode andar mais rápido

        # 2) Move em X e corrige se bateu numa parede
        self.rect.x += round(dx * passo)
        for parede in paredes:
            if self.rect.colliderect(parede):
                if dx > 0:
                    self.rect.right = parede.left   # bateu andando para a direita
                elif dx < 0:
                    self.rect.left = parede.right   # bateu andando para a esquerda

        # 3) Depois move em Y e corrige do mesmo jeito.
        #    Separar X e Y deixa a espiã "deslizar" encostada na parede.
        self.rect.y += round(dy * passo)
        for parede in paredes:
            if self.rect.colliderect(parede):
                if dy > 0:
                    self.rect.bottom = parede.top
                elif dy < 0:
                    self.rect.top = parede.bottom


# ===================================================================================
# COLETÁVEIS  (classe base + 3 filhas = HERANÇA; cada uma se desenha diferente = POLIMORFISMO)
# ===================================================================================
class Coletavel(pygame.sprite.Sprite):
    def __init__(self, x, y, nome, pontos):
        super().__init__()
        self.nome = nome
        self.pontos = pontos
        self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
        self.desenhar_icone(self.image)          # cada filha desenha do seu jeito
        self.rect = self.image.get_rect(center=(x, y))

    def desenhar_icone(self, superficie):
        pygame.draw.rect(superficie, (255, 255, 255), (0, 0, 12, 12))


class Caderneta(Coletavel):
    def __init__(self, x, y):
        super().__init__(x, y, "Caderneta", 1)

    def desenhar_icone(self, superficie):
        pygame.draw.rect(superficie, (60, 110, 230), (1, 0, 10, 12))      # capa azul
        pygame.draw.line(superficie, (255, 255, 255), (3, 4), (9, 4))     # "linhas"
        pygame.draw.line(superficie, (255, 255, 255), (3, 7), (9, 7))


class PenDrive(Coletavel):
    def __init__(self, x, y):
        super().__init__(x, y, "Pen drive", 2)

    def desenhar_icone(self, superficie):
        pygame.draw.rect(superficie, (40, 190, 80), (3, 3, 6, 9))         # corpo verde
        pygame.draw.rect(superficie, (200, 200, 200), (4, 0, 4, 3))       # ponta USB


class GPU(Coletavel):
    def __init__(self, x, y):
        super().__init__(x, y, "GPU", 3)

    def desenhar_icone(self, superficie):
        pygame.draw.rect(superficie, (240, 190, 40), (0, 2, 12, 8))       # placa dourada
        pygame.draw.circle(superficie, (60, 60, 60), (4, 6), 2)          # ventoinhas
        pygame.draw.circle(superficie, (60, 60, 60), (8, 6), 2)


# Dicionário que liga o texto do arquivo de dados à CLASSE certa
TIPOS = {"caderneta": Caderneta, "pendrive": PenDrive, "gpu": GPU}


# ===================================================================================
# SALA  (é aqui que mora o recurso do "teto")
# ===================================================================================
class Sala:
    VELOCIDADE_FADE = 600   # quanto a transparência muda por segundo (0 a 255)

    def __init__(self, nome, rect, tem_teto, fonte):
        self.nome = nome
        self.rect = rect
        self.tem_teto = tem_teto
        self.opacidade = 255            # 255 = teto fechado; 0 = teto invisível
        self.teto = self._criar_teto(fonte)

    def _criar_teto(self, fonte):
        """Desenha UMA vez a imagem do telhado (fica guardada para todo quadro)."""
        teto = pygame.Surface(self.rect.size)
        teto.fill((70, 45, 35))
        # listras diagonais para parecer telhas
        for i in range(0, self.rect.width + self.rect.height, 12):
            pygame.draw.line(teto, (95, 62, 45), (i, 0), (i - self.rect.height, self.rect.height), 3)
        pygame.draw.rect(teto, (35, 22, 15), teto.get_rect(), 4)   # borda
        texto = fonte.render(self.nome, True, (230, 210, 180))
        teto.blit(texto, texto.get_rect(center=teto.get_rect().center))
        return teto

    def contem(self, ponto):
        return self.rect.collidepoint(ponto)

    def atualizar(self, dt, jogador_esta_aqui, modo_teto):
        # O teto vai sumindo (ou voltando) aos poucos, em vez de piscar de uma vez
        if jogador_esta_aqui or not modo_teto:
            alvo = 0
        else:
            alvo = 255
        if self.opacidade < alvo:
            self.opacidade = min(alvo, self.opacidade + self.VELOCIDADE_FADE * dt)
        elif self.opacidade > alvo:
            self.opacidade = max(alvo, self.opacidade - self.VELOCIDADE_FADE * dt)

    def desenhar_teto(self, tela):
        if self.tem_teto and self.opacidade > 0:
            self.teto.set_alpha(int(self.opacidade))
            tela.blit(self.teto, self.rect)


# ===================================================================================
# INVENTÁRIO  (dicionário com a contagem de cada tipo)
# ===================================================================================
class Inventario:
    def __init__(self):
        self.contagem = {"Caderneta": 0, "Pen drive": 0, "GPU": 0}
        self.pontos = 0

    def adicionar(self, item):
        self.contagem[item.nome] += 1
        self.pontos += item.pontos


# ===================================================================================
# HUD
# ===================================================================================
class HUD:
    def __init__(self):
        self.fonte = pygame.font.Font(None, 24)
        self.fonte_grande = pygame.font.Font(None, 30)
        # um ícone de cada tipo, só para desenhar no painel
        self.icones = {"Caderneta": Caderneta(0, 0).image,
                       "Pen drive": PenDrive(0, 0).image,
                       "GPU": GPU(0, 0).image}

    def texto(self, tela, msg, x, y, cor=(255, 255, 255), fonte=None):
        fonte = fonte or self.fonte
        tela.blit(fonte.render(msg, True, cor), (x, y))

    def desenhar(self, tela, inventario, sala_atual, modo_teto, restantes, mensagem):
        # painel da direita
        pygame.draw.rect(tela, (20, 24, 48), (LARGURA_MAPA, 0, LARGURA - LARGURA_MAPA, ALTURA))
        x = LARGURA_MAPA + 12
        self.texto(tela, "PROTÓTIPO", x, 12, (230, 190, 60), self.fonte_grande)
        self.texto(tela, "Sala:", x, 50, (170, 170, 170))
        self.texto(tela, sala_atual, x, 70)

        y = 110
        for nome, quantidade in inventario.contagem.items():   # um contador por tipo
            tela.blit(pygame.transform.scale(self.icones[nome], (18, 18)), (x, y))
            self.texto(tela, f"{nome}: {quantidade}", x + 26, y + 1)
            y += 30
        self.texto(tela, f"Pontos: {inventario.pontos}", x, y + 6, (230, 190, 60))
        self.texto(tela, f"Faltam: {restantes}", x, y + 30, (170, 170, 170))

        modo = "TETO" if modo_teto else "ABERTO"
        self.texto(tela, "Modo do mapa:", x, 300, (170, 170, 170))
        self.texto(tela, modo, x, 320, (120, 220, 255), self.fonte_grande)

        # faixa de baixo
        pygame.draw.rect(tela, (10, 10, 20), (0, ALTURA_MAPA, LARGURA_MAPA, ALTURA - ALTURA_MAPA))
        self.texto(tela, "WASD/setas: mover   TAB: teto/aberto   F1: depurar   ESC: sair",
                   10, ALTURA_MAPA + 8, (170, 170, 170))
        if mensagem:
            self.texto(tela, mensagem, 10, ALTURA_MAPA + 32, (120, 255, 140))


# ===================================================================================
# PROTÓTIPO (no projeto real isto é a cena Fase)
# ===================================================================================
class Prototipo:
    def __init__(self):
        pygame.init()
        self.tela = pygame.display.set_mode((LARGURA, ALTURA))
        pygame.display.set_caption("Operação Bilionário - protótipo do mapa")
        self.relogio = pygame.time.Clock()
        self.rodando = True

        # Fundo: a imagem do mapa, carregada e reduzida UMA vez só
        caminho = os.path.join(PASTA, dados.IMAGEM)
        imagem = pygame.image.load(caminho).convert()
        self.fundo = pygame.transform.smoothscale(imagem, (LARGURA_MAPA, ALTURA_MAPA))

        # Paredes: lista de retângulos (já na escala da tela)
        self.paredes = [escalar(*p) for p in dados.PAREDES]

        # Salas
        fonte_teto = pygame.font.Font(None, 28)
        self.salas = [Sala(s["nome"], escalar(*s["rect"]), s["tem_teto"], fonte_teto)
                      for s in dados.SALAS]

        # Jogador
        x, y = dados.INICIO_JOGADOR
        self.jogador = Jogador(x * ESCALA, y * ESCALA)

        # Coletáveis: o dicionário TIPOS escolhe qual classe criar
        self.itens = pygame.sprite.Group()
        for tipo, x, y in dados.COLETAVEIS:
            classe = TIPOS[tipo]
            self.itens.add(classe(x * ESCALA, y * ESCALA))

        self.inventario = Inventario()
        self.hud = HUD()
        self.modo_teto = True
        self.depurar = False
        self.mensagem = ""
        self.tempo_mensagem = 0

    def sala_do_jogador(self):
        for sala in self.salas:
            if sala.contem(self.jogador.rect.center):
                return sala
        return None

    def tratar_eventos(self):
        # Proteção contra um bug conhecido do pygame 2.6.1: com um controle de
        # videogame conectado (ou registrado no Windows), event.get() pode dar
        # "SystemError ... KeyError: 0". Em vez de fechar o jogo, pulamos este quadro.
        try:
            eventos = pygame.event.get()
        except SystemError:
            return

        for evento in eventos:
            if evento.type == pygame.QUIT:
                self.rodando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    self.rodando = False
                elif evento.key == pygame.K_TAB:
                    self.modo_teto = not self.modo_teto
                elif evento.key == pygame.K_F1:
                    self.depurar = not self.depurar
            elif evento.type == pygame.MOUSEBUTTONDOWN and self.depurar:
                mx, my = evento.pos
                if mx < LARGURA_MAPA and my < ALTURA_MAPA:
                    # mostra a coordenada na IMAGEM ORIGINAL (para colar no dados_mapa.py)
                    print(f"Clique em ({int(mx / ESCALA)}, {int(my / ESCALA)})")

    def atualizar(self, dt):
        teclas = pygame.key.get_pressed()
        self.jogador.mover(dt, teclas, self.paredes)

        # Colisão com coletáveis: spritecollide devolve a lista do que foi tocado
        # e, com dokill=True, já remove esses itens do grupo.
        pegos = pygame.sprite.spritecollide(self.jogador, self.itens, True)
        for item in pegos:
            self.inventario.adicionar(item)
            self.mensagem = f"Pegou: {item.nome} (+{item.pontos})"
            self.tempo_mensagem = 2.0
            if len(self.itens) == 0:
                self.mensagem = "Tudo coletado! A Central agradece."
                self.tempo_mensagem = 5.0

        if self.tempo_mensagem > 0:
            self.tempo_mensagem -= dt
            if self.tempo_mensagem <= 0:
                self.mensagem = ""

        atual = self.sala_do_jogador()
        for sala in self.salas:
            sala.atualizar(dt, sala is atual, self.modo_teto)

    def desenhar(self):
        self.tela.fill((0, 0, 0))
        self.tela.blit(self.fundo, (0, 0))
        self.itens.draw(self.tela)
        self.tela.blit(self.jogador.image, self.jogador.rect)

        # Os tetos são desenhados POR CIMA de tudo: escondem itens e (no futuro)
        # inimigos das salas onde a espiã não está.
        for sala in self.salas:
            sala.desenhar_teto(self.tela)

        if self.depurar:
            for parede in self.paredes:
                pygame.draw.rect(self.tela, (255, 0, 0), parede, 1)
            for sala in self.salas:
                pygame.draw.rect(self.tela, (255, 255, 0), sala.rect, 1)
            pygame.draw.rect(self.tela, (0, 255, 255), self.jogador.rect, 1)

        atual = self.sala_do_jogador()
        nome_sala = atual.nome if atual else "-"
        self.hud.desenhar(self.tela, self.inventario, nome_sala, self.modo_teto,
                          len(self.itens), self.mensagem)
        pygame.display.flip()

    def rodar(self):
        while self.rodando:
            dt = self.relogio.tick(FPS) / 1000
            self.tratar_eventos()
            self.atualizar(dt)
            self.desenhar()
        pygame.quit()


if __name__ == "__main__":
    Prototipo().rodar()
