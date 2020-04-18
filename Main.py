import pygame, sys, random
from random import randint
# Define some colors
BLACK = (200,200, 200)
WHITE = (255, 255, 255)
speedd = 1
rings = 5
final_score = 0
size = width, height = 800, 600
screen = pygame.display.set_mode(size)
pygame.display.set_caption('Ring Collector')
class Block(pygame.sprite.Sprite):
    # constructor
    def __init__(self, width, height, isPlayer):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        if isPlayer:
            self.image = pygame.Surface([width, height])
            self.image.fill(background_color)
        else:
            self.image = pygame.image.load('ring.png').convert()
        self.rect = self.image.get_rect()


# Initialize Pygame
pygame.init()
sound_dead = pygame.mixer.Sound('dead.wav')
sound_points = pygame.mixer.Sound('points.wav')
sound_stage = pygame.mixer.Sound('nextstage.wav')
# Set the height and width of the screen
width_range, height_range = 750, 550
# This is a list of 'sprites.'
block_list = pygame.sprite.Group()
all_sprites_list = pygame.sprite.Group()
num_box_hit = 0

# -------- Main Program Loop -----------
while 1:
    background_color = (random.randrange(200), random.randrange(200), random.randrange(200))
    clock = pygame.time.Clock()

    for i in range(rings):
        ring_n_player = Block(20, 15, False)
        # Set a random location for the block
        ring_n_player.rect.x = random.randrange(width_range)
        ring_n_player.rect.y = random.randrange(height_range)
        # Add the block to the list of objects
        block_list.add(ring_n_player)
        all_sprites_list.add(ring_n_player)
    player_rect = Block(10, 20, True)
    all_sprites_list.add(player_rect)
    if randint(0, 1) == 0:
        speed = [-speedd, -speedd]
    else:
        speed = [speedd, speedd]
    b = pygame.sprite.Sprite() # create sprite
    spike = pygame.image.load("spike.png")
    b.hero = pygame.image.load("hero.png")
    hero_rect = b.hero.get_rect()
    spike_rand_x = randint(10, 750)
    spike_rand_y = randint(10, 550)
    spike_rect = spike.get_rect()
    pygame.mixer.init()
    playSound = True
    dead = False
    restart = False

    while 1:
        screen.fill(background_color)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                restart = True
                break
        pos = pygame.mouse.get_pos()
        player_rect.rect.x = pos[0]
        player_rect.rect.y = pos[1]
        # See if the HERO is grabbing coins
        if not dead:
            blocks_hit_list = pygame.sprite.spritecollide(player_rect, block_list, True)
            # Check the list of collisions.
            for ring_n_player in blocks_hit_list:
                num_box_hit += 1
                sound_points.play()
                final_score += 1
        spike_rect = spike_rect.move(speed)
        if spike_rect.left + spike_rand_x < 0 or spike_rect.right + spike_rand_x > width:
            speed[0] = -speed[0]
        if spike_rect.top + spike_rand_y < 0 or spike_rect.bottom + spike_rand_y > height:
            speed[1] = -speed[1]
        # Draw all the spites
        all_sprites_list.draw(screen)
        screen.blit(b.hero, (pos[0] - 10, pos[1] - 20))
        screen.blit(spike, (spike_rect.x+spike_rand_x, spike_rect.y+spike_rand_y))
        font = pygame.font.SysFont("calibri", 40)
        score1 = font.render(str(final_score), True, (255, 255, 255))
        screen.blit(score1, (10, 10))
        if (spike_rect.left + spike_rand_x) < pos[0] < (spike_rect.right + spike_rand_x) and \
                                (spike_rect.top + spike_rand_y) < pos[1] < (spike_rect.bottom + spike_rand_y):
            spike = pygame.image.load("hero_dead1.png")
            b.hero = pygame.image.load("clear.png")
            dead = True
            speed = [0, 0]
            speedd = 1
            if playSound:
                sound_dead.play()
                playSound = False
        if dead and restart:
            block_list.empty()
            all_sprites_list.empty()
            num_box_hit = 0
            final_score = 0
            break
        if num_box_hit == rings:
            block_list.empty()
            all_sprites_list.empty()
            num_box_hit = 0
            speedd += 1
            sound_stage.play()
            break
        pygame.display.flip()
        # 100 frames per second
        clock.tick(100)