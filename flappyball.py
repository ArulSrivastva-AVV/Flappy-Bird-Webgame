import pygame
import random

pygame.init()

# Constants
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GRAVITY = 0.25
BIRD_JUMP = -6
PIPE_SPEED = 3
PIPE_GAP = 150

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
# Added a smaller font for the "Press Space" message
game_font = pygame.font.SysFont("Arial", 50, bold=True)
small_font = pygame.font.SysFont("Arial", 25, bold=True)

# Load Images (Ensure bird.png and pipe.png are in the folder)
bird_img = pygame.image.load('bird.png').convert_alpha()
bird_img = pygame.transform.scale(bird_img, (34, 24))
pipe_img = pygame.image.load('pipe.png').convert_alpha()
pipe_img = pygame.transform.scale(pipe_img, (50, 500))

# Game Variables
bird_rect = bird_img.get_rect(center = (50, 300))
bird_movement = 0
pipes = []
score = 0
game_active = True

SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 1200)

def create_pipe():
    random_pipe_pos = random.randint(200, 450)
    bottom_rect = pipe_img.get_rect(midtop = (SCREEN_WIDTH + 50, random_pipe_pos))
    top_rect = pipe_img.get_rect(midbottom = (SCREEN_WIDTH + 50, random_pipe_pos - PIPE_GAP))
    return {"rect": bottom_rect, "scored": False}, {"rect": top_rect, "scored": False}

def draw_pipes(pipe_list):
    for pipe in pipe_list:
        if pipe["rect"].bottom >= SCREEN_HEIGHT:
            screen.blit(pipe_img, pipe["rect"])
        else:
            flip_pipe = pygame.transform.flip(pipe_img, False, True)
            screen.blit(flip_pipe, pipe["rect"])

def update_score(pipe_list, current_score):
    for pipe in pipe_list:
        if bird_rect.left > pipe["rect"].right and not pipe["scored"]:
            pipe["scored"] = True
            current_score += 0.5 
    return current_score

# --- NEW: Function to draw score anywhere ---
def draw_score(status):
    if status == 'playing':
        score_surf = game_font.render(str(int(score)), True, (255, 255, 255))
        score_rect = score_surf.get_rect(center = (SCREEN_WIDTH//2, 80))
        screen.blit(score_surf, score_rect)
    
    if status == 'game_over':
        # Big Score in the middle
        score_surf = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
        score_rect = score_surf.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        screen.blit(score_surf, score_rect)
        
        # Restart Message
        restart_surf = small_font.render('PRESS SPACE TO RESTART', True, (255, 255, 255))
        restart_rect = restart_surf.get_rect(center = (SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
        screen.blit(restart_surf, restart_rect)

# Main Loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bird_movement = BIRD_JUMP
            if not game_active:
                game_active = True
                pipes.clear()
                bird_rect.center = (50, 300)
                bird_movement = 0
                score = 0

        if event.type == SPAWNPIPE and game_active:
            pipes.extend(create_pipe())

    screen.fill((135, 206, 235))

    if game_active:
        # Bird
        bird_movement += GRAVITY
        bird_rect.centery += bird_movement
        screen.blit(bird_img, bird_rect)

        # Pipes
        for pipe in pipes:
            pipe["rect"].centerx -= PIPE_SPEED
        
        score = update_score(pipes, score)
        pipes = [p for p in pipes if p["rect"].right > -50]
        draw_pipes(pipes)

        # Collision
        for pipe in pipes:
            if bird_rect.colliderect(pipe["rect"]): 
                game_active = False
        if bird_rect.top <= 0 or bird_rect.bottom >= SCREEN_HEIGHT: 
            game_active = False
        
        draw_score('playing')
    else:
        # Drawing pipes and bird static in the background looks better
        draw_pipes(pipes)
        screen.blit(bird_img, bird_rect)
        # Show the Game Over UI
        draw_score('game_over')

    pygame.display.update()
    clock.tick(60)
