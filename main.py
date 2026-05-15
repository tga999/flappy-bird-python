import pygame
import sys
import random

pygame.init()

#ASSETS

bg=pygame.image.load("assets/bg.png")
bg=pygame.transform.scale(bg,(400,600))

bird_frames=[
    pygame.image.load("assets/bird/frame-1.png"),
    pygame.image.load("assets/bird/frame-2.png"),
]

tuboArriba = pygame.image.load("assets/tubos/tubo_arriba.png")
tuboArriba = pygame.transform.scale(tuboArriba, (70, 400))
tuboAbajo = pygame.image.load("assets/tubos/tubo_abajo.png")
tuboAbajo = pygame.transform.scale(tuboAbajo, (70, 400))


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

bird_index = 0
animation_speed= 0.1
bird_img = bird_frames[bird_index]

def animar_pajaro():
    global bird_index, bird_img
    bird_index += animation_speed
    if bird_index >= len(bird_frames):
        bird_index = 0
    bird_img = bird_frames[int(bird_index)]
    
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
        if tubo["rect"].bottom >= HEIGHT:
            SCREEN.blit(tuboAbajo, tubo["rect"])
        else:
            SCREEN.blit(tuboArriba, tubo["rect"])

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

#High-score
def cargar_high_score():
    try:
        with open ("highscore.txt", "r") as f:
            return int(f.read())
    except:
        return 0
    
def guardar_high_score(score):
    with open ("highscore.txt", "w") as f:
        f.write(str(score))

score = 0
highscore= cargar_high_score()

font = pygame.font.Font(None, 40)

def mostrar_score(score):

    score_surface = font.render(
        f"Score: {int(score)}",
        True,
        (0, 0, 0)
    )

    score_rect = score_surface.get_rect(center=(200, 50))

    SCREEN.blit(score_surface, score_rect)
    
    hs_surface = font.render(f"Highscore: {highscore}", True, (0, 0, 0))
    hs_rect = hs_surface.get_rect(center=(200, 90))
    SCREEN.blit(hs_surface, hs_rect)


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
        (0, 0, 0)
    )

    game_over_rect = game_over_surface.get_rect(center=(200, 250))

    SCREEN.blit(game_over_surface, game_over_rect)

    restart_surface = font.render(
        "ESPACIO | W para reiniciar",
        True,
        (0, 0, 0)
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
        SCREEN.blit(bg, (0, 0))

        # Física pájaro
        animar_pajaro()
        bird_movement += gravity
        bird_y += bird_movement
        bird = pygame.transform.scale(bird_img, (40, 40))
        
        # Dibujar pájaro
        SCREEN.blit(bird, (bird_x - 20, int(bird_y) - 20))

        # Tubos
        tubos_list = mover_tubos(tubos_list)

        dibujar_tubos(tubos_list)

        # Score
        actualizar_score()

        mostrar_score(score)

        # Colisiones
        if not colision(tubos_list):

            game_active = False

            if score > highscore:
                highscore = score
                guardar_high_score(highscore)

    # Game-over

    else:

        SCREEN.blit(bg, (0, 0))

        game_over_screen()

    #Update display

    pygame.display.update()

    clock.tick(FPS)