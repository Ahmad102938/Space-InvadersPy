import pygame
import random
import math
from pygame import mixer

# intialze the pygame
pygame.init()

screen = pygame.display.set_mode((800, 600))

# background
background = pygame.image.load('IMG/background1.jpg')

# background sound
mixer.music.load('Audio/backgroundms.wav')
mixer.music.play(-1)
 
# title and logo
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('IMG/spaceship.png')
pygame.display.set_icon(icon)

# quit button
quit_font = pygame.font.Font('freesansbold.ttf', 32)
surf = quit_font.render('Quit', True, (204,0,0))
button = pygame.Rect(700, 10, 80, 50)

# player
playerimg = pygame.image.load('IMG/shooter.png')
playerx = 370
playery = 500
playerx_change = 0

# enemy
enemyimg = []
enemyx = []
enemyy = []
enemyX_change = []
enemyY_change = []
NumOfEnemy = 6

for i in range(NumOfEnemy):
    enemyimg.append(pygame.image.load('IMG/alien.png'))
    enemyx.append(random.randint(0, 736))
    enemyy.append(random.randint(50, 200))
    enemyX_change.append(0.7)
    enemyY_change.append(40)

# bullet
bulletimg = pygame.image.load('IMG/bullet.png')
bulletX = 0
bulletY = 500
bulletX_change = 0.7
bulletY_change = 3
bullet_state = "ready"

# score
score = 0
font = pygame.font.Font('font/coffeeTerrace.ttf', 40)
scoreX =10
scoreY = 10

def Show_Score(x, y):
    Is_score = font.render("Score: " + str(score), True, (255, 255, 0))
    screen.blit(Is_score, (x, y))

# game over
over_font = pygame.font.Font('font/gameover.ttf', 150)

def Game_Over():
    over = over_font.render("GAME OVER", True, (204, 0, 0))
    Is_score = over_font.render("Score: " + str(score), True, (255, 255, 0))
    screen.blit(over, (250, 250))
    screen.blit(Is_score, (250, 150))
    
def player(x, y):
    screen.blit(playerimg, (x, y))
    
def enemy(x, y, i):
    screen.blit(enemyimg[i], (x, y))
    
def fire(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletimg, (x+16, y+10))
    
def collision(enemyx, enemyy, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyx-bulletX, 2)) + (math.pow(enemyy-bulletY, 2)))
    if distance < 27:
        return True
    else:
        return False
    
# gameloop

running = True
while running:
    screen.fill((0, 0, 0))
    # background image
    screen.blit(background, (0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # quit mouse button function
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button.collidepoint(event.pos):
                running = False
        
        # keyboard mechanism
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerx_change = -1.3
            if event.key == pygame.K_RIGHT:
                playerx_change = 1.3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    Bullet_Sound = mixer.Sound('Audio/laser.wav')
                    Bullet_Sound.play()
                    bulletX = playerx
                    fire(bulletX, bulletY)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerx_change = 0
    
    # hovering effect in quit button
    a,b = pygame.mouse.get_pos()
    if button.x <= a <= button.x + 80 and button.y <= b <= button.y + 50:
        pygame.draw.rect(screen, (32,32,32), button)
    else:
        pygame.draw.rect(screen, (0,0,0), button)
    screen.blit(surf,(button.x +5, button.y+5))     
    # player boundries
    playerx += playerx_change
    if playerx <= 0:
        playerx = 0
    elif playerx >=736:
        playerx = 736
        
    # enemy movement 
    for i in range(NumOfEnemy):
        # game over
        if enemyy[i] >=460:
            for j in range(NumOfEnemy):
                enemyy[j] = 1500
            Game_Over()
            break
        
        enemyx[i]+= enemyX_change[i] 
        if enemyx[i] <= 0:
            enemyX_change[i] = 0.7
            enemyy[i] = enemyy[i] + enemyY_change[i]
        elif enemyx[i] >=736:
            enemyX_change[i] = -0.7
            enemyy[i] = enemyy[i] + enemyY_change[i]
            
        # collision
        collied = collision(enemyx[i], enemyy[i], bulletX, bulletY)
        if collied:
            collapse_Sound = mixer.Sound('Audio/collapse.wav')
            collapse_Sound.play()
            bulletY = 500
            bullet_state = "ready"
            score += 1
            # print(score)
            enemyx[i] = random.randint(0, 736)
            enemyy[i] = random.randint(50, 200)
            
        enemy(enemyx[i], enemyy[i], i)
        
    # bullet movement
    if bulletY <=0:
        bulletY = 500
        bullet_state  = "ready"
    
    if bullet_state is "fire":
        fire(bulletX, bulletY)
        bulletY -= bulletY_change
          
    player(playerx, playery)
    Show_Score(scoreX, scoreY)
    pygame.display.update()