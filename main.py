import pygame
import math
from pygame.locals import *
from sys import exit
from random import randint

pygame.init()
pygame.mixer.init()
pygame.font.init()

#Variáveis gerais
width = 640
height = 576
screen = pygame.display.set_mode((width, height))
points = 0
pygame.display.set_caption('Hollow Shooter')
background = pygame.image.load('sprites pixel/bg1.png').convert_alpha(screen)
relogio = pygame.time.Clock()
pygame.mouse.set_visible(False)
music = pygame.mixer.music.load('rolonaijogoswav (1).wav')
pygame.mixer.music.set_volume(0.13)
pygame.mixer.music.play(-1)
bulletSoundEffect = pygame.mixer.Sound('tiroEfeito.wav')
bulletSoundEffect.set_volume(0.25)
myFont = pygame.font.SysFont('Consolas', 30)
icon = pygame.image.load('sprites pixel/morcegos/morcego1.png')
pygame.display.set_icon(icon)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('sprites pixel/rolonai_idle/rolonai-idle1.png'))
        self.sprites.append(pygame.image.load('sprites pixel/rolonai_idle/rolonai-idle2.png'))
        self.sprites.append(pygame.image.load('sprites pixel/rolonai_idle/rolonai-idle3.png'))
        self.sprites.append(pygame.image.load('sprites pixel/rolonai_idle/rolonai-idle4.png'))
        self.sprites.append(pygame.image.load('sprites pixel/rolonai_idle/rolonai-idle5.png'))
        self.sprites.append(pygame.image.load('sprites pixel/rolonai_idle/rolonai-idle6.png'))
        self.sprites.append(pygame.image.load('sprites pixel/rolonai_idle/rolonai-idle7.png'))
        self.sprites.append(pygame.image.load('sprites pixel/rolonai_idle/rolonai-idle8.png'))
        self.sprites.append(pygame.image.load('sprites pixel/rolonai_idle/rolonai-idle9.png'))
        self.sprites.append(pygame.image.load('sprites pixel/rolonai_idle/rolonai-idle10.png'))
        self.atual = 0
        self.image = self.sprites[self.atual]
        playerx = width / 2
        playery = height / 2
        self.rect = self.image.get_rect(center = (playerx, playery))
        self.speed = 9
        self.playerLife = 100
        self.canShoot = True
        self.gameOver = False
        self.points = 0
    
    def playerInput(self):
        if pygame.key.get_pressed()[pygame.K_w] and self.canMoveUp:
            self.rect.centery -= self.speed 
        if pygame.key.get_pressed()[pygame.K_a] and self.canMoveLeft:
            self.rect.centerx -= self.speed 
        if pygame.key.get_pressed()[pygame.K_s] and self.canMoveDown:
            self.rect.centery += self.speed
        if pygame.key.get_pressed()[pygame.K_d] and self.canMoveRight:
            self.rect.centerx += self.speed 
    
    def playerCollision(self):
        if self.rect.right >=570:
            self.canMoveRight = False
        elif self.rect.right < 570:
            self.canMoveRight = True

        if self.rect.bottom >= 510:
            self.canMoveDown = False
        elif self.rect.bottom < 510:
            self.canMoveDown = True

        if self.rect.centery <= 180:
            self.canMoveUp = False
        elif self.rect.centery > 180:
            self.canMoveUp = True

        if self.rect.left <= 70:
            self.canMoveLeft = False
        elif self.rect.left > 70:
            self.canMoveLeft = True

    def update(self):
        self.atual = self.atual + 0.5
        if self.atual >= len(self.sprites):
            self.atual = 0
        self.image = self.sprites[int(self.atual)]
        self.playerInput()
        self.playerCollision()

    #retorna para a bala as coordenadas do player e do mouse
    def createBullet(self):
        return Bullet(self.rect.centerx, self.rect.centery, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

player = Player()
playerGroup = pygame.sprite.GroupSingle()
playerGroup.add(player)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, xSpeed, ySpeed):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.sprites.append(pygame.image.load('sprites pixel/morcegos/morcego1.png'))
        self.sprites.append(pygame.image.load('sprites pixel/morcegos/morcego2.png'))
        self.sprites.append(pygame.image.load('sprites pixel/morcegos/morcego3.png'))
        self.sprites.append(pygame.image.load('sprites pixel/morcegos/morcego4.png'))
        self.sprites.append(pygame.image.load('sprites pixel/morcegos/morcego5.png'))
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.rect = self.image.get_rect(center = (400, 300))
        self.xSpeed = randint(-8, 8)
        self.ySpeed = randint(-8, 8)
        self.rect_sprite = self.rect
    
    def enemyCollision(self):
        if self.rect.right >= 570:
            self.xSpeed *= -1
            self.image = pygame.transform.flip(self.image, True, False)
        if self.rect.bottom >= 510:
            self.ySpeed *= -1
        if self.rect.centery <= 180:
            self.ySpeed *= -1
        if self.rect.left <= 75:
            self.xSpeed *= -1
            self.image = pygame.transform.flip(self.image, True, False)

    def createEnemy(self):
        return Enemy(randint(-10, 10), randint(-10, 10))
    
    def attack(self):
        if self.rect.colliderect(player.rect):
            player.playerLife -= 1

    def update(self):
        self.atual = self.atual + 0.5
        if self.atual >= len(self.sprites):
            self.atual = 0
        self.image = self.sprites[int(self.atual)]
        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed
        self.attack()
        self.enemyCollision()

enemy = Enemy(randint(-10, 10), randint(-10, 10))
enemyGroup = pygame.sprite.Group()
enemyGroup.add(enemy)

