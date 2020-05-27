import sys
import json
import random
import pygame

pygame.init()
clock = pygame.time.Clock()

screen_height = 786
screen_width = 1024
middle_canvas_x = screen_width / 2
middle_canvas_y = screen_height / 2

white = (91, 91, 91)
red = (225, 0, 0)

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Duck Runner')

# Sprites #

idleSprite = pygame.image.load("sprites/sprite_0.png").convert_alpha()
runSprites = [pygame.image.load("sprites/sprite_1.png").convert_alpha(),
              pygame.image.load("sprites/sprite_2.png").convert_alpha()]
startanimation = [pygame.image.load("sprites/startanimation0.png").convert_alpha(),
                  pygame.image.load("sprites/startanimation1.png").convert_alpha()]
ground = pygame.image.load("sprites/ground.png").convert_alpha()
titlescreen = pygame.image.load("sprites/titlescreen.png").convert_alpha()
deadduck = pygame.image.load("sprites/deadscene.png").convert_alpha()
enemy_1 = pygame.image.load("sprites/enemy_1.png").convert_alpha()
enemy_2 = pygame.image.load("sprites/enemy_2.png").convert_alpha()
enemy_3 = pygame.image.load("sprites/enemy_3.png").convert_alpha()
clouds = pygame.image.load("sprites/clouds.png").convert_alpha()

# Icons #

iconHover = pygame.image.load("icons/icons0.png").convert_alpha()
iconCredits = pygame.image.load("icons/icons1.png").convert_alpha()
iconStart = pygame.image.load("icons/icons2.png").convert_alpha()
iconShop = pygame.image.load("icons/icons3.png").convert_alpha()


class charachterHandler(object):
    def __init__(self):
        self.currentCharactherID = 1

    def loadCharachter(self):
        return


class player(object):
    def __init__(self):
        self.player = pygame.Rect(50,570,64,128)
        self.jump = False
        self.jumpCooldown = False

    def renderPlayer(self):
        pygame.draw.rect(screen, red, self.player)
        if self.jump:
            if not menu.isMainMenu:
                self.player.y -= 20
        if self.player.y < 300:
            self.jump = False
            self.jumpCooldown = True
        if self.jumpCooldown:
            if not menu.isMainMenu:
                self.player.y += 10
                if self.player.y > 569:
                    self.jumpCooldown = False

    def enemyCollosion(self):
        if self.player.colliderect(enviroment.enemyhitbox1):
            menu.isMainMenu = True
        if self.player.colliderect(enviroment.enemyhitbox2):
            menu.isMainMenu = True
        if self.player.colliderect(enviroment.enemyhitbox3):
            menu.isMainMenu = True

class enviroment(object):
    def __init__(self, speed=15):
        self.speed = speed
        self.cloudSpeed = 3
        self.groundhitbox1 = pygame.Rect(0, 666, 1200, 64)
        self.groundhitbox2 = pygame.Rect(1200, 666, 1200, 64)
        self.cloudshitbox1 = pygame.Rect(0, middle_canvas_y - 150, 1200, 64)
        self.cloudshitbox2 = pygame.Rect(1200, middle_canvas_y - 150, 1200, 64)
        self.enemyhitbox1 = pygame.Rect(1000, 606, 64, 80)
        self.enemyhitbox2 = pygame.Rect(2000, 606, 64, 80)
        self.enemyhitbox3 = pygame.Rect(3000, 606, 120, 80)

    def renderEnviroment(self):
        pygame.draw.rect(screen, white, self.groundhitbox1)
        pygame.draw.rect(screen, white, self.groundhitbox2)

        pygame.draw.rect(screen, white, self.cloudshitbox1)
        pygame.draw.rect(screen, white, self.cloudshitbox2)

        screen.blit(ground, (self.groundhitbox1.x, self.groundhitbox1.y))
        screen.blit(ground, (self.groundhitbox2.x, self.groundhitbox2.y))

        screen.blit(clouds, (self.cloudshitbox1.x, self.cloudshitbox1.y))
        screen.blit(clouds, (self.cloudshitbox2.x, self.cloudshitbox2.y))

        if not menu.isMainMenu:
            self.groundhitbox1.x -= self.speed
            self.groundhitbox2.x -= self.speed

        self.cloudshitbox1.x -= self.cloudSpeed
        self.cloudshitbox2.x -= self.cloudSpeed

        if self.groundhitbox1.right < 0:
            self.groundhitbox1.left = 1200
        if self.groundhitbox2.right < 0:
            self.groundhitbox2.left = 1200

        if self.cloudshitbox1.right < 0:
            self.cloudshitbox1.left = 1200
        if self.cloudshitbox2.right < 0:
            self.cloudshitbox2.left = 1200

    def renderEnemies(self):
        pygame.draw.rect(screen, white, self.enemyhitbox1)
        pygame.draw.rect(screen, white, self.enemyhitbox2)
        pygame.draw.rect(screen, white, self.enemyhitbox3)

        screen.blit(enemy_1, (self.enemyhitbox1.x, self.enemyhitbox1.y))
        screen.blit(enemy_2, (self.enemyhitbox2.x, self.enemyhitbox2.y))
        screen.blit(enemy_3, (self.enemyhitbox3.x, self.enemyhitbox3.y))

        if self.enemyhitbox1.right < 0:
            self.enemyhitbox1.x = random.uniform(3000, 1200)
        if self.enemyhitbox2.right < 0:
            self.enemyhitbox2.x = random.uniform(4500, 5000)
        if self.enemyhitbox3.right < 0:
            self.enemyhitbox3.x = random.uniform(9500, 10000)

        if not menu.isMainMenu:
            self.enemyhitbox1.x -= self.speed
            self.enemyhitbox2.x -= self.speed
            self.enemyhitbox3.x -= self.speed

    def relocateEnemies(self):
        self.enemyhitbox1.x = 1000
        self.enemyhitbox2.x = 2000
        self.enemyhitbox3.x = 3000

