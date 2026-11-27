# entidades.py
# Clases de los elementos interactivos del videojuego.

import random

import pygame

from config import (
    ANCHO,
    ALTO,
    AZUL,
    BLANCO,
    CELESTE,
    GRIS,
    ROJO,
    VELOCIDAD_NAVE,
    VELOCIDAD_DISPARO,
    VELOCIDAD_METEORITO_MIN,
    VELOCIDAD_METEORITO_MAX,
)


class Nave(pygame.sprite.Sprite):
    """Representa la nave controlada por el jugador."""

    def __init__(self):
        super().__init__()

        # Superficie transparente de la nave.
        self.image = pygame.Surface((64, 64), pygame.SRCALPHA)

        # Cuerpo principal: figura triangular.
        pygame.draw.polygon(
            self.image,
            CELESTE,
            [(32, 3), (14, 51), (50, 51)]
        )

        # Alas laterales.
        pygame.draw.polygon(
            self.image,
            AZUL,
            [(15, 34), (2, 55), (24, 51)]
        )
        pygame.draw.polygon(
            self.image,
            AZUL,
            [(49, 34), (62, 55), (40, 51)]
        )

        # Cabina y propulsor.
        pygame.draw.ellipse(
            self.image,
            BLANCO,
            (27, 22, 10, 16)
        )
        pygame.draw.polygon(
            self.image,
            ROJO,
            [(25, 53), (32, 63), (39, 53)]
        )

        # Posición inicial de la nave.
        self.rect = self.image.get_rect(
            midbottom=(ANCHO // 2, ALTO - 18)
        )

        # Posición horizontal con decimales.
        self.pos_x = float(self.rect.x)

    def update(self, teclas, dt):
        """Mueve la nave sin salir de la pantalla."""

        direccion = 0

        if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
            direccion -= 1

        if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
            direccion += 1

        # El movimiento se ajusta al tiempo transcurrido.
        self.pos_x += direccion * VELOCIDAD_NAVE * dt

        # Evitar que la nave salga del escenario.
        self.pos_x = max(
            0,
            min(self.pos_x, ANCHO - self.rect.width)
        )

        self.rect.x = round(self.pos_x)
class Disparo(pygame.sprite.Sprite):
    """Proyectil disparado por la nave."""

    def __init__(self, x, y):
        super().__init__()

        # Crear un proyectil rectangular.
        self.image = pygame.Surface(
            (6, 18),
            pygame.SRCALPHA
        )
        self.image.fill(CELESTE)

        # Ubicar el disparo sobre la nave.
        self.rect = self.image.get_rect(
            midbottom=(x, y)
        )

        self.pos_y = float(self.rect.y)

    def update(self, dt):
        """Desplaza el disparo hacia arriba."""

        self.pos_y -= VELOCIDAD_DISPARO * dt
        self.rect.y = round(self.pos_y)

        # Eliminarlo cuando sale de la pantalla.
        if self.rect.bottom < 0:
            self.kill()
class Meteorito(pygame.sprite.Sprite):
    """Meteorito que desciende desde la parte superior."""

    def __init__(self):
        super().__init__()

        # Cada meteorito tendrá un tamaño diferente.
        radio = random.randint(14, 27)
        tamano = radio * 2 + 4

        self.image = pygame.Surface(
            (tamano, tamano),
            pygame.SRCALPHA
        )

        centro = tamano // 2

        # Dibujar meteorito y sus cráteres.
        pygame.draw.circle(
            self.image,
            GRIS,
            (centro, centro),
            radio
        )

        pygame.draw.circle(
            self.image,
            (90, 100, 120),
            (centro - radio // 3, centro - radio // 4),
            max(3, radio // 4)
        )

        pygame.draw.circle(
            self.image,
            (175, 180, 190),
            (centro + radio // 4, centro + radio // 5),
            max(2, radio // 6)
        )

        # Posición inicial aleatoria.
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(
            0,
            ANCHO - self.rect.width
        )
        self.rect.y = -self.rect.height

        self.pos_y = float(self.rect.y)

        # Velocidad distinta para cada meteorito.
        self.velocidad = random.randint(
            VELOCIDAD_METEORITO_MIN,
            VELOCIDAD_METEORITO_MAX
        )

    def update(self, dt):
        """Mueve el meteorito hacia abajo."""

        self.pos_y += self.velocidad * dt
        self.rect.y = round(self.pos_y)

        # Eliminar al salir del escenario.
        if self.rect.top > ALTO:
            self.kill() 
