import pygame
import random
import math

# Initialize the pygame
pygame.init()

# Create a window
screen = pygame.display.set_mode((800, 600))

# Window Title and icons
pygame.display.set_caption("Space War")
icon = pygame.image.load('assets/icon.png')
background = pygame.image.load('assets/background.png')
pygame.display.set_icon(icon)

# create a player
player = pygame.image.load('assets/player.png')
playerX = 400 - 32
playerY = 480
player_velocity = 5
change = 0

# create a enemy
enemy = pygame.image.load('assets/enemy.png')
enemyX = random.randint(0,800-64)
enemyY = random.randint(50,160)
enemy_velocity_x = 4
enemy_velocity_y = 40

# create a bullet
bullet = pygame.image.load('assets/bullet.png')
bulletX = 0
bulletY = 480+16
bullet_velocity_y = 10
bullet_state = "ready"


score = 0

def isCollision(ex,ey,bx,by):
    distance = math.sqrt((ex+32-bx-16)**2+(ey+32-by-16)**2)
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
    screen.blit(bullet, (x+32-16, y))


# Main game loop
gameon = True
while gameon:

    # background color
    screen.fill((0, 0, 0))
    screen.blit(background,(0,0))

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
                    bulletX = playerX
                    fire(bullet,bulletX,bulletY)

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

    #for enemy
    enemyX += enemy_velocity_x
    if enemyX >= 736:
        enemy_velocity_x *= -1
        enemyY += enemy_velocity_y
    if enemyX <= 0:
        enemy_velocity_x *= -1
        enemyY += enemy_velocity_y

    #bullet
    if bullet_state == "fire":
        bulletY -= bullet_velocity_y
        fire(bullet,bulletX,bulletY)

        #Checking Collission
        if isCollision(enemyX,enemyY,bulletX,bulletY):
            bullet_state = "ready"
            bulletY = 480 - 16
            enemyX = random.randint(0, 800 - 64)
            enemyY = random.randint(50, 160)
            score +=1
            print(score)

    if bulletY <= 0:
        bullet_state = "ready"
        bulletY = 480-16

    # drawing game charecters
    player_update(player, playerX, playerY)
    enemy_update(enemy, enemyX, enemyY)
    pygame.display.update()
