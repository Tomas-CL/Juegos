import pygame
import random
import time

# Definición de constantes
ANCHO_VENTANA = 800
ALTO_VENTANA = 600
TAMANO_BLOQUE = 30
FPS = 30
VELOCIDAD_NORMAL_BASE = 1
VELOCIDAD_RAPIDA = 10

# Definición de colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
ROJO = (255, 0, 0)
VERDE = (0, 255, 0)
AMARILLO = (255, 255, 0)
MAGENTA = (255, 0, 255)
CIAN = (0, 255, 255)

# Definición de las formas de los bloques
formas = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3, 0],
     [0, 3, 3]],

    [[4, 0, 0],
     [4, 4, 4]],

    [[0, 0, 5],
     [5, 5, 5]],

    [[6, 6, 6, 6]],

    [[7, 7],
     [7, 7]]
]

# Clase para manejar el bloque actual
class Bloque:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.forma = random.choice(formas)
        self.color = random.choice([AZUL, ROJO, VERDE, AMARILLO, MAGENTA, CIAN])

    def rotar(self):
        self.forma = [[self.forma[y][x] for y in range(len(self.forma))] for x in range(len(self.forma[0])-1, -1, -1)]

# Clase principal para el juego
class Tetris:
    def __init__(self):
        self.tablero = [[0] * 10 for _ in range(20)]
        self.game_over = False
        self.velocidad_normal = VELOCIDAD_NORMAL_BASE
        self.velocidad = self.velocidad_normal
        self.puntos = 0
        self.pausa = False
        self.lineas_completadas = 0
        self.lista_bloques = self.crear_lista_bloques()
        self.nuevo_bloque()

    def crear_lista_bloques(self):
        lista_bloques = list(range(len(formas)))
        random.shuffle(lista_bloques)
        return lista_bloques
    
    def nuevo_bloque(self):
        if not self.lista_bloques:
            self.lista_bloques = self.crear_lista_bloques()
        tipo_bloque = self.lista_bloques.pop()
        self.bloque_actual = Bloque(tipo_bloque, 0)

    def colision(self, dx=0, dy=0):
        for y in range(len(self.bloque_actual.forma)):
            for x in range(len(self.bloque_actual.forma[0])):
                if self.bloque_actual.forma[y][x]:
                    if (self.bloque_actual.x + x + dx < 0 or self.bloque_actual.x + x + dx >= 10 or
                            self.bloque_actual.y + y + dy >= 20 or
                            self.tablero[self.bloque_actual.y + y + dy][self.bloque_actual.x + x + dx]):
                        return True
        return False

    def actualizar_tablero(self):
        if not self.colision(dy=1):
            self.bloque_actual.y += 1
        else:
            for y in range(len(self.bloque_actual.forma)):
                for x in range(len(self.bloque_actual.forma[0])):
                    if self.bloque_actual.forma[y][x]:
                        self.tablero[self.bloque_actual.y + y][self.bloque_actual.x + x] = self.bloque_actual.color
            lineas_completas = self.eliminar_filas_completas()
            self.puntos += lineas_completas * 10
            self.bloque_actual = Bloque(3, 0)
            if self.colision():
                self.game_over = True

    def eliminar_filas_completas(self):
        lineas_completas = 0
        for y in range(20):
            if all(self.tablero[y]):
                del self.tablero[y]
                self.tablero.insert(0, [0] * 10)
                lineas_completas += 1
        return lineas_completas

    def mover_bloque(self, dx):
        if not self.colision(dx=dx):
            self.bloque_actual.x += dx

    def rotar_bloque(self):
        self.bloque_actual.rotar()
        if self.colision():
            self.bloque_actual.rotar()

    def actualizar_velocidad(self, lineas_completadas):
        self.lineas_completadas += lineas_completadas
        self.velocidad_normal = max(2, VELOCIDAD_NORMAL_BASE - self.lineas_completadas)
        self.velocidad = self.velocidad_normal

