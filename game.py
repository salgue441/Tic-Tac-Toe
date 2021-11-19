import sys, time, pygame as pg
from pygame import rect
from pygame.locals import *

ganador, empate = None, None

class Game:
    def __init__(self):
        # variables generales
        global ganador, empate
        self.ganador, self.empate = ganador, empate # eventos de ganador o empate
        self.width, self.height = int(600), int(600) # propiedades de la ventana
        self.tablero = [[None] * 3, [None] * 3, [None] * 3] # matriz del tablero, tamaño 3 x 3
        self.XO = 'x'

        # Colores
        # Equivalencias en HEX: blanco -> (#ffffff), verde -> (#0acf83), negro -> (#000000)
        self.BLANCO, self.VERDE, self.NEGRO = (255, 255, 255), (10, 207, 131), (0, 0, 0)
        # asignando colores a las líneas
        self.linea_de_tablero, self.linea_de_ganador = self.NEGRO, self.VERDE

    """ Función que crea la ventana de inicio """
    def ventana_de_inicio(self, screen, cover):
        # screen.fill(self.BLANCO)
        time.sleep(6)

        # poniendo la imagen en pantalla
        time.sleep(6) # transición
        screen.blit(cover, (0, 0))

        # refrescando la pantalla 
        pg.display.update()

        time.sleep(5) # transición
        screen.fill(self.BLANCO)

    """ Función que dibuja las líneas del tablero """
    def dibuja_lineas_de_tablero(self, screen):
        # line parameters: (surface, color, start_pos, end_pos, width(int))
        # líneas verticales
        pg.draw.line(screen, self.linea_de_tablero, (self.width / 3, self.height - 475), \
            (self.width / 3, self.height + 100), 5)
        pg.draw.line(screen, self.linea_de_tablero, (self.width / 3 * 2, self.height - 475), \
            (self.width / 3 * 2, self.height + 100), 5)

        # líneas horizontales
        pg.draw.line(screen, self.linea_de_tablero, (0, self.height / 3 * 1.5), \
            (self.width, self.height / 3 * 1.5), 5)
        pg.draw.line(screen, self.linea_de_tablero, (0, self.height / 3 * 2.5), \
            (self.width, self.height / 3 * 2.5), 5)

    """ Muestra en pantalla el turno del jugador; si hay ganador o empate """
    def estatus_de_empate_o_ganador(self, screen):
        # muestra el turno de cada jugador
        global ganador, empate
        if (ganador == None):
            mensaje = "Turno de: " + self.XO.upper()
        # en caso de ganador muestra "usuario ganó!"
        else:
            mensaje = ganador.upper() + " ganó!"
        
        # en caso de empate muestra "Empate!"
        if (empate == True):
            mensaje = "Empate!"

        # parámetros -> render(text, antialias, color, background = None) -> Surface
        cursive_font = pg.font.Font("assets/Fonts/Pacifico-Regular.ttf", 32)
        texto = cursive_font.render(mensaje, True, self.VERDE)

        # parámetros -> fill(color, rect = None, special_flags = 0) -> rect
        screen.fill((self.BLANCO), (0, 0, 600, 100)) #crea separación entre el texto y lo demás

        # posición del texto en pantalla
        texto_rect = texto.get_rect(midtop = (self.width / 2, self.height - 580))
        screen.blit(texto, texto_rect) # muestra el texto en su posición en la pantalla

    """ Función que muestra una línea en los tres en línea """
    def buscando_ganador(self, screen):
        """ Busca al ganador al buscar tres en línea. Busca al ganador en vertical, horizontal, 
        diagonal de izquierda a derecha y derecha a izquierda. """
        global ganador, empate
        # buscando ganador en filas
        for row in range(0, 3):
            if ((self.tablero[row][0] == self.tablero[row][1] == self.tablero[row][2]) and \
                (self.tablero[row][0] is not None)):
                ganador = self.tablero[row][0] # asignando ganador a la casilla [row][0]
                # dibujando la línea de ganador
                pg.draw.line(screen, self.linea_de_ganador, \
                    (0, (row + 1) * self.height / 3  ), \
                    (self.width, (row + 1) * self.height / 3 ), 4)
                break
        
        # buscando ganador en columnas
        for col in range(0, 3):
            if ((self.tablero[0][col] == self.tablero[1][col] == self.tablero[2][col]) and \
                (self.tablero[0][col] is not None)):
                ganador = self.tablero[0][col] # asignando ganador a casilla [0][col]
                # dibujando línea de ganador
                pg.draw.line(screen, self.linea_de_ganador, 
                    ((col + 1) * self.width / 3 - self.width / 6, self.height - 475), \
                    ((col + 1) * self.width / 3 - self.width / 6, self.height + 100), 4)
                break

        # buscando ganador en diagonal -> izquierda a derecha
        if ((self.tablero[0][0] == self.tablero[1][1] == self.tablero[2][2]) and \
            (self.tablero[0][0] is not None)):
            ganador = self.tablero[0][0] # asignando ganador en casilla [0][0]
            pg.draw.line(screen, self.linea_de_ganador, (-100, 0), (self.width, self.height + 100), 4)

        # buscando ganador en giadonal -> derecha a izquierda
        if ((self.tablero[0][2] == self.tablero[1][1] == self.tablero[2][0]) and \
            (self.tablero[0][2] is not None)):
            ganador = self.tablero[0][2]
            pg.draw.line(screen, self.linea_de_ganador, (0, 700), (700, 0), 4)

        # en caso de no haber ganador, revisa todas las filas y devuelve empate
        if (all([all(row) for row in self.tablero]) and self.ganador is None):
            empate = True
        
        self.estatus_de_empate_o_ganador(screen)
        pg.display.update()

    """ Función para posicionar 'x' y 'o' y los cambia por las imágenes cargadas"""
    def dibuja_caracter_XO(self, row, col, screen):
        # para las filas
        if (row == 1):
            posx = 155
        elif (row == 2):
            posx = self.width / 3 + 155
        elif (row == 3):
            posx = self.width / 3 * 2 + 155

        # para las columnas
        if (col == 1):
            posy = 52.5
        elif (col == 2):
            posy = self.height / 3 + 52.5
        elif (col == 3):
            posy = self.height / 3 * 2 + 52.5
        
        # haciendo que el tablero muestre los valores correctos
        self.tablero[row - 1][col - 1] = self.XO

        # cambiando XO por las imágenes
        if (self.XO == 'x'):
            X_icon = pg.image.load("assets/Images/X_icon.png")
            X_icon = pg.transform.scale(X_icon, (96, 96))
            screen.blit(X_icon, (posy, posx))
            self.XO = 'o'
        else:
            O_icon = pg.image.load("assets/Images/O_icon.png")
            O_icon = pg.transform.scale(O_icon, (96, 96))
            screen.blit(O_icon, (posy, posx))
            self.XO = 'x'

        pg.display.update()

    """ Función que se encarga del click-del-usuario """
    def click_de_usuario(self, screen):
        x, y = pg.mouse.get_pos()

        # print(x, y), usado en debugging
        # encuentra las coordenadas del click en columnas
        if (x < self.width / 3):
            col = 1
        elif (x < self.width / 3 * 2):
            col = 2
        elif (x < self.width):
            col = 3
        else:
            col = None

        # encuentra las coordenadas del click en columnas
        if (y < self.height / 3):
            row = 1
        elif (y < self.height / 3 * 2):
            row = 2
        elif (y < self.height):
            row = 3
        else:
            row = None

        if (row and col and self.tablero[row - 1][col - 1] is None):
            self.dibuja_caracter_XO(row, col, screen)
            self.buscando_ganador(screen)

    """ Función que reinicia los datos de la partida"""
    def reiniciar_partida(self, screen):
        global empate, ganador
        time.sleep(5) # transición
        screen.fill(self.BLANCO)
        time.sleep(5) # transición
        ganador, empate = None, None # reinicia los valores de ganador, empate
        self.XO = 'x' # reinicia el caracter a su valor inicial
        self.tablero = [[None] * 3, [None] * 3, [None] * 3] # reinicia la matriz de tablero

    """ Función que se encarga de los eventos del juego """
    def update(self,dt, screen):
        global ganador, empate
        for event in pg.event.get():
            # si el usuario desea salir
            if event.type == QUIT:
                pg.quit()
                sys.exit()
            # click del mouse
            elif event.type == MOUSEBUTTONDOWN:
                self.click_de_usuario(screen)
                if (ganador or empate):
                    self.guarda_ganadores()
                    self.reiniciar_partida(screen)

    """ Función que renderiza todos los componentes a la pantalla """
    def draw_screen(self, screen):
        # screen.fill(self.BLANCO) # pinta la ventana de blanco
        self.dibuja_lineas_de_tablero(screen) # dibuja las líneas del tablero
        self.estatus_de_empate_o_ganador(screen) 

        pg.display.flip() # muestra en la ventana 
        pg.display.update() # refresca la pantalla 

    """ Función que genera un archivo .txt que guarda los ganadores"""
    def guarda_ganadores(self):
        global ganador, empate
        file, mensaje = open("records.txt", "a+"), " "
        mensaje_divisor = "---------- Partida -----------\n"
        file.write(mensaje_divisor)
    
        if (ganador == 'x' or ganador == 'o'):
            mensaje = ganador.upper() + " ganó! \n"
        elif (empate == True):
            mensaje = "Empate! \n"

        file.write(mensaje)
        file.close()
    
    """ Función principal del programa """
    def run_game(self): 
        # iniciando pygame en la ventana
        pg.init()

        # fps 
        FPS = 60.0
        fpsClock = pg.time.Clock()

        # propiedades de la ventana
        WIDTH, HEIGHT = self.width, self.height
        screen = pg.display.set_mode((WIDTH, HEIGHT + 100), 4, 32)
        
        caption1, caption2, caption3 = "Tic", " Tac ", "Toe"
        caption =  caption1 + caption2 + caption3
        pg.display.set_caption(caption)
        icon = pg.image.load("assets/Images/logo.png")
        pg.display.set_icon(icon)

        # cargando la imagen de inicio
        cover = pg.image.load("assets/Images/startup_screen.png").convert()
        cover = pg.transform.scale(cover, (self.width, self.height + 100))

        # Main game loop
        dt = 1 / FPS * 1000

        self.ventana_de_inicio(screen, cover)
        # ciclo principal
        while True:
            self.update(dt, screen)
            self.draw_screen(screen)

            dt = fpsClock.tick(FPS)