class Spider(pygame.sprite.Sprite):
    def __init__(self, xSpeed, ySpeed):
        super().__init__()
        pygame.sprite.Sprite.__init__(self)
        self.sprites = []
        self.sprites.append(pygame.image.load('sprites pixel/aranha/aranha1.png'))
        self.sprites.append(pygame.image.load('sprites pixel/aranha/aranha2.png'))
        self.sprites.append(pygame.image.load('sprites pixel/aranha/aranha3.png'))
        self.sprites.append(pygame.image.load('sprites pixel/aranha/aranha4.png'))
        self.sprites.append(pygame.image.load('sprites pixel/aranha/aranha5.png'))
        self.sprites.append(pygame.image.load('sprites pixel/aranha/aranha6.png'))
        self.sprites.append(pygame.image.load('sprites pixel/aranha/aranha7.png'))
        self.sprites.append(pygame.image.load('sprites pixel/aranha/aranha8.png'))
        self.atual = 0
        self.image = self.sprites[self.atual]
        self.rect = self.image.get_rect(center = (200, 300))
        self.xSpeed = randint(-4, 4)
        self.ySpeed = randint(-4, 4)
        self.rect_sprite = self.rect

    
    def spiderCollision(self):
        if self.rect.right >= 570:
            self.xSpeed *= -1
            self.image = pygame.transform.flip(self.image, True, False)
        if self.rect.bottom >= 510:
            self.ySpeed *= -1
        if self.rect.centery <= 180:
            self.ySpeed *= -1
        if self.rect.left <= 75:
            self.xSpeed *= -1
            self.image = pygame.transform.flip(self.image, True, False)

    def createSpider(self):
        return Spider(randint(-10, 50), randint(-10, 50))
    
    def attack(self):
        if self.rect.colliderect(player.rect):
            player.playerLife -= 1

    def update(self):
        self.atual = self.atual + 0.5
        if self.atual >= len(self.sprites):
            self.atual = 0
        self.image = self.sprites[int(self.atual)]
        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed
        self.attack()
        self.spiderCollision()

spider = Spider(randint(-5, 5), randint(-5, 5))
spiderGroup = pygame.sprite.Group()
spiderGroup.add(spider)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, bulletx, bullety, targetx, targety):
        super().__init__()
        self.image = pygame.Surface((10, 10))
        self.image.fill((236, 242, 213))
        #cria a bala dentro das coordenadas do player
        self.rect = self.image.get_rect(center = (bulletx, bullety)) #corrigir
        #velocidade da bala
        self.speed = 15
        #calcula o angulo para a bala seguir em direção a mira
        angle = math.atan2(targety-bullety, targetx-bulletx)
        self.dx = math.cos(angle) * self.speed 
        self.dy = math.sin(angle) * self.speed 
        self.x = bulletx
        self.y = bullety

    def destroyBullet(self):
        if self.rect.right >=570:
            self.kill()
        if self.rect.bottom >= 510:
            self.kill()
        if self.rect.centery <= 179:
            self.kill()
        if self.rect.left <= 74:
            self.kill()

        if pygame.sprite.spritecollide(self, enemyGroup, True):
            self.kill()
            enemyGroup.remove(enemy)
            player.points += 1

        if pygame.sprite.spritecollide(self, spiderGroup, True):
            self.kill()
            spiderGroup.remove(spider)
            player.points += 1
        
    def update(self):

        self.destroyBullet()

        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

bulletGroup = pygame.sprite.Group()

class Heart(pygame.sprite.Sprite):
    def __init__(self, heartx):
        super().__init__()
        self.image = pygame.image.load('sprites pixel/coracao/coracao1.png')
        self.image = pygame.transform.scale(self.image, (64, 56))
        self.rect = self.image.get_rect(center = (heartx, 60))

    def update(self):
        if player.playerLife <= 66:
            heart3.kill()

        if player.playerLife <= 33:
            heart2.kill()

        if player.playerLife <= 0:
            heart1.kill()
            player.kill()
            player.canShoot = False
            player.gameOver = True

class Aim(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('sprites pixel/miras/mira2.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.rect = self.image.get_rect(center = (0, 0))

    def update(self):
        self.rect.centerx = pygame.mouse.get_pos()[0]
        self.rect.centery = pygame.mouse.get_pos()[1]

aim = Aim()
aimGroup = pygame.sprite.GroupSingle()
aimGroup.add(aim)

heart1 = Heart(60)
heart2 = Heart(130)
heart3 = Heart(200)
heartGroup = pygame.sprite.Group()
heartGroup.add(heart1, heart2, heart3)

while True:
    relogio.tick(30)
    screen.blit(background, (0, 0))

    playerGroup.update()
    bulletGroup.update()
    spiderGroup.update()
    enemyGroup.update()
    aimGroup.update()
    heartGroup.update()
    playerGroup.draw(screen)
    bulletGroup.draw(screen)
    spiderGroup.draw(screen)
    enemyGroup.draw(screen)
    aimGroup.draw(screen)
    heartGroup.draw(screen)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN and player.canShoot:
            bulletGroup.add(player.createBullet())
            pygame.mixer.Sound.play(bulletSoundEffect)

    if player.gameOver:
        gameOverText = myFont.render('Game Over', False, (236, 242, 213))
        gameOverText2 = myFont.render('Reabra o jogo para recomeçar', False, (236, 242, 213))
        screen.blit(gameOverText, (230, 188))
        screen.blit(gameOverText2, (80, 228))

    randomNum = randint(1,100)
    if randomNum == 2:
        enemyGroup.add(enemy.createEnemy())
    if randomNum == 4:
        spiderGroup.add(spider.createSpider())

    pointsText = myFont.render(f'Pontos: {player.points}', False, (236, 242, 213))
    screen.blit(pointsText, (425, 40))
    pygame.display.update()
