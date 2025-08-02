#Create your own shooter

from pygame import *
from random import randint
from time import sleep
window = display.set_mode((700,500))
background = transform.scale(image.load("galaxy.jpg"), (700,500))

FPS = time.Clock()

mixer.init()
mixer.music.load("space.ogg")
mixer.music.play()

class Gamesprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(width,height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))
    
    def returntoposition(self):
        self.rect.x = 50
        self.rect.y = 50
        window.blit(self.image,(self.rect.x, self.rect.y))

class Player(Gamesprite):
    def update(self):
        global point
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        
        if keys_pressed[K_RIGHT] and self.rect.x < 700:
            self.rect.x += self.speed

    def Fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 8, 8, 8)
        bullet_group.add(bullet)
        mixer.init()
        mixer.music.load("fire.ogg")
        mixer.music.play()
    

class Enemy(Gamesprite):
    def update(self):
        global missed
        if self.rect.y < 525:
            self.rect.y += self.speed
            
        else:
            self.rect.y = 0
            self.rect.x = randint(100,650)
            self.speed = randint(1,5)
            missed += 1

    def autofire(self):
        bulletenemy = EnemyBullet("bullet.png", self.rect.centerx, self.rect.top, 8, 8, 8)
        Enemybullet_group.add(bulletenemy)

        
class Bullet(Gamesprite):
    def update(self):  
        if self.rect.y < 525:
            self.rect.y -= self.speed
        else:
            self.kill()

class EnemyBullet(Gamesprite):
    def update(self):  
        if self.rect.y < 525:
            self.rect.y += self.speed
        else:
            self.kill()

# class BossBullet_Big(Gamesprite):
#     def update(self):
#         if self.rect.y < 525:
#             self.rect.y += self.speed
#         else:
#             self.kill()

# class Boss(Gamesprite):
#     def __init__(self, player_image, player_x, player_y, player_speed, width, height, health):
#         super().__init__(player_image, player_x, player_y, player_speed, width, height)
#         self.health = health
    
#     def update(self):
#         if self.rect.y < 525:
#             self.rect.y += self.speed
        
    
#     def fire_rand_bullet(self):
#         x = self.rect.centerx
#         for i in range(randint(1,6)):
#             bulletboss_small = EnemyBullet("bullet.png", x, self.rect.top, 8, 8, 8)
#             x += 2
#         bulletboss_small_group.add(bulletboss_small)
    
#     def fire_big_bullet(self):
#         bulletboss_big = BossBullet_Big("bullet.png", self.rect.centerx, self.rect.top, 12, 50, 50)

#     def fire(self):
#         random_number = randint(1,2)
#         if random_number == 1:
#             fire_rand_bullet()
#         if random_number == 2:
#             fire_big_bullet
            

#     def teleport(self):
#         if self.health % 10 == 0:
#             self.rect.x = randint(150,650)
    


rocket = Player("rocket.png", 10, 440, 9, 50, 50)
ufo1 = Enemy("ufo.png", randint(150,650),0, randint(1,4), 40, 40)
ufo2 = Enemy("ufo.png", randint(150,650),0, randint(1,4), 40, 40)
ufo3 = Enemy("ufo.png", randint(150,650),0, randint(1,4), 40, 40)
ufo4 = Enemy("ufo.png", randint(150,650),0, randint(1,4), 40, 40)
ufo5 = Enemy("ufo.png", randint(150,650),0, randint(1,4), 40, 40)

# Boss_ufo = Enemy("ufo.png", 275, 0, 1, 80, 80, 40)

ufo_group = sprite.Group()
ufo_group.add(ufo1)
ufo_group.add(ufo2)
ufo_group.add(ufo3)
ufo_group.add(ufo4)
ufo_group.add(ufo5)

bullet_group = sprite.Group()

Enemybullet_group = sprite.Group()

#     


font.init()
text = font.Font(None, 36)

game = True

point = 0
missed = 0


last_Update_Time = time.get_ticks()
last_Update_Time2 = time.get_ticks()
bullet_fire = 0

while game:
    CurrentTime = time.get_ticks()
    #enemy autofire
    if CurrentTime - last_Update_Time > 1500:
        last_Update_Time = time.get_ticks()

        randomfire = randint(1,5)
        randomfire_counter = 0

        for i in ufo_group:
            if randomfire_counter < randomfire:
                i.autofire()
                randomfire_counter += 1
            else:
                break

    text_win = text.render(
        "Point: " + str(point), 1, (255,255,255)
    )

    text_lose = text.render(
        "Missed: " + str(missed), 1, (255,255,255)
    )

    you_lose = text.render(
        "Defeat", 1, (245, 10, 10)
    )

    you_win = text.render(
        "Victory", 1, (10, 245, 50)
    )

    text_reload = text.render(
        "Wait. Reloading", 1, (245, 10, 10)
    )

    window.blit(background, (0,0))
    window.blit(text_win, (20,20))
    window.blit(text_lose, (20,50))


    rocket.reset()
    rocket.update()

    ufo_group.update()
    ufo_group.draw(window)

    bullet_group.update()
    bullet_group.draw(window)

    Enemybullet_group.update()
    Enemybullet_group.draw(window)

    sprites_list = sprite.groupcollide(
        ufo_group, bullet_group, True, True
    )

    sprites_list2 = sprite.spritecollide(
        rocket, ufo_group, False
    )

    sprites_list3 = sprite.spritecollide(
        rocket, Enemybullet_group, False
    )

    # sprites_listboss = sprite.spritecollide(
    #     bulletgroup, Boss_ufo, False
    # )

    for i in range(len(sprites_list)):
        point += 1
        ufo = Enemy("ufo.png", randint(150,650),0, randint(1,5), 40, 40)
        ufo_group.add(ufo)
    

    CurrentTime2 = time.get_ticks()

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                if bullet_fire <= 5:
                    rocket.Fire()
                    bullet_fire += 1
    if bullet_fire > 5:
        window.blit(text_reload, (300,480))
        display.update()
        if CurrentTime2 - last_Update_Time2 > 3000:
            last_Update_Time2 = time.get_ticks()
            bullet_fire = 0    




    if sprites_list2:
        window.blit(you_lose, (300,200))
        display.update()
        mixer.music.stop()
        sleep(6)
        game = False
    
    if sprites_list3:
        window.blit(you_lose, (300,200))
        display.update()
        mixer.music.stop()
        sleep(6)
        game = False

    if missed >= 3:
        window.blit(you_lose, (300,200))
        display.update()
        mixer.music.stop()
        sleep(6)
        game = False

    # if point >= 10:
    #     for i in ufo_group:
    #         i.kill()
    #     Boss_ufo.update()
    #     Boss_ufo.draw(window)
    #     if sprites_listboss:
    #         Boss_ufo.health -= 1
    #         if Boss_ufo.health == 0:
    #             window.blit(you_win, (300,200))
    #             display.update()
    #             mixer.music.stop()
    #             sleep(6)
    #             game = False
    
    #if Boss_ufo.rect.y > 525:
        # window.blit(you_lose, (300,200))
        # display.update()
        # mixer.music.stop()
        # sleep(6)
        # game = False


    
    display.update()
    FPS.tick(30)