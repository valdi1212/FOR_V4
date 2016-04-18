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
RESPAWN_SPEED = 10000
RELOAD_SPEED = 400
MOVE_GRUNTS_DOWN = 3000
# only change needed to change the speeds of the enemies is the constants
MOVE_ELITES_DOWN = 1500
ENEMIES = 16
WHITE = (255, 255, 255)


# setting up pygame
pygame.init()
screen_size = screen_width, screen_height = 800, 600
screen = pygame.display.set_mode(screen_size, 0, 32)
pygame.display.set_caption('Space Invader')
font = pygame.font.SysFont("monospace", 15)
large_font = pygame.font.SysFont("monospace", 45)
# setting the number of enemies in a single row
ROWSIZE = ((screen_width/2) - 80) / 40

# creating events for the timers
move_grunts_down_event = pygame.USEREVENT + 1
move_elites_down_event = pygame.USEREVENT + 2
reloaded_event = pygame.USEREVENT + 3
respawn_event = pygame.USEREVENT + 4

move_left = True
reloaded = True

# groups
grunt_list = pygame.sprite.Group()
elite_list = pygame.sprite.Group()
enemy_list = pygame.sprite.Group()
missile_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()


def spawn_grunts(count):
    temp_x = 40
    temp_y = 40
    for i in range(count):
        block = Enemy(enemy_image)
        block.rect.x = temp_x
        block.rect.y = temp_y

        if temp_x < (screen_width/2) - 80:
            temp_x += 40
        else:
            temp_x = 40
            temp_y += 40

        grunt_list.add(block)
        enemy_list.add(block)
        all_sprites_list.add(block)


def spawn_elites(count):
    temp_x = (screen_width/2) + 40
    temp_y = 40
    for i in range(count):
        block = Enemy(enemy_image)
        block.rect.x = temp_x
        block.rect.y = temp_y

        if temp_x < screen_width - 80:
            temp_x += 40
        else:
            temp_x = (screen_width/2) + 40
            temp_y += 40

        elite_list.add(block)
        enemy_list.add(block)
        all_sprites_list.add(block)

spawn_elites(ENEMIES)
spawn_grunts(ENEMIES)

# variables
score = 0
running = True
clock = pygame.time.Clock()
player = Player((screen_width / 2) - 40, screen_height - 40, player_image, screen)
all_sprites_list.add(player)

# set the timers
pygame.time.set_timer(move_grunts_down_event, MOVE_GRUNTS_DOWN)
pygame.time.set_timer(move_elites_down_event, MOVE_ELITES_DOWN)
pygame.time.set_timer(respawn_event, RESPAWN_SPEED)

# setting lose label
lose_label = large_font.render("YOU LOSE!", 1, WHITE)

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
    if player.alive:
        if e.type == move_grunts_down_event:
            for block in grunt_list:
                block.rect.y += 40
        if e.type == move_elites_down_event:
            for block in elite_list:
                block.rect.y += 40
        if e.type == reloaded_event:
            reloaded = True
            pygame.time.set_timer(reloaded_event, 0)
        if e.type == respawn_event:
            spawn_grunts(ROWSIZE * 2)
            spawn_elites(ROWSIZE * 2)

        if key[pygame.K_a]:
            if player.rect.x < -20:
                player.rect.x = screen_width
            player.rect.x -= 5
        elif key[pygame.K_d]:
            if player.rect.x > screen_width:
                player.rect.x = - 20
            player.rect.x += 5

        # adding movement on y-axis
        if key[pygame.K_w]:
            player.rect.y -= 5
        elif key[pygame.K_s]:
            player.rect.y += 5

        # adding rotation
        if e.type == pygame.KEYDOWN:
            if key[pygame.K_q]:
                player.rotate_left()
            elif key[pygame.K_e]:
                player.rotate_right()

        if key[pygame.K_SPACE]:
            if reloaded:
                shot = Missile(missile_image, player.dir)
                # center the missile in the player rect
                shot.rect.center = player.rect.center
                missile_list.add(shot)
                all_sprites_list.add(shot)
                # resets the reloading proccess
                reloaded = False
                pygame.time.set_timer(reloaded_event, RELOAD_SPEED)

    # check if the player has collided with an enemy
    for block in pygame.sprite.spritecollide(player, enemy_list, 1):
        player.alive = False

    # check if the missiles have collided with anything
    for block in pygame.sprite.groupcollide(missile_list, grunt_list, True, True).keys():
        score += 1

    for block in pygame.sprite.groupcollide(missile_list, elite_list, True, True).keys():
        score += 5

    # moves the missile at a constant speed upwards -- will have to find way
    #  to make them fire in the direction the player is turned to
    for shot in missile_list:
        shot.fly()

    # clear the screen
    screen.blit(background_image, (0, 0))

    # render
    screen.blit(score_label, (0, 0))
    # chekcs if the player is alive, if not kill all sprites and display lose message
    if not player.alive:
        for sprite in all_sprites_list:
            sprite.kill()
        screen.blit(lose_label, ((screen_width/2) - 100, (screen_height/2) - 50))
    # updates the player rotation
    player.update()
    all_sprites_list.draw(screen)
    pygame.display.flip()

pygame.quit()
