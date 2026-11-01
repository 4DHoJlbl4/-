from pygame import *

mixer.init()
font.init()

GREEN = (154, 205, 50)
# BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_speed, player_x, player_y):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (65, 65))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 635:
            self.rect.x += self.speed
        if keys_pressed[K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if keys_pressed[K_s] and self.rect.y < 440:
            self.rect.y += self.speed

class Enemy(GameSprite):
    def update(self):
        if self.rect.x <= 500:
            self.direction = 'right'
        if self.rect.x >= 650:
            self.direction = 'left'
        if self.direction == 'left':
            self.rect.x -= self.speed
        else:
            self.rect.x += self.speed

class Wall(sprite.Sprite):
    def __init__(self, 
    color: tuple, 
    wall_x: int,
    wall_y: int,
    wall_width: int, 
    wall_height: int):
        super().__init__()
        self.color = color
        self.width = wall_width
        self.height = wall_height
        self.image = Surface((wall_width, wall_height))
        self.image.fill(color)

        self.rect = self.image.get_rect()
        self.rect.x = wall_x
        self.rect.y = wall_y
    def draw_wall(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Font():
    pass
    
player = Player('hero.png', 10, 25, 50)
enemy = Enemy('cyborg.png', 5, 450, 350)
golds = GameSprite('treasure.png', 10, 620, 430)
win = font.SysFont('Impact', 70).render('You WIN', 1, GREEN, WHITE)
lose = font.SysFont('Impact', 70).render('You LOSE', 1, RED, WHITE)

window = display.set_mode((700, 500))
display.set_caption('Лабиринт')
clock = time.Clock()
FPS = 60

w1 = Wall(GREEN, 100, 0, 10, 400)
w2 = Wall(GREEN, 100, 400, 210, 10)
w3 = Wall(GREEN, 300, 0, 10, 400)
w4 = Wall(GREEN, 425, 150, 10, 400)
w5 = Wall(GREEN, 425, 150, 70, 10)
w6 = Wall(GREEN, 490, 150, 10, 400)

background = transform.scale(image.load('background.jpg'), (700, 500))

mixer.music.load('jungles.ogg')
mixer.music.play()
mixer.music.set_volume(0.1)
money = mixer.Sound('money.ogg')
kick = mixer.Sound('kick.ogg')

game = True
finish = False

while game:
    if finish != True:
        window.blit(background, (0, 0))
        player.reset()
        enemy.reset()
        golds.reset()
        player.update()
        enemy.update()
        w1.draw_wall()
        w2.draw_wall()
        w3.draw_wall()
        w4.draw_wall()
        w5.draw_wall()
        w6.draw_wall()

        if sprite.collide_rect(player, golds):
            finish = True
            window.blit(win, (225, 175))
            money.play()
        
        if (sprite.collide_rect(player, enemy) or 
        sprite.collide_rect(player, w1) or
        sprite.collide_rect(player, w2) or
        sprite.collide_rect(player, w3) or
        sprite.collide_rect(player, w4) or
        sprite.collide_rect(player, w5) or
        sprite.collide_rect(player, w6)):
            finish = True
            window.blit(lose, (220, 175))
            kick.play()


    for e in event.get():
        if e.type == QUIT:
            game = False

    display.update()
    clock.tick(FPS)