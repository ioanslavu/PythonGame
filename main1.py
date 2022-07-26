import pygame
import os
import time
import random
from pygame import mixer
pygame.font.init()
#prepare font

# SETEAZA DIMENSIUNEA ECRANULUI
WIDTH, HEIGHT = 750, 750
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# SET THE NAME OF WINDOW
pygame.display.set_caption("Space invaders")

#import sound 
pygame.mixer.init()
pygame.mixer.music.load('background.wav')
pygame.mixer.music.play(-1)

# load images

RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
HEALTH_PACK = pygame.image.load(os.path.join("assets", "health_pack.png"))

#PLAYER
YELLOW_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))

# LASERS
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))

#PLAYER LASER
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))

#Background

BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))
MEN = pygame.transform.scale(pygame.image.load(os.path.join("assets", "meniu.png")), (WIDTH, HEIGHT))
#prima functie face conversia imaginii la 750 750
#a doua functie salvea bg

class Laser:
    def __init__(self, x, y, img):
        self.x = x
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)
    def draw(self, window):
        window.blit(self.img, (self.x, self.y))
    def move(self, vel):
        self.y += vel
    def off_screem(self, height):
        return not (self.y <= height and self.y >=0)
    def collision(self, obj):
        return collide(self, obj)

class HealthPack():
    def __init__(self, x, y):
          self.x = x
          self.y = y
          self.health_image = HEALTH_PACK
          self.mask = pygame.mask.from_surface(self.health_image)
    def collision(self, obj):
        return collide(self, obj)
    def draw(self, window):
        window.blit(self.health_image, (self.x, self.y))
    def get_width(self):
        return self.health_image.get_width()
    def get_height(self):
        return self.health_image.get_height()
    def move(self, vel):
        self.y += vel

class Ship:
    COOLDOWN = 50
    def __init__(self, x, y, health = 100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img = None
        self.laser_img = None
        self.lasers = []
        self.cool_down_counter = 0
    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screem(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def cooldown(self):
        if self.cool_down_counter >= self.COOLDOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def get_width(self):
        return self.ship_img.get_width()
    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):
    def __init__(self, x, y, health = 100):
        super().__init__(x, y, health)
        #super face referinta la player si foloseste metodata de initializare din __init__
        #in init se tin minte extensile. un fel de struct de la c/cpp
        self.ship_img = YELLOW_SPACE_SHIP
        self.laser_img = YELLOW_LASER
        #mask e pentru colision
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health
    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(-vel)
            if laser.off_screem(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)

class Enemy(Ship):
    COLOR_MAP = {
                "red": (RED_SPACE_SHIP, RED_LASER),
                "green": (GREEN_SPACE_SHIP, GREEN_LASER),
                "blue": (BLUE_SPACE_SHIP, BLUE_LASER)
                }
    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)
    
    def move(self, vel):
        self.y += vel


def collide(obj1, obj2):
    offset_x = obj2.x - obj1.x
    offset_y = obj2.y - obj1.y
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None

def meniu():
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    from sys import exit
    while run:
        pygame.display.update()
        clock.tick(FPS)
        WIN.blit(MEN, (0,0))
        text_font = pygame.font.SysFont("comicsans", 60)
        text1_label = text_font.render("Space invaders, proiect Stanciu Vlad", 1, (255, 0, 0))
        text2_label = text_font.render("Press s start a new game", 1, (255, 0, 0))
        text3_label = text_font.render("Press p to pause", 1, (255, 0, 0))
        text4_label = text_font.render("Press r to resume game", 1, (255, 0, 0))
        text5_label = text_font.render("Move wasd, press space to shoot", 1, (255, 0, 0))
        WIN.blit(text1_label, (10, 10))
        WIN.blit(text2_label, (10, 60))
        WIN.blit(text3_label, (10, 110))
        WIN.blit(text4_label, (10, 160))
        WIN.blit(text5_label, (10, 210))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_s]:
            main()
        if keys[pygame.K_r]:
            run = False

