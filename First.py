import pygame
from src.Player import Player
from src.Enemy import Enemy
from src.Missile import Missile

# loading images
player_image = pygame.image.load('src/img/player.png')
enemy_image = pygame.image.load('src/img/alien.png')
background_image = pygame.image.load('src/img/nebula_blue.png')
missile_image = pygame.image.load('src/img/missile.png')

# setting constants
RELOAD_SPEED = 400
MOVE_DOWN = 3000
ENEMIES = 36
WHITE = (255, 255, 255)

# setting up pygame
pygame.init()
screen_size = screen_width, screen_height = 800, 600
screen = pygame.display.set_mode(screen_size, 0, 32)
pygame.display.set_caption('Space Invader')
font = pygame.font.SysFont("monospace", 15)
win_font = pygame.font.SysFont("monospace", 45)

# creating events for the timers
move_down_event = pygame.USEREVENT + 1
reloaded_event = pygame.USEREVENT + 2

move_left = True
reloaded = True

# groups
block_list = pygame.sprite.Group()
missile_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()

temp_x = 40
temp_y = 40
for i in range(ENEMIES):
    block = Enemy(enemy_image)
    # dislike using random when they should preferably be ordered in "blocks"
    # block.rect.x = random.randrange(screen_width - 40)
    # block.rect.y = random.randrange(screen_height - 300)
    block.rect.x = temp_x
    block.rect.y = temp_y

    if temp_x < screen_width - 80:
        temp_x += 40
    else:
        temp_x = 40
        temp_y += 40

    block_list.add(block)
    all_sprites_list.add(block)

# variables
score = 0
running = True
clock = pygame.time.Clock()
player = Player((screen_width / 2) - 40, screen_height - 40, player_image, screen)
all_sprites_list.add(player)

# set the timers
pygame.time.set_timer(move_down_event, MOVE_DOWN)

# setting win label
win_label = win_font.render("YOU WIN!", 1, WHITE)

while running:
    # setting up labels, have to do in loop to update the variables
    score_label = font.render("Score: " + str(score), 1, WHITE)

    # lock the framerate
    clock.tick(60)

    # events
    e = pygame.event.poll()
    key = pygame.key.get_pressed()
    if e.type == pygame.QUIT:
        running = False
    if key[pygame.K_ESCAPE]:
        running = False

    if e.type == move_down_event:
        for block in block_list:
            block.rect.y += 40
    if e.type == reloaded_event:
        reloaded = True
        pygame.time.set_timer(reloaded_event, 0)

    if key[pygame.K_LEFT]:
        if player.rect.x < -20:
            player.rect.x = screen_width
        player.rect.x -= 5
    elif key[pygame.K_RIGHT]:
        if player.rect.x > screen_width:
            player.rect.x = - 20
        player.rect.x += 5

    if key[pygame.K_SPACE]:
        if reloaded:
            shot = Missile(missile_image)
            shot.rect.x = player.rect.x + 26
            shot.rect.y = player.rect.y - 12
            missile_list.add(shot)
            all_sprites_list.add(shot)
            reloaded = False
            pygame.time.set_timer(reloaded_event, RELOAD_SPEED)

    # check if the missiles have collided with anything
    for block in pygame.sprite.groupcollide(missile_list, block_list, True, True).keys():
        score += 1

    # moves the missile at a constant speed upwards -- will have to find way
    #  to make them fire in the direction the player is turned to
    for shot in missile_list:
        shot.rect.y -= 5

    # clear the screen
    screen.blit(background_image, (0, 0))

    # render
    screen.blit(score_label, (0, 0))
    if score == ENEMIES:
        screen.blit(win_label, ((screen_width/2) - 100, (screen_height/2) - 50))
    all_sprites_list.draw(screen)
    pygame.display.flip()

pygame.quit()
