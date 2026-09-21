import pygame
import math
import random
import sys


# ============================================================
# CONFIGURACIÓN
# ============================================================

ANCHO = 1000
ALTO = 700

FPS = 60

pygame.init()

pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Te Amo ❤️")

reloj = pygame.time.Clock()


# ============================================================
# COLORES
# ============================================================

NEGRO = (2, 2, 7)

DORADO = (255, 215, 0)
DORADO_CLARO = (255, 235, 100)

AMARILLO = (255, 220, 30)

BLANCO = (255, 255, 255)

ROSADO = (255, 80, 150)

ROJO = (255, 60, 90)


# ============================================================
# FUENTES
# ============================================================

fuente_titulo = pygame.font.SysFont(
    "arial",
    65,
    bold=True
)

fuente_frase = pygame.font.SysFont(
    "arial",
    25,
    bold=True
)

fuente_pequena = pygame.font.SysFont(
    "arial",
    18,
    bold=True
)


# ============================================================
# FUNCIONES
# ============================================================

def texto_centrado(texto, fuente, color, x, y):

    superficie = fuente.render(
        texto,
        True,
        color
    )

    rectangulo = superficie.get_rect(
        center=(x, y)
    )

    pantalla.blit(
        superficie,
        rectangulo
    )


# ============================================================
# CORAZÓN MATEMÁTICO
# ============================================================

def crear_corazon():

    puntos = []

    escala = 15

    centro_x = ANCHO // 2
    centro_y = 370

    for i in range(800):

        t = random.uniform(0, math.pi * 2)

        x = 16 * math.sin(t) ** 3

        y = (
            13 * math.cos(t)
            - 5 * math.cos(2 * t)
            - 2 * math.cos(3 * t)
            - math.cos(4 * t)
        )

        # Agregamos pequeñas variaciones
        x += random.uniform(-0.15, 0.15)
        y += random.uniform(-0.15, 0.15)

        px = centro_x + x * escala
        py = centro_y - y * escala

        puntos.append(
            [px, py]
        )

    return puntos


particulas_corazon = crear_corazon()


# ============================================================
# PARTÍCULAS DEL CORAZÓN
# ============================================================

class ParticulaCorazon:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.tamano = random.choice([
            1,
            2,
            2,
            3
        ])

        self.brillo = random.randint(
            150,
            255
        )

        self.velocidad = random.uniform(
            0.5,
            2
        )

        self.offset = random.uniform(
            0,
            math.pi * 2
        )

    def actualizar(self, tiempo):

        movimiento = math.sin(
            tiempo * 2 + self.offset
        ) * 0.8

        self.y += movimiento * 0.02

    def dibujar(self):

        intensidad = max(
            100,
            min(255, int(self.brillo))
        )

        color = (
            255,
            intensidad,
            20
        )

        pygame.draw.circle(
            pantalla,
            color,
            (
                int(self.x),
                int(self.y)
            ),
            self.tamano
        )


particulas = []

for x, y in particulas_corazon:

    particulas.append(
        ParticulaCorazon(x, y)
    )


# ============================================================
# PARTÍCULAS DEL FONDO
# ============================================================

class ParticulaFondo:

    def __init__(self):

        self.x = random.randint(
            0,
            ANCHO
        )

        self.y = random.randint(
            0,
            ALTO
        )

        self.tamano = random.randint(
            1,
            3
        )

        self.velocidad = random.uniform(
            0.2,
            1.2
        )

        self.brillo = random.randint(
            80,
            220
        )

    def actualizar(self):

        self.y -= self.velocidad

        if self.y < 0:

            self.y = ALTO

            self.x = random.randint(
                0,
                ANCHO
            )

    def dibujar(self):

        color = (
            255,
            random.randint(170, 230),
            40
        )

        pygame.draw.circle(
            pantalla,
            color,
            (
                int(self.x),
                int(self.y)
            ),
            self.tamano
        )


particulas_fondo = []

for i in range(250):

    particulas_fondo.append(
        ParticulaFondo()
    )


# ============================================================
# CORAZONES DEL FONDO
# ============================================================

def dibujar_corazon_pequeno(
    superficie,
    x,
    y,
    tamano,
    color
):

    puntos = []

    for i in range(40):

        t = (
            math.pi * 2
            * i
            / 40
        )

        hx = (
            16
            * math.sin(t) ** 3
        )

        hy = (
            13 * math.cos(t)
            - 5 * math.cos(2 * t)
            - 2 * math.cos(3 * t)
            - math.cos(4 * t)
        )

        px = x + hx * tamano
        py = y - hy * tamano

        puntos.append(
            (
                px,
                py
            )
        )

    pygame.draw.polygon(
        superficie,
        color,
        puntos
    )


corazones_fondo = []

for i in range(18):

    corazones_fondo.append({
        "x": random.randint(
            30,
            ANCHO - 30
        ),

        "y": random.randint(
            150,
            ALTO - 30
        ),

        "tamano": random.uniform(
            0.5,
            1.2
        ),

        "velocidad": random.uniform(
            0.1,
            0.4
        ),

        "fase": random.uniform(
            0,
            math.pi * 2
        )
    })


# ============================================================
# FLORES
# ============================================================

