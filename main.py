# LIBRARIES #
from optparse import check_choice
from tabnanny import check
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
            collision_sound.play()
            return False
        
    if bird_rect.top <= -100 or bird_rect.bottom >= floor_y_pos:
        return False
    
    return True

def rotate_bird(bird):
    new_bird = pygame.transform.rotozoom(bird, -bird_movement *3, 1)
    return new_bird

def bird_animation():
    new_bird = bird_frames[bird_index]
    new_bird_rect = new_bird.get_rect(center = (bird_startx, bird_rect.centery))

    return new_bird, new_bird_rect

def score_display(game_state):
# GAME STATES
    if game_state == 'menu':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255,255,255))
        score_rect = score_surface.get_rect(center = (screen_w/2, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255,255,255))
        high_score_rect = score_surface.get_rect(center = (screen_w/2.4, 595))
        screen.blit(high_score_surface, high_score_rect)

    if game_state == 'playing':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255,255,255))
        score_rect = score_surface.get_rect(center = (screen_w/2, 100))
        screen.blit(score_surface, score_rect)

    if game_state == 'game_over':
        score_surface = game_font.render(f'Score: {int(score)}', True, (255,255,255))
        score_rect = score_surface.get_rect(center = (screen_w/2, 100))
        screen.blit(score_surface, score_rect)

        high_score_surface = game_font.render(f'High score: {int(high_score)}', True, (255,255,255))
        high_score_rect = score_surface.get_rect(center = (screen_w/2.4, 595))
        screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
    if score > high_score:
        high_score = score
    return high_score

# INITIALIZATION #

#pygame.mixer.pre_init(frequency = 44100, size = 16, channels = 1, buffer = 512)

pygame.init()

screen_w = 403.2
screen_h = 716.8
screen = pygame.display.set_mode((screen_w, screen_h))  # Canvas
scale_factor = 1.428571429
clock = pygame.time.Clock() 
game_font = pygame.font.Font('font/04B_19.TTF', 28)

# GAME VARIABLES #

gravity = 0.25 # Not the real value but an abstract value
bird_movement = 0
game_active = True
gameover = True
startup_menu = True
score = 0
high_score = 0

bg_surface = pygame.image.load('sprites/background-day.png').convert()
bg_surface = pygame.transform.scale(bg_surface, (screen_w, screen_h))

msg_w = 184*scale_factor
msg_h = 267*scale_factor
menu_surface = pygame.transform.scale((pygame.image.load('sprites/message.png').convert_alpha()), (msg_w, msg_h))
menu_rect = menu_surface.get_rect(center = (screen_w/2, screen_h/2))

gameover_surface = pygame.transform.scale((pygame.image.load('sprites/gameover-msg.png').convert_alpha()), (msg_w, msg_h))
gameover_rect = gameover_surface.get_rect(center = (screen_w/2, screen_h/2))

floor_w = screen_w
floor_h = 112
floor_surface = pygame.image.load('sprites/base.png').convert()
floor_surface = pygame.transform.scale(floor_surface, (screen_w, floor_h))
floor_x_pos = 0
floor_y_pos = 630

bird_w = 34*scale_factor
bird_h = 24*scale_factor
bird_startx = 70
bird_starty = 358.4

# bird_surface = pygame.image.load('sprites/bluebird-midflap.png').convert_alpha()
# bird_surface = pygame.transform.scale(bird_surface, (bird_w, bird_h))
# # Next line takes bird_surface and creates a rectangle around it
# bird_rect = bird_surface.get_rect(center = (bird_startx, bird_starty))

bird_downflap = pygame.transform.scale(pygame.image.load('sprites/bluebird-downflap.png').convert_alpha(), (bird_w, bird_h))
bird_midflap = pygame.transform.scale(pygame.image.load('sprites/bluebird-midflap.png').convert_alpha(), (bird_w, bird_h))
bird_upflap = pygame.transform.scale(pygame.image.load('sprites/bluebird-upflap.png').convert_alpha(), (bird_w, bird_h))
bird_frames = [bird_downflap, bird_midflap, bird_upflap]
bird_index = 0
bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center = (bird_startx, bird_starty))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

 
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

flap_sound = pygame.mixer.Sound('sound/sfx_wing.wav')
collision_sound = pygame.mixer.Sound('sound/sfx_hit.wav')
score_sound = pygame.mixer.Sound('sound/sfx_point.wav')
score_sound_countdown = 200


# GAME LOOP #
 
while True:
    for event in pygame.event.get(): # event loop
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit() # Shuts down game completely

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and game_active:
                startup_menu = False
                bird_movement = 0
                bird_movement -= 8.399999997
                flap_sound.play()
            
            if event.key == pygame.K_SPACE and game_active == False:
                game_active = True
                pipe_list.clear()
                bird_rect.center = (bird_startx, bird_starty)
                bird_movement -= 8.399999997
                score = 0

        if event.type == SPAWNPIPE:
            pipe_list.extend(create_pipe())

        if event.type == BIRDFLAP:
            if bird_index < 2:
                bird_index += 1
            else:
                bird_index = 0

            bird_surface, bird_rect = bird_animation()
            
    
    screen.blit(bg_surface, (0,0))
    
    if game_active and startup_menu == False:
        # Bird
        bird_movement += gravity
        bird_rect.centery += bird_movement
        rotated_bird = rotate_bird(bird_surface)
        screen.blit(rotated_bird, bird_rect)

        # Collision
        game_active = check_collision(pipe_list)

        # Pipes
        pipe_list = move_pipes(pipe_list)
        draw_pipes(pipe_list)

        # Score
        score+=0.005
        score_display('playing')
        
        score_sound_countdown -= 1
        if score_sound_countdown <= 0:
            score_sound.play()
            score_sound_countdown = 200

    if game_active and startup_menu:
        gameover = False
        bird_movement = 0
        # Menu
        screen.blit(menu_surface, menu_rect)
        high_score = update_score(score, high_score)
        score_display('menu')

    if game_active == False:
        gameover = True
        bird_movement = 0
        screen.blit(gameover_surface, gameover_rect)
        high_score = update_score(score, high_score)
        score_display('game_over')

    # Floor
    floor_x_pos -= 1
    draw_floor()
    if floor_x_pos <= -screen_w:
        floor_x_pos = 0

    pygame.display.update() 
    # Limit frame rate
    clock.tick(120)