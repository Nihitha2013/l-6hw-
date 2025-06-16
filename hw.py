import math
import random
import pygame

pygame.init()

screen_width = 800
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Space Game")
background = pygame.image.load("background.png")



playerImg = pygame.image.load("player.png")  
playerX = 370
playerY = 380
playerX_change = 0

enemyImg = []
enemyX = []
enemyY = []
enemyX_change = []
enemyY_change = []
num_of_enemy = 6

for _ in range(num_of_enemy):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, screen_width - 64))
    enemyY.append(random.randint(50, 150))
    enemyX_change.append(4)
    enemyY_change.append(40)

bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = playerY
bulletY_change = 10
bullet_state = "ready"  

score_value = 0
font = pygame.font.Font("freesansbold.ttf", 30)
textX = 10
textY = 10


over_font = pygame.font.Font("freesansbold.ttf", 60)

def show_score(x, y):
    score = font.render("Score: " + str(score_value), True, "white")
    screen.blit(score, (x, y))

def game_over_text():
    over_text = over_font.render("Game Over", True, "white")
    screen.blit(over_text, (200, 250))

def player(x, y):
    screen.blit(playerImg, (x, y))

def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))

def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10)) 

def isCollision(enemyX, enemyY, bulletX, bulletY):
    dist = math.sqrt((enemyX - bulletX) ** 2 + (enemyY - bulletY) ** 2)
    return dist < 27

running = True
while running:
    screen.fill((0, 0, 0))
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -5
            if event.key == pygame.K_RIGHT:
                playerX_change = 5
            if event.key == pygame.K_SPACE:
                if bullet_state == "ready":
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)


        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

  
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= screen_width - 64:
        playerX = screen_width - 64

 
    for i in range(num_of_enemy):
     
        if enemyY[i] > 340:
            for j in range(num_of_enemy):
                enemyY[j] = 2000  
            game_over_text()
            break

        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 4
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= screen_width - 64:
            enemyX_change[i] = -4
            enemyY[i] += enemyY_change[i]

        
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = playerY
            bullet_state = "ready"
            score_value += 1
            enemyX[i] = random.randint(0, screen_width - 64)
            enemyY[i] = random.randint(50, 150)

        enemy(enemyX[i], enemyY[i], i)

    
    if bullet_state == "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change

    if bulletY <= 0:
        bulletY = playerY
        bullet_state = "ready"

    player(playerX, playerY)
    show_score(textX, textY)
    pygame.display.update()