class Flor:

    def __init__(self, x, y, escala):

        self.x = x
        self.y = y

        self.escala = escala

        self.angulo = random.uniform(
            0,
            math.pi * 2
        )

        self.fase = random.uniform(
            0,
            math.pi * 2
        )

    def dibujar(self, tiempo):

        movimiento = math.sin(
            tiempo * 1.5 + self.fase
        ) * 4

        x = self.x
        y = self.y + movimiento

        # Tallo

        pygame.draw.line(
            pantalla,
            (60, 130, 45),
            (
                int(x),
                int(y + 10 * self.escala)
            ),
            (
                int(x),
                int(y + 55 * self.escala)
            ),
            max(
                1,
                int(3 * self.escala)
            )
        )

        # Pétalos

        radio = 17 * self.escala

        for i in range(8):

            angulo = (
                math.pi * 2
                * i
                / 8
            )

            px = (
                x
                + math.cos(angulo)
                * radio
            )

            py = (
                y
                + math.sin(angulo)
                * radio
            )

            pygame.draw.circle(
                pantalla,
                AMARILLO,
                (
                    int(px),
                    int(py)
                ),
                max(
                    3,
                    int(10 * self.escala)
                )
            )

        # Centro

        pygame.draw.circle(
            pantalla,
            (180, 100, 10),
            (
                int(x),
                int(y)
            ),
            max(
                3,
                int(8 * self.escala)
            )
        )


flores = [

    Flor(120, 520, 1.2),
    Flor(250, 590, 0.8),
    Flor(750, 570, 1.1),
    Flor(870, 490, 0.9),
    Flor(180, 410, 0.65),
    Flor(820, 400, 0.65)

]


# ============================================================
# FRASES
# ============================================================

frases = [

    "Eres una persona muy especial ❤️",

    "Gracias por estar en mi vida",

    "Contigo todo es más bonito ✨",

    "Eres mi lugar favorito",

    "Te quiero muchísimo ❤️",

    "Nunca olvides lo importante que eres"

]


indice_frase = 0

tiempo_frase = 0


# ============================================================
# ANIMACIÓN DEL TÍTULO
# ============================================================

def dibujar_titulo(tiempo):

    brillo = (
        math.sin(tiempo * 3)
        + 1
    ) / 2

    intensidad = int(
        180 + brillo * 75
    )

    color_brillo = (
        255,
        intensidad,
        100
    )

    # Sombra brillante

    texto_sombra = fuente_titulo.render(
        "Te Amo",
        True,
        (100, 70, 0)
    )

    rect_sombra = texto_sombra.get_rect(
        center=(
            ANCHO // 2 + 3,
            85 + 3
        )
    )

    pantalla.blit(
        texto_sombra,
        rect_sombra
    )

    # Texto principal

    texto = fuente_titulo.render(
        "Te Amo",
        True,
        color_brillo
    )

    rect = texto.get_rect(
        center=(
            ANCHO // 2,
            85
        )
    )

    pantalla.blit(
        texto,
        rect
    )


# ============================================================
# TEXTO DE LA FRASE
# ============================================================

def dibujar_frase():

    frase = frases[indice_frase]

    texto = fuente_frase.render(
        frase,
        True,
        (255, 240, 150)
    )

    rect = texto.get_rect(
        center=(
            ANCHO // 2,
            ALTO - 55
        )
    )

    pantalla.blit(
        texto,
        rect
    )


# ============================================================
# BUCLE PRINCIPAL
# ============================================================

ejecutando = True

tiempo_total = 0

while ejecutando:

    dt = reloj.tick(FPS) / 1000

    tiempo_total += dt

    tiempo_frase += dt


    # --------------------------------------------------------
    # EVENTOS
    # --------------------------------------------------------

    for evento in pygame.event.get():

        if evento.type == pygame.QUIT:

            ejecutando = False

        if evento.type == pygame.KEYDOWN:

            # ESC = salir

            if evento.key == pygame.K_ESCAPE:

                ejecutando = False


    # --------------------------------------------------------
    # CAMBIAR FRASE
    # --------------------------------------------------------

    if tiempo_frase >= 3.5:

        tiempo_frase = 0

        indice_frase += 1

        if indice_frase >= len(frases):

            indice_frase = 0


    # --------------------------------------------------------
    # FONDO
    # --------------------------------------------------------

    pantalla.fill(
        NEGRO
    )


    # --------------------------------------------------------
    # CORAZONES DEL FONDO
    # --------------------------------------------------------

    for corazon in corazones_fondo:

        corazon["y"] -= (
            corazon["velocidad"]
        )

        if corazon["y"] < -50:

            corazon["y"] = ALTO + 30

        brillo = int(
            20
            + 20
            * (
                math.sin(
                    tiempo_total
                    + corazon["fase"]
                )
                + 1
            )
        )

        dibujar_corazon_pequeno(
            pantalla,
            corazon["x"],
            corazon["y"],
            corazon["tamano"],
            (
                brillo,
                5,
                brillo
            )
        )


    # --------------------------------------------------------
    # PARTÍCULAS DE FONDO
    # --------------------------------------------------------

    for particula in particulas_fondo:

        particula.actualizar()

        particula.dibujar()


    # --------------------------------------------------------
    # TÍTULO
    # --------------------------------------------------------

    dibujar_titulo(
        tiempo_total
    )


    # --------------------------------------------------------
    # CORAZÓN GRANDE
    # --------------------------------------------------------

    for particula in particulas:

        particula.actualizar(
            tiempo_total
        )

        particula.dibujar()


    # --------------------------------------------------------
    # FLORES
    # --------------------------------------------------------

    for flor in flores:

        flor.dibujar(
            tiempo_total
        )


    # --------------------------------------------------------
    # FRASE
    # --------------------------------------------------------

    dibujar_frase()


    # --------------------------------------------------------
    # ACTUALIZAR PANTALLA
    # --------------------------------------------------------

    pygame.display.flip()


# ============================================================
# CERRAR
# ============================================================

pygame.quit()

sys.exit()