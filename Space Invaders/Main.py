###############  imports  ########################
import math
import random

import pygame
from pygame import mixer
###############  Intialize the pygame ####################
pygame.init()


###############  create the screen  #####################
screen = pygame.display.set_mode((800,600))


###############  Background ###########################
Background = pygame.image.load("background.png")


################  Title and Icon  ####################
pygame.display.set_caption("Space Invaders")


################  player  #################
playerImg = pygame.image.load("Player.png")
playerX = 370
playerY = 480
playerX_change = 0


################  using blit makes it draw on the screen  ###############################
def player(x,y):
    screen.blit(playerImg, (x, y))


##################   Enemy  #############################################################
#making mutiple enemy's
EnemyImg = []
EnemyX = []
EnemyY = []
EnemyX_change = []
EnemyY_change = []
num_eme = 6
# Ememy
for i in range(num_eme):
    EnemyImg.append(pygame.image.load('enemy.png'))
    EnemyX.append(random.randint(0, 736))
    EnemyY.append(random.randint(50, 150))
    EnemyX_change.append(4)
    EnemyY_change.append(40)


##################   Bullet  ###########################################################
# ready = you can't see the bullet on the screen
#fire = the bullet is currently moving
bulletImg = pygame.image.load("Bullet.png")
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 6
bullet_state = "ready"

#################  Score  #########################################################
score_value = 0
font = pygame.font.Font('freesansbold.ttf', 32)

textX = 10
textY = 10
##################  Game Over  #####################
over_font = pygame.font.Font('freesansbold.ttf', 64)


##################  using blit makes it draw on the screen  ###########################
def show_score(x,y):
    score = font.render("score : " + str(score_value), True, (255, 255, 255))
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(over_text, (250, 250))


def player(x, y):
    screen.blit(playerImg, (x, y))

def Enemy(x, y, i):
    screen.blit(EnemyImg[i], (x, y))  

def fire_bullet(x,y):
    global bullet_state
    bullet_state = "fire"
    screen.blit (bulletImg, (x + 16, y + 10))

def isCollision(enemyX, enemyY, bulletX,bulletY):
    distance = math.sqrt(math.pow(enemyX - bulletX, 2) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False

############### Game Loop ################
running = True
while running:
    
    # RGB = Red , Green, Blue
    screen.fill((0,0,0))
############  Background Image  ##################
    screen.blit(Background, (0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
####################  if keystroke is pressed check whether it is right or left.  ######################
        if event.type == pygame.KEYDOWN:
            if event.key ==pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                #get the current X cordinate of the spaceship
                   bulletX = playerX
                   fire_bullet(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                   playerX_change = 0
# 5 = 5 + -0.01 -> 5=5 - 0.1
# 5 = 5 + 0.1

    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736
     
     #  movement of enemy
    for i in range(num_eme):

        # Game Over
        if EnemyY[i] > 440:
            for j in range(num_eme):
                EnemyY[j] = 2000
            game_over_text()
            break
        
        EnemyX[i] += EnemyX_change[i]
        if EnemyX[i] <= 0:
            EnemyX_change[i] = 4
            EnemyY[i] += EnemyY_change[i]
        elif EnemyX[i] >= 736:
            EnemyX_change[i] = -4
            EnemyY[i] += EnemyY_change[i]
#######################  Collision  ##################################
        collision = isCollision(EnemyX[i], EnemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            EnemyX[i] = random.randint(0, 736)
            EnemyY[i] = random.randint(50, 150)
        Enemy(EnemyX[i], EnemyY[i], i)
####################  Bullet Movement  #########################
    if bulletY <=0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change
    
    player(playerX, playerY)
    show_score(textX,textY)
    pygame.display.update()