# jogo.py
# Classe Jogo: o "coração" do programa.
# Ela inicia o Pygame, cria a janela, guarda a cena atual
# e roda o loop principal (eventos -> atualizar -> desenhar).

import pygame

import config
from cenas.tela_inicial import TelaInicial


class Jogo:
    def __init__(self):
        pygame.init()

        # Cria a janela com o tamanho definido no config.py
        self.tela = pygame.display.set_mode((config.LARGURA, config.ALTURA))
        pygame.display.set_caption(config.TITULO)

        # O relógio controla o FPS (quantas vezes por segundo o loop roda)
        self.relogio = pygame.time.Clock()

        # Enquanto for True, o loop principal continua
        self.rodando = True

        # A primeira cena é a tela inicial.
        # Passamos "self" para a cena conseguir falar com o Jogo
        # (por exemplo, pedir para trocar de cena).
        self.cena_atual = TelaInicial(self)

    # ---------- Métodos que as cenas podem chamar ----------

    def trocar_cena(self, nova_cena):
        """Troca a cena que está sendo mostrada."""
        self.cena_atual = nova_cena

    def ir_para_menu(self):
        """Volta para a tela inicial (atalho usado por várias cenas)."""
        self.trocar_cena(TelaInicial(self))

    def sair(self):
        """Encerra o loop principal na próxima volta."""
        self.rodando = False

    # ---------- Loop principal ----------

    def rodar(self):
        while self.rodando:
            # tick() espera o tempo necessário para manter o FPS
            # e devolve quantos milissegundos se passaram.
            # Dividimos por 1000 para ter o tempo em SEGUNDOS (dt).
            dt = self.relogio.tick(config.FPS) / 1000

            # 1) EVENTOS: teclado, mouse, fechar janela...
            eventos = pygame.event.get()
            for evento in eventos:
                if evento.type == pygame.QUIT:   # clicou no X da janela
                    self.sair()

            # Repassamos os eventos para a cena atual tratar do jeito dela
            self.cena_atual.tratar_eventos(eventos)

            # 2) ATUALIZAR: lógica (movimento, colisões, timers...)
            self.cena_atual.atualizar(dt)

            # 3) DESENHAR: tudo que aparece na tela
            self.cena_atual.desenhar(self.tela)

            # Mostra na janela o que foi desenhado neste quadro
            pygame.display.flip()

        pygame.quit()
