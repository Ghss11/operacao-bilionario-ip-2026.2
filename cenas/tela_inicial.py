# cenas/tela_inicial.py
# Primeira tela: título do jogo + "Pressione ENTER".
# Nesta Etapa 1 ela é simples; na Etapa 4 vamos caprichar no visual.

import pygame

import config
from cenas.cena import Cena


class TelaInicial(Cena):
    def __init__(self, jogo):
        super().__init__(jogo)  # roda o __init__ da classe mãe (Cena)

        # Fontes: None = fonte padrão do Pygame (não precisa de arquivo).
        # Criamos as fontes UMA vez aqui, e não a cada quadro (fica mais rápido).
        self.fonte_titulo = pygame.font.Font(None, 80)
        self.fonte_texto = pygame.font.Font(None, 36)

        # Contador de tempo para fazer o "Pressione ENTER" piscar
        self.tempo = 0

    def tratar_eventos(self, eventos):
        for evento in eventos:
            if evento.type == pygame.KEYDOWN:          # alguma tecla foi apertada
                if evento.key == pygame.K_RETURN:       # foi o ENTER?
                    # Import aqui dentro para evitar "import circular"
                    # (TelaSelecao também pode querer importar TelaInicial).
                    from cenas.tela_selecao import TelaSelecao
                    self.jogo.trocar_cena(TelaSelecao(self.jogo))
                elif evento.key == pygame.K_ESCAPE:     # ESC fecha o jogo
                    self.jogo.sair()

    def atualizar(self, dt):
        self.tempo += dt

    def desenhar(self, tela):
        tela.fill(config.AZUL_ESCURO)

        # 1) Título centralizado
        titulo = self.fonte_titulo.render(config.TITULO, True, config.DOURADO)
        rect_titulo = titulo.get_rect(center=(config.LARGURA // 2, config.ALTURA // 3))
        tela.blit(titulo, rect_titulo)

        # 2) "Pressione ENTER" piscando: aparece meio segundo, some meio segundo
        if int(self.tempo * 2) % 2 == 0:
            texto = self.fonte_texto.render("Pressione ENTER", True, config.BRANCO)
            rect_texto = texto.get_rect(center=(config.LARGURA // 2, config.ALTURA * 2 // 3))
            tela.blit(texto, rect_texto)
