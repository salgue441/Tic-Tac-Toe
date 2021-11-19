""" Parte principal del programa """
from game import Game # importa del archivo Game

game = Game()

# Función principal
def main():
    running = True

    while running:
        game.run_game()

""" al utilizar un diferente archivo para los contenidos del juego, 
utilcé __name__ == "__main__" para que solo si el nombre es main se corra
el juego"""
if __name__ == "__main__":
    main()


