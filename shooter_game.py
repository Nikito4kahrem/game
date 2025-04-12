 #Создай собственный Шутер!
from random import *
from typing import Any
from pygame import *

Black = 0, 0, 40
win_heidth = 500
win_wight = 700
popusk = 0
moni = 0

win = display.set_mode((700, 500))
background = transform.scale(image.load('galaxy.jpg'),(700, 500))
display.set_caption('шутер ☺')

mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()


font.init()
font1 = font.SysFont(None, 36)
winner = font1.render('YOU WIN!', True, (0, 255, 0))
loser = font1.render('YOU LOSER!', True, (180, 0, 0))
font2 = font.SysFont(None, 36)

clock = time.Clock()
FPS = 60


class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, says_x, says_y, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (says_x, says_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        win.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys [K_UP] and self.rect.y >5:
            self.rect.y -= self.speed
        if keys [K_DOWN] and self.rect.y < win_heidth - 80:
            self.rect.y += self.speed
        if keys [K_LEFT] and self.rect.x >5:
            self.rect.x -= self.speed
        if keys [K_RIGHT] and self.rect.x < win_wight - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        global popusk

        self.rect.y += self.speed

        if self.rect.y > win_heidth:
            self.rect.x = randint(80, win_wight - 80)
            self.rect.y = 0
            popusk = popusk + 1
            mixer.music.load('zapikivanie-mata-05-sekundyi-37288.ogg')
            mixer.music.play()

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

        
            

player = Player('rocket.png', 50, 400, 65, 100, 10)

ufos = sprite.Group()
for i in range(1, 6):
    ufo = Enemy('ufo.png', randint(80, win_wight- 80), -40, 90, 65, randint(1, 3))
    ufos.add(ufo)

bullets = sprite.Group()


finish = False
game = True 
while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
    
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                mixer.music.load('fire.ogg')
                mixer.music.play()
                player.fire()
    
    
    if finish != True:
        win.blit(background,(0, 0))

        player.reset()
        player.update()
        ufos.draw(win)
        ufos.update()
        bullets.draw(win)
        bullets.update()  

    if moni >= 10:
        for i in range(1, 4):
            ufo = Enemy('asteroid.png', randint(80, win_wight- 80), -40, 90, 65, randint(1, 100))
            ufos.add(ufo)
        
        #win.blit(winner, (250, 250))  
        #finish = True

    
    
    if sprite.spritecollide(player, ufos, False) or popusk >= 1000000:
        win.blit(loser, (250, 250))         
        finish = True    
            
    
    sprite_list = sprite.groupcollide(ufos, bullets, True, True)

    for i in sprite_list:
        ufo = Enemy('ufo.png', randint(80, win_wight- 80), -40, 90, 65, randint(1, 5))
        ufos.add(ufo)
        moni = moni + 1

    

    text_lose = font1.render('Пропущено: ' + str(popusk),1, (255, 255, 255))
    win.blit(text_lose, (10, 50))
    text_moni = font2.render('Счёт: ' + str(moni), 1, (255, 255, 255))
    win.blit(text_moni, (10, 20))
    display.update()
    clock.tick(FPS)
