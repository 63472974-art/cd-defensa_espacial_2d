# main.py
# Defensa Espacial 2D - Sesión 1.
#
# Funcionalidades:
# - Movimiento de la nave.
# - Disparos.
# - Generación de meteoritos.
# - Colisiones.
# - Puntuación.
#
# El bucle utiliza asyncio para facilitar su futura
# adaptación a navegadores mediante Pygbag.

import asyncio
import random

import pygame

from config import (
    ANCHO,
    ALTO,
    FPS,
    NEGRO_ESPACIO,
    BLANCO,
    CELESTE,
    AMARILLO,
    ROJO,
    INTERVALO_DISPARO,
    INTERVALO_METEORITO,
    PUNTOS_METEORITO,
)

from entidades import Nave, Disparo, Meteorito


async def main():
    """Ejecuta el videojuego."""

    pygame.init()

    # Crear ventana.
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Defensa Espacial 2D")

    reloj = pygame.time.Clock()
    fuente = pygame.font.Font(None, 32)
    fuente_pequena = pygame.font.Font(None, 23)

    # Crear jugador.
    nave = Nave()

    # Grupos que almacenan los objetos del juego.
    disparos = pygame.sprite.Group()
    meteoritos = pygame.sprite.Group()

    # Crear estrellas para el fondo.
    estrellas = []

    for _ in range(85):
        x = random.randint(0, ANCHO - 1)
        y = random.randint(0, ALTO - 1)
        velocidad = random.randint(25, 80)
        tamano = random.choice([1, 1, 2])

        estrellas.append([float(x), float(y), velocidad, tamano])

    # Variables de la partida.
    puntuacion = 0
    impactos_recibidos = 0

    ultimo_disparo = -INTERVALO_DISPARO
    ultimo_meteorito = pygame.time.get_ticks()

    ejecutando = True

    while ejecutando:

        # Tiempo entre fotogramas, expresado en segundos.
        dt = min(reloj.tick(FPS) / 1000.0, 0.05)

        # ---------------------------------------
        # 1. PROCESAMIENTO DE EVENTOS
        # ---------------------------------------
        for evento in pygame.event.get():

            if evento.type == pygame.QUIT:
                ejecutando = False

            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False

        if not ejecutando:
            break

        # Consultar las teclas presionadas.
        teclas = pygame.key.get_pressed()
        tiempo_actual = pygame.time.get_ticks()

        # ---------------------------------------
        # 2. MOVIMIENTO DE LA NAVE
        # ---------------------------------------
        nave.update(teclas, dt)

        # ---------------------------------------
        # 3. CREACIÓN DE DISPAROS
        # ---------------------------------------
        if teclas[pygame.K_SPACE]:

            tiempo_transcurrido = (
                tiempo_actual - ultimo_disparo
            )

            if tiempo_transcurrido >= INTERVALO_DISPARO:

                disparo = Disparo(
                    nave.rect.centerx,
                    nave.rect.top
                )

                disparos.add(disparo)
                ultimo_disparo = tiempo_actual

        # ---------------------------------------
        # 4. GENERACIÓN DE METEORITOS
        # ---------------------------------------
        if tiempo_actual - ultimo_meteorito >= INTERVALO_METEORITO:

            meteorito = Meteorito()
            meteoritos.add(meteorito)

            ultimo_meteorito = tiempo_actual

        # ---------------------------------------
        # 5. ACTUALIZACIÓN DE OBJETOS
        # ---------------------------------------
        disparos.update(dt)
        meteoritos.update(dt)

        # ---------------------------------------
        # 6. COLISIONES: DISPARO Y METEORITO
        # ---------------------------------------
        colisiones = pygame.sprite.groupcollide(
            meteoritos,
            disparos,
            True,
            True
        )

        # Cada meteorito destruido suma 10 puntos.
        puntuacion += len(colisiones) * PUNTOS_METEORITO

        # ---------------------------------------
        # 7. COLISIONES: NAVE Y METEORITO
        # ---------------------------------------
        impactos = pygame.sprite.spritecollide(
            nave,
            meteoritos,
            True
        )

        # En la sesión 1 solo contamos los impactos.
        # Las vidas y Game Over se agregan en sesión 2.
        impactos_recibidos += len(impactos)

        # ---------------------------------------
        # 8. DIBUJAR FONDO ESPACIAL
        # ---------------------------------------
        pantalla.fill(NEGRO_ESPACIO)

        for estrella in estrellas:

            # Desplazamiento vertical de las estrellas.
            estrella[1] += estrella[2] * dt

            if estrella[1] >= ALTO:
                estrella[1] = 0.0
                estrella[0] = float(
                    random.randint(0, ANCHO - 1)
                )

            pygame.draw.circle(
                pantalla,
                BLANCO,
                (round(estrella[0]), round(estrella[1])),
                estrella[3]
            )

        # ---------------------------------------
        # 9. DIBUJAR ELEMENTOS DEL JUEGO
        # ---------------------------------------
        disparos.draw(pantalla)
        meteoritos.draw(pantalla)

        # La nave es un solo sprite.
        pantalla.blit(nave.image, nave.rect)

        # ---------------------------------------
        # 10. MOSTRAR INFORMACIÓN
        # ---------------------------------------
        texto_puntos = fuente.render(
            f"PUNTOS: {puntuacion}",
            True,
            AMARILLO
        )

        texto_impactos = fuente.render(
            f"IMPACTOS: {impactos_recibidos}",
            True,
            ROJO
        )

        texto_titulo = fuente_pequena.render(
            "DEFENSA ESPACIAL - PROTOTIPO",
            True,
            CELESTE
        )

        texto_controles = fuente_pequena.render(
            "A/D o flechas: mover | ESPACIO: disparar | ESC: salir",
            True,
            BLANCO
        )

        pantalla.blit(texto_puntos, (20, 15))
        pantalla.blit(
            texto_impactos,
            (ANCHO - texto_impactos.get_width() - 20, 15)
        )

        pantalla.blit(
            texto_titulo,
            (
                (ANCHO - texto_titulo.get_width()) // 2,
                20
            )
        )

        pantalla.blit(
            texto_controles,
            (
                (ANCHO - texto_controles.get_width()) // 2,
                ALTO - 22
            )
        )

        # Actualizar la ventana.
        pygame.display.flip()

        # Permite ceder el control al navegador
        # durante una futura adaptación con Pygbag.
        await asyncio.sleep(0)

    pygame.quit()


if __name__ == "__main__":
    asyncio.run(main()) 
