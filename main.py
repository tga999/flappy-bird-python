import pygame
import sys
import random


pygame.init()

# Config ventana
WIDTH = 400
HEIGHT = 600

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# FPS
FPS = 60
clock = pygame.time.Clock()

# Posición inicial del pájaro
bird_x = 100
bird_y = 300

# Física del pájaro
gravity = 0.5
bird_movement = 0

# TUBOS
tubos_list = []

# Lógica tubos
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


# Mover tubos

def mover_tubos(tubos):
    for tubo in tubos:
        tubo["rect"].centerx -= 3
        
    return tubos

# Dibujar tubos
    
def dibujar_tubos(tubos):
    for tubo in tubos:
        pygame.draw.rect(SCREEN, (0, 200, 0), tubo["rect"])
        
#Evento para generar tubos
SPAWNTUBO = pygame.USEREVENT
pygame.time.set_timer(SPAWNTUBO, 1200)

#Colision tubos
def colision(tubos):
    bird_hitbox = pygame.Rect(bird_x - 20, bird_y - 20, 40, 40)
    for tubo in tubos:
        if bird_hitbox.colliderect(tubo["rect"]):
            return False
        
    if bird_hitbox.top <= -50 or bird_hitbox.bottom >= 600:
        return False
    return True

#Estado del juego
game_active = True

#SCORE
score = 0
font = pygame.font.Font(None, 40)

#Funcion score
def mostrar_score(score):
    score_surface = font.render(
        f"Score: {int(score)}", True, (255, 255, 255)
    )
    score_rect = score_surface.get_rect(center=(200, 50))
    SCREEN.blit(score_surface, score_rect)

#Score real
def actualizar_score():

    global score

    for tubo in tubos_list:

        rect = tubo["rect"]

        # Solo tubos de abajo
        if rect.bottom >= HEIGHT:

            # Pasó el pájaro y todavía no contó
            if rect.centerx < bird_x and not tubo["scored"]:

                score += 1

                tubo["scored"] = True
                
# GAME LOOP
while True:
    
    #Eventos
    for event in pygame.event.get():
        
        if event.type == SPAWNTUBO:
            tubos_list.extend(crear_tubo())
        
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        #Jump
        if event.type == pygame.KEYDOWN:

            if game_active:

                if event.key in [pygame.K_SPACE, pygame.K_w]:
                    bird_movement = -8

            else:

                if event.key in [pygame.K_SPACE, pygame.K_w]:

                    game_active = True
                    tubos_list.clear()
                    bird_y = 300
                    bird_movement = 0
                    score = 0
                    
    if game_active:           
        #Gravedad del pajaro
        bird_movement += gravity
        bird_y += bird_movement
        
        #Fondo
        SCREEN.fill((135, 206, 235))
        
        #Dibujar pajaro
        pygame.draw.circle(SCREEN, (255, 255,0),(bird_x,int(bird_y)), 20)
        
        #Actualizar tubos, dibujarlos, mostrar score y actualizar
        tubos_list = mover_tubos(tubos_list)
        dibujar_tubos(tubos_list)
        mostrar_score(score)
        actualizar_score()
        
        
        #Colisiones
        game_active = colision(tubos_list)
        
        #Actualizar pantalla
        pygame.display.update()
        
        #Controlar fps
        clock.tick(60)