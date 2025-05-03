#Создай собственный Шутер!

from pygame import *
from random import randint
window = display.set_mode((1200, 700))
display.set_caption("SHYTER")
background = transform.scale(image.load("galaxy.jpg"),(1200, 700))
keys_pressed = key.get_pressed()

point = 0
lost = 0

bullets = sprite.Group()

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, width, height, player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < -10:
            self.kill()



class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 1155:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet("bullet.png", self.rect.centerx - 7, self.rect.top - 20, 15, 25, 15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 700:
            self.rect.y = -10
            self.rect.x = randint(0, 1155)
            self.speed = randint(1, 3)
            lost = lost + 1
            print(lost)

class Wall(sprite.Sprite):
    def __init__(self, color_1, color_2, color_3, wall_x, wall_y, wall_width, wall_height):
        super().__init__()
        self.color_1 = color_1
        self.color_2 = color_2
        self.color_3 = color_3
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((self.width, self.height))
        self.image.fill((color_1, color_2, color_3))
        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



x1 = randint(0, 1155)
x2 = randint(0, 1155)
x3 = randint(0, 1155)
x4 = randint(0, 1155)
x5 = randint(0, 1155)

speed1 = randint(1, 3)
speed2 = randint(1, 3)
speed3 = randint(1, 3)
speed4 = randint(1, 3)
speed5 = randint(1, 3)

hero = Player("rocket.png", 583, 620, 45, 50, 10)
enemy1 = Enemy("ufo.png", x1, -30, 60, 35, speed1)
enemy2 = Enemy("ufo.png", x2, -30, 60, 35, speed2)
enemy3 = Enemy("ufo.png", x3, -30, 60, 35, speed3)
enemy4 = Enemy("ufo.png", x4, -30, 60, 35, speed4)
enemy5 = Enemy("ufo.png", x5, -30, 60, 35, speed5)

enemies = sprite.Group()
enemies.add(enemy1)
enemies.add(enemy2)
enemies.add(enemy3)
enemies.add(enemy4)
enemies.add(enemy5)

font.init()
fontM = font.SysFont('Arial', 70)
fontS = font.SysFont('Arial', 50)
fontXS = font.SysFont('Arial', 20)
final = fontM.render("You win!", True, (255, 215, 0))
lose = fontM.render("U LOSE(", True, (175, 0, 0))
invinsiblityL = fontXS.render("", True, (0, 250, 0))


mixer.init()
mtlpp = mixer.Sound("METALPIPE.ogg")
space = mixer.Sound("space.ogg")
shot = mixer.Sound("fire.ogg")

space.play()



clock = time.Clock()
FPS = 60

invinsiblity = False

finish = False
game = True
while game:

    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                hero.fire()
                shot.play()
            elif e.key == K_i and invinsiblity == False:
                invinsiblity = True
                print("invinsiblity enabled")
                invinsiblityL = fontXS.render("Invinsiblity Enabled", True, (0, 250, 0))
            elif e.key == K_i and invinsiblity == True:
                invinsiblity = False
                print("invinsiblity disabled")
                invinsiblityL = fontXS.render("", True, (0, 250, 0))

    if finish != True:    
        keys_pressed = key.get_pressed()
        points = fontS.render("Счёт: "+str(point), True, (250, 250, 250))
        llost = fontS.render("Пропущено: "+str(lost), True, (250, 250, 250))
        window.blit(background,(0, 0))
        window.blit(points, (20, 40))
        window.blit(llost, (20, 90))
        window.blit(invinsiblityL, (1050, 20))
        hero.reset()
        bullets.update()
        bullets.draw(window)
        enemies.update()
        enemies.draw(window)
        hero.update()
        sprites_list = sprite.groupcollide(enemies, bullets, True, True)
        for c in sprites_list:
            point = point + 1
            enemy = Enemy("ufo.png", randint(0, 1155), -30, 60, 35, randint(1, 3))
            enemies.add(enemy)
        clock.tick(FPS)

        if point >= 100:
            finish = True
            points = fontS.render("Счёт: "+str(point), True, (0, 235, 0))
            window.blit(background,(0, 0))
            window.blit(llost, (20, 90))
            window.blit(points, (20, 40))
            hero.reset()
            enemies.draw(window)
            bullets.draw(window)
            window.blit(final, (500,300))

        if sprite.spritecollide(hero, enemies, False) and invinsiblity == False or lost >= 3 and invinsiblity == False:    
            mtlpp.play()
            llost = fontS.render("Пропущено: "+str(lost), True, (200, 0, 0))
            window.blit(background,(0, 0))
            window.blit(llost, (20, 90))
            window.blit(points, (20, 40))
            hero.reset()
            enemies.draw(window)
            bullets.draw(window)
            window.blit(lose, (500,300))
            finish = True
            print("U LOSE(")

    display.update()

#недоделанный код для уничтожения врага при столкновении с бессмертием
'''
        if invisiblity == False:
            if sprite.spritecollide(hero, enemies, False) or lost >= 3:                
                mtlpp.play()
                llost = fontS.render("Пропущено: "+str(lost), True, (200, 0, 0))
                window.blit(background,(0, 0))
                window.blit(llost, (20, 90))
                window.blit(points, (20, 40))
                hero.reset()
                enemies.draw(window)
                bullets.draw(window)
                window.blit(lose, (500,300))
                finish = True
                print("U LOSE(")
        elif invisiblity == True:
            if sprite.spritecollide(hero, enemies, False, True) or lost >= 3:
'''