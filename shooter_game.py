from pygame import *
from random import randint
import os
from time import time as timer
font.init()
mixer.init()

lost = 0
score = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, player_width,player_height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (player_width, player_height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 1840:
            self.rect.x += self.speed
    
    def fire(self):
        bullets.add(Bullet("bullet.png", self.rect.centerx,self.rect.top, -15, 15, 20 ))
        
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost 
        if self.rect.y > 1080:
            self.rect.x = randint(80,1840)
            self.rect.y = -80
            lost += 1
    
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y == 0:
            self.kill()

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d, %d" % (0, 0)
window = display.set_mode((1920, 1080),0,0)
display.set_caption("Стрелялка")
background = transform.scale(image.load("0e2ff94f2d4ca58175e3ef06aa9188b6.jpg"),(1920, 1080))
font = font.SysFont("Arial", 60)
mixer.music.load("space.ogg")
mixer.music.play()
fire = mixer.Sound("fire.ogg")
clock = time.Clock()
run = True
finish = False
player = Player("graphic-assault-type-cs-unit.png", 890, 940, 15, 120, 140)
enemyes = sprite.Group()
bullets = sprite.Group()
lets = sprite.Group()
for i in range(3):
    lets.add(Enemy("klipartz.com.png", randint(80,1840), -40, randint(1,3), 120,140))
for i in range(5):
    enemyes.add(Enemy("ufo.png", randint(80,1840), -40, randint(3,5), 120, 150))
win = font.render("Победа!!!", True, (255, 255, 255))
lose = font.render("Поражение....", True, (255, 255, 255))

num_fire = 0
rel_time = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    fire.play()
                    player.fire()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True

        


    if finish != True:
        window.blit(background, (0,0))
        kill = font.render("Убиты: "+ str(score), True, (255, 255, 255))
        miss = font.render("Пропущены: "+ str(lost), True, (255, 255, 255))  
        window.blit(kill, (10, 20))
        window.blit(miss, (10, 50))
        collides = sprite.groupcollide(enemyes, bullets, True, True)
        for collide in collides:
            score +=1
            enemyes.add(Enemy("ufo.png", randint(80,1840), -40, randint(3,5), 80, 80))
        if sprite.spritecollide(player, enemyes, False) or lost > 5 or sprite.spritecollide(player, lets, False):
            finish = True
            window.blit(lose, (900, 540))
        if score == 25:
            finish = True
            window.blit( win, (900, 540))
        sprite.groupcollide(lets, bullets, False, True)
        lets.update()
        lets.draw(window)
        player.update()
        player.reset()
        enemyes.update()
        enemyes.draw(window)
        bullets.update()
        bullets.draw(window)
        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                reload_text = font.render("Перезарядка!!!", True, (255 ,255, 255))
                window.blit(reload_text, (900, 900))
            else:
                num_fire = 0 
                rel_time = False
        display.update()
        clock.tick(75)