# Función para dibujar la caja de información
def dibujar_info_box(pantalla):
    # Dimensiones y posición de la caja flotante
    info_box_x = 450
    info_box_y = 150
    info_box_ancho = 350
    info_box_alto = 225

    # Crear un rectángulo semi-transparente
    superficie_transparente = pygame.Surface((info_box_ancho, info_box_alto))
    superficie_transparente.set_alpha(128)
    superficie_transparente.fill((50, 50, 50))
    pantalla.blit(superficie_transparente, (info_box_x, info_box_y))

    # Configuración del texto
    font = pygame.font.Font(None, 24)
    instrucciones = [
        "Controles:",
        "Flecha izquierda/Derecha: Mover",
        "Flecha arriba: Rotar",
        "Flecha abajo: Caer rápido",
        "Pausa: Espacio",
        "Bajar volumen: F2",
        "Subir Volumen: F3"
    ]

    # Dibujar el texto sobre la caja flotante
    for i, linea in enumerate(instrucciones):
        texto = font.render(linea, True, BLANCO)
        pantalla.blit(texto, (info_box_x + 10, info_box_y + 10 + i * 30))

# Función principal
def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("Tetris")
    reloj = pygame.time.Clock()
    juego = Tetris()
    tiempo_ultimo_movimiento = time.time()

    fuente = pygame.font.Font(None, 36)

    # Cargar la música del Tetris y reproducirla
    pygame.mixer.music.load('audio/cancion_tecno.mp3')
    pygame.mixer.music.play(-1)

    # Volumen inicial de la música
    volumen_musica = 0.5
    pygame.mixer.music.set_volume(volumen_musica)

    while not juego.game_over:
        tiempo_actual = time.time()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                juego.game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    juego.mover_bloque(-1)
                elif event.key == pygame.K_RIGHT:
                    juego.mover_bloque(1)
                elif event.key == pygame.K_UP:
                    juego.rotar_bloque()
                elif event.key == pygame.K_DOWN:
                    juego.velocidad = VELOCIDAD_RAPIDA
                elif event.key == pygame.K_F3:
                    volumen_musica = min(volumen_musica + 0.1, 1.0)
                    pygame.mixer.music.set_volume(volumen_musica)
                elif event.key == pygame.K_F2:
                    volumen_musica = max(volumen_musica - 0.1, 0.0)
                    pygame.mixer.music.set_volume(volumen_musica)
                elif event.key == pygame.K_SPACE:
                    juego.pausa = not juego.pausa
                    if juego.pausa:
                        pygame.mixer.music.pause()
                    else:
                        pygame.mixer.music.unpause()
                    time.sleep(0.2)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    juego.velocidad = juego.velocidad_normal

        if not juego.pausa and tiempo_actual - tiempo_ultimo_movimiento > 1 / juego.velocidad:
            juego.actualizar_tablero()
            tiempo_ultimo_movimiento = tiempo_actual

        pantalla.fill(NEGRO)
        for y, fila in enumerate(juego.tablero):
            for x, color in enumerate(fila):
                pygame.draw.rect(pantalla, color, (x*TAMANO_BLOQUE, y*TAMANO_BLOQUE, TAMANO_BLOQUE, TAMANO_BLOQUE))
                pygame.draw.rect(pantalla, BLANCO, (x*TAMANO_BLOQUE, y*TAMANO_BLOQUE, TAMANO_BLOQUE, TAMANO_BLOQUE), 1)

        for y, fila in enumerate(juego.bloque_actual.forma):
            for x, valor in enumerate(fila):
                if valor:
                    pygame.draw.rect(pantalla, juego.bloque_actual.color, ((juego.bloque_actual.x + x) * TAMANO_BLOQUE, (juego.bloque_actual.y + y) * TAMANO_BLOQUE, TAMANO_BLOQUE, TAMANO_BLOQUE))
                    pygame.draw.rect(pantalla, BLANCO, ((juego.bloque_actual.x + x) * TAMANO_BLOQUE, (juego.bloque_actual.y + y) * TAMANO_BLOQUE, TAMANO_BLOQUE, TAMANO_BLOQUE), 1)

        dibujar_info_box(pantalla)

        puntaje_texto = fuente.render(f"Puntaje: {juego.puntos}", True, ROJO)
        pygame.draw.rect(pantalla, BLANCO, (ANCHO_VENTANA - 150, 0, 150, 50))
        pantalla.blit(puntaje_texto, (ANCHO_VENTANA - 140, 10))

        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()
main()