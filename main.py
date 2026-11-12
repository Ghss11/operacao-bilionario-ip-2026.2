# main.py
# Ponto de entrada do jogo. Ele só faz duas coisas:
# cria o objeto Jogo e manda ele rodar.
# Para executar:  python main.py

from jogo import Jogo


def main():
    jogo = Jogo()
    jogo.rodar()


# Este "if" garante que main() só roda quando executamos
# este arquivo diretamente (e não quando ele é importado).
if __name__ == "__main__":
    main()
