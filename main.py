import pygame
import random
import math

from pygame import mixer
# Intialize the pygame
pygame.init()

# create the screen
screen = pygame.display.set_mode((800, 600))

background = pygame.image.load('dp.png')
mixer.music.load('background.wav')
mixer.music.play(-1)

pygame.display.set_caption("Star Wars Game")
icon = pygame.image.load('enemy.png')
pygame.display.set_icon(icon)

playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemies = 9

for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(0.4)
    enemyY_change.append(40)

bulletImg = pygame.image.load('bulletg.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 2
bullet_state = "ready"


score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10

over_font = pygame.font.Font('freesansbold.ttf', 64)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, (0, 255, 0))
    screen.blit(score, (x, y))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))

def game_over():
    score = "Final Score  "+ str(score_value)
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    score_text = font.render(score, True, (255, 255, 0))
    screen.blit(over_text, (200, 250))
    screen.blit(score_text, (300, 330))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    dist = math.sqrt(math.pow(enemyX-bulletX, 2) + math.pow(enemyY - bulletY, 2))
    if dist < 27:
        return True
    else:
        return False


running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -0.4
            if event.key == pygame.K_RIGHT:
                playerX_change = 0.4
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    bullet_Sound = mixer.Sound('laser.wav')
                    bullet_Sound.play()
                    bulletX = playerX
                    bullet(bulletX, bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    playerX += playerX_change

    if playerX <= 0:
        playerX = 0
    elif playerX >=736:
        playerX = 736

    for i in range(num_of_enemies):
        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over()
            break

        enemyX[i] += enemyX_change[i]

        if enemyX[i] <= 0:
            enemyX_change[i] = 0.3
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -0.3
            enemyY[i] += enemyY_change[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            explosion_Sound = mixer.Sound('explosion.wav')
            explosion_Sound.play()
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(50, 150)



        enemy(enemyX[i], enemyY[i], i)

    #bullet movement
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        bullet(bulletX, bulletY)
        bulletY -= bulletY_change


    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()