def main():
    run = True
    FPS = 60
    level1 = 0
    lives = 5
    player_vel = 5
    laser_vel = 5
    main_font = pygame.font.SysFont("comicsans", 50)
    lost_font = pygame.font.SysFont("comicsans", 60)

    enemies = []
    wave_length = 0
    hp_count = 0
    enemy_vel = 1
    hp_vel = 1

    hp = []

    player = Player(300, 650)

    lost = False
    lost_count = 0

    clock = pygame.time.Clock()

    from sys import exit

    def redraw_window():
        WIN.blit(BG, (0,0))
        #blit ia o imagine si o deseneaza la locatia definita
        # 0,0 e stanga sus 
        lives_label = main_font.render(f"Lives: {lives}", 1, (255, 0, 0))
        level_label = main_font.render(f"Level: {level1}", 1, (100, 255, 0))
        health_label = main_font.render(f"Health: {player.health}", 1, (255, 0, 0) )
        #draw text
        #value and color of text rgb color codes

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width()-10 , 10))
        WIN.blit(health_label, (WIDTH/2 - health_label.get_width()/2, 10))
        #position of text (label)

        for enemy in enemies:
            enemy.draw(WIN)

        for health_pack in hp:
            health_pack.draw(WIN)

        player.draw(WIN)

        if lost:
            lost_label = lost_font.render("You are dying!!!", 1, (255, 0, 0))
            time_label = lost_font.render(f"{5 - lost_count // FPS}", 1, (255, 0, 0))
            WIN.blit(lost_label, (WIDTH/2 - lost_label.get_width()/2, 350))
            WIN.blit(time_label, (WIDTH/2 - time_label.get_width()/2, 350 + lost_label.get_height()))


        pygame.display.update()
        #update screen

    while run:
        clock.tick(FPS)
        redraw_window()
        #foarte important

        if lives <= 0 or player.health < 0:
            lost = True
            lost_count += 1
        
        if lost:
            if lost_count > FPS * 5:
                meniu()


        if len(enemies) == 0:
            level1 += 1
            hp_count += 1
            if hp_count > 3:
                hp_count = 3
            hp_vel += 1
            if len(hp) == 0:
                for j in range(hp_count):
                    health_pack = HealthPack(random.randrange(50, WIDTH-50), random.randrange(-3000, -1000))
                    hp.append(health_pack)
            wave_length += 5
            for i in range(wave_length):
                enemy = Enemy(random.randrange(50, WIDTH-50), random.randrange(-1500, -100), random.choice(["red", "blue", "green"]))
                enemies.append(enemy)
                # add in enemies list
        

        #always run at this speed (pe orice calculator)
        for event in pygame.event.get():
            #in bucla asta se verifica evenimente de 60 de ori pe secunda
            #pygame wensite look events
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
                #inchide fereastra 
        keys = pygame.key.get_pressed()
        #formeaza o lista cu toate tastele
        #tells if a key is presed
        if keys[pygame.K_a] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys[pygame.K_d] and player.x + player_vel < WIDTH - player.get_width():
            player.x += player_vel
        if keys[pygame.K_w] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys[pygame.K_s] and player.y + player_vel < HEIGHT - player.get_height():
            player.y += player_vel
        if keys[pygame.K_SPACE]:
            player.shoot()
        if keys[pygame.K_p]:
            meniu()
        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            if random.randrange(0, 50) == 1:
                enemy.shoot()
            if enemy.y + enemy.get_height() > HEIGHT:
                lives -= 1
                enemies.remove(enemy)
        for health_pack in hp[:]:
            health_pack.move(hp_vel)
            if health_pack.y + health_pack.get_height() > HEIGHT:
                hp.remove(health_pack)
            if health_pack.collision(player):
                hp.remove(health_pack)
                buff = random.randrange(0, 3)
                if buff == 0:
                    player.health += 50
                    if player.health > 200:
                        player.health = 200
                        buff = 2
                if buff == 1:
                    lives += 1
                    if lives >= 5:
                        lives = 5
                        player.health += 50
                        if player.health > 200:
                            player.health = 200
                if buff == 2 and player.COOLDOWN > 20:
                    player.COOLDOWN -= 10
        player.move_lasers(laser_vel, enemies)
        #bucla run se parcurge de 60 de ori pe secunda
meniu()

#tine mine coordonata (0,0) e in stanga sus 