class counter(object):
    def __init__(self):
        self.counter = 0
        self.respawnCount = 0
        self.screenCount = 0

    def count(self):
        self.counter += 1
        if self.counter >= 30:
            self.counter = 0
            self.screenCount += 1
        if self.screenCount >= 2:
            self.screenCount = 0

    def respawn(self):
        self.respawnCount += 1
        print(self.respawnCount)
        if self.respawnCount >= 10:
            self.respawnCount = 0
            return True
        
class menu(object):
    def __init__(self):
        self.isMainMenu = True
        self.click = False
        self.upArrow = False

def menuHandeler():
    if menu.isMainMenu:
        screen.blit(titlescreen, (middle_canvas_x, middle_canvas_y - 300))
        screen.blit(startanimation[counter.screenCount], (middle_canvas_x - 290, middle_canvas_y - 300))
        
        mx, my = pygame.mouse.get_pos()

        iconHitbox2 = pygame.Rect(393 + 64, 355, 128, 128)
        iconHitbox1 = pygame.Rect(393 + 64 - 128, 355, 128, 128)
        iconHitbox3 = pygame.Rect(393 + 64 + 128, 355, 128, 128)

        pygame.draw.rect(screen, white, iconHitbox1)
        pygame.draw.rect(screen, white, iconHitbox2)
        pygame.draw.rect(screen, white, iconHitbox3)

        if iconHitbox1.collidepoint((mx, my)):
            screen.blit(iconHover, (iconHitbox1.x + 10, iconHitbox1.y + 10))
            if menu.click:
                menu.click = False

        if iconHitbox2.collidepoint((mx, my)):
            screen.blit(iconHover, (iconHitbox2.x + 10, iconHitbox2.y + 10))
            if menu.click:
                if counter.respawn():
                    menu.isMainMenu = False
                    enviroment.relocateEnemies()
                    menu.click = False

        if iconHitbox3.collidepoint((mx, my)):
            screen.blit(iconHover, (iconHitbox3.x + 10, iconHitbox3.y + 10))
            if menu.click:
                print("Clicked Shop")
                menu.click = False

        if menu.upArrow:
            if counter.respawn():
                menu.isMainMenu = False
                enviroment.relocateEnemies()
                menu.upArrow = False

        screen.blit(iconStart, (393 + 64, 355))
        screen.blit(iconCredits, (393 + 64 - 128, 355))
        screen.blit(iconShop, (393 + 64 + 128, 355))

def renderGraphics():
    screen.fill(white)
    enviroment.renderEnviroment()
    enviroment.renderEnemies()
    player.renderPlayer()
    player.enemyCollosion()
    counter.count()

# Game Loop #
player = player()
enviroment = enviroment()
counter = counter()
menu = menu()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if not player.jumpCooldown:
                    player.jump = True
                if menu.isMainMenu:
                    menu.upArrow = True
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            menu.click = True

    renderGraphics()
    menuHandeler()

    clock.tick(60)
    pygame.display.flip()