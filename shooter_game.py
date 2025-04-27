#Создай собственный Шутер!
from pygame import *
import pygame
import random
import time as tm

window = display.set_mode((700, 500))
display.set_caption("cosmic_shooter")
clock = time.Clock()
FPS = 60

class GameSprite(pygame.sprite.Sprite):
    def __init__(self, image, size, pos, speed):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(image), (size[0], size[1]))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
    def update(self, window):
        window.blit(self.image, self.rect)

    def move_up(self):
        self.rect.y -= self.speed

    def move_down(self):
        self.rect.y += self.speed

    def move_left(self):
        self.rect.x -= self.speed

    def move_right(self):
        self.rect.x += self.speed

    def check_collision(self, other_sprite):
        return self.rect.colliderect

class Player(GameSprite):
    def update(self, window):
        window.blit(self.image, self.rect)
        keys_pressed = key.get_pressed()
        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.move_left()
        if keys_pressed[K_RIGHT] and self.rect.x + self.image.get_size()[0] < 695:
            self.move_right()
        if keys_pressed[K_UP] and self.rect.y > 695:
            self.move_up()
        if keys_pressed[K_DOWN] and self.rect.y < 395:
            self.move_down()

lost = 0
shot = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > 495:
            self.rect.y = -45
            x = random.sample([80, 160, 240, 320, 400, 480, 560, 640], 1)
            self.rect.x = x[0]
            global lost
            lost += 1

class Bullet(GameSprite):
    def update(self, window):
        window.blit(self.image, self.rect)
        if self.rect.y > 0:
            self.move_up()
        else:
            bullets.remove(self)

player = Player("cosmic_rocket.png", (65, 65), (300, 420), 3)

invaders = sprite.Group()
x = random.sample([80, 160, 240, 320, 400, 480, 560, 640], 5)
for i in range(5):
    invader = Enemy("IKP_1000.PNG", (65, 65), (x[i], 50), 1)
    invaders.add(invader)

bullets = sprite.Group()

init()
mixer.init()
mixer.music.load("CP Violation.mp3")
mixer.music.play()

win_width = 700
win_heigt = 500
window = display.set_mode((win_width, win_heigt))
display.set_caption("cosmic_shooter")
Galaxy = pygame.transform.scale(pygame.image.load("Cosmic_fight.jpg"), (win_width, win_heigt))

font.init()
font = font.SysFont('Arial', 70)
text_score = font.render('Cчет:' + str(shot), 1, (255, 251, 255))
window.blit(text_score, (10, 10))

text_skip = font.render('Пропущено:' + str(lost), 1, (255, 251, 255))
window.blit(text_skip, (10, 60))

is_game = True
finish = False
last_shot = time.get_ticks()

while is_game:
    for e in pygame.event.get():
        if e.type == QUIT:
            is_game = False

    if finish != True:
        keys_pressed = key.get_pressed()
        if keys_pressed[K_SPACE]:
            if time.get_ticks() - last_shot > 250:
                bullet = Bullet("laser.PNG", (10, 10), (player.rect.x + 30, player.rect.y), 4)
                bullets.add(bullet)
                sound = mixer.Sound('laser_shot.mp3')
                sound.play()
                last_shot = time.get_ticks()
        kill = sprite.groupcollide(invaders, bullets, True, True )
        if kill:
            for k, v in kill.items():
                #if invaders != bullets:
                invaders.remove(k)
                #blast = Enemy('blast.gif', (65, 65), (x[0] , 50), 1) 
                #blast = Enemy('blast.gif', (65, 65), (x[0] , 50), 1)
                x = random.sample([80, 160, 240, 320, 400, 480, 560, 640], 1)
                invader = Enemy("IKP_1000.PNG", (65, 65), (x[0] , 50), 1)
                invaders.add(invader)
                shot += 1
                if shot >= 50:
                    finish = True
                    text_res = font.render('Победа на вашей стороне!', 1, (0, 255, 0))
                    window.blit(text_res, (20, 200))
                    display.update()
                    tm.sleep(2)

        kill = sprite.spritecollide(player, invaders, False)
        if kill or lost >= 15:
            finish = True
            text_res = font.render('Повезёт в следующий раз!', 1, (255, 0, 0))
            window.blit(text_res, (20, 200))
            display.update()
            tm.sleep(2)

        window.blit(Galaxy, (0, 0))
        clock.tick(FPS)
        player.update(window)
        invaders.draw(window)
        invaders.update()
        bullets.draw(window)
        bullets.update(window)
        text_score = font.render('Cчет:' + str(shot), 1, (255, 251, 255))
        window.blit(text_score, (10, 10))
        text_skip = font.render('Пропущено:' + str(lost), 1, (255, 251, 255))
        window.blit(text_skip, (10, 60))
        display.update()