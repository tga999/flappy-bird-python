import pygame
import sys
import random

pygame.init()

#Config de pantalla

WIDTH = 400
HEIGHT = 600

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

FPS = 60
clock = pygame.time.Clock()

#Pájaro

bird_x = 100
bird_y = 300

gravity = 0.5
bird_movement = 0

#Tubos

tubos_list = []

def crear_tubo():

    random_tubo_pos = random.randint(200, 500)

    bajo_tubo = {
        "rect": pygame.Rect(400, random_tubo_pos, 70, 400),
        "scored": False
    }

    arriba_tubo = {
        "rect": pygame.Rect(400, random_tubo_pos - 600, 70, 400),
        "scored": False
    }

    return bajo_tubo, arriba_tubo


def mover_tubos(tubos):

    for tubo in tubos:
        tubo["rect"].centerx -= 3

    return tubos


def dibujar_tubos(tubos):

    for tubo in tubos:
        pygame.draw.rect(
            SCREEN,
            (0, 200, 0),
            tubo["rect"]
        )

#Timer para generar tubos

SPAWNTUBO = pygame.USEREVENT
pygame.time.set_timer(SPAWNTUBO, 1200)

#Colisiones

def colision(tubos):

    bird_hitbox = pygame.Rect(
        bird_x - 20,
        bird_y - 20,
        40,
        40
    )

    for tubo in tubos:

        if bird_hitbox.colliderect(tubo["rect"]):
            return False

    if bird_hitbox.top <= -50 or bird_hitbox.bottom >= HEIGHT:
        return False

    return True

#Score

score = 0

font = pygame.font.Font(None, 40)

def mostrar_score(score):

    score_surface = font.render(
        f"Score: {int(score)}",
        True,
        (255, 255, 255)
    )

    score_rect = score_surface.get_rect(center=(200, 50))

    SCREEN.blit(score_surface, score_rect)


def actualizar_score():

    global score

    for tubo in tubos_list:

        rect = tubo["rect"]

        # Solo tubos de abajo
        if rect.bottom >= HEIGHT:

            # El tubo pasó al pájaro
            if rect.centerx < bird_x and not tubo["scored"]:

                score += 1

                tubo["scored"] = True

#Pantalla game-over

def game_over_screen():

    game_over_surface = font.render(
        "PERDISTE!",
        True,
        (255, 255, 255)
    )

    game_over_rect = game_over_surface.get_rect(center=(200, 250))

    SCREEN.blit(game_over_surface, game_over_rect)

    restart_surface = font.render(
        "ESPACIO | W para reiniciar",
        True,
        (255, 255, 255)
    )

    restart_rect = restart_surface.get_rect(center=(200, 320))

    SCREEN.blit(restart_surface, restart_rect)


#Estado del juego


game_active = True


# Loop del juego

while True:

    # EVENTOS

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        #EVENTO TUBOS
        if event.type == SPAWNTUBO:
            tubos_list.extend(crear_tubo())

        #CONTROLES
        if event.type == pygame.KEYDOWN:

            #JUMP
            if game_active:

                if event.key in [pygame.K_SPACE, pygame.K_w]:
                    bird_movement = -8

            #RESETEO
            else:

                if event.key in [pygame.K_SPACE, pygame.K_w]:

                    game_active = True
                    tubos_list.clear()
                    bird_y = 300
                    bird_movement = 0
                    score = 0

    #Juego

    if game_active:

        # Fondo
        SCREEN.fill((135, 206, 235))

        # Física pájaro
        bird_movement += gravity
        bird_y += bird_movement

        # Dibujar pájaro
        pygame.draw.circle(
            SCREEN,
            (255, 255, 0),
            (bird_x, int(bird_y)),
            20
        )

        # Tubos
        tubos_list = mover_tubos(tubos_list)

        dibujar_tubos(tubos_list)

        # Score
        actualizar_score()

        mostrar_score(score)

        # Colisiones
        game_active = colision(tubos_list)

    # Game-over

    else:

        SCREEN.fill((0, 0, 0))

        game_over_screen()

    #Update display

    pygame.display.update()

    clock.tick(FPS)