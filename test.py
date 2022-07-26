import pygame
import sys
import os
import random
 
#import spaceships
PLAYER_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_yellow.png"))
RED_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_red_small.png"))
GREEN_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_green_small.png"))
BLUE_SPACE_SHIP = pygame.image.load(os.path.join("assets", "pixel_ship_blue_small.png"))
HEALTH_PACK = pygame.image.load(os.path.join("assets", "health_pack.png"))

#import lasers
YELLOW_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_yellow.png"))
RED_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_red.png"))
GREEN_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_green.png"))
BLUE_LASER = pygame.image.load(os.path.join("assets", "pixel_laser_blue.png"))

#import sound 
pygame.mixer.init()
pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)


WIDTH = 800
HEIGHT = 750

#import bacground 
BG = pygame.transform.scale(pygame.image.load(os.path.join("assets", "background-black.png")), (WIDTH, HEIGHT))
MEN = pygame.transform.scale(pygame.image.load(os.path.join("assets", "meniu.png")), (WIDTH, HEIGHT))
 
FPS = 60
 
COLOR_BLACK = (0, 0, 0)
COLOR_RED = (255, 0, 0)

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
        self.ship_img = PLAYER_SPACE_SHIP
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

 
def main():
    # Initialize imported pygame modules
    pygame.init()
 
    # Set the window's caption
    pygame.display.set_caption("Pong")
 
    clock = pygame.time.Clock()
 
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
 
    background = pygame.Surface((WIDTH, HEIGHT))
    background = background.convert()
    background.fill(COLOR_BLACK)

    player = Player(WIDTH/2 - 50, HEIGHT - 100)
    enemies = []
    score = 0
    high_score = 0
    player_vel = 5
    wave_length = 10
    enemy_vel = 1
    laser_vel = 5

 
    # Blit everything to screen
    screen.blit(background, (0, 0))
 
    # Update the screen
    pygame.display.flip()

    def redraw_window():
        screen.blit(BG, (0,0))
        text_font = pygame.font.SysFont("comicsans", 30)
        score_label = text_font.render(f"Score: {score}", 1, (255, 0, 0))
        high_score_label = text_font.render(f"High_Score: {high_score}", 1, (255, 0, 0))
        health_label = text_font.render(f"Health: {player.health}", 1, (255, 0, 0) )
        screen.blit(score_label, (10,10))
        screen.blit(high_score_label, (WIDTH - high_score_label.get_width()-10 , 10))
        screen.blit(health_label, (WIDTH/2 - health_label.get_width()/2, 10))
        player.draw(screen)
        #pygame.display.update()

        for enemy in enemies:
            enemy.draw(screen)
 
    # Main loop
    while True:
        clock.tick(FPS)
        redraw_window()
        list_linie = []
        list_coloane = [200, 300, 400, 500, 600]
        for i in range(40):
            list_linie.append(i*10 + 5)
        # Erase everything drawn at last step by filling the background
        # with color black
        background.fill(COLOR_BLACK)
 
        # Check for Quit event
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        if len(enemies) == 0:
            for i in range(wave_length):
                j = random.choice(list_coloane)
                k = random.choice(list_linie)
                enemy = Enemy(j, k, random.choice(["red", "blue", "green"])) 
                enemies.append(enemy)
                list_linie.remove(k)
 
        # Check for key presses and update paddles accordingly
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_w] and player.y - player_vel > 0:
            player.y -= player_vel
        if keys_pressed[pygame.K_s] and player.y + player_vel < HEIGHT - player.get_height():
            player.y += player_vel
        if keys_pressed[pygame.K_a] and player.x - player_vel > 0:
            player.x -= player_vel
        if keys_pressed[pygame.K_d] and player.x + player_vel < WIDTH - player.get_width():
            player.x += player_vel
        if keys_pressed[pygame.K_SPACE]:
            player.shoot()

        for enemy in enemies[:]:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            for i in list_coloane:
                min = HEIGHT
                for enemy in enemies:
                    if enemy.y < min and enemy.x == i:
                        min = enemy.y
                        first = enemy
                first.shoot()
            if enemy.x  > WIDTH - enemy.get_width():
                enemy_vel *= -1
            if enemy.x < 0:
                enemy_vel *= -1

        # Update game state
 
        # Render current game state
        player.move_lasers(laser_vel, enemies)
        pygame.display.flip()
        screen.blit(background, (0, 0))
 
 
if __name__ == '__main__':
    main()