import pygame
import random
import math
from pygame import mixer

# Initialize the pygame
pygame.init()

# Create a window
screen = pygame.display.set_mode((800, 600))

# Window Title and icons
pygame.display.set_caption("Space War")
icon = pygame.image.load('assets/icon.png')
background = pygame.image.load('assets/background.png')
pygame.display.set_icon(icon)

# music
mixer.music.load('assets/audio/background.wav')
mixer.music.play(-1)

# create a player
player = pygame.image.load('assets/player.png')
playerX = 400 - 32
playerY = 480
player_velocity = 5
change = 0

# create a enemy
enemy = []
enemyX = []
enemyY = []
enmey_dir = []
enemy_velocity_x = []
enemy_velocity_y = 40
enemy_num = 6
enemy_kill_sound = mixer.Sound('assets/audio/explosion.wav')

for i in range(enemy_num):
    enemy.append(pygame.image.load('assets/enemy.png'))
    enemyX.append(random.randint(0, 800 - 64))
    enemyY.append(random.randint(50, 160))
    enmey_dir.append(random.randint(-1, 0))
    enemy_velocity_x.append(random.randint(3,6))

# create a bullet
bullet = pygame.image.load('assets/bullet.png')
bulletX = 0
bulletY = 480 + 16
bullet_velocity_y = 10
bullet_state = "ready"
bullet_sound = mixer.Sound('assets/audio/laser.wav')

score = 0
font = pygame.font.Font("freesansbold.ttf",20)
scoreX = 10
scoreY = 10
def show_score(x,y):
    score_value = font.render("Score : "+ str(score),True,(240,240,240))
    screen.blit(score_value,(x,y))

def isCollision(ex, ey, bx, by):
    distance = math.sqrt((ex + 32 - bx - 16) ** 2 + (ey + 32 - by - 16) ** 2)
    if distance <= 48:
        return True
    else:
        return False


def player_update(player, x, y):
    screen.blit(player, (x, y))


def enemy_update(enemy, x, y):
    screen.blit(enemy, (x, y))


def fire(bullet, x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bullet, (x + 32 - 16, y))


# Main game loop
gameon = True
while gameon:

    # background color
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameon = False

        # Handling keystrokes
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                change = -1 * player_velocity
            if event.key == pygame.K_RIGHT:
                change = player_velocity
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bullet_sound.play()
                    bulletX = playerX
                    fire(bullet, bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                change = 0

    # Checking Out of bounds
    # For player
    playerX += change
    if playerX >= 736:
        playerX = 736
    if playerX <= 0:
        playerX = 0

    # for enemy
    for i in range(enemy_num):
        enemy_update(enemy[i], enemyX[i], enemyY[i])
        enemyX[i] += enemy_velocity_x[i]
        if enemyX[i] >= 736:
            enemy_velocity_x[i] *= -1
            enemyY[i] += enemy_velocity_y
        if enemyX[i] <= 0:
            enemy_velocity_x[i] *= -1
            enemyY[i] += enemy_velocity_y

        # Checking Collission
        if isCollision(enemyX[i], enemyY[i], bulletX, bulletY):
            enemy_kill_sound.play()
            bullet_state = "ready"
            bulletY = 480 - 16
            enemyX[i] = random.randint(0, 800 - 64)
            enemyY[i] = random.randint(50, 160)
            enemy_velocity_x[i] = random.randint(3, 6)
            score += 1



    # bullet
    if bullet_state == "fire":
        bulletY -= bullet_velocity_y
        fire(bullet, bulletX, bulletY)


    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480 - 16

    # drawing game charecters
    player_update(player, playerX, playerY)
    show_score(scoreX, scoreY)
    pygame.display.update()
