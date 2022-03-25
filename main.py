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
background = pygame.image.load('background_img.png').convert_alpha(screen)
relogio = pygame.time.Clock()
pygame.mouse.set_visible(False)
music = pygame.mixer.music.load('rolonaijogoswav (1).wav')
pygame.mixer.music.set_volume(0.01)
pygame.mixer.music.play(-1)

myFont = pygame.font.SysFont('Consolas', 30)

bulletSoundEffect = pygame.mixer.Sound('tirogomes.wav')


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('rolonai_idle/rolonai-idle1.png'))
        self.sprites.append(pygame.image.load('rolonai_idle/rolonai-idle2.png'))
        self.sprites.append(pygame.image.load('rolonai_idle/rolonai-idle3.png'))
        self.sprites.append(pygame.image.load('rolonai_idle/rolonai-idle4.png'))
        self.sprites.append(pygame.image.load('rolonai_idle/rolonai-idle5.png'))
        self.sprites.append(pygame.image.load('rolonai_idle/rolonai-idle6.png'))
        self.sprites.append(pygame.image.load('rolonai_idle/rolonai-idle7.png'))
        self.sprites.append(pygame.image.load('rolonai_idle/rolonai-idle8.png'))
        self.sprites.append(pygame.image.load('rolonai_idle/rolonai-idle9.png'))
        self.sprites.append(pygame.image.load('rolonai_idle/rolonai-idle10.png'))

        self.walkingSprites = []
        self.walkingSprites.append(pygame.image.load('rolonai_pisadinha/rolonaipisadinha1.png'))
        self.walkingSprites.append(pygame.image.load('rolonai_pisadinha/rolonaipisadinha2.png'))
        self.walkingSprites.append(pygame.image.load('rolonai_pisadinha/rolonaipisadinha3.png'))
        self.walkingSprites.append(pygame.image.load('rolonai_pisadinha/rolonaipisadinha4.png'))
        self.walkingSprites.append(pygame.image.load('rolonai_pisadinha/rolonaipisadinha5.png'))
        self.walkingSprites.append(pygame.image.load('rolonai_pisadinha/rolonaipisadinha6.png'))
        self.walkingSprites.append(pygame.image.load('rolonai_pisadinha/rolonaipisadinha7.png'))
        self.walkingSprites.append(pygame.image.load('rolonai_pisadinha/rolonaipisadinha8.png'))
        self.walkingSprites.append(pygame.image.load('rolonai_pisadinha/rolonaipisadinha9.png'))
        self.walkingSprites.append(pygame.image.load('rolonai_pisadinha/rolonaipisadinha10.png'))

        self.currentSprite = 0

        self.image = self.sprites[self.currentSprite]
        #coordenadas em que o player é criado
        playerx = width / 2
        playery = height / 2
        self.rect = self.image.get_rect(center = (playerx, playery))
        #velocidade do player
        self.speed = 12
        #vida do player
        self.playerLife = 100
        self.canShoot = True

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

    def idleAnimate(self):
        self.sprites
        

    def update(self):
        self.playerInput()
        self.playerCollision()

    #retorna para a bala as coordenadas do player e do mouse
    def createBullet(self):
        return Bullet(self.rect.centerx, self.rect.centery, pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1])

#Cria uma instância do player
player = Player()
playerGroup = pygame.sprite.GroupSingle()
playerGroup.add(player)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, xSpeed, ySpeed):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('morcegalhas/morcego1.png'))
        self.sprites.append(pygame.image.load('morcegalhas/morcego2.png'))
        self.sprites.append(pygame.image.load('morcegalhas/morcego3.png'))
        self.sprites.append(pygame.image.load('morcegalhas/morcego4.png'))
        self.sprites.append(pygame.image.load('morcegalhas/morcego5.png'))

        self.spritesDeath = []
        self.spritesDeath.append(pygame.image.load('morcegalhas/morcegomorte1.png'))
        self.spritesDeath.append(pygame.image.load('morcegalhas/morcegomorte2.png'))
        self.spritesDeath.append(pygame.image.load('morcegalhas/morcegomorte3.png'))
        self.currentSprite = 0
        self.image = self.sprites[self.currentSprite]
        self.rect = self.image.get_rect(center = (400, 300))
        self.xSpeed = randint(-10, 10)
        self.ySpeed = randint(-10, 10)
        self.rect_sprite = self.rect

    def flyingAnimate(self):
        self.image = self.sprites[int(self.currentSprite)]
        self.currentSprite += 0.5
        if self.currentSprite <= len(self.sprites):
            self.currentSprite = 0
            pass

    
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
        self.rect.x += self.xSpeed
        self.rect.y += self.ySpeed
        self.flyingAnimate()
        self.attack()
        self.enemyCollision()

enemy = Enemy(randint(-10, 10), randint(-10, 10))
enemyGroup = pygame.sprite.Group()
enemyGroup.add(enemy)

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
        
    def update(self):

        self.destroyBullet()

        self.x = self.x + self.dx
        self.y = self.y + self.dy
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)

#cria um grupo para manter todas as instâncias criadas das balas
bulletGroup = pygame.sprite.Group()

class Heart(pygame.sprite.Sprite):
    def __init__(self, heartx):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.image.load('coraçao/coracao1.png'))
        self.sprites.append(pygame.image.load('coraçao/coracao2.png'))
        self.sprites.append(pygame.image.load('coraçao/coracao3.png'))
        self.sprites.append(pygame.image.load('coraçao/coracao4.png'))
        self.sprites.append(pygame.image.load('coraçao/coracao5.png'))
        self.currentSprite = 0
        self.image = self.sprites[self.currentSprite]
        self.image = pygame.transform.scale(self.image, (64, 56))
        self.rect = self.image.get_rect(center = (heartx, 60))

    def update(self):

        self.image = self.sprites[int(self.currentSprite)]
        self.image = pygame.transform.scale(self.image, (64, 56))
        
        if player.playerLife <= 66:
            self.currentSprite += 0.2
            if self.currentSprite >= len(self.sprites):
                self.currentSprite == 0
                self.kill()
                pass

        if player.playerLife <= 33:
            heart2.currentSprite += 0.2
            if heart2.currentSprite >= len(heart2.sprites):
                heart2.currentSprite == 0
                heart2.kill()
                pass

        if player.playerLife == 0:
            heart1.currentSprite += 0.2
            if heart1.currentSprite >= len(heart1.sprites):
                heart1.currentSprite == 0
                heart1.kill()
                pass
            player.kill()
            player.canShoot = False
        

class Aim(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('miras/mira2.png').convert_alpha()
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

    #desenha a atualiza os itens na tela
    playerGroup.update()
    bulletGroup.update()
    aimGroup.update()
    enemyGroup.update()
    heartGroup.update()
    playerGroup.draw(screen)
    bulletGroup.draw(screen)
    aimGroup.draw(screen)
    enemyGroup.draw(screen)
    heartGroup.draw(screen)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        if event.type == MOUSEBUTTONDOWN and player.canShoot:
            bulletGroup.add(player.createBullet())
            pygame.mixer.Sound.play(bulletSoundEffect)

    randomNum = randint(1,75)
    if randomNum == 2:
        enemyGroup.add(enemy.createEnemy())

    pointsText = myFont.render(f'Pontos: {player.points}', False, (236, 242, 213))
    screen.blit(pointsText, (425, 40))
        
    pygame.display.update()