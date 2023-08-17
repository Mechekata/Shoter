import pygame
from time import time
from random import randint

pygame.init()

#висота та ширина
w_win = 700
h_win = 500

#кольори
blue = (125, 249, 255)
green = (62, 218, 148)
red = (255, 0, 0)
bleck = (0, 0, 0)
white = (255, 255, 255)
yellow = (255, 228, 107)

#створи вікно гри
window = pygame.display.set_mode((w_win, h_win))

FPS = 55
clock = pygame.time.Clock()

# супер клас
class GameSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__()
        self.rect = pygame.Rect(x, y, w, h)
        image = pygame.transform.scale(image, (w, h))
        self.image = image
        self.speed = speed
    def update(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

hp_img = pygame.image.load('hp.png')

class Player(GameSprite):
    def __init__(self, x, y, w, h, image, speed, hp):
        super().__init__(x, y, w, h, image, speed)
        self.hp = hp
        harts = []
        x = 650
        for i in range (self.hp):
            h = GameSprite(x, 0, 20, 20, hp_img, 0)
            harts.append(h)
            x -= 25
        self.harts = harts

    def move(self):
        move_ = pygame.key.get_pressed()   
        if move_[pygame.K_d]:
            if self.rect.x <= 660:
                self.rect.x += self.speed   
        if move_[pygame.K_a]:
            if self.rect.x >= 0:
                self.rect.x -= self.speed

    def shoot(self):
        # # s = pygame.key.get_pressed()
        # if s[pygame.K_SPACE]:
            bullet = Bullet(self.rect.centerx - 7, self.rect.y, 5, 10, bullet_img, 5)
            bullet = Bullet(self.rect.centerx + 2, self.rect.y, 5, 10, bullet_img, 5)
            bullet_music.play()


# enemies = []
enemies_group = pygame.sprite.Group()

class Enemy(GameSprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image, speed)
        # enemies.append(self)
        enemies_group.add(self)

    def update(self):
        global miss
        self.rect.y += self.speed
        if self.rect.y >= 500:
            enemies_group.remove(self)
            miss += 1

bullets_group = pygame.sprite.Group()

class Bullet(GameSprite):
    def __init__(self, x, y, w, h, image, speed):
        super().__init__(x, y, w, h, image, speed)
        bullets_group.add(self)

# метод группи ищет update
    def update(self):
        self.rect.y -= self.speed
        if self.rect.bottom <= 0:
            bullets_group.remove(self)

player_img = pygame.image.load('rocket2-.png')
player = Player(350, 400, 40, 90, player_img, 4, 3)
enemy_img = pygame.image.load('ufo3-.png')
bullet_img = pygame.image.load('bullet.png')
galaxy = pygame.image.load('galaxy.jpg')

font1 = pygame.font.SysFont(None, 50)
font2 = pygame.font.SysFont(None, 25)

YOU_LOSE = font1.render("Ти програв(", True, (bleck))
YOU_WIN = font1.render("Ти виграв)", True, (bleck))
new_game_lb = font2.render("Щоб розпочати нову гру натисніть <пробіл>", True, (bleck))

bullet_music = pygame.mixer.Sound("lazer_sound2.mp3")

#безкінечний цикл
game = True
finish = False
miss = 0
score = 0
max_score = 0

en_min_speed = 1
en_max_speed = 3

enemy_wait = 50

try:
    with open('hit.txt', 'r') as file:
        max_score = int(file.read())
except FileNotFoundError:
    file = open('hit.txt', 'x')
    file.close()
except ValueError:
    pass

print(max_score)

while game:                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                              
    if not finish:

        miss_lb = font1.render('Прорущено: '+str(miss), True, (250, 250, 250))
        score_lb = font1.render(f'Рахунок: '+str(score), True, (250, 250, 250))

        if enemy_wait == 0:
            enemy = Enemy(randint(0, 650), 10, 50, 50, enemy_img, randint(en_min_speed, en_max_speed))
            enemy_wait = randint(70, 150)
        else:
            enemy_wait -= 1

        window.blit(galaxy, (0, 0))
        window.blit(miss_lb, (10, 10))
        window.blit(score_lb, (10, 50))
        for h in player.harts:
            h.update()
        player.update()
        player.move()
        # player.shoot()

        # for enemy in enemies[:]:
        #     enemy.update()
        #     enemy.move()

        enemies_group.draw(window)
        enemies_group.update()

        bullets_group.draw(window)
        bullets_group.update()
        # bullets_group.sprites()
        # print(bullets_group.sprites())

        if pygame.sprite.spritecollide(player, enemies_group, False):
            hp =- 1
        if player.hp <= 0 or miss >= 3:
            if score > max_score:
                max_score = score
                with open('hit.txt', 'w') as file:
                    file.write(str(max_score))
            finish = True

        # if miss >= 3:
        #     window.fill(red)
        #     window.blit(YOU_LOSE, (165, 250))
        #     window.blit(new_game_lb, (180, 300))
        #     finihs = True
        
        if pygame.sprite.groupcollide(enemies_group, bullets_group, True, True):
            score += 1
            if score % 25 == 0:
                en_min_speed * 1.3
                en_max_speed * 1.3
            print(score)

        #оброби подію «клік за кнопкою "Закрити вікно"»
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.shoot()
        pygame.display.update()
        clock.tick(FPS)