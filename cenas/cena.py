# cenas/cena.py
# Classe BASE de todas as telas do jogo (tela inicial, seleção, fase, tela final).
#
# Ideia de Orientação a Objetos usada aqui:
#   - HERANÇA: cada tela "é uma" Cena (class TelaInicial(Cena)).
#   - POLIMORFISMO: o Jogo chama tratar_eventos/atualizar/desenhar
#     sem saber QUAL cena está ativa; cada filha responde do seu jeito.


class Cena:
    def __init__(self, jogo):
        # Guardamos uma referência ao Jogo para poder pedir
        # coisas a ele, como jogo.trocar_cena(...) ou jogo.sair().
        self.jogo = jogo

    def tratar_eventos(self, eventos):
        """Recebe a lista de eventos do Pygame (teclas, mouse...)."""
        pass  # a classe filha substitui (sobrescreve) este método

    def atualizar(self, dt):
        """Lógica do jogo. dt = segundos desde o último quadro."""
        pass

    def desenhar(self, tela):
        """Desenha a cena na superfície 'tela'."""
        pass
