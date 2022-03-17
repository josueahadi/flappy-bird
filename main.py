# LIBRARIES #
import pygame, sys, random

# FUNCTIONS & SUBPROCEDURES #

def draw_floor():
    screen.blit(floor_surface, (floor_x_pos, floor_y_pos)) 
    screen.blit(floor_surface, (floor_x_pos+screen_w, floor_y_pos))

def create_pipe():
    random_pipe_pos = random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop = (pipe_x_pos, random_pipe_pos))
    top_pipe = pipe_surface.get_rect(midbottom = (pipe_x_pos, random_pipe_pos - 210))
    return bottom_pipe, top_pipe

def move_pipes(pipes):
    for pipe in pipes:
        pipe.centerx -= 5
    return pipes

def draw_pipes(pipes):
    for pipe in pipes:
        if pipe.bottom >= screen_h:
            screen.blit(pipe_surface, pipe)
        else:
            flip_pipe = pygame.transform.flip(pipe_surface, False, True)
            screen.blit(flip_pipe, pipe)

def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            return False
        
    if bird_rect.top <= -100 or bird_rect.bottom >= floor_y_pos:
        return False
    
    return True

def rotate_bird(bird):
    new_bird

# INITIALIZATION #

pygame.init()

screen_w = 403.2
screen_h = 716.8
screen = pygame.display.set_mode((screen_w, screen_h))  # Canvas
scale_factor = 1.428571429
clock = pygame.time.Clock() 

# GAME VARIABLES #

gravity = 0.25 # Not the real value but an abstract value
bird_movement = 0
game_active = True

bg_surface = pygame.image.load('sprites/background-day.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (screen_w, screen_h))

floor_w = screen_w
floor_h = 112
floor_surface = pygame.image.load('sprites/base.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (screen_w, floor_h))
floor_x_pos = 0
floor_y_pos = 630

bird_w = 34*scale_factor
bird_h = 24*scale_factor
bird_surface = pygame.image.load('sprites/bluebird-midflap.png').convert()
bird_surface = pygame.transform.scale(bird_surface, (bird_w, bird_h))
bird_startx = 70
bird_starty = 358.4
# Next line takes bird_surface and creates a rectangle around it
bird_rect = bird_surface.get_rect(center = (bird_startx, bird_starty))
 
pipe_w = 52*scale_factor
pipe_h = 320*scale_factor
pipe_surface = pygame.image.load('sprites/pipe-green.png').convert()
pipe_surface = pygame.transform.scale(pipe_surface, (pipe_w, pipe_h))
pipe_list = []
SPAWNPIPE = pygame.USEREVENT # Triggered by timer
pygame.time.set_timer(SPAWNPIPE, 1200) # Trigger event every 1.2 seconds
pipe_x_pos = screen_w + (2*pipe_w)
pipe_y_pos = screen_h/2
pipe_height = [300, 420, 560] # Possible heights the pipes can have 

# GAME LOOP #

while True:
    for event in pygame.event.get(): # event loop
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() # Shuts down game completely

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                bird_movement = 0
                bird_movement -= 8.399999997
            
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (bird_startx, bird_starty)
                bird_movement = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())
            
    
    screen.blit(bg_surface, (0,0))
    
    if game_active:
        # Bird
        bird_movement += gravity
        rotated_bird = rotate_bird(bird_surface)
        bird_rect.centery += bird_movement
        screen.blit(rotated_surface, bird_rect)

        # Collision
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -screen_w:
        floor_x_pos = 0

    pygame.display.update()
    # Limit frame rate
    clock.tick(120)