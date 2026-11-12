# cenas/tela_selecao.py
# Tela de seleção de personagem.
# NA ETAPA 1 ela é só um "esqueleto" para provar que a TROCA DE CENAS funciona.
# Na Etapa 4 ela vai ganhar os três cartões das espiãs.

import pygame

import config
from cenas.cena import Cena


class TelaSelecao(Cena):
    def __init__(self, jogo):
        super().__init__(jogo)
        self.fonte = pygame.font.Font(None, 40)

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN and evento.key == pygame.K_ESCAPE:
                self.jogo.ir_para_menu()   # ESC volta para a tela inicial

    def desenhar(self, tela):
        tela.fill(config.VERDE_ESCURO)

        linhas = [
            "Tela de Selecao (em construcao)",
            "ESC para voltar",
        ]
        # Laço FOR + enumerate: desenha cada linha um pouco mais abaixo
        for i, linha in enumerate(linhas):
            img = self.fonte.render(linha, True, config.BRANCO)
            rect = img.get_rect(center=(config.LARGURA // 2, config.ALTURA // 2 + i * 50))
            tela.blit(img, rect